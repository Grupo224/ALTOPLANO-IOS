# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAERPLink(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Literal["Created", "Updated", "Read"]
		company: DF.Link
		created_at: DF.Datetime
		erp_doctype: DF.Link
		erp_document: DF.DynamicLink
		link_key: DF.Data
		operation_key: DF.Data
		run: DF.Link
		tool_call: DF.Link
	# end: auto-generated types
	pass
