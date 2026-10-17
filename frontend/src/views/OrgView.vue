<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Organigrama Vivo</div>
          <h1 class="os-h1">Quién es quién</h1>
          <p class="text-sm" style="color: var(--os-steel)">Arrastra los nodos. Agrega desde la biblioteca.</p>
        </div>
        <div class="flex gap-2">
          <Button variant="solid" theme="blue" label="＋ Nodo" @click="addNode('Custom')" />
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
            <div v-for="n in nodes" :key="n.name" class="node" :style="{ left: (n.x || 0) + 'px', top: (n.y || 0) + 'px' }" @pointerdown.stop="startDrag($event, n)">
              <div class="node-type">{{ typeIcon(n.node_type) }}</div>
              <div class="node-label">{{ n.title }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { osApi, humanError } from '../resources/os'

const nodes = ref([])
const relations = ref([])

const nodeTypes = [
  { type: 'Company', label: 'Empresa', icon: '⌂' }, { type: 'Department', label: 'Departamento', icon: '▦' },
  { type: 'Designation', label: 'Puesto', icon: '✧' }, { type: 'Employee', label: 'Empleado', icon: '👤' },
  { type: 'Agent', label: 'Agente IA', icon: '◇' }, { type: 'Custom', label: 'Nodo', icon: '●' },
]
function typeIcon(t) { return nodeTypes.find((x) => x.type === t)?.icon || '●' }

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

async function addNode(type) {
  const t = nodeTypes.find((x) => x.type === type)
  try {
    const r = await osApi.addOrgNode(t.label, type, 60 + nodes.value.length * 30, 60)
    nodes.value.push({ name: r.name, title: t.label, node_type: type, x: 60, y: 60 })
    toast.success('Nodo agregado.')
  } catch (e) { toast.error(humanError(e)) }
}

let dragNode = null, sx = 0, sy = 0, ox = 0, oy = 0
function startDrag(e, node) {
  dragNode = node; sx = e.clientX; sy = e.clientY; ox = node.x || 0; oy = node.y || 0
  window.addEventListener('pointermove', onDrag); window.addEventListener('pointerup', endDrag)
}
function onDrag(e) { if (!dragNode) return; dragNode.x = ox + (e.clientX - sx); dragNode.y = oy + (e.clientY - sy) }
function endDrag() {
  window.removeEventListener('pointermove', onDrag); window.removeEventListener('pointerup', endDrag)
  const n = dragNode; dragNode = null
  if (n) osApi.saveOrgNode(n.name, n.x, n.y).catch(() => {})
}

onMounted(load)
</script>
