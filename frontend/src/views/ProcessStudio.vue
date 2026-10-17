<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Process Studio</div>
          <h1 class="os-h1">{{ process.process_title || 'Proceso' }}</h1>
          <p class="text-sm" style="color: var(--os-steel)">Arrastra nodos. Haz clic en dos para conectarlos. Doble clic para renombrar.</p>
        </div>
        <div class="flex gap-2">
          <Button variant="ghost" label="← Procesos" @click="$router.push('/processes')" />
          <Button variant="solid" theme="blue" label="Guardar" :loading="saving" @click="save" />
        </div>
      </div>

      <div class="flow-layout">
        <div class="palette os-card">
          <div class="mb-2 text-sm font-semibold" style="color:#fff">Biblioteca</div>
          <button v-for="t in stepTypes" :key="t.type" class="palette-btn" @click="addStep(t.type)"><span class="mr-1.5">{{ t.icon }}</span>{{ t.label }}</button>
        </div>
        <div class="canvas">
          <div class="world">
            <svg class="wires">
              <line v-for="(e, i) in edges" :key="i" :x1="center(e.source).x" :y1="center(e.source).y" :x2="center(e.target).x" :y2="center(e.target).y" />
            </svg>
            <div v-for="n in nodes" :key="n.key" class="node" :class="{ selected: n.key === selectedKey, 'from-node': n.key === connectFrom }" :style="{ left: n.x + 'px', top: n.y + 'px' }" @pointerdown.stop="startDrag($event, n)" @dblclick.stop="rename(n)">
              <div class="node-type">{{ typeIcon(n.type) }}</div>
              <div class="node-label">{{ n.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { osApi, humanError } from '../resources/os'

const route = useRoute()
const router = useRouter()
const process = ref({})
const nodes = ref([])
const edges = ref([])
const selectedKey = ref(null)
const connectFrom = ref(null)
const saving = ref(false)

const stepTypes = [
  { type: 'START', label: 'Inicio', icon: '⏵' }, { type: 'HUMAN', label: 'Humano', icon: '👤' },
  { type: 'HYBRID', label: 'Híbrido', icon: '🤝' }, { type: 'AI', label: 'IA', icon: '◇' },
  { type: 'SYSTEM', label: 'Sistema', icon: '⚙' }, { type: 'GATEWAY', label: 'Decisión', icon: '⑂' },
  { type: 'APPROVAL', label: 'Aprobación', icon: '☑' }, { type: 'WAIT', label: 'Espera', icon: '⏳' },
  { type: 'END', label: 'Fin', icon: '⏹' },
]
function typeIcon(t) { return stepTypes.find((x) => x.type === t)?.icon || '●' }

async function load() {
  try {
    const d = await osApi.getProcess(route.params.name)
    process.value = d
    nodes.value = (d.steps || []).map((s) => ({ key: s.step_key, type: s.step_type, label: s.step_title, x: s.x, y: s.y }))
    edges.value = (d.edges || []).map((e) => ({ source: e.source_step_key, target: e.target_step_key, relation_type: e.relation_type }))
  } catch (e) { toast.error(humanError(e)) }
}

function center(id) {
  const n = nodes.value.find((x) => x.key === id)
  return n ? { x: n.x + 70, y: n.y + 22 } : { x: 0, y: 0 }
}

async function addStep(type) {
  try {
    const r = await osApi.addProcessStep(route.params.name, type, type)
    nodes.value.push({ key: r.step_key, type, label: type, x: 40, y: 40 })
    toast.success('Paso agregado.')
  } catch (e) { toast.error(humanError(e)) }
}

let dragNode = null, sx = 0, sy = 0, ox = 0, oy = 0, moved = false
function startDrag(e, node) {
  dragNode = node; moved = false
  sx = e.clientX; sy = e.clientY; ox = node.x; oy = node.y
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
  if (!moved && n) clickNode(n)
}

function clickNode(node) {
  if (connectFrom.value) {
    if (connectFrom.value !== node.key && !edges.value.some((e) => e.source === connectFrom.value && e.target === node.key)) {
      edges.value.push({ source: connectFrom.value, target: node.key, relation_type: 'NEXT' })
    }
    connectFrom.value = null; selectedKey.value = null
  } else { connectFrom.value = node.key; selectedKey.value = node.key }
}

function rename(node) { const v = prompt('Nombre del paso:', node.label); if (v && v.trim()) node.label = v.trim() }

async function save() {
  saving.value = true
  try {
    await osApi.saveProcessCanvas(route.params.name, nodes.value.map((n) => ({ step_key: n.key, step_title: n.label, x: n.x, y: n.y })), edges.value.map((e) => ({ source_step_key: e.source, target_step_key: e.target, relation_type: e.relation_type })))
    toast.success('Proceso guardado.')
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

onMounted(load)
</script>
