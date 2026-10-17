<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">Process Studio</div>
          <h1 class="os-h1">Procesos</h1>
          <p class="text-sm" style="color: var(--os-steel)">Dibuja cómo se hace el trabajo: pasos, decisiones y responsables.</p>
        </div>
        <Button variant="solid" theme="blue" label="＋ Nuevo proceso" @click="openCreate = true" />
      </div>

      <div v-if="loading" class="py-8 text-center" style="color: var(--os-steel)">Cargando…</div>
      <div v-else-if="!rows.length" class="os-card py-10 text-center" style="color: var(--os-steel)">Aún no hay procesos. Crea el primero.</div>
      <div v-else class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        <RouterLink v-for="p in rows" :key="p.name" :to="'/processes/' + p.name" class="os-card transition hover:border-[#ff9422]">
          <div class="mb-1 flex items-center justify-between">
            <span class="font-medium" style="color:#fff">{{ p.process_title }}</span>
            <span class="os-pill">{{ p.status || 'Draft' }}</span>
          </div>
          <div class="text-xs" style="color: var(--os-steel)">{{ p.process_code }}</div>
          <div class="mt-2 text-sm" style="color: var(--os-text)">{{ p.purpose }}</div>
        </RouterLink>
      </div>

      <Dialog v-model:open="openCreate" title="Nuevo proceso" size="md">
        <div class="flex flex-col gap-3">
          <TextInput v-model="form.process_title" label="Nombre del proceso" />
          <TextInput v-model="form.process_code" label="Código / ID" />
          <TextInput v-model="form.purpose" label="Propósito" />
          <Select v-model="form.risk_level" label="Criticidad" :options="['Low','Medium','High','Critical']" />
          <Select v-model="form.trigger_type" label="Disparador" :options="['Manual','ERP Event','Webhook','Schedule','External']" />
        </div>
        <template #actions="{ close }">
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" label="Crear" :loading="saving" @click="create" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useList, call, Button, Dialog, TextInput, Select, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { osApi, humanError } from '../resources/os'

const list = useList({ doctype: 'OS Process', fields: ['name', 'process_title', 'process_code', 'purpose', 'status', 'risk_level'], orderBy: 'modified desc', limit: 100 })
const rows = computed(() => list.data || [])
const loading = computed(() => list.loading)

const openCreate = ref(false)
const form = reactive({ process_title: '', process_code: '', purpose: '', risk_level: 'Medium', trigger_type: 'Manual' })
const saving = ref(false)

async function create() {
  if (!form.process_title.trim()) { toast.warning('Escribe el nombre del proceso.'); return }
  saving.value = true
  try {
    await osApi.createProcess({ process_title: form.process_title, process_code: form.process_code, purpose: form.purpose, risk_level: form.risk_level, trigger_type: form.trigger_type })
    toast.success('Proceso creado.')
    openCreate.value = false
    list.reload()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}
</script>
