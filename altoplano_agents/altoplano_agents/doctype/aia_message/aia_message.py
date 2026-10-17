# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAMessage(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		actor: DF.Literal["User", "Agent", "Human", "System"]
		body: DF.TextEditor | None
		company: DF.Link
		consent: DF.Link | None
		conversation: DF.Link
		created_at: DF.Datetime
		delivery_state: DF.Literal["Queued", "Sent", "Delivered", "Read", "Failed", "Unknown"]
		direction: DF.Literal["Inbound", "Outbound", "Internal"]
		event_key: DF.Data
		external_message_id: DF.Data | None
		native_communication: DF.Link | None
		whatsapp_template: DF.Link | None
	# end: auto-generated types
	pass
