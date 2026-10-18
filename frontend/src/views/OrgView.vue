<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Organigrama Vivo</div>
          <h1 class="os-h1">Quién es quién</h1>
          <p class="text-sm" style="color: var(--os-steel)">Arrastra el lienzo para moverte, haz zoom, y arrastra el punto ● de un nodo a otro para conectarlos.</p>
        </div>
        <div class="flex items-center gap-2">
          <div class="zoom-bar">
            <button class="zbtn" title="Alejar" @click="zoomBy(-0.2)">−</button>
            <button class="zbtn zval" title="Restablecer" @click="resetZoom">{{ Math.round(zoom * 100) }}%</button>
            <button class="zbtn" title="Acercar" @click="zoomBy(0.2)">＋</button>
          </div>
          <Button variant="solid" theme="blue" label="＋ Nodo" @click="openCreate()" />
        </div>
      </div>

      <div class="org-layout">
        <div class="org-side">
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Nodos ({{ nodes.length }})</div>
            <div v-if="!nodes.length" class="text-xs" style="color: var(--os-steel)">Sin nodos todavía.</div>
            <div v-for="n in nodes" :key="n.name" class="org-list-item" @click="editNode(n.name)">
              <span class="mr-1.5">{{ typeIcon(n.node_type) }}</span>
              <span class="flex-1 truncate">{{ n.title }}</span>
              <span class="text-xs" style="color: var(--os-steel)">{{ typeLabel(n.node_type) }}</span>
            </div>
          </div>
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Conexiones ({{ relations.length }})</div>
            <div v-if="!relations.length" class="text-xs" style="color: var(--os-steel)">Arrastra el punto ● de un nodo a otro para conectar.</div>
            <div v-for="r in relations" :key="r.name" class="org-list-item">
              <span class="flex-1 truncate">{{ nodeTitle(r.from_node) }} → {{ nodeTitle(r.to_node) }}</span>
              <button class="text-xs" style="color:#ff6b6b" title="Quitar conexión" @click.stop="removeRelation(r)">✕</button>
            </div>
          </div>
        </div>

        <div class="canvas" ref="canvasEl" @wheel="onWheel">
          <div class="world" :style="worldStyle" @pointerdown="startPan">
            <svg class="wires">
              <line v-for="(r, i) in relations" :key="i" :x1="center(r.from_node).x" :y1="center(r.from_node).y" :x2="center(r.to_node).x" :y2="center(r.to_node).y" />
            </svg>
            <div v-for="n in nodes" :key="n.name" class="node" :data-name="n.name" :class="{ selected: n.name === editingName }" :style="{ left: (n.x || 0) + 'px', top: (n.y || 0) + 'px' }" @pointerdown.stop="startDrag($event, n)">
              <div class="node-type">{{ typeIcon(n.node_type) }}</div>
              <div class="node-label">{{ n.title }}</div>
              <div class="node-port" title="Arrastra para conectar" @pointerdown.stop="startConnect($event, n)"></div>
            </div>
          </div>
          <svg v-if="connectLine" class="temp-wire" style="pointer-events:none">
            <line :x1="connectLine.x1" :y1="connectLine.y1" :x2="connectLine.x2" :y2="connectLine.y2" />
          </svg>
        </div>
      </div>

      <Dialog v-model:open="dialogOpen" :title="editingName ? 'Editar nodo' : 'Nuevo nodo'" size="xl">
        <OsForm v-if="dialogOpen && !metaLoading" :fields="metaFields" :value="form" />
        <template #actions="{ close }">
          <Button v-if="editingName" variant="ghost" theme="red" label="Eliminar" @click="removeNode()" />
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" :label="editingName ? 'Guardar' : 'Crear'" :loading="saving" @click="save" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { call, Button, Dialog, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import OsForm from '../components/OsForm.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'

const nodes = ref([])
const relations = ref([])
const zoom = ref(1)
const pan = reactive({ x: 0, y: 0 })
const canvasEl = ref(null)

const dialogOpen = ref(false)
const editingName = ref(null)
const form = reactive({})
const saving = ref(false)
const metaFields = ref([])
const metaLoading = ref(false)

const nodeTypes = [
  { type: 'Company', label: 'Empresa', icon: '⌂' }, { type: 'Department', label: 'Departamento', icon: '▦' },
  { type: 'Designation', label: 'Puesto', icon: '✧' }, { type: 'Employee', label: 'Empleado', icon: '👤' },
  { type: 'Agent', label: 'Agente IA', icon: '◇' }, { type: 'Custom', label: 'Nodo', icon: '●' },
]
function typeIcon(t) { return nodeTypes.find((x) => x.type === t)?.icon || '●' }
function typeLabel(t) { return nodeTypes.find((x) => x.type === t)?.label || t }
function nodeTitle(name) { return nodes.value.find((x) => x.name === name)?.title || name }

const worldStyle = computed(() => ({ transform: 'translate(' + pan.x + 'px,' + pan.y + 'px) scale(' + zoom.value + ')', transformOrigin: '0 0' }))

function zoomBy(d) { zoom.value = Math.min(2.5, Math.max(0.25, zoom.value + d)) }
function resetZoom() { zoom.value = 1; pan.x = 0; pan.y = 0 }
function onWheel(e) {
  if (e.ctrlKey || e.metaKey || true) { e.preventDefault(); zoomBy(e.deltaY < 0 ? 0.1 : -0.1) }
}

async function loadMeta() {
  metaLoading.value = true
  try {
    const r = await osApi.getDoctypeMeta('OS Org Node')
    metaFields.value = (r.fields || []).filter((f) => !['x', 'y'].includes(f.fieldname))
  } catch (e) { toast.error(humanError(e)) } finally { metaLoading.value = false }
}

async function load() {
  try {
    const d = await osApi.getOrg()
    nodes.value = d.nodes || []
    relations.value = d.relations || []
  } catch (e) { toast.error(humanError(e)) }
}

function center(name) {
  const n = nodes.value.find((x) => x.name === name)
  return n ? { x: (n.x || 0) + 70, y: (n.y || 0) + 22 } : { x: 0, y: 0 }
}

function openCreate() {
  editingName.value = null
  resetForm(metaFields.value, form, { node_type: 'Custom', is_active: true })
  dialogOpen.value = true
}

async function editNode(name) {
  try {
    const doc = await call('frappe.client.get', { doctype: 'OS Org Node', name })
    editingName.value = name
    resetForm(metaFields.value, form, {})
    fillFromDoc(metaFields.value, form, doc)
    dialogOpen.value = true
  } catch (e) { toast.error(humanError(e)) }
}

async function save() {
  saving.value = true
  try {
    const values = coerceValues(metaFields.value, form)
    if (editingName.value) {
      await osApi.updateDoc('OS Org Node', editingName.value, values)
      toast.success('Nodo guardado.')
    } else {
      const r = await call('frappe.client.insert', { doc: { doctype: 'OS Org Node', x: 80, y: 80, ...values } })
      editingName.value = r.name
      toast.success('Nodo creado.')
    }
    dialogOpen.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

async function removeNode() {
  if (!confirm('¿Eliminar este nodo y sus conexiones?')) return
  try {
    await osApi.deleteOrgNode(editingName.value)
    toast.success('Nodo eliminado.')
    dialogOpen.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) }
}

async function removeRelation(r) {
  try {
    await osApi.deleteOrgRelation(r.name)
    toast.success('Conexión eliminada.')
    await load()
  } catch (e) { toast.error(humanError(e)) }
}

// ---- pan (arrastrar fondo) ----
let panning = false, psx = 0, psy = 0, pox = 0, poy = 0
function startPan(e) {
  if (e.target.closest('.node') || e.target.closest('.node-port')) return
  panning = true; psx = e.clientX; psy = e.clientY; pox = pan.x; poy = pan.y
  window.addEventListener('pointermove', onPanMove); window.addEventListener('pointerup', endPan)
}
function onPanMove(e) { if (!panning) return; pan.x = pox + (e.clientX - psx); pan.y = poy + (e.clientY - psy) }
function endPan() { panning = false; window.removeEventListener('pointermove', onPanMove); window.removeEventListener('pointerup', endPan) }

// ---- mover nodo ----
let dragNode = null, sx = 0, sy = 0, ox = 0, oy = 0, moved = false
function startDrag(e, node) {
  dragNode = node; moved = false
  sx = e.clientX; sy = e.clientY; ox = node.x || 0; oy = node.y || 0
  window.addEventListener('pointermove', onDragMove); window.addEventListener('pointerup', endDrag)
}
function onDragMove(e) {
  if (!dragNode) return
  const dx = (e.clientX - sx) / zoom.value, dy = (e.clientY - sy) / zoom.value
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) moved = true
  dragNode.x = ox + dx; dragNode.y = oy + dy
}
function endDrag() {
  window.removeEventListener('pointermove', onDragMove); window.removeEventListener('pointerup', endDrag)
  const n = dragNode; dragNode = null
  if (!n) return
  if (moved) { osApi.saveOrgNode(n.name, n.x, n.y).catch(() => {}) }
  else { editNode(n.name) }
}

// ---- conectar arrastrando el puerto (n8n-like) ----
const connectLine = ref(null)
let connectSource = null
function startConnect(e, node) {
  connectSource = node.name
  const cw = canvasEl.value
  const rect = cw.getBoundingClientRect()
  const nx = (node.x || 0) + 70, ny = (node.y || 0) + 22
  const sx = rect.left + (nx * zoom.value) + pan.x
  const sy = rect.top + (ny * zoom.value) + pan.y
  connectLine.value = { x1: sx - rect.left, y1: sy - rect.top, x2: e.clientX - rect.left, y2: e.clientY - rect.top }
  window.addEventListener('pointermove', onConnectMove); window.addEventListener('pointerup', endConnect)
}
function onConnectMove(e) {
  if (!connectLine.value) return
  const rect = canvasEl.value.getBoundingClientRect()
  connectLine.value.x2 = e.clientX - rect.left
  connectLine.value.y2 = e.clientY - rect.top
}
function endConnect(e) {
  window.removeEventListener('pointermove', onConnectMove); window.removeEventListener('pointerup', endConnect)
  connectLine.value = null
  const from = connectSource; connectSource = null
  const el = document.elementFromPoint(e.clientX, e.clientY)
  const nodeEl = el && el.closest('.node')
  if (!nodeEl || !from) return
  const to = nodeEl.getAttribute('data-name')
  if (!to || to === from) return
  handleConnect(from, to)
}
async function handleConnect(from, to) {
  const exists = relations.value.some((r) => r.from_node === from && r.to_node === to)
  if (exists) return
  try {
    await osApi.addOrgRelation(from, to, 'REPORTS_TO')
    await load()
    toast.success('Conectado.')
  } catch (e) { toast.error(humanError(e)) }
}

onMounted(() => { loadMeta(); load() })
</script>
