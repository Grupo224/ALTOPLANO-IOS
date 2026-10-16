<template>
  <AppLayout>
    <div class="p-6">
      <div class="mb-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold">Mis agentes</h1>
          <p class="text-sm text-ink-gray-5">Crea, prueba y activa agentes para tu negocio.</p>
        </div>
        <Button variant="solid" theme="blue" label="Crear agente" @click="openCreate" />
      </div>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!agents.length" class="rounded-lg border border-outline-gray-2 p-8 text-center">
        <div class="text-sm font-medium">Aún no tienes agentes</div>
        <div class="mb-4 text-sm text-ink-gray-5">Cuéntanos sobre tu negocio y crea tu primer agente.</div>
        <Button variant="solid" theme="blue" label="Crear agente" @click="openCreate" />
      </div>
      <div v-else class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <RouterLink v-for="a in agents" :key="a.name" :to="'/agents/' + a.name"
          class="rounded-xl border border-outline-gray-2 bg-surface-base p-4 transition hover:shadow-md">
          <div class="mb-2 flex items-center justify-between">
            <span class="text-sm font-medium">{{ a.display_name }}</span>
            <Badge :label="a.observed_state" variant="subtle" :theme="stateTheme(a.observed_state)" />
          </div>
          <p class="mb-3 line-clamp-2 text-sm text-ink-gray-6">{{ a.summary || 'Sin objetivo definido' }}</p>
          <div class="text-[11px] text-ink-gray-4">{{ a.audience }} · {{ a.company }}</div>
        </RouterLink>
      </div>

      <Dialog v-model:open="showCreate" title="Crear agente" size="md">
        <div class="flex flex-col gap-3">
          <TextInput v-model="form.display_name" label="Nombre del agente" placeholder="Ej. Atención al cliente" />
          <Textarea v-model="form.summary" label="Qué hará" placeholder="Responde preguntas y crea seguimientos" />
          <Select v-model="form.audience" label="Público" :options="['Customer','Internal']" />
          <TextInput v-model="form.template" label="Plantilla (opcional)" placeholder="Nombre de plantilla publicada" />
        </div>
        <template #actions="{ close }">
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" label="Crear" :loading="creating" @click="create" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, Dialog, TextInput, Textarea, Select, Badge } from 'frappe-ui'
import { toast } from 'frappe-ui'
import { RouterLink } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const agents = ref([])
const loading = ref(true)
const showCreate = ref(false)
const creating = ref(false)
const form = ref({ display_name: '', summary: '', audience: 'Customer', template: '' })

function stateTheme(s) {
  const map = { Active: 'green', NeedsSetup: 'amber', Draft: 'gray', Degraded: 'amber', Failed: 'red', Paused: 'gray', Archived: 'gray' }
  return map[s] || 'gray'
}

async function load() {
  loading.value = true
  try { agents.value = await api.listAgents() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
function openCreate() { form.value = { display_name: '', summary: '', audience: 'Customer', template: '' }; showCreate.value = true }
async function create() {
  creating.value = true
  try {
    const a = await api.createAgent(form.value)
    toast.success('Agente creado.')
    showCreate.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { creating.value = false }
}
onMounted(load)
</script>
