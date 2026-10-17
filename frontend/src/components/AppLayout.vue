<template>
  <div class="app-shell as-app bg-[var(--as-bg)] text-ink-gray-9">
    <aside class="as-sidebar shrink-0">
      <div class="as-brand">◭ altoplano<small>AGENT STUDIO</small></div>
      <div class="as-workspace">▦ &nbsp; {{ session.company || 'Grupo Altoplano' }}</div>

      <template v-for="(group, gi) in navGroups" :key="gi">
        <div class="as-navlabel">{{ group.label }}</div>
        <RouterLink
          v-for="item in group.items"
          :key="item.route"
          :to="item.route"
          class="as-nav-btn"
          :class="{ active: $route.path === item.route || (item.route !== '/' && $route.path.startsWith(item.route)) }"
        >
          <span>{{ item.icon }}</span><span>{{ item.label }}</span>
        </RouterLink>
      </template>

      <div class="as-foot">● &nbsp; Entorno de demostración<br>OpenClaw × Frappe<br>Altoplano · La experiencia</div>
    </aside>

    <main class="flex min-w-0 flex-1 flex-col">
      <div class="as-top">
        <span class="text-sm text-ink-gray-7">Workspace &nbsp; / &nbsp; {{ currentLabel }}</span>
        <div class="flex items-center gap-2">
          <span class="as-pill">● Datos de ejemplo</span>
          <span class="flex h-8 w-8 items-center justify-center rounded-full bg-surface-blue-2 text-sm font-semibold text-ink-blue-7">{{ initials }}</span>
        </div>
      </div>
      <div class="scroll-area min-h-0 flex-1">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useSession } from '../composables/useSession'

const { state: session, load } = useSession()
onMounted(() => load())

const navGroups = [
  {
    label: 'Workspace',
    items: [
      { label: 'Mis agentes', route: '/agents', icon: '◇' },
      { label: 'Flujos de trabajo', route: '/flows', icon: '⌘' },
      { label: 'Cerebro ERP', route: '/cerebro', icon: '◌' },
    ],
  },
  {
    label: 'Conocimiento y acceso',
    items: [
      { label: 'Contexto general', route: '/business', icon: '▤' },
      { label: 'Conectores', route: '/connections', icon: '⊞' },
    ],
  },
  {
    label: 'Control',
    items: [
      { label: 'Consumo y límites', route: '/spending', icon: '◴' },
      { label: 'Ejecuciones', route: '/activity', icon: '≡' },
      { label: 'Agenda', route: '/agenda', icon: '📅' },
    ],
  },
]

const currentLabel = computed(() => {
  const flat = navGroups.flatMap((g) => g.items)
  const m = flat.find((i) => i.route !== '/' && routeMatches(i.route))
  return m ? m.label : 'Inicio'
})
function routeMatches(r) {
  return typeof window !== 'undefined' && window.location.pathname.startsWith(r)
}

const initials = computed(() => (session.fullName || session.user || 'AQ').split(/\s+/).slice(0, 2).map((x) => x[0]).join('').toUpperCase())
</script>
