# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAAuditEvent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		actor: DF.Link | None
		after_hash: DF.Data | None
		before_hash: DF.Data | None
		company: DF.Link
		created_at: DF.Datetime
		event_type: DF.Data
		object_doctype: DF.Link
		object_name: DF.DynamicLink
		summary: DF.SmallText
		trace_id: DF.Data
	# end: auto-generated types
	pass
