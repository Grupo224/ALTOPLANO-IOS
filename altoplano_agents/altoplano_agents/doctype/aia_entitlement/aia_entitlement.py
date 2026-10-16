# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAEntitlement(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link
		limits_json: DF.Code
		origin: DF.Literal["LocalAdmin", "PlatformSigned"]
		plan_code: DF.Data
		platform_account_id: DF.Data
		received_at: DF.Datetime
		signature: DF.TextEditor | None
		status: DF.Literal["Trial", "Active", "Grace", "Suspended", "Cancelled"]
		valid_from: DF.Datetime
		valid_until: DF.Datetime
	# end: auto-generated types
	pass
