<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">{{ eyebrow }}</div>
          <h1 class="os-h1">{{ title }}</h1>
          <p class="text-sm" style="color: var(--os-steel)">{{ description }}</p>
        </div>
        <Button v-if="!readOnly" variant="solid" theme="blue" :label="'＋ ' + createLabel" @click="openCreate()" />
      </div>

      <div v-if="loading" class="py-8 text-center" style="color: var(--os-steel)">Cargando…</div>
      <div v-else-if="!rows.length" class="os-card py-10 text-center" style="color: var(--os-steel)">Aún no hay registros. Crea el primero.</div>
      <div v-else class="os-card overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="text-left text-xs uppercase" style="color: var(--os-steel)">
              <th v-for="c in columns" :key="c.fieldname" class="px-3 py-2.5">{{ c.label }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in rows" :key="r.name" class="cursor-pointer border-t hover:bg-[#16233a]" style="border-color: #1a283e" @click="editRow(r)">
              <td v-for="c in columns" :key="c.fieldname" class="px-3 py-2.5" style="color: var(--os-text)">{{ r[c.fieldname] || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <Dialog v-model:open="dialogOpen" :title="(editingName ? 'Editar ' : 'Nuevo ') + createLabel" size="xl">
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
import AppLayout from './AppLayout.vue'
import OsForm from './OsForm.vue'
import { osApi, humanError, resetForm, fillFromDoc, coerceValues } from '../resources/os'

const props = defineProps({
  eyebrow: String,
  title: String,
  description: String,
  doctype: { type: String, required: true },
  fields: { type: Array, required: true },
  columns: { type: Array, required: true },
  createLabel: { type: String, default: 'registro' },
  defaults: { type: Object, default: () => ({}) },
  readOnly: { type: Boolean, default: false },
})

const list = useList({ doctype: props.doctype, fields: props.fields, orderBy: 'modified desc', limit: 200 })
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
    const r = await osApi.getDoctypeMeta(props.doctype)
    metaFields.value = r.fields || []
  } catch (e) { toast.error(humanError(e)) } finally { metaLoading.value = false }
}

function openCreate() {
  editingName.value = null
  resetForm(metaFields.value, form, props.defaults || {})
  dialogOpen.value = true
}

async function editRow(r) {
  if (props.readOnly) return
  editingName.value = r.name
  resetForm(metaFields.value, form, {})
  if (r && r.__doc) {
    fillFromDoc(metaFields.value, form, r.__doc)
    dialogOpen.value = true
    return
  }
  try {
    const doc = await call('frappe.client.get', { doctype: props.doctype, name: r.name })
    fillFromDoc(metaFields.value, form, doc)
    dialogOpen.value = true
  } catch (e) { toast.error(humanError(e)) }
}

async function save() {
  saving.value = true
  try {
    const values = coerceValues(metaFields.value, form)
    if (editingName.value) {
      await osApi.updateDoc(props.doctype, editingName.value, values)
      toast.success('Guardado.')
    } else {
      await call('frappe.client.insert', { doc: { doctype: props.doctype, ...props.defaults, ...values } })
      toast.success(props.createLabel + ' creado.')
    }
    dialogOpen.value = false
    list.reload()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

onMounted(loadMeta)
</script>
