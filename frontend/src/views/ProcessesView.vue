<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">Process Studio</div>
          <h1 class="os-h1">Procesos</h1>
          <p class="text-sm" style="color: var(--os-steel)">Dibuja cómo se hace el trabajo: pasos, decisiones y responsables.</p>
        </div>
        <Button variant="solid" theme="blue" label="＋ Nuevo proceso" @click="openCreate()" />
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

      <Dialog v-model:open="dialogOpen" :title="editingName ? 'Editar proceso' : 'Nuevo proceso'" size="xl">
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
import { RouterLink } from 'vue-router'
import { useList, call, Button, Dialog, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import OsForm from '../components/OsForm.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'

const list = useList({ doctype: 'OS Process', fields: ['name', 'process_title', 'process_code', 'purpose', 'status', 'risk_level'], orderBy: 'modified desc', limit: 200 })
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
    const r = await osApi.getDoctypeMeta('OS Process')
    metaFields.value = (r.fields || []).filter((f) => !['steps', 'edges', 'goals', 'canvas_json'].includes(f.fieldname))
  } catch (e) { toast.error(humanError(e)) } finally { metaLoading.value = false }
}

function openCreate() {
  editingName.value = null
  resetForm(metaFields.value, form, { status: 'Draft', trigger_type: 'Manual', max_autonomy: 'L1', risk_level: 'Medium', version_label: '1' })
  dialogOpen.value = true
}

async function editRow(p) {
  editingName.value = p.name
  resetForm(metaFields.value, form, {})
  try {
    const doc = await call('frappe.client.get', { doctype: 'OS Process', name: p.name })
    fillFromDoc(metaFields.value, form, doc)
    dialogOpen.value = true
  } catch (e) { toast.error(humanError(e)) }
}

async function save() {
  saving.value = true
  try {
    const values = coerceValues(metaFields.value, form)
    if (editingName.value) {
      await osApi.updateDoc('OS Process', editingName.value, values)
      toast.success('Proceso guardado.')
    } else {
      const r = await call('frappe.client.insert', { doc: { doctype: 'OS Process', ...values } })
      toast.success('Proceso creado.')
      editingName.value = r.name
    }
    dialogOpen.value = false
    list.reload()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

onMounted(loadMeta)
</script>
