<template>
  <AppLayout>
    <div class="os-body">
      <div class="os-eyebrow">Sistema operativo vivo</div>
      <h1 class="os-h1">Command Center</h1>
      <p class="mb-6 text-sm" style="color: var(--os-steel)">Dibuja cómo funciona tu empresa, decide qué hace una persona y qué la IA, ejecuta y guarda evidencia desde un solo mapa.</p>

      <div class="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <div class="os-card"><span>Procesos</span><strong>{{ counts.process }}</strong></div>
        <div class="os-card"><span>Ejecuciones</span><strong>{{ counts.run }}</strong></div>
        <div class="os-card"><span>Aprobaciones pendientes</span><strong>{{ counts.approval }}</strong></div>
        <div class="os-card"><span>Agentes IA</span><strong>{{ counts.agent }}</strong></div>
      </div>

      <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <RouterLink v-for="c in cards" :key="c.route" :to="c.route" class="os-card transition hover:border-[#ff9422]">
          <div class="mb-1 text-xl" style="color: var(--os-orange)">{{ c.icon }}</div>
          <div class="font-medium" style="color:#fff">{{ c.title }}</div>
          <div class="text-xs" style="color: var(--os-steel)">{{ c.desc }}</div>
        </RouterLink>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { call } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'

const counts = reactive({ process: 0, run: 0, approval: 0, agent: 0 })

const cards = [
  { icon: '⊞', title: 'Organigrama', desc: 'Quién es quién y quién responde a quién.', route: '/org' },
  { icon: '⑂', title: 'Procesos', desc: 'Dibuja cómo se hace el trabajo.', route: '/processes' },
  { icon: '▤', title: 'SOP', desc: 'Instrucciones claras paso a paso.', route: '/sop' },
  { icon: '✓', title: 'Mi Trabajo', desc: 'Lo que te toca hacer hoy.', route: '/work' },
  { icon: '☑', title: 'Aprobaciones', desc: 'Decisiones que esperan tu visto bueno.', route: '/approvals' },
  { icon: '◇', title: 'Agentes y Prompts', desc: 'La IA que ejecuta tu proceso.', route: '/agents' },
]

onMounted(async () => {
  try {
    const [p, r, a, ag] = await Promise.all([
      call('frappe.client.get_count', { doctype: 'OS Process' }),
      call('frappe.client.get_count', { doctype: 'OS Run' }),
      call('frappe.client.get_count', { doctype: 'OS Approval', filters: { status: 'Pending' } }),
      call('frappe.client.get_count', { doctype: 'OS Agent' }),
    ])
    counts.process = p || 0; counts.run = r || 0; counts.approval = a || 0; counts.agent = ag || 0
  } catch (e) { /* noop */ }
})
</script>
