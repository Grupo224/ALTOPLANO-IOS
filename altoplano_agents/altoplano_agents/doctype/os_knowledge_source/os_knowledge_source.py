import frappe
from frappe.model.document import Document


class OSKnowledgeSource(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		content: DF.LongText | None
		department: DF.Link | None
		file: DF.Attach | None
		owner_user: DF.Link | None
		process_ref: DF.Link | None
		sensitivity: DF.Literal["Public", "Internal", "Confidential", "Restricted"]
		source_title: DF.Data
		source_type: DF.Literal["Document", "Email", "CRM", "Meeting", "ERP", "Policy", "Website", "Other"]
		status: DF.Literal["Active", "Under Review", "Outdated"]
		summary: DF.SmallText | None
		tags: DF.SmallText | None
		url_or_reference: DF.Data | None
		valid_from: DF.Date | None
		valid_until: DF.Date | None
	# end: auto-generated types
	pass
