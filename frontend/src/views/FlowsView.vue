<template>
  <AppLayout>
    <div class="p-6">
      <div class="mb-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold">Flujos</h1>
          <p class="text-sm text-ink-gray-5">Diseña el recorrido de tus agentes: disparador → lógica → herramientas → respuesta.</p>
        </div>
        <Button variant="solid" theme="blue" label="Nuevo flujo" @click="openCreate()" />
      </div>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!flows.length" class="rounded-lg border border-dashed border-outline-gray-2 p-10 text-center">
        <div class="mb-2 text-2xl">🔀</div>
        <div class="mb-1 font-medium">Aún no tienes flujos</div>
        <div class="mb-4 text-sm text-ink-gray-5">Crea tu primer flujo para definir cómo responde tu agente.</div>
        <Button variant="solid" theme="blue" label="Crear flujo" @click="openCreate()" />
      </div>

      <div v-else class="grid gap-3 lg:grid-cols-2">
        <div v-for="f in flows" :key="f.name" class="cursor-pointer rounded-xl border p-4 transition" :class="selected === f.name ? 'border-outline-blue-4 bg-surface-base' : 'border-outline-gray-2 bg-surface-base hover:bg-surface-gray-1'" @click="select(f)">
          <div class="mb-1 flex items-center justify-between gap-2">
            <span class="truncate font-medium">{{ f.title }}</span>
            <Badge :label="statusLabel(f.status)" variant="subtle" :theme="statusTheme(f.status)" />
          </div>
          <div class="text-xs text-ink-gray-5">v{{ f.revision }} · {{ shortDate(f.modified) }}</div>
        </div>
      </div>

      <!-- Editor -->
      <div v-if="selectedFlow" class="mt-6 rounded-xl border border-outline-gray-2 bg-surface-base p-5">
        <div class="mb-4 flex items-center justify-between">
          <div>
            <div class="font-medium">{{ selectedFlow.title }}</div>
            <div class="text-xs text-ink-gray-5">v{{ selectedFlow.revision }}</div>
          </div>
          <Button variant="ghost" size="sm" label="Cerrar" @click="selectedFlow = null" />
        </div>

        <div class="mb-4 flex flex-wrap gap-2">
          <Badge v-for="n in nodes" :key="n.id" :label="typeLabel(n.type)" variant="subtle" theme="blue" />
          <Badge v-if="!nodes.length" label="Sin nodos" variant="subtle" theme="gray" />
        </div>

        <div class="mb-2 text-xs font-medium uppercase text-ink-gray-5">Diseño del flujo (JSON)</div>
        <Textarea v-model="graphText" class="font-mono text-xs" :rows="10" />
        <div class="mt-3 flex gap-2">
          <Button variant="solid" theme="blue" label="Guardar flujo" :loading="saving" @click="saveFlow" />
          <Button variant="ghost" label="Cancelar" @click="selectedFlow = null" />
        </div>
        <div v-if="graphError" class="mt-2 text-sm text-ink-red-7">{{ graphError }}</div>
      </div>

      <Dialog v-model:open="showCreate" title="Nuevo flujo" size="sm">
        <TextInput v-model="newTitle" label="Nombre del flujo" placeholder="Atención al cliente" />
        <template #actions="{ close }">
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" label="Crear" :loading="creating" @click="create" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Button, Badge, Dialog, TextInput, Textarea, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const flows = ref([])
const loading = ref(true)
const showCreate = ref(false)
const newTitle = ref('')
const creating = ref(false)
const saving = ref(false)
const selected = ref('')
const selectedFlow = ref(null)
const graphText = ref('')
const graphError = ref('')

const NODE_LABELS = { trigger: 'Disparador', agent: 'Agente', condition: 'Condición', tool: 'Herramienta', approval: 'Aprobación', response: 'Respuesta' }

const nodes = computed(() => {
  try { return JSON.parse(graphText.value || '{}').nodes || [] } catch { return [] }
})
function typeLabel(t) { return NODE_LABELS[t] || t || 'Nodo' }
function statusLabel(s) { return { Draft: 'Borrador', Published: 'Publicado', Archived: 'Archivado' }[s] || s || 'Borrador' }
function statusTheme(s) { return { Published: 'green', Archived: 'gray' }[s] || 'amber' }
function shortDate(d) { return d ? String(d).slice(0, 16) : '' }

async function load() {
  loading.value = true
  try { flows.value = await api.listFlows() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}

function openCreate() { newTitle.value = ''; showCreate.value = true }

async function create() {
  if (!newTitle.value.trim()) { toast.warning('Escribe un nombre para el flujo.'); return }
  creating.value = true
  try {
    const f = await api.createFlow({ title: newTitle.value })
    toast.success('Flujo creado.')
    showCreate.value = false
    await load()
    selected.value = f.name
    await select({ name: f.name, title: f.title, status: f.status, revision: f.revision })
  } catch (e) { toast.error(humanError(e)) } finally { creating.value = false }
}

async function select(f) {
  selected.value = f.name
  try {
    const d = await api.getFlow(f.name)
    selectedFlow.value = d
    graphText.value = d.graph_json || ''
    graphError.value = ''
  } catch (e) { toast.error(humanError(e)) }
}

async function saveFlow() {
  try { JSON.parse(graphText.value) } catch (e) { graphError.value = 'JSON inválido: ' + e.message; return }
  saving.value = true
  try {
    await api.saveFlow({ name: selectedFlow.value.name, title: selectedFlow.value.title, graph_json: graphText.value })
    toast.success('Flujo guardado.')
    selectedFlow.value = null
    selected.value = ''
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

onMounted(load)
</script>
