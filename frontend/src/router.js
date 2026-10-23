import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'CommandCenter', component: () => import('./views/CommandCenter.vue') },
  { path: '/org', name: 'Org', component: () => import('./views/OrgView.vue') },
  { path: '/processes', name: 'Processes', component: () => import('./views/ProcessesView.vue') },
  { path: '/processes/:name', name: 'ProcessStudio', component: () => import('./views/ProcessStudio.vue'), props: true },
  { path: '/sop', name: 'SOP', component: () => import('./views/SopView.vue') },
  { path: '/work', name: 'Work', component: () => import('./views/WorkView.vue') },
  { path: '/approvals', name: 'Approvals', component: () => import('./views/ApprovalsView.vue') },
  { path: '/runs', name: 'Runs', component: () => import('./views/RunsView.vue') },
  { path: '/runs/:name', name: 'RunDetail', component: () => import('./views/RunDetailView.vue'), props: true },
  { path: '/agents', name: 'Agents', component: () => import('./views/AgentsView.vue') },
  { path: '/prompts', name: 'Prompts', component: () => import('./views/PromptsView.vue') },
  { path: '/roles', name: 'Roles', component: () => import('./views/RolesView.vue') },
  { path: '/kpis', name: 'KPIs', component: () => import('./views/KpisView.vue') },
  { path: '/integrations', name: 'Integrations', component: () => import('./views/IntegrationsView.vue') },
  { path: '/knowledge', name: 'Knowledge', component: () => import('./views/KnowledgeView.vue') },
  { path: '/analytics', name: 'Analytics', component: () => import('./views/AnalyticsView.vue') },
]

const router = createRouter({
  history: createWebHistory('/ios'),
  routes,
})

export default router
