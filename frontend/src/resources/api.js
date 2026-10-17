// Capa de datos: métodos semánticos v1 de Altoplano IA Agents.
import { call } from 'frappe-ui'

const NS = 'altoplano_agents.api.v1.'

export const api = {
  boot: () => call(NS + 'boot.boot'),
  dashboard: () => call(NS + 'dashboard.dashboard'),
  // negocio
  getProfile: () => call(NS + 'business.get_profile'),
  saveProfile: (fields) => call(NS + 'business.save_profile', fields),
  // catálogo
  templates: () => call(NS + 'catalog.templates'),
  skills: () => call(NS + 'catalog.skills'),
  tools: () => call(NS + 'catalog.tools'),
  // agentes
  listAgents: () => call(NS + 'agents.list_agents'),
  getAgent: (agent) => call(NS + 'agents.get_agent', { agent }),
  createAgent: (fields) => call(NS + 'agents.create_agent', fields),
  updateAgent: (fields) => call(NS + 'agents.update_agent', fields),
  createRevision: (agent) => call(NS + 'agents.create_revision', { agent }),
  // conexiones
  listConnections: () => call(NS + 'connections.list_connections'),
  createConnection: (fields) => call(NS + 'connections.create_connection', fields),
  // conversaciones
  listConversations: () => call(NS + 'conversations.list_conversations'),
  getMessages: (conversation) => call(NS + 'conversations.get_messages', { conversation }),
  handoff: (conversation, assigned_user) => call(NS + 'conversations.handoff', { conversation, assigned_user }),
  // aprobaciones
  listApprovals: () => call(NS + 'approvals.list_approvals'),
  decide: (approval, decision, reason) => call(NS + 'approvals.decide', { approval, decision, reason }),
  // gastos
  usageSummary: () => call(NS + 'usage.summary'),
  usageEvents: () => call(NS + 'usage.events'),
  // actividad
  activity: () => call(NS + 'erp.activity'),
  // cerebro
  cerebroStart: () => call(NS + 'cerebro.start'),
  cerebroAsk: (conversation, message) => call(NS + 'cerebro.ask', { conversation, message }),
  // agenda
  calendars: () => call(NS + 'calendar.list_calendars'),
  appointments: () => call(NS + 'calendar.list_appointments'),
  createCalendar: (fields) => call(NS + 'calendar.create_calendar', fields),
}

export function humanError(err) {
  if (Array.isArray(err?.messages) && err.messages.length) return err.messages.join(' · ')
  if (typeof err?.message === 'string' && err.message.trim()) return err.message
  return 'Error desconocido'
}
