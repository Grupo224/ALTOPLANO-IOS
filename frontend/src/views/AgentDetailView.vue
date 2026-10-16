<template>
  <AppLayout>
    <div class="p-6">
      <RouterLink to="/agents" class="mb-3 inline-flex items-center gap-1 text-sm text-ink-gray-5 hover:text-ink-gray-9">
        <span class="lucide-arrow-left size-4"></span> Mis agentes
      </RouterLink>
      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else class="max-w-3xl">
        <div class="mb-4 flex items-center gap-3">
          <h1 class="text-xl font-semibold">{{ agent.display_name }}</h1>
          <Badge :label="agent.observed_state" variant="subtle" theme="gray" />
        </div>

        <div class="mb-4 rounded-xl border border-outline-gray-2 bg-surface-base p-4">
          <div class="mb-2 text-sm font-medium">Objetivo</div>
          <TextInput v-model="summary" class="mb-3" placeholder="Qué hará este agente" />
          <div class="mb-2 text-sm font-medium">Indicaciones</div>
          <Textarea v-model="instructions" class="mb-3" placeholder="Instrucciones en lenguaje cotidiano" rows="5" />
          <Button variant="solid" theme="blue" label="Guardar" :loading="saving" @click="save" />
        </div>

        <div class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
          <div class="mb-2 text-sm font-medium">Revisión</div>
          <p class="mb-3 text-sm text-ink-gray-5">Crea una revisión inmutable del borrador actual para poder probarlo.</p>
          <Button variant="subtle" label="Crear revisión" @click="revise" />
          <div v-if="agent.current_revision" class="mt-2 text-sm text-ink-gray-5">
            Revisión actual: {{ agent.current_revision }}
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, Badge, TextInput, Textarea } from 'frappe-ui'
import { toast } from 'frappe-ui'
import { RouterLink, useRoute } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const route = useRoute()
const agent = ref({})
const summary = ref('')
const instructions = ref('')
const loading = ref(true)
const saving = ref(false)

async function load() {
  loading.value = true
  try {
    agent.value = await api.getAgent(route.params.id)
    summary.value = agent.value.summary || ''
    instructions.value = agent.value.instructions || ''
  } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
async function save() {
  saving.value = true
  try {
    await api.updateAgent({ agent: agent.value.name, summary: summary.value, instructions: instructions.value })
    toast.success('Guardado.')
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}
async function revise() {
  try {
    const r = await api.createRevision(agent.value.name)
    toast.success('Revisión creada: ' + r.name)
    await load()
  } catch (e) { toast.error(humanError(e)) }
}
onMounted(load)
</script>
