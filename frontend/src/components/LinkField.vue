<template>
  <Select v-model="value" :options="options" :label="label" :placeholder="'Buscar ' + label" />
</template>

<script setup>
import { computed } from 'vue'
import { Select, useList } from 'frappe-ui'

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: '' },
  doctype: { type: String, required: true },
  titleField: { type: String, default: 'name' },
})
const emit = defineEmits(['update:modelValue'])

const value = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const tf = computed(() => (props.titleField && props.titleField !== 'name' ? props.titleField : 'name'))
const listFields = computed(() => (tf.value === 'name' ? ['name'] : ['name', tf.value]))

const list = useList({ doctype: props.doctype, fields: listFields.value, limit: 200, orderBy: 'modified desc' })

const options = computed(() => {
  const arr = (list.data || []).map((r) => ({ label: r[tf.value] || r.name, value: r.name }))
  if (props.modelValue && !arr.some((o) => o.value === props.modelValue)) {
    arr.unshift({ label: props.modelValue, value: props.modelValue })
  }
  return arr
})
</script>
