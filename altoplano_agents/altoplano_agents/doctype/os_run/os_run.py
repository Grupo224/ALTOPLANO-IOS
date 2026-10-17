import frappe
from frappe.model.document import Document


class OSRun(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link | None
		completed_at: DF.Datetime | None
		context_json: DF.Code | None
		correlation_id: DF.Data | None
		current_step_key: DF.Data | None
		initiated_by: DF.Link | None
		process_ref: DF.Link
		process_version: DF.Data | None
		run_code: DF.Data | None
		run_mode: DF.Literal["Test", "Live"]
		started_at: DF.Datetime | None
		status: DF.Literal["Queued", "Running", "Waiting", "Approved", "Completed", "Failed", "Skipped", "Cancelled"]
		summary: DF.SmallText | None
		trigger_ref_doctype: DF.Link | None
		trigger_ref_name: DF.DynamicLink | None
		trigger_type: DF.Literal["Manual", "ERP Event", "Webhook", "Schedule", "External"]
	# end: auto-generated types
	pass
