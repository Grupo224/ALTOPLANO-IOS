<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">Prompts</div>
          <h1 class="os-h1">Prompts</h1>
          <p class="text-sm" style="color: var(--os-steel)">Los prompts reutilizables que tus agentes y pasos usan al ejecutar. Separa la identidad del agente (SOUL/SKILL) del prompt que consume.</p>
        </div>
        <Button variant="solid" theme="blue" label="＋ Nuevo prompt" @click="openCreate" />
      </div>

      <div v-if="loading" class="py-8 text-center" style="color: var(--os-steel)">Cargando…</div>
      <div v-else-if="!rows.length" class="os-card py-10 text-center" style="color: var(--os-steel)">Aún no hay prompts. Crea el primero.</div>
      <div v-else class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        <div v-for="p in rows" :key="p.name" class="os-card transition hover:border-[#ff9422] cursor-pointer" @click="edit(p)">
          <div class="mb-1 flex items-center justify-between">
            <span class="font-medium" style="color:#fff">{{ p.prompt_title }}</span>
            <span class="os-pill">{{ p.status || 'Draft' }}</span>
          </div>
          <div class="text-xs" style="color: var(--os-steel)">{{ p.prompt_code }}</div>
          <div class="mt-2 text-sm" style="color: var(--os-text)">{{ p.system_instruction }}</div>
        </div>
      </div>

      <Dialog v-model:open="dialogOpen" :title="editingName ? 'Editar prompt' : 'Nuevo prompt'" size="xl">
        <div v-if="metaLoading" class="py-6 text-center" style="color: var(--os-steel)">Cargando formulario…</div>
        <OsForm v-else :fields="metaFields" :value="form" />
        <template #actions="{ close }">
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" :label="editingName ? 'Guardar' : 'Crear'" :loading="saving" @click="save" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useList, call, Button, Dialog, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import OsForm from '../components/OsForm.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'

const list = useList({ doctype: 'OS Prompt', fields: ['name', 'prompt_title', 'prompt_code', 'status', 'system_instruction'], orderBy: 'modified desc', limit: 200 })
const rows = computed(() => list.data || [])
const loading = computed(() => list.loading)

const dialogOpen = ref(false)
const editingName = ref(null)
const form = reactive({})
const saving = ref(false)
const metaFields = ref([])
const metaLoading = ref(false)

async function loadMeta() {
  metaLoading.value = true
  try {
    const r = await osApi.getDoctypeMeta('OS Prompt')
    metaFields.value = r.fields || []
  } catch (e) { toast.error(humanError(e)) } finally { metaLoading.value = false }
}

function openCreate() {
  editingName.value = null
  resetForm(metaFields.value, form, { status: 'Draft' })
  dialogOpen.value = true
}

async function edit(p) {
  editingName.value = p.name
  resetForm(metaFields.value, form, {})
  try {
    const doc = await call('frappe.client.get', { doctype: 'OS Prompt', name: p.name })
    fillFromDoc(metaFields.value, form, doc)
    dialogOpen.value = true
  } catch (e) { toast.error(humanError(e)) }
}

async function save() {
  saving.value = true
  try {
    const values = coerceValues(metaFields.value, form)
    if (editingName.value) {
      await osApi.updateDoc('OS Prompt', editingName.value, values)
      toast.success('Prompt guardado.')
    } else {
      await call('frappe.client.insert', { doc: { doctype: 'OS Prompt', ...values } })
      toast.success('Prompt creado.')
    }
    dialogOpen.value = false
    list.reload()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

onMounted(loadMeta)
</script>
