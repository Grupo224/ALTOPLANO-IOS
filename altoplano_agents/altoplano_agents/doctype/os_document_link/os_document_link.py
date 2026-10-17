# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OSDocumentLink(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_key: DF.Data | None
		document_status_snapshot: DF.Data | None
		is_primary: DF.Check
		label: DF.Data | None
		link_role: DF.Literal["Source", "Target", "Result", "Related"]
		process_ref: DF.Link | None
		reference_doctype: DF.Link
		reference_name: DF.DynamicLink
		run: DF.Link
		step_key: DF.Data | None
		step_run: DF.Link | None
	# end: auto-generated types
	pass
