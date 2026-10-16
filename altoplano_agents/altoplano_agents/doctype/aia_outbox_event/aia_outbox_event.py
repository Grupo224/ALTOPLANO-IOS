# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAOutboxEvent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		aggregate_doctype: DF.Link
		aggregate_name: DF.DynamicLink
		attempt_count: DF.Int
		company: DF.Link
		destination: DF.Literal["Runtime", "Channel", "ERPWorker", "UsageFeed"]
		event_key: DF.Data
		fencing_token: DF.Int
		lease_owner: DF.Data | None
		lease_until: DF.Datetime | None
		next_attempt: DF.Datetime | None
		payload_json: DF.Code
		remote_request_id: DF.Data | None
		revision_hash: DF.Data | None
		state: DF.Literal["Queued", "Sending", "Sent", "Failed", "Unknown"]
	# end: auto-generated types
	pass
