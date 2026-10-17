# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OSProcessAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_key: DF.Data
		action_label: DF.Data
		action_type: DF.Literal["OPEN_DOCUMENT", "CREATE_DOCUMENT", "UPDATE_DOCUMENT", "CREATE_FROM_SOURCE", "SUBMIT_DOCUMENT", "LINK_DOCUMENT"]
		completion_rule: DF.Literal["Manual", "Document Linked", "Document Exists", "Document Submitted"]
		defaults_json: DF.Code | None
		description: DF.SmallText | None
		field_mapping_json: DF.Code | None
		is_required: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		required_role: DF.Link | None
		sort_order: DF.Int
		source_doctype: DF.Link | None
		step_key: DF.Data
		submit_after_create: DF.Check
		system: DF.Literal["ERPNext", "External"]
		target_doctype: DF.Link | None
	# end: auto-generated types
	pass
