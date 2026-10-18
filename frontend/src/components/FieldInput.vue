<template>
  <Select v-if="field.type === 'select'" v-model="value" :options="field.options" :label="t(field.label)" />
  <LinkField v-else-if="field.type === 'link'" v-model="value" :label="t(field.label)" :doctype="field.linkDoctype" />
  <Textarea v-else-if="field.type === 'textarea'" v-model="value" :label="t(field.label)" :rows="3" :placeholder="field.hint || ''" />
  <TextInput v-else-if="field.type === 'number'" v-model="value" :label="t(field.label)" type="number" :placeholder="field.hint || ''" />
  <TextInput v-else v-model="value" :label="t(field.label)" :placeholder="field.hint || ''" />
</template>

<script setup>
import { computed } from 'vue'
import { TextInput, Textarea, Select } from 'frappe-ui'
import LinkField from './LinkField.vue'
import { t } from '../resources/es'

const props = defineProps({
  field: { type: Object, required: true },
  modelValue: null,
})
const emit = defineEmits(['update:modelValue'])

const value = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})
</script>
