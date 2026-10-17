import frappe
from frappe.model.document import Document


class AIAAppointment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link | None
		booking_key: DF.Data
		calendar: DF.Link
		cancel_reason: DF.SmallText | None
		company: DF.Link
		contact: DF.Link | None
		conversation: DF.Link | None
		customer: DF.Link | None
		event: DF.Link
		hold_expires_at: DF.Datetime | None
		last_notification: DF.Link | None
		notification_policy: DF.Literal["None; HumanApproval; ApprovedTemplates"]
		revision: DF.Int
		source: DF.Literal["Portal; WhatsApp; Email; InternalAgent"]
		status: DF.Literal["Held; Confirmed; Cancelled; Completed; NoShow"]
		timezone: DF.Data
	# end: auto-generated types
	pass
