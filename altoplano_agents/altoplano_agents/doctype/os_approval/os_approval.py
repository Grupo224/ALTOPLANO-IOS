import frappe
from frappe.model.document import Document


class OSApproval(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		context_snapshot: DF.Code | None
		decided_at: DF.Datetime | None
		decided_by: DF.Link | None
		decision_comment: DF.SmallText | None
		due_by: DF.Datetime | None
		process_ref: DF.Link | None
		requested_at: DF.Datetime | None
		requested_role: DF.Link | None
		requested_to: DF.Link | None
		risk_level: DF.Literal["Low", "Medium", "High", "Critical"]
		run: DF.Link
		status: DF.Literal["Pending", "Approved", "Rejected"]
		step_run: DF.Link | None
	# end: auto-generated types
	pass
