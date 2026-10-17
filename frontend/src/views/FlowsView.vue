<template>
  <AppLayout>
    <div class="p-6">
      <div class="mb-5 flex flex-wrap items-end gap-3">
        <div class="min-w-[200px] flex-1">
          <div class="as-eyebrow">Flow builder</div>
          <h1 class="as-h1">Diseña cómo trabajan juntos.</h1>
          <p class="text-sm text-ink-gray-5">Arrastra nodos. Haz clic en dos para conectarlos. Doble clic para renombrar.</p>
        </div>
        <Select v-model="flowId" :options="flowOptions" class="w-64" placeholder="Elegir flujo" />
        <Button variant="subtle" label="＋ Nuevo" @click="newFlow" />
        <Button variant="solid" theme="blue" label="Guardar" :loading="saving" @click="save" />
        <Button variant="ghost" icon="lucide-trash-2" tooltip="Eliminar nodo" @click="removeNode" />
        <Button variant="solid" theme="blue" label="▷ Probar flujo" @click="runFlow" />
      </div>

      <div class="flow-layout">
        <div class="card palette">
          <h2 class="mb-2 text-sm font-semibold">Biblioteca</h2>
          <button v-for="t in nodeTypes" :key="t.type" class="palette-btn" @click="addNode(t.type)"><span class="mr-2">{{ t.icon }}</span>{{ t.label }}</button>
        </div>

        <div class="canvas" @pointerdown="canvasDown">
          <div class="world" :style="{ transform: 'scale(' + zoom + ')' }">
            <svg class="wires">
              <line v-for="(e, i) in edges" :key="i" :x1="center(e[0]).x" :y1="center(e[0]).y" :x2="center(e[1]).x" :y2="center(e[1]).y" />
            </svg>
            <div
              v-for="n in nodes"
              :key="n.id"
              class="node"
              :class="{ selected: n.id === selectedId, 'from-node': n.id === connectFrom }"
              :style="{ left: n.x + 'px', top: n.y + 'px' }"
              @pointerdown.stop="startDrag($event, n)"
              @dblclick.stop="rename(n)"
            >
              <div class="node-type">{{ typeIcon(n.type) }}</div>
              <div class="node-label">{{ n.label }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="notice">Prueba local: muestra el recorrido del flujo. Los nodos no ejecutan llamadas externas.</div>
      <div v-if="runResult" class="mt-3 rounded-lg bg-surface-blue-2 px-4 py-3 text-sm text-ink-blue-7">{{ runResult }}</div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Button, Select, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const nodeTypes = [
  { type: 'trigger', label: 'Disparador', icon: 'ϟ' },
  { type: 'agent', label: 'Agente IA', icon: '◇' },
  { type: 'condition', label: 'Condición', icon: '⑂' },
  { type: 'tool', label: 'Herramienta MCP', icon: '⊞' },
  { type: 'approval', label: 'Aprobación', icon: '☑' },
  { type: 'response', label: 'Respuesta', icon: '↗' },
]
function typeIcon(t) { return nodeTypes.find((x) => x.type === t)?.icon || '●' }
function typeLabel(t) { return nodeTypes.find((x) => x.type === t)?.label || t }

const flows = ref([])
const flowId = ref('')
const flowName = ref('')
const nodes = ref([])
const edges = ref([])
const zoom = ref(1)
const selectedId = ref(null)
const connectFrom = ref(null)
const saving = ref(false)
const runResult = ref('')
let seq = 1

const flowOptions = computed(() => flows.value.map((f) => ({ label: f.title, value: f.name })))

async function loadFlows() {
  flows.value = await api.listFlows()
  if (flows.value.length && !flowId.value) {
    flowId.value = flows.value[0].name
    await open(flows.value[0].name)
  }
}

async function open(name) {
  try {
    const d = await api.getFlow(name)
    flowName.value = d.title
    const g = safeParse(d.graph_json)
    nodes.value = (g.nodes || []).map((n) => ({ id: n.id, type: n.type, label: (n.config && n.config.label) || typeLabel(n.type), x: (n.config && n.config.position && n.config.position.x) || 40, y: (n.config && n.config.position && n.config.position.y) || 40 }))
    edges.value = (g.edges || []).map((e) => [e.source, e.target])
    seq = nodes.value.length + 1
    selectedId.value = null
    connectFrom.value = null
    runResult.value = ''
  } catch (e) { toast.error(humanError(e)) }
}

function safeParse(s) { try { return JSON.parse(s || '{}') } catch { return {} } }

async function newFlow() {
  const f = await api.createFlow({ title: 'Nuevo flujo' })
  await loadFlows()
  flowId.value = f.name
  await open(f.name)
  toast.success('Flujo creado.')
}

function addNode(type) {
  const t = nodeTypes.find((x) => x.type === type)
  nodes.value.push({ id: 'n' + seq++, type, label: t.label, x: 60 + (nodes.value.length % 5) * 40, y: 60 + (nodes.value.length % 5) * 60 })
}

function center(id) {
  const n = nodes.value.find((x) => x.id === id)
  return n ? { x: n.x + 70, y: n.y + 22 } : { x: 0, y: 0 }
}

// Drag
let dragNode = null
let startX = 0, startY = 0, origX = 0, origY = 0, moved = false
function startDrag(e, node) {
  dragNode = node
  moved = false
  startX = e.clientX; startY = e.clientY
  origX = node.x; origY = node.y
  window.addEventListener('pointermove', onDrag)
  window.addEventListener('pointerup', endDrag)
}
function onDrag(e) {
  if (!dragNode) return
  const dx = (e.clientX - startX) / zoom.value
  const dy = (e.clientY - startY) / zoom.value
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) moved = true
  dragNode.x = origX + dx
  dragNode.y = origY + dy
}
function endDrag() {
  window.removeEventListener('pointermove', onDrag)
  window.removeEventListener('pointerup', endDrag)
  const node = dragNode
  dragNode = null
  if (!moved && node) clickNode(node)
}

function clickNode(node) {
  if (connectFrom.value) {
    if (connectFrom.value !== node.id && !edges.value.some((e) => e[0] === connectFrom.value && e[1] === node.id)) {
      edges.value.push([connectFrom.value, node.id])
    }
    connectFrom.value = null
  } else {
    connectFrom.value = node.id
    selectedId.value = node.id
  }
}

function canvasDown() {
  if (!connectFrom.value && selectedId.value) { selectedId.value = null }
}

function removeNode() {
  if (!selectedId.value && !connectFrom.value) { toast.warning('Selecciona un nodo primero.'); return }
  const id = connectFrom.value || selectedId.value
  nodes.value = nodes.value.filter((n) => n.id !== id)
  edges.value = edges.value.filter((e) => e[0] !== id && e[1] !== id)
  selectedId.value = null
  connectFrom.value = null
}

function rename(node) {
  const name = prompt('Nombre del nodo:', node.label)
  if (name && name.trim()) node.label = name.trim()
}

async function save() {
  if (!flowId.value) { toast.warning('Crea o elige un flujo primero.'); return }
  saving.value = true
  try {
    const graph = {
      schema_version: 'altoplano.flow/1',
      nodes: nodes.value.map((n) => ({ id: n.id, type: n.type, config: { label: n.label, position: { x: n.x, y: n.y } } })),
      edges: edges.value.map((e) => ({ source: e[0], target: e[1], port: 'out' })),
      limits: { max_steps: 20, timeout_seconds: 120 },
    }
    await api.saveFlow({ name: flowId.value, title: flowName.value || 'Flujo', graph_json: JSON.stringify(graph) })
    toast.success('Flujo guardado.')
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

function runFlow() {
  if (!nodes.value.length) { runResult.value = 'Agrega nodos para probar el flujo.'; return }
  const start = nodes.value.find((n) => n.type === 'trigger') || nodes.value[0]
  const path = [start]
  const seen = new Set([start.id])
  let cur = start
  while (true) {
    const edge = edges.value.find((e) => e[0] === cur.id && !seen.has(e[1]))
    if (!edge) break
    const next = nodes.value.find((n) => n.id === edge[1])
    if (!next) break
    path.push(next); seen.add(next.id); cur = next
  }
  runResult.value = 'Recorrido: ' + path.map((n) => typeLabel(n.type)).join(' → ')
}

onMounted(loadFlows)
</script>

<style>
.flow-layout { display: grid; grid-template-columns: 185px 1fr; gap: 15px; }
.palette { padding: 16px; background: #fff; border: 1px solid #e1e6eb; border-radius: 11px; }
.palette-btn { width: 100%; margin-bottom: 10px; text-align: left; padding: 10px; border: 1px solid #dfe4e9; background: #fff; border-radius: 8px; color: #25364a; }
.palette-btn:hover { background: #edf2f1; }
.canvas { height: 510px; overflow: auto; position: relative; border: 1px solid #dce3e7; border-radius: 10px; background-color: #f3f6f5; background-image: radial-gradient(#cbd7d1 1px, transparent 1px); background-size: 18px 18px; }
.world { position: relative; width: 1050px; height: 700px; transform-origin: 0 0; }
.wires { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.wires line { stroke: #98c1b1; stroke-width: 2; }
.node { position: absolute; background: #fff; border: 1px solid #dce3e7; border-radius: 8px; padding: 10px 14px; cursor: grab; user-select: none; min-width: 120px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.node.selected { border-color: #143e37; box-shadow: 0 0 0 2px #c3dcd1; }
.node.from-node { border-color: #143e37; background: #eaf1ee; }
.node-type { font-size: 16px; font-weight: 700; color: #225547; }
.node-label { font-size: 13px; color: #25364a; margin-top: 3px; }
.notice { margin-top: 15px; font-size: 12px; color: #7b8794; }
@media (max-width: 768px) { .flow-layout { grid-template-columns: 1fr; } }
</style>
