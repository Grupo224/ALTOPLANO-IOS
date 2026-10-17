import frappe
from frappe.model.document import Document


class OSEvidence(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		evidence_type: DF.Literal["File", "Link", "Record", "Note"]
		external_reference: DF.Data | None
		file: DF.Attach | None
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
		run: DF.Link
		step_run: DF.Link | None
		summary: DF.SmallText | None
		verification_status: DF.Literal["Pending", "Verified", "Rejected"]
		verified_at: DF.Datetime | None
		verified_by: DF.Link | None
	# end: auto-generated types
	pass
