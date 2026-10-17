<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">{{ eyebrow }}</div>
          <h1 class="os-h1">{{ title }}</h1>
          <p class="text-sm" style="color: var(--os-steel)">{{ description }}</p>
        </div>
        <Button v-if="!readOnly" variant="solid" theme="blue" :label="'＋ ' + createLabel" @click="open()" />
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
            <tr v-for="r in rows" :key="r.name" class="border-t" style="border-color: #1a283e">
              <td v-for="c in columns" :key="c.fieldname" class="px-3 py-2.5" style="color: var(--os-text)">{{ r[c.fieldname] || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <Dialog v-model:open="openCreate" :title="'Nuevo ' + createLabel" size="md">
        <div class="flex flex-col gap-3">
          <TextInput v-for="f in createFields" :key="f.fieldname" v-model="form[f.fieldname]" :label="f.label" :type="f.type || 'text'" />
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
import { useList, call, Button, Dialog, TextInput, toast } from 'frappe-ui'
import AppLayout from './AppLayout.vue'
import { humanError } from '../resources/os'

const props = defineProps({
  eyebrow: String,
  title: String,
  description: String,
  doctype: { type: String, required: true },
  fields: { type: Array, required: true },
  columns: { type: Array, required: true },
  createLabel: { type: String, default: 'registro' },
  readOnly: { type: Boolean, default: false },
  createFields: { type: Array, default: () => [] },
  defaults: { type: Object, default: () => ({}) },
})

const list = useList({ doctype: props.doctype, fields: props.fields, orderBy: 'modified desc', limit: 100 })
const rows = computed(() => list.data || [])
const loading = computed(() => list.loading)

const openCreate = ref(false)
const form = reactive({})
const saving = ref(false)

function open() { for (const f of props.createFields) form[f.fieldname] = ''; openCreate.value = true }

async function create() {
  saving.value = true
  try {
    await call('frappe.client.insert', { doc: { doctype: props.doctype, ...props.defaults, ...form } })
    toast.success(props.createLabel + ' creado.')
    openCreate.value = false
    list.reload()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}
</script>
