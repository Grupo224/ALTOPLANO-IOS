# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAEventInbox(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attempts: DF.Int
		company: DF.Link
		error_code: DF.Data | None
		event_key: DF.Data
		payload_digest: DF.Data
		payload_json: DF.Code
		processed_at: DF.Datetime | None
		provider_event_id: DF.Data | None
		received_at: DF.Datetime
		source_connection: DF.Link
		status: DF.Literal["Received", "Validated", "Queued", "Processing", "Processed", "Failed", "Quarantined"]
	# end: auto-generated types
	pass
