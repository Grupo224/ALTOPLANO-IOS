<template>
  <AppLayout>
    <div class="p-6">
      <h1 class="mb-1 text-xl font-semibold">Gastos</h1>
      <p class="mb-4 text-sm text-ink-gray-5">Consumo y control presupuestario de tus agentes.</p>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <template v-else>
        <div v-if="summary" class="mb-4 grid gap-3 sm:grid-cols-3">
          <div class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
            <div class="text-sm text-ink-gray-5">Presupuesto</div>
            <div class="text-xl font-semibold">{{ formatMoney(summary.budget) }}</div>
          </div>
          <div class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
            <div class="text-sm text-ink-gray-5">Consumido</div>
            <div class="text-xl font-semibold">{{ formatMoney(summary.spent) }}</div>
          </div>
          <div class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
            <div class="text-sm text-ink-gray-5">Disponible</div>
            <div class="text-xl font-semibold">{{ formatMoney(summary.remaining) }}</div>
          </div>
        </div>

        <div v-if="!events.length" class="rounded-lg border border-outline-gray-2 p-8 text-center text-sm text-ink-gray-5">
          Sin eventos de consumo.
        </div>
        <div v-else class="overflow-hidden rounded-xl border border-outline-gray-2">
          <table class="w-full text-sm">
            <thead class="bg-surface-gray-2 text-left text-ink-gray-5">
              <tr><th class="px-4 py-2">Fecha</th><th class="px-4 py-2">Concepto</th><th class="px-4 py-2 text-right">Importe</th></tr>
            </thead>
            <tbody>
              <tr v-for="e in events" :key="e.name" class="border-t border-outline-gray-2">
                <td class="px-4 py-2 text-ink-gray-5">{{ e.creation }}</td>
                <td class="px-4 py-2">{{ e.agent || e.type || e.name }}</td>
                <td class="px-4 py-2 text-right">{{ formatMoney(e.amount) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const summary = ref(null)
const events = ref([])
const loading = ref(true)

function formatMoney(v) {
  const n = Number(v) || 0
  return '$ ' + n.toLocaleString('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

async function load() {
  loading.value = true
  try {
    const [s, ev] = await Promise.all([api.usageSummary(), api.usageEvents()])
    summary.value = s
    events.value = ev || []
  } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
onMounted(load)
</script>
