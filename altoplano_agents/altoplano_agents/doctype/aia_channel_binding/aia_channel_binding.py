# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAChannelBinding(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link
		audience: DF.Literal["Customer", "Internal"]
		channel: DF.Literal["Portal", "Telegram", "WhatsApp"]
		company: DF.Link
		connection: DF.Link
		enabled: DF.Check
		external_account_id: DF.Data | None
		inbox_id: DF.Data | None
		route_key: DF.Data
		session_scope: DF.Data
	# end: auto-generated types
	pass
