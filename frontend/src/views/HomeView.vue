<template>
  <AppLayout>
    <div class="p-6">
      <h1 class="mb-1 text-xl font-semibold">Altoplano IA Agents</h1>
      <p class="mb-5 text-sm text-ink-gray-5">Administra agentes de IA integrados a los datos y permisos de tu ERP.</p>

      <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <RouterLink v-for="c in cards" :key="c.route" :to="c.route"
          class="rounded-xl border border-outline-gray-2 bg-surface-base p-4 transition hover:shadow-md">
          <div class="mb-1 text-xl">{{ c.icon }}</div>
          <div class="text-sm font-medium">{{ c.title }}</div>
          <div class="text-[12px] text-ink-gray-5">{{ c.desc }}</div>
        </RouterLink>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const cards = [
  { icon: '🧠', title: 'Cerebro', desc: 'Consulta el ERP y ejecuta acciones autorizadas.', route: '/cerebro' },
  { icon: '🤖', title: 'Mis agentes', desc: 'Crea, prueba y activa agentes para tu negocio.', route: '/agents' },
  { icon: '📖', title: 'Información', desc: 'Define qué deben saber tus agentes de tu negocio.', route: '/business' },
  { icon: '💬', title: 'Conversaciones', desc: 'Revisa y transfiere conversaciones de clientes.', route: '/conversations' },
  { icon: '🔌', title: 'Conexiones', desc: 'Canales e integraciones autorizadas.', route: '/connections' },
  { icon: '🛡️', title: 'Aprobaciones', desc: 'Confirma las acciones propuestas por Cerebro.', route: '/approvals' },
]
</script>
