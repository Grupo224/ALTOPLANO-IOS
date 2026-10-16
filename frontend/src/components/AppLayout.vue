<template>
  <div class="app-shell bg-surface-gray-2 text-ink-gray-9">
    <aside class="flex h-full w-64 shrink-0 flex-col border-r border-outline-gray-2 bg-surface-base">
      <div class="flex h-14 items-center gap-2 border-b border-outline-gray-2 px-4">
        <img :src="logoUrl" class="h-8 w-8 rounded-lg" alt="" />
        <div class="leading-tight">
          <div class="text-sm font-semibold">Altoplano IA Agents</div>
          <div class="text-[11px] text-ink-gray-5">ERPNext</div>
        </div>
      </div>
      <nav class="scroll-area flex-1 py-2">
        <RouterLink v-for="item in nav" :key="item.route" :to="item.route"
          class="flex items-center gap-2.5 px-4 py-2 text-sm"
          :class="$route.path === item.route || (item.route !== '/' && $route.path.startsWith(item.route)) ? 'bg-surface-blue-2 font-medium text-ink-blue-7' : 'text-ink-gray-7 hover:bg-surface-gray-2'">
          <span class="size-4" :class="'lucide-' + item.icon"></span>{{ item.label }}
        </RouterLink>
      </nav>
      <div class="border-t border-outline-gray-2 p-3 text-[11px] text-ink-gray-5">
        <span v-if="session.company" class="block truncate">{{ session.company }}</span>
        <span class="block">{{ session.fullName || session.user }}</span>
      </div>
    </aside>
    <main class="scroll-area min-w-0 flex-1">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import { useSession } from '../composables/useSession'

const logoUrl = '/assets/altoplano_agents/images/logo.svg'
const { state: session, load } = useSession()
onMounted(() => load())

const nav = [
  { label: 'Inicio', route: '/', icon: 'layout-grid' },
  { label: 'Cerebro', route: '/cerebro', icon: 'message-circle' },
  { label: 'Mis agentes', route: '/agents', icon: 'bot' },
  { label: 'Información', route: '/business', icon: 'book-open' },
  { label: 'Conversaciones', route: '/conversations', icon: 'messages-square' },
  { label: 'Conexiones', route: '/connections', icon: 'plug' },
  { label: 'Aprobaciones', route: '/approvals', icon: 'shield-check' },
  { label: 'Gastos', route: '/spending', icon: 'wallet' },
  { label: 'Actividad', route: '/activity', icon: 'history' },
]
</script>
