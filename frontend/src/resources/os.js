import { call } from 'frappe-ui'

const NS = 'altoplano_agents.api.v1.os_api.'

export const osApi = {
  getProcess: (name) => call(NS + 'get_process', { name }),
  saveProcessCanvas: (name, steps, edges) => call(NS + 'save_process_canvas', { name, steps, edges }),
  addProcessStep: (name, stepTitle, stepType) => call(NS + 'add_process_step', { name, step_title: stepTitle, step_type: stepType }),
  getOrg: () => call(NS + 'get_org'),
  addOrgNode: (title, nodeType, x, y) => call(NS + 'add_org_node', { title, node_type: nodeType, x, y }),
  saveOrgNode: (name, x, y) => call(NS + 'save_org_node', { name, x, y }),
}

export function humanError(err) {
  if (Array.isArray(err?.messages) && err.messages.length) return err.messages.join(' · ')
  if (typeof err?.message === 'string' && err.message.trim()) return err.message
  return 'Error desconocido'
}
