# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAToolGrant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		access_level: DF.Literal["Read", "CreateDraft", "ExecuteScoped"]
		max_calls_per_run: DF.Int
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		requires_approval: DF.Check
		scope_json: DF.Code
		tool: DF.Link
	# end: auto-generated types
	pass
