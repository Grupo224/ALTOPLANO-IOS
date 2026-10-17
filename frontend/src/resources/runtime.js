import { call } from 'frappe-ui'

// Runtime LivingOrg (bridge portado): motor de runs + acciones ERPNext + aprobaciones.
const BRIDGE = 'altoplano_agents.bridge.'

export const bridgeApi = {
  capabilities: () => call(BRIDGE + 'status.capabilities'),
  startRun: (processName, mode = 'Test', sourceDoctype = null, sourceName = null) =>
    call(BRIDGE + 'api.start_run', { process_name: processName, mode, source_doctype: sourceDoctype, source_name: sourceName }),
  startStep: (stepRunName) => call(BRIDGE + 'api.start_step', { step_run_name: stepRunName }),
  completeStep: (stepRunName, comment = '', outcome = null) =>
    call(BRIDGE + 'api.complete_step', { step_run_name: stepRunName, comment, outcome }),
  executeAction: (stepRunName, actionKey, opts = {}) =>
    call(BRIDGE + 'api.execute_action', { step_run_name: stepRunName, action_key: actionKey, ...opts }),
  getStepActions: (stepRunName) => call(BRIDGE + 'api.get_step_actions', { step_run_name: stepRunName }),
  decideApproval: (approvalName, decision, comment = '') =>
    call(BRIDGE + 'approvals.decide', { approval_name: approvalName, decision, comment }),
}
