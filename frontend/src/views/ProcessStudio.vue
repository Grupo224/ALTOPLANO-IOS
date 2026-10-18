<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Estudio de procesos</div>
          <h1 class="os-h1">{{ process.process_title || 'Proceso' }}</h1>
          <p class="text-sm" style="color: var(--os-steel)">Diseña el flujo como pasos conectados: arrastra el punto ● de un paso a otro, o activa "Conectar".</p>
        </div>
        <div class="flex items-center gap-2">
          <Button variant="ghost" label="← Procesos" @click="$router.push('/processes')" />
          <Button variant="ghost" label="✎ Editar datos" @click="wizardOpen = true" />
          <Button variant="ghost" :theme="connectMode ? 'orange' : 'gray'" :label="connectMode ? 'Conectar: activo' : 'Conectar'" @click="toggleConnect" />
          <Button variant="solid" theme="orange" label="▶ Ejecutar prueba" :loading="running" @click="runProcess" />
          <Button variant="solid" theme="blue" label="Guardar" :loading="saving" @click="save" />
        </div>
      </div>

      <div class="org-layout">
        <div class="org-side">
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Agregar paso</div>
            <button v-for="t in stepTypes" :key="t.type" class="palette-btn" @click="addStep(t.type)"><span class="mr-1.5">{{ t.icon }}</span>{{ t.label }}</button>
          </div>
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Pasos ({{ nodes.length }})</div>
            <div v-if="!nodes.length" class="text-xs" style="color: var(--os-steel)">Agrega el primer paso.</div>
            <div v-for="n in nodes" :key="n.step_key" class="org-list-item" @click="editNode(n)">
              <span class="mr-1.5">{{ typeIcon(n.step_type) }}</span>
              <span class="flex-1 truncate">{{ n.step_title }}</span>
            </div>
          </div>
          <div class="org-panel">
            <div class="mb-2 text-sm font-semibold" style="color:#fff">Conexiones ({{ relations.length }})</div>
            <div v-if="!relations.length" class="text-xs" style="color: var(--os-steel)">Conecta pasos arrastrando el punto del borde.</div>
            <div v-for="r in relations" :key="r.edge_key" class="org-list-item">
              <span class="flex-1 truncate">{{ stepTitle(r.source_step_key) }} → {{ stepTitle(r.target_step_key) }}</span>
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
            <template #node-step="nodeProps">
              <div class="vf-org-node" :data-step-type="nodeProps.data.step_type" :class="{ 'vf-connect-source': connectMode && connectSource === nodeProps.id }">
                <Handle type="target" :position="Position.Left" />
                <div class="vf-org-icon">{{ typeIcon(nodeProps.data.step_type) }}</div>
                <div class="vf-org-label">{{ nodeProps.data.step_title }}</div>
                <div class="vf-org-sub">{{ typeLabel(nodeProps.data.step_type) }}</div>
                <Handle type="source" :position="Position.Right" />
              </div>
            </template>
          </VueFlow>
        </div>
      </div>

      <Dialog v-model:open="dialogOpen" :title="editingKey ? 'Editar paso' : 'Nuevo paso'" size="xl">
        <OsForm v-if="dialogOpen && !metaLoading" :fields="metaFields" :value="form" />
        <template #actions="{ close }">
          <Button v-if="editingKey" variant="ghost" theme="red" label="Eliminar" @click="removeStep()" />
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" :label="editingKey ? 'Guardar' : 'Agregar'" :loading="saving" @click="saveStep" />
        </template>
      </Dialog>

      <ProcessWizard v-model:open="wizardOpen" :name="route.params.name" @saved="load" />
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Dialog, toast } from 'frappe-ui'
import { VueFlow, Handle, Position, MarkerType } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import AppLayout from '../components/AppLayout.vue'
import OsForm from '../components/OsForm.vue'
import ProcessWizard from '../components/ProcessWizard.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'
import { bridgeApi } from '../resources/runtime'

const route = useRoute()
const $router = useRouter()
const process = ref({})
const nodes = ref([])
const relations = ref([])
const connectMode = ref(false)
const connectSource = ref(null)
const saving = ref(false)
const running = ref(false)
const wizardOpen = ref(false)

const dialogOpen = ref(false)
const editingKey = ref(null)
const form = reactive({})
const metaFields = ref([])
const metaLoading = ref(false)

const stepTypes = [
  { type: 'START', label: 'Inicio', icon: '⏵' }, { type: 'HUMAN', label: 'Humano', icon: '👤' },
  { type: 'HYBRID', label: 'Híbrido', icon: '🤝' }, { type: 'AI', label: 'IA', icon: '◇' },
  { type: 'SYSTEM', label: 'Sistema', icon: '⚙' }, { type: 'GATEWAY', label: 'Decisión', icon: '◆' },
  { type: 'APPROVAL', label: 'Aprobación', icon: '☑' }, { type: 'WAIT', label: 'Espera', icon: '⏳' },
  { type: 'END', label: 'Fin', icon: '⏹' },
]
function typeIcon(t) { return stepTypes.find((x) => x.type === t)?.icon || '●' }
function typeLabel(t) { return stepTypes.find((x) => x.type === t)?.label || t }
function stepTitle(key) { return nodes.value.find((x) => x.step_key === key)?.step_title || key }

const vfNodes = computed({
  get: () => nodes.value.map((n) => ({
    id: n.step_key,
    type: 'step',
    position: { x: n.x || 0, y: n.y || 0 },
    data: { step_title: n.step_title, step_type: n.step_type },
  })),
  set: () => {},
})
const vfEdges = computed({
  get: () => relations.value.map((r) => ({
    id: r.edge_key,
    source: r.source_step_key,
    target: r.target_step_key,
    type: 'smoothstep',
    markerEnd: MarkerType.ArrowClosed,
    style: { stroke: '#38b2ac', strokeWidth: 2 },
  })),
  set: () => {},
})

async function loadMeta() {
  metaLoading.value = true
  try {
    const r = await osApi.getDoctypeMeta('OS Process Step')
    metaFields.value = (r.fields || []).filter((f) => !['step_key', 'x', 'y', 'name'].includes(f.fieldname))
  } catch (e) { toast.error(humanError(e)) } finally { metaLoading.value = false }
}

async function load() {
  try {
    const d = await osApi.getProcess(route.params.name)
    process.value = d
    nodes.value = (d.steps || []).map((s) => ({ step_key: s.step_key, step_title: s.step_title, step_type: s.step_type, x: s.x, y: s.y, ...s }))
    relations.value = (d.edges || []).map((e) => ({ edge_key: e.edge_key, source_step_key: e.source_step_key, target_step_key: e.target_step_key, relation_type: e.relation_type }))
  } catch (e) { toast.error(humanError(e)) }
}

async function addStep(type) {
  try {
    const r = await osApi.addProcessStep(route.params.name, typeLabel(type), type)
    await load()
    const n = nodes.value.find((x) => x.step_key === r.step_key)
    if (n) editNode(n)
  } catch (e) { toast.error(humanError(e)) }
}

function editNode(n) {
  editingKey.value = n.step_key
  resetForm(metaFields.value, form, { step_type: n.step_type, step_title: n.step_title })
  fillFromDoc(metaFields.value, form, n)
  dialogOpen.value = true
}

async function saveStep() {
  saving.value = true
  try {
    const values = coerceValues(metaFields.value, form)
    if (editingKey.value) {
      await osApi.saveProcessStep(route.params.name, editingKey.value, values)
      toast.success('Paso guardado.')
    } else {
      await osApi.addProcessStep(route.params.name, values.step_title, values.step_type)
      toast.success('Paso agregado.')
    }
    dialogOpen.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

async function removeStep() {
  try {
    await osApi.deleteProcessStep(route.params.name, editingKey.value)
    toast.success('Paso eliminado.')
    dialogOpen.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) }
}

async function removeRelation(r) {
  try {
    await osApi.deleteProcessEdge(route.params.name, r.source_step_key, r.target_step_key)
    toast.success('Conexión eliminada.')
    await load()
  } catch (e) { toast.error(humanError(e)) }
}

function toggleConnect() {
  connectMode.value = !connectMode.value
  connectSource.value = null
  if (connectMode.value) toast.info('Conectar: haz clic en el paso origen y luego en el destino.')
}

function onConnect(connection) {
  if (!connection.source || !connection.target || connection.source === connection.target) return
  const exists = relations.value.some((r) => r.source_step_key === connection.source && r.target_step_key === connection.target)
  if (exists) { toast.info('Ya están conectados.'); return }
  osApi.addProcessEdge(route.params.name, connection.source, connection.target, 'NEXT')
    .then(() => { toast.success('Conectado.'); return load() })
    .catch((e) => toast.error(humanError(e)))
}

function onNodeDragStop(e) {
  const id = e.node?.id
  const pos = e.node?.position
  if (id && pos) osApi.saveProcessStepPosition(route.params.name, id, Math.round(pos.x), Math.round(pos.y)).catch(() => {})
}

function onNodeClick(e) {
  if (!e.node?.id) return
  if (connectMode.value) {
    if (!connectSource.value) {
      connectSource.value = e.node.id
      toast.info('Origen elegido. Ahora haz clic en el destino.')
    } else {
      const from = connectSource.value
      connectSource.value = null
      if (from !== e.node.id) {
        const exists = relations.value.some((r) => r.source_step_key === from && r.target_step_key === e.node.id)
        if (exists) { toast.info('Ya están conectados.'); return }
        osApi.addProcessEdge(route.params.name, from, e.node.id, 'NEXT')
          .then(() => { toast.success('Conectado.'); return load() })
          .catch((err) => toast.error(humanError(err)))
      }
    }
    return
  }
  const n = nodes.value.find((x) => x.step_key === e.node.id)
  if (n) editNode(n)
}

function onEdgeClick(e) {
  if (e.edge?.id) {
    const r = relations.value.find((x) => x.edge_key === e.edge.id)
    if (r) removeRelation(r)
  }
}

async function save() {
  saving.value = true
  try {
    await osApi.saveProcessCanvas(
      route.params.name,
      nodes.value.map((n) => ({ step_key: n.step_key, step_title: n.step_title, x: n.x, y: n.y })),
      relations.value.map((r) => ({ edge_key: r.edge_key, source_step_key: r.source_step_key, target_step_key: r.target_step_key, relation_type: r.relation_type })),
    )
    toast.success('Proceso guardado.')
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

async function runProcess() {
  running.value = true
  try {
    const r = await bridgeApi.startRun(route.params.name, 'Test')
    toast.success('Ejecución creada: ' + r.run_code)
    $router.push('/runs/' + r.run)
  } catch (e) { toast.error(humanError(e)) } finally { running.value = false }
}

onMounted(() => { loadMeta(); load() })
</script>
