# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAConversation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link | None
		assigned_user: DF.Link | None
		audience: DF.Literal["Customer", "Internal"]
		binding: DF.Link | None
		company: DF.Link
		external_conversation_id: DF.Data | None
		handler_state: DF.Literal["Bot", "Human", "Closed"]
		identity_binding: DF.Link | None
		last_activity: DF.Datetime | None
		memory_scope: DF.Data
		session_key: DF.Data
		summary: DF.SmallText | None
	# end: auto-generated types
	pass
