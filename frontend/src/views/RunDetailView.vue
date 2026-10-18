<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="os-eyebrow">Centro de ejecución</div>
          <h1 class="os-h1">{{ run.run_code || 'Ejecución' }}</h1>
          <p class="text-sm" style="color: var(--os-steel)">{{ run.process_ref }} · {{ run.status }}</p>
        </div>
        <Button variant="ghost" label="← Ejecuciones" @click="$router.push('/runs')" />
      </div>

      <div v-if="loading" class="py-8 text-center" style="color: var(--os-steel)">Cargando…</div>
      <div v-else class="space-y-3">
        <div v-for="s in steps" :key="s.name" class="os-card flex items-center justify-between gap-3">
          <div class="min-w-0">
            <div class="font-medium" style="color:#fff">{{ s.step_title_snapshot || s.step_key }}</div>
            <div class="text-xs" style="color: var(--os-steel)">{{ s.step_type_snapshot || '' }} · {{ s.actor_user || s.actor_role || '' }}</div>
            <div v-if="s.reference_doctype && s.reference_name" class="text-xs mt-1" style="color: var(--os-orange)">→ {{ s.reference_doctype }}: {{ s.reference_name }}</div>
          </div>
          <div class="flex items-center gap-2">
            <span class="os-pill">{{ s.status }}</span>
            <Button v-if="s.status === 'Queued' || s.status === 'Blocked'" variant="solid" theme="blue" label="Iniciar" @click="startStep(s)" />
            <Button v-if="s.status === 'Running' || s.status === 'Approved'" variant="solid" theme="blue" label="Completar" @click="openComplete(s)" />
          </div>
        </div>
      </div>

      <Dialog v-model:open="completeOpen" title="Completar paso" size="md">
        <Textarea v-model="comment" label="Comentario / evidencia" rows="3" />
        <template #actions="{ close }">
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" label="Completar" :loading="saving" @click="completeStep" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { call, Button, Dialog, Textarea, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { bridgeApi } from '../resources/runtime'
import { humanError } from '../resources/os'

const route = useRoute()
const run = ref({})
const steps = ref([])
const loading = ref(false)
const saving = ref(false)
const completeOpen = ref(false)
const comment = ref('')
const activeStep = ref(null)

async function load() {
  loading.value = true
  try {
    run.value = await call('frappe.client.get', { doctype: 'OS Run', name: route.params.name })
    steps.value = await call('frappe.client.get_list', { doctype: 'OS Step Run', filters: { run: route.params.name }, fields: ['name', 'step_key', 'step_title_snapshot', 'step_type_snapshot', 'status', 'actor_user', 'actor_role', 'reference_doctype', 'reference_name'], order_by: 'queued_at asc' })
  } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}

async function startStep(s) {
  try {
    await bridgeApi.startStep(s.name)
    toast.success('Paso iniciado.')
    await load()
  } catch (e) { toast.error(humanError(e)) }
}

function openComplete(s) { activeStep.value = s; comment.value = ''; completeOpen.value = true }

async function completeStep() {
  saving.value = true
  try {
    await bridgeApi.completeStep(activeStep.value.name, comment.value)
    toast.success('Paso completado.')
    completeOpen.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

onMounted(load)
</script>
