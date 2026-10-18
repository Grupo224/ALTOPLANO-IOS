<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">Centro de ejecución</div>
          <h1 class="os-h1">Ejecuciones</h1>
          <p class="text-sm" style="color: var(--os-steel)">Cada corrida de un proceso, con su estado y evidencia. Clic para abrir y avanzar pasos.</p>
        </div>
      </div>

      <div v-if="loading" class="py-8 text-center" style="color: var(--os-steel)">Cargando…</div>
      <div v-else-if="!rows.length" class="os-card py-10 text-center" style="color: var(--os-steel)">Aún no hay ejecuciones. Ejecuta un proceso desde el estudio de procesos.</div>
      <div v-else class="os-card overflow-x-auto">
        <table class="w-full text-sm">
          <thead><tr class="text-left text-xs uppercase" style="color: var(--os-steel)">
            <th class="px-3 py-2.5">Código</th><th class="px-3 py-2.5">Proceso</th><th class="px-3 py-2.5">Estado</th><th class="px-3 py-2.5">Iniciado por</th>
          </tr></thead>
          <tbody>
            <tr v-for="r in rows" :key="r.name" class="cursor-pointer border-t hover:bg-[#16233a]" style="border-color: #1a283e" @click="$router.push('/runs/' + r.name)">
              <td class="px-3 py-2.5" style="color: var(--os-text)">{{ r.run_code }}</td>
              <td class="px-3 py-2.5" style="color: var(--os-text)">{{ r.process_ref }}</td>
              <td class="px-3 py-2.5"><span class="os-pill">{{ r.status }}</span></td>
              <td class="px-3 py-2.5" style="color: var(--os-text)">{{ r.initiated_by || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useList } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'

const list = useList({ doctype: 'OS Run', fields: ['name', 'run_code', 'process_ref', 'status', 'initiated_by'], orderBy: 'modified desc', limit: 200 })
const rows = computed(() => list.data || [])
const loading = computed(() => list.loading)
</script>
