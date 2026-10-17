import frappe
from frappe.model.document import Document


class OSStepRun(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		actor_agent: DF.Link | None
		actor_user: DF.Link | None
		approval_required: DF.Check
		attempt_no: DF.Int
		completed_at: DF.Datetime | None
		error_code: DF.Data | None
		error_message: DF.SmallText | None
		evidence_required: DF.Check
		execution_type_snapshot: DF.Data | None
		input_json: DF.Code | None
		output_json: DF.Code | None
		queued_at: DF.Datetime | None
		run: DF.Link
		started_at: DF.Datetime | None
		status: DF.Literal["Queued", "Running", "Waiting", "Approved", "Completed", "Failed", "Skipped", "Cancelled"]
		step_key: DF.Data
		step_title_snapshot: DF.Data | None
	# end: auto-generated types
	pass
