import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('./views/HomeView.vue') },
  { path: '/agents', name: 'Agents', component: () => import('./views/AgentsView.vue') },
  { path: '/agents/:id', name: 'AgentDetail', component: () => import('./views/AgentDetailView.vue'), props: true },
  { path: '/business', name: 'Business', component: () => import('./views/BusinessView.vue') },
  { path: '/connections', name: 'Connections', component: () => import('./views/ConnectionsView.vue') },
  { path: '/conversations', name: 'Conversations', component: () => import('./views/ConversationsView.vue') },
  { path: '/approvals', name: 'Approvals', component: () => import('./views/ApprovalsView.vue') },
  { path: '/spending', name: 'Spending', component: () => import('./views/SpendingView.vue') },
  { path: '/cerebro', name: 'Cerebro', component: () => import('./views/CerebroView.vue') },
  { path: '/activity', name: 'Activity', component: () => import('./views/ActivityView.vue') },
]

const router = createRouter({
  history: createWebHistory('/ai-agents'),
  routes,
})

export default router
