<template>
  <div class="flex flex-col gap-3">
    <div v-for="f in fields" :key="f.fieldname">
      <TextInput v-if="isInput(f)" v-model="value[f.fieldname]" :label="f.label" :placeholder="f.description || ''" />
      <Textarea v-else-if="isTextarea(f)" v-model="value[f.fieldname]" :label="f.label" :placeholder="f.description || ''" :rows="f.fieldtype === 'Code' ? 6 : 3" />
      <Select v-else-if="f.fieldtype === 'Select'" v-model="value[f.fieldname]" :label="f.label" :options="selectOptions(f)" />
      <LinkField v-else-if="f.fieldtype === 'Link'" v-model="value[f.fieldname]" :label="f.label" :doctype="f.link_doctype" :title-field="f.link_title_field || 'name'" />
      <Checkbox v-else-if="f.fieldtype === 'Check'" v-model="value[f.fieldname]" :label="f.label" />
      <TextInput v-else v-model="value[f.fieldname]" :label="f.label" />
    </div>
  </div>
</template>

<script setup>
import { TextInput, Textarea, Select, Checkbox } from 'frappe-ui'
import LinkField from './LinkField.vue'

defineProps({
  fields: { type: Array, required: true },
  value: { type: Object, required: true },
})

function isInput(f) {
  return ['Data', 'Int', 'Float', 'Currency', 'Date', 'Datetime', 'Time'].includes(f.fieldtype)
}
function isTextarea(f) {
  return ['Small Text', 'Long Text', 'Text Editor', 'Code'].includes(f.fieldtype)
}
function selectOptions(f) {
  return (f.options || '').split('\n').filter(Boolean).map((o) => ({ label: o, value: o }))
}
</script>
