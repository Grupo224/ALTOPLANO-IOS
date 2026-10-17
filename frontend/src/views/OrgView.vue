<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Organigrama Vivo</div>
          <h1 class="os-h1">Quién es quién</h1>
          <p class="text-sm" style="color: var(--os-steel)">Arrastra los nodos. Clic en un nodo para editar su información. Usa "Conectar" para unir dos nodos.</p>
        </div>
        <div class="flex gap-2">
          <Button variant="ghost" :theme="connectMode ? 'orange' : 'gray'" :label="connectMode ? 'Conectar: ON' : 'Conectar'" @click="connectMode = !connectMode" />
          <Button variant="solid" theme="blue" label="＋ Nodo" @click="openCreate()" />
        </div>
      </div>

      <div class="flow-layout">
        <div class="palette os-card">
          <div class="mb-2 text-sm font-semibold" style="color:#fff">Tipos de nodo</div>
          <button v-for="t in nodeTypes" :key="t.type" class="palette-btn" @click="addNode(t.type)"><span class="mr-1.5">{{ t.icon }}</span>{{ t.label }}</button>
        </div>
        <div class="canvas">
          <div class="world">
            <svg class="wires">
              <line v-for="(r, i) in relations" :key="i" :x1="center(r.from_node).x" :y1="center(r.from_node).y" :x2="center(r.to_node).x" :y2="center(r.to_node).y" />
            </svg>
            <div v-for="n in nodes" :key="n.name" class="node" :class="{ selected: n.name === connectFrom }" :style="{ left: (n.x || 0) + 'px', top: (n.y || 0) + 'px' }" @pointerdown.stop="startDrag($event, n)">
              <div class="node-type">{{ typeIcon(n.node_type) }}</div>
              <div class="node-label">{{ n.title }}</div>
            </div>
          </div>
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
import { ref, reactive, onMounted } from 'vue'
import { call, Button, Dialog, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import OsForm from '../components/OsForm.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'

const nodes = ref([])
const relations = ref([])
const connectMode = ref(false)
const connectFrom = ref(null)

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

async function addNode(type) {
  try {
    const r = await osApi.addOrgNode(type, type, 60 + nodes.value.length * 30, 60)
    await load()
    await editNode(r.name)
  } catch (e) { toast.error(humanError(e)) }
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
  try {
    await call('frappe.client.delete', { doctype: 'OS Org Node', name: editingName.value })
    toast.success('Nodo eliminado.')
    dialogOpen.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) }
}

// drag + click-to-edit / connect
let dragNode = null, sx = 0, sy = 0, ox = 0, oy = 0, moved = false
function startDrag(e, node) {
  dragNode = node; moved = false
  sx = e.clientX; sy = e.clientY; ox = node.x || 0; oy = node.y || 0
  window.addEventListener('pointermove', onDrag); window.addEventListener('pointerup', endDrag)
}
function onDrag(e) {
  if (!dragNode) return
  const dx = e.clientX - sx, dy = e.clientY - sy
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) moved = true
  dragNode.x = ox + dx; dragNode.y = oy + dy
}
function endDrag() {
  window.removeEventListener('pointermove', onDrag); window.removeEventListener('pointerup', endDrag)
  const n = dragNode; dragNode = null
  if (!n) return
  if (moved) { osApi.saveOrgNode(n.name, n.x, n.y).catch(() => {}) }
  else if (connectMode.value) { handleConnect(n.name) }
  else { editNode(n.name) }
}
async function handleConnect(name) {
  if (!connectFrom.value) { connectFrom.value = name; return }
  const from = connectFrom.value
  connectFrom.value = null
  if (from === name) return
  const exists = relations.value.some((r) => r.from_node === from && r.to_node === name)
  if (!exists) {
    try {
      await call('frappe.client.insert', { doc: { doctype: 'OS Org Relation', from_node: from, to_node: name, relation_type: 'REPORTS_TO' } })
      await load()
      toast.success('Relación creada.')
    } catch (e) { toast.error(humanError(e)) }
  }
}

onMounted(() => { loadMeta(); load() })
</script>
