import frappe
from frappe.model.document import Document


class OSProcess(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.os_process_edge.os_process_edge import OSProcessEdge
		from altoplano_agents.altoplano_agents.doctype.os_process_goal.os_process_goal import OSProcessGoal
		from altoplano_agents.altoplano_agents.doctype.os_process_step.os_process_step import OSProcessStep
		from frappe.types import DF

		canvas_json: DF.LongText | None
		changelog: DF.LongText | None
		clients: DF.Data | None
		company: DF.Link
		controls: DF.SmallText | None
		definition_of_done: DF.SmallText | None
		department: DF.Link | None
		docs: DF.Attach | None
		edges: DF.Table[OSProcessEdge]
		evidence_required: DF.SmallText | None
		exceptions: DF.SmallText | None
		frequency: DF.Literal["On Demand", "Daily", "Weekly", "Biweekly", "Monthly"]
		gates: DF.SmallText | None
		goals: DF.Table[OSProcessGoal]
		inputs: DF.SmallText | None
		kaizen: DF.LongText | None
		kpis: DF.SmallText | None
		max_autonomy: DF.Literal["L0", "L1", "L2", "L3", "L4"]
		next_review_on: DF.Date | None
		org_area: DF.Link | None
		outcome: DF.SmallText | None
		outputs: DF.SmallText | None
		owner_user: DF.Link
		policy: DF.Link | None
		priority: DF.Literal["Low", "Medium", "High", "Critical"]
		process_code: DF.Data
		process_title: DF.Data
		published_on: DF.Datetime | None
		purpose: DF.SmallText
		raci_consulted: DF.SmallText | None
		raci_informed: DF.SmallText | None
		raci_responsible: DF.Link | None
		responsible_node: DF.Link | None
		risk_level: DF.Literal["Low", "Medium", "High", "Critical"]
		rules: DF.SmallText | None
		scope: DF.SmallText | None
		sla_minutes: DF.Int
		sop: DF.Link | None
		status: DF.Literal["Draft", "Pilot", "Active", "Degraded", "Retired"]
		steps: DF.Table[OSProcessStep]
		suppliers: DF.SmallText | None
		trigger_reference: DF.Data | None
		trigger_type: DF.Literal["Manual", "ERP Event", "Webhook", "Schedule", "External"]
		version_label: DF.Data
	# end: auto-generated types
	pass
