import frappe
from frappe.model.document import Document


class AIAEmailBinding(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allowed_attachment_types_json: DF.Code
		allowed_recipient_domains: DF.SmallText | None
		auth_owner: DF.Link | None
		auto_create_contacts: DF.Check
		company: DF.Link
		config_version: DF.Int
		connection: DF.Link
		email_account: DF.Link
		last_inbound_communication: DF.Link | None
		last_outgoing_queue: DF.Link | None
		mailbox_kind: DF.Literal["Personal; Shared; Service"]
		max_attachment_mb: DF.Int
		max_recipients_per_message: DF.Int
		native_reply_suppressed: DF.Check
		process_historical_mail: DF.Check
		processing_from: DF.Datetime | None
		receive_enabled: DF.Check
		reply_policy: DF.Literal["DraftOnly; HumanApproval; AutoWithinPolicy"]
		send_enabled: DF.Check
	# end: auto-generated types
	pass
