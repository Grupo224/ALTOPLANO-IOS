<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Organigrama Vivo</div>
          <h1 class="os-h1">Quién es quién</h1>
          <p class="text-sm" style="color: var(--os-steel)">Arrastra el lienzo, haz zoom, mueve los nodos y conecta arrastrando el punto del borde.</p>
        </div>
        <Button variant="solid" theme="blue" label="＋ Nodo" @click="openCreate()" />
      </div>

      <div class="org-layout">
        <div class="org-side">
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Agregar</div>
            <button v-for="t in nodeTypes" :key="t.type" class="palette-btn" @click="addNode(t.type)"><span class="mr-1.5">{{ t.icon }}</span>{{ t.label }}</button>
          </div>
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Nodos ({{ nodes.length }})</div>
            <div v-if="!nodes.length" class="text-xs" style="color: var(--os-steel)">Sin nodos todavía.</div>
            <div v-for="n in nodes" :key="n.name" class="org-list-item" @click="editNode(n.name)">
              <span class="mr-1.5">{{ typeIcon(n.node_type) }}</span>
              <span class="flex-1 truncate">{{ n.title }}</span>
            </div>
          </div>
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Conexiones ({{ relations.length }})</div>
            <div v-if="!relations.length" class="text-xs" style="color: var(--os-steel)">Conecta arrastrando el punto del borde de un nodo a otro.</div>
            <div v-for="r in relations" :key="r.name" class="org-list-item">
              <span class="flex-1 truncate">{{ nodeTitle(r.from_node) }} → {{ nodeTitle(r.to_node) }}</span>
              <button class="text-xs" style="color:#ff6b6b" title="Quitar conexión" @click.stop="removeRelation(r)">✕</button>
            </div>
          </div>
        </div>

        <div class="org-canvas">
          <VueFlow
            v-model:nodes="vfNodes"
            v-model:edges="vfEdges"
            :default-viewport="{ zoom: 1, x: 40, y: 40 }"
            :min-zoom="0.2"
            :max-zoom="3"
            fit-view-on-init
            :edges-updatable="false"
            @connect="onConnect"
            @node-drag-stop="onNodeDragStop"
            @node-click="onNodeClick"
            @edge-click="onEdgeClick"
          >
            <Background pattern-color="#1a283e" :gap="18" />
            <MiniMap />
            <Controls />
            <template #node-org="nodeProps">
              <div class="vf-org-node" :data-node-type="nodeProps.data.node_type">
                <Handle type="target" :position="Position.Left" />
                <div class="vf-org-icon">{{ typeIcon(nodeProps.data.node_type) }}</div>
                <div class="vf-org-label">{{ nodeProps.data.title }}</div>
                <div class="vf-org-sub">{{ typeLabel(nodeProps.data.node_type) }}</div>
                <Handle type="source" :position="Position.Right" />
              </div>
            </template>
          </VueFlow>
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
import { VueFlow, Handle, Position, MarkerType } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import AppLayout from '../components/AppLayout.vue'
import OsForm from '../components/OsForm.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'

const nodes = ref([])
const relations = ref([])

const dialogOpen = ref(false)
const editingName = ref(null)
const form = reactive({})
const saving = ref(false)
const metaFields = ref([])
const metaLoading = ref(false)

const nodeTypes = [
  { type: 'Company', label: 'Empresa', icon: '⌂', color: '#4f8ef7' },
  { type: 'Department', label: 'Departamento', icon: '▦', color: '#38b2ac' },
  { type: 'Designation', label: 'Puesto', icon: '✧', color: '#b58cff' },
  { type: 'Employee', label: 'Empleado', icon: '👤', color: '#ff9422' },
  { type: 'Agent', label: 'Agente IA', icon: '◇', color: '#f5a0d0' },
  { type: 'Custom', label: 'Nodo', icon: '●', color: '#75879f' },
]
function typeIcon(t) { return nodeTypes.find((x) => x.type === t)?.icon || '●' }
function typeLabel(t) { return nodeTypes.find((x) => x.type === t)?.label || t }
function typeColor(t) { return nodeTypes.find((x) => x.type === t)?.color || '#75879f' }
function nodeTitle(name) { return nodes.value.find((x) => x.name === name)?.title || name }

// vue-flow nodes/edges (derivados de nodes/relations)
const vfNodes = computed({
  get: () => nodes.value.map((n) => ({
    id: n.name,
    type: 'org',
    position: { x: n.x || 0, y: n.y || 0 },
    data: { title: n.title, node_type: n.node_type },
  })),
  set: () => {},
})
const vfEdges = computed({
  get: () => relations.value.map((r) => ({
    id: r.name,
    source: r.from_node,
    target: r.to_node,
    type: 'smoothstep',
    markerEnd: MarkerType.ArrowClosed,
    style: { stroke: '#ff9422', strokeWidth: 2 },
  })),
  set: () => {},
})

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

function openCreate() {
  editingName.value = null
  resetForm(metaFields.value, form, { node_type: 'Custom', is_active: true })
  dialogOpen.value = true
}

async function addNode(type) {
  try {
    const r = await osApi.addOrgNode(type, type, 120 + nodes.value.length * 40, 120 + nodes.value.length * 40)
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
      const r = await call('frappe.client.insert', { doc: { doctype: 'OS Org Node', x: 160, y: 160, ...values } })
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

// ---- eventos vue-flow ----
function onConnect(connection) {
  if (!connection.source || !connection.target || connection.source === connection.target) return
  const exists = relations.value.some((r) => r.from_node === connection.source && r.to_node === connection.target)
  if (exists) { toast.info('Ya están conectados.'); return }
  osApi.addOrgRelation(connection.source, connection.target, 'REPORTS_TO')
    .then(() => { toast.success('Conectado.'); return load() })
    .catch((e) => toast.error(humanError(e)))
}

function onNodeDragStop(e) {
  const id = e.node?.id
  const pos = e.node?.position
  if (id && pos) osApi.saveOrgNode(id, Math.round(pos.x), Math.round(pos.y)).catch(() => {})
}

function onNodeClick(e) {
  if (e.node?.id) editNode(e.node.id)
}

function onEdgeClick(e) {
  if (e.edge?.id) {
    const r = relations.value.find((x) => x.name === e.edge.id)
    if (r) removeRelation(r)
  }
}

onMounted(() => { loadMeta(); load() })
</script>
