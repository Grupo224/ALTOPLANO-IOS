import frappe
from frappe.model.document import Document


class OSStepRun(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_snapshot_json: DF.Code | None
		action_status: DF.Literal["Not Required", "Ready", "Executed", "Failed", "Skipped"]
		actor_agent: DF.Link | None
		actor_role: DF.Link | None
		actor_user: DF.Link | None
		approval_required: DF.Check
		approval_role_snapshot: DF.Link | None
		attempt_no: DF.Int
		completed_at: DF.Datetime | None
		error_code: DF.Data | None
		error_message: DF.SmallText | None
		evidence_required: DF.Check
		execution_type_snapshot: DF.Data | None
		input_json: DF.Code | None
		instructions_snapshot: DF.LongText | None
		last_action_at: DF.Datetime | None
		output_json: DF.Code | None
		policy_snapshot: DF.Data | None
		process_version_snapshot: DF.Data | None
		prompt_snapshot: DF.Data | None
		queued_at: DF.Datetime | None
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		run: DF.Link
		sop_snapshot: DF.Data | None
		source_doctype: DF.Link | None
		source_name: DF.DynamicLink | None
		started_at: DF.Datetime | None
		status: DF.Literal["Blocked", "Queued", "Running", "Waiting", "Approved", "Completed", "Failed", "Skipped", "Cancelled"]
		step_key: DF.Data
		step_title_snapshot: DF.Data | None
		step_type_snapshot: DF.Data | None
	# end: auto-generated types
	pass
