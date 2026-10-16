# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAIdentityBinding(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link
		connection: DF.Link
		contact: DF.Link | None
		customer: DF.Link | None
		external_subject_id: DF.Data
		status: DF.Literal["Pending", "Verified", "Revoked"]
		user: DF.Link | None
		verification_method: DF.Literal["PortalConsent", "AdminVerified"]
		verified_at: DF.Datetime | None
		verified_by: DF.Link | None
	# end: auto-generated types
	pass
