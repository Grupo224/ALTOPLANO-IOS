<template>
  <AppLayout>
    <div class="p-6">
      <h1 class="mb-1 text-xl font-semibold">Actividad</h1>
      <p class="mb-4 text-sm text-ink-gray-5">Registro auditable de acciones de ERP conectadas.</p>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!items.length" class="rounded-lg border border-outline-gray-2 p-8 text-center text-sm text-ink-gray-5">
        Sin actividad registrada.
      </div>
      <div v-else class="flex flex-col gap-3">
        <div v-for="it in items" :key="it.name" class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
          <div class="mb-1 flex items-center justify-between">
            <span class="text-sm font-medium">{{ it.doctype || it.type || it.name }}</span>
            <span class="text-[12px] text-ink-gray-5">{{ it.creation }}</span>
          </div>
          <div class="text-sm text-ink-gray-6">{{ it.subject || it.description || '—' }}</div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const items = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try { items.value = await api.activity() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
onMounted(load)
</script>
