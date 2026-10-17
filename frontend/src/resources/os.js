import { call } from 'frappe-ui'

const NS = 'altoplano_agents.api.v1.os_api.'

export const osApi = {
  getDoctypeMeta: (doctype) => call(NS + 'get_doctype_meta', { doctype }),
  getProcess: (name) => call(NS + 'get_process', { name }),
  saveProcessCanvas: (name, steps, edges) => call(NS + 'save_process_canvas', { name, steps, edges }),
  addProcessStep: (name, stepTitle, stepType) => call(NS + 'add_process_step', { name, step_title: stepTitle, step_type: stepType }),
  saveProcessStep: (name, stepKey, values) => call(NS + 'save_process_step', { name, step_key: stepKey, values }),
  deleteProcessStep: (name, stepKey) => call(NS + 'delete_process_step', { name, step_key: stepKey }),
  getOrg: () => call(NS + 'get_org'),
  addOrgNode: (title, nodeType, x, y) => call(NS + 'add_org_node', { title, node_type: nodeType, x, y }),
  saveOrgNode: (name, x, y) => call(NS + 'save_org_node', { name, x, y }),
  createProcess: (fields) => call(NS + 'create_process', fields),
  updateDoc: (doctype, name, values) => call(NS + 'update_doc', { doctype, name, values }),
}

export function humanError(err) {
  if (Array.isArray(err?.messages) && err.messages.length) return err.messages.join(' · ')
  if (typeof err?.message === 'string' && err.message.trim()) return err.message
  return 'Error desconocido'
}

export function resetForm(metaFields, form, defaults = {}) {
  for (const k in form) delete form[k]
  for (const f of metaFields) form[f.fieldname] = f.fieldtype === 'Check' ? false : ''
  Object.assign(form, defaults || {})
}

export function fillFromDoc(metaFields, form, doc) {
  for (const f of metaFields) {
    const v = doc ? doc[f.fieldname] : undefined
    form[f.fieldname] = f.fieldtype === 'Check' ? !!v : (v ?? '')
  }
}

export function coerceValues(metaFields, form) {
  const out = {}
  for (const f of metaFields) {
    const v = form[f.fieldname]
    if (f.fieldtype === 'Check') out[f.fieldname] = v ? 1 : 0
    else if (f.fieldtype === 'Int') out[f.fieldname] = parseInt(v, 10) || 0
    else if (f.fieldtype === 'Float' || f.fieldtype === 'Currency') out[f.fieldname] = parseFloat(v) || 0
    else out[f.fieldname] = v
  }
  return out
}
