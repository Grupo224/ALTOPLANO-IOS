<template>
  <div class="app-shell">
    <aside class="os-sidebar shrink-0">
      <div class="os-brand">LIVINGORG<small>OS · SISTEMA OPERATIVO VIVO</small></div>

      <template v-for="(group, gi) in navGroups" :key="gi">
        <div class="os-navlabel">{{ group.label }}</div>
        <RouterLink v-for="item in group.items" :key="item.route" :to="item.route" class="os-nav-btn" :class="{ active: isActive(item.route) }">
          <span>{{ item.icon }}</span><span>{{ item.label }}</span>
        </RouterLink>
      </template>

      <div class="os-foot">● &nbsp; Entorno de demostración<br>LivingOrg OS × Frappe</div>
    </aside>

    <main class="flex min-w-0 flex-1 flex-col">
      <div class="os-top">
        <span class="text-sm" style="color: var(--os-steel)">Altoplano &nbsp; / &nbsp; {{ currentLabel }}</span>
        <div class="flex items-center gap-2">
          <span class="os-pill">● En vivo</span>
          <span class="flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold" style="background:#23334a;color:#ff9422">{{ initials }}</span>
        </div>
      </div>
      <div class="scroll-area min-h-0 flex-1">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navGroups = [
  {
    label: 'Operación',
    items: [
      { label: 'Command Center', route: '/', icon: '⌂' },
      { label: 'Organigrama', route: '/org', icon: '⊞' },
      { label: 'Procesos', route: '/processes', icon: '⑂' },
      { label: 'SOP', route: '/sop', icon: '▤' },
      { label: 'Mi Trabajo', route: '/work', icon: '✓' },
      { label: 'Aprobaciones', route: '/approvals', icon: '☑' },
      { label: 'Ejecuciones', route: '/runs', icon: '▶' },
    ],
  },
  {
    label: 'Gobierno',
    items: [
      { label: 'Agentes y Prompts', route: '/agents', icon: '◇' },
      { label: 'Roles', route: '/roles', icon: '✧' },
      { label: 'KPIs', route: '/kpis', icon: '◴' },
      { label: 'Integraciones', route: '/integrations', icon: '⊞' },
    ],
  },
  {
    label: 'Conocimiento',
    items: [
      { label: 'Conocimiento', route: '/knowledge', icon: '▦' },
    ],
  },
  {
    label: 'Analítica',
    items: [
      { label: 'Analítica', route: '/analytics', icon: '▥' },
    ],
  },
]

const flat = navGroups.flatMap((g) => g.items)
const currentLabel = computed(() => flat.find((i) => isActive(i.route))?.label || 'Command Center')
const initials = computed(() => (typeof frappe !== 'undefined' && frappe.session?.user ? frappe.session.user.slice(0, 2).toUpperCase() : 'AQ'))

function isActive(r) {
  if (r === '/') return route.path === '/'
  return route.path === r || route.path.startsWith(r + '/')
}
</script>
