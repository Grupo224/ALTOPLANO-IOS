<template>
  <AppLayout>
    <div class="os-body">
      <div class="mb-6 flex flex-wrap items-start justify-between gap-3">
        <div>
          <div class="os-eyebrow">Process Studio</div>
          <h1 class="os-h1">Procesos</h1>
          <p class="text-sm" style="color: var(--os-steel)">Define el proceso con el asistente (SIPOC, RACI, metas) y dibuja su flujo en el lienzo.</p>
        </div>
        <Button variant="solid" theme="blue" label="＋ Nuevo proceso" @click="wizardOpen = true" />
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

      <ProcessWizard v-model:open="wizardOpen" @saved="onSaved" />
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useList, Button } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import ProcessWizard from '../components/ProcessWizard.vue'

const list = useList({ doctype: 'OS Process', fields: ['name', 'process_title', 'process_code', 'purpose', 'status', 'risk_level'], orderBy: 'modified desc', limit: 200 })
const rows = computed(() => list.data || [])
const loading = computed(() => list.loading)

const wizardOpen = ref(false)
const router = useRouter()

function onSaved(p) {
  list.reload()
  if (p && p.name) router.push('/processes/' + p.name)
}
</script>
