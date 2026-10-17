<template>
  <AppLayout>
    <div class="as-body">
      <div class="mb-6 flex items-start justify-between">
        <div>
          <div class="as-eyebrow">Inteligencia con dirección</div>
          <h1 class="as-h1">Tu equipo de agentes.</h1>
          <p class="text-sm text-ink-gray-5">Cada agente, un propósito. Tú tienes el control.</p>
        </div>
        <RouterLink to="/wizard">
          <Button variant="solid" theme="blue" label="＋ Crear agente" />
        </RouterLink>
      </div>

      <div class="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div class="as-stat"><span>Agentes</span><strong>{{ agents.length }}</strong><small>en tu workspace</small></div>
        <div class="as-stat"><span>Activos</span><strong>{{ activeCount }}</strong><small>en operación</small></div>
        <div class="as-stat"><span>Flujos</span><strong>{{ flowCount }}</strong><small>diseñados</small></div>
        <div class="as-stat"><span>Conectores</span><strong>{{ connCount }}</strong><small>configurados</small></div>
      </div>

      <div class="mb-2 flex items-center justify-between">
        <h2 class="text-base font-semibold">Agentes del workspace</h2>
        <span class="text-xs text-ink-gray-5">{{ agents.length }} en total</span>
      </div>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!agents.length" class="rounded-lg border border-dashed border-outline-gray-2 p-10 text-center">
        <div class="mb-2 text-2xl">◇</div>
        <div class="mb-1 font-medium">Aún no tienes agentes</div>
        <div class="mb-4 text-sm text-ink-gray-5">Crea tu primer agente para empezar.</div>
        <RouterLink to="/wizard"><Button variant="solid" theme="blue" label="Crear agente" /></RouterLink>
      </div>
      <div v-else class="as-grid">
        <div v-for="a in agents" :key="a.name" class="as-card relative">
          <div class="as-avatar">{{ a.display_name?.[0] || '◇' }}</div>
          <h2 class="mb-1 text-base font-semibold">{{ a.display_name }}</h2>
          <p class="text-xs text-ink-gray-5">{{ a.summary || a.audience || '—' }}</p>
          <div class="mt-3 flex flex-wrap gap-1.5">
            <span class="as-tag">{{ a.model_id || 'Modelo por defecto' }}</span>
            <span v-if="a.audience" class="as-tag">{{ a.audience }}</span>
          </div>
          <div class="mt-4 flex items-center justify-between border-t border-outline-gray-2 pt-3 text-[11px] text-ink-gray-5">
            <span>{{ a.desired_state || 'Draft' }}</span>
            <Badge :label="statusLabel(a.desired_state)" variant="subtle" :theme="statusTheme(a.desired_state)" />
          </div>
        </div>
      </div>

      <div class="as-intro">
        <span style="font-size:30px">⌘</span>
        <div class="flex-1">
          <h2 class="text-base font-semibold">De una conversación a un proceso completo.</h2>
          <p class="text-xs text-ink-gray-5">Conecta agentes, decisiones y herramientas en un flujo visual.</p>
        </div>
        <RouterLink to="/flows"><Button variant="subtle" theme="blue" label="Explorar flujos →" /></RouterLink>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { Button, Badge, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const agents = ref([])
const flowCount = ref(0)
const connCount = ref(0)
const loading = ref(true)

const activeCount = computed(() => agents.value.filter((a) => ['Active', 'Published', 'Live'].includes(a.desired_state)).length)

function statusLabel(s) { return { Draft: 'Borrador', Active: 'Activo', Published: 'Activo', Live: 'Activo', Paused: 'Pausado' }[s] || s || 'Borrador' }
function statusTheme(s) { return { Active: 'green', Published: 'green', Live: 'green' }[s] || 'amber' }

onMounted(async () => {
  try {
    const [a, f, c] = await Promise.all([api.listAgents(), api.listFlows(), api.listConnections()])
    agents.value = a || []
    flowCount.value = (f || []).length
    connCount.value = (c || []).length
  } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
})
</script>
