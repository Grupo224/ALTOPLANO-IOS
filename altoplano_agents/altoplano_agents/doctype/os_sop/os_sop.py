import frappe
from frappe.model.document import Document


class OSSOP(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.os_sop_step.os_sop_step import OSSOPStep
		from frappe.types import DF

		approved_by: DF.Link | None
		approved_on: DF.Datetime | None
		controls: DF.SmallText | None
		definition_of_done: DF.SmallText | None
		department: DF.Link | None
		estimated_time_minutes: DF.Int
		evidence_required: DF.SmallText | None
		exceptions: DF.SmallText | None
		expected_result: DF.SmallText | None
		file: DF.Attach | None
		last_reviewed_on: DF.Date | None
		metrics: DF.SmallText | None
		next_review_on: DF.Date | None
		objective: DF.SmallText | None
		owner_user: DF.Link | None
		procedure_legacy: DF.TextEditor | None
		process_ref: DF.Link | None
		responsible_node: DF.Link | None
		responsible_users: DF.SmallText | None
		risk_level: DF.Literal["Low", "Medium", "High", "Critical"]
		roles: DF.SmallText | None
		scope: DF.SmallText | None
		sop_code: DF.Data | None
		sop_title: DF.Data
		status: DF.Literal["Draft", "In Review", "Approved", "Published", "Obsolete"]
		steps: DF.Table[OSSOPStep]
		tools: DF.SmallText | None
		trigger: DF.Data | None
		valid_from: DF.Date | None
		valid_until: DF.Date | None
		version_label: DF.Data | None
	# end: auto-generated types
	pass
