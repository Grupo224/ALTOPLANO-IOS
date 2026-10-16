<template>
  <AppLayout>
    <div class="p-6">
      <h1 class="mb-1 text-xl font-semibold">Información del negocio</h1>
      <p class="mb-4 text-sm text-ink-gray-5">Lo que tus agentes deben saber para representarte.</p>
      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else class="max-w-2xl rounded-xl border border-outline-gray-2 bg-surface-base p-4">
        <div class="flex flex-col gap-3">
          <TextInput v-model="form.display_name" label="Nombre del negocio" />
          <Textarea v-model="form.offering" label="Qué ofrece tu negocio" rows="4" />
          <TextInput v-model="form.audience" label="A quién atiendes" />
          <Select v-model="form.tone" label="Cómo quieres que responda" :options="['Cercano','Profesional','Breve']" />
          <TextInput v-model="form.timezone" label="Zona horaria" placeholder="America/Mexico_City" />
          <Textarea v-model="form.handoff_instructions" label="Cuándo pedir ayuda humana" rows="3" />
        </div>
        <Button variant="solid" theme="blue" class="mt-4" label="Guardar" :loading="saving" @click="save" />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, TextInput, Textarea, Select } from 'frappe-ui'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const loading = ref(true)
const saving = ref(false)
const form = ref({})

async function load() {
  loading.value = true
  try {
    const p = await api.getProfile()
    form.value = p || { display_name: '', offering: '', audience: '', tone: 'Cercano', timezone: '', handoff_instructions: '' }
  } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
async function save() {
  saving.value = true
  try { await api.saveProfile(form.value); toast.success('Perfil guardado.') } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}
onMounted(load)
</script>
