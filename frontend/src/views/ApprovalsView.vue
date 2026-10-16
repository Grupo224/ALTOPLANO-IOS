<template>
  <AppLayout>
    <div class="p-6">
      <h1 class="mb-1 text-xl font-semibold">Aprobaciones</h1>
      <p class="mb-4 text-sm text-ink-gray-5">Acciones que Cerebro propone y requieren tu confirmación.</p>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!approvals.length" class="rounded-lg border border-outline-gray-2 p-8 text-center text-sm text-ink-gray-5">
        No hay aprobaciones pendientes.
      </div>
      <div v-else class="flex flex-col gap-3">
        <div v-for="a in approvals" :key="a.name" class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
          <div class="mb-1 flex items-center justify-between">
            <span class="text-sm font-medium">{{ a.tool || a.action || a.name }}</span>
            <Badge :label="a.state || 'Pending'" variant="subtle" theme="amber" />
          </div>
          <p class="mb-3 text-sm text-ink-gray-6">{{ a.summary || a.payload || '—' }}</p>
          <div class="flex gap-2">
            <Button variant="solid" theme="green" label="Aprobar" @click="decide(a, 'Approved')" />
            <Button variant="solid" theme="red" label="Rechazar" @click="decide(a, 'Rejected')" />
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, Badge } from 'frappe-ui'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const approvals = ref([])
const loading = ref(true)

async function load() {
  loading.value = true
  try { approvals.value = await api.listApprovals() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
async function decide(a, decision) {
  try { await api.decide(a.name, decision, ''); toast.success(decision === 'Approved' ? 'Aprobado.' : 'Rechazado.'); await load() }
  catch (e) { toast.error(humanError(e)) }
}
onMounted(load)
</script>
