import frappe
from frappe.model.document import Document


class AIAMessagingConsent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		channel: DF.Literal["WhatsApp", "Email"]
		company: DF.Link
		connection: DF.Link
		consent_key: DF.Data
		contact: DF.Link | None
		evidence_hash: DF.Data | None
		evidence_method: DF.Literal["Form", "InboundRequest", "WrittenConsent", "ProviderImport", "OptOut"]
		evidence_reference: DF.Data | None
		expires_at: DF.Datetime | None
		external_subject_id: DF.Data
		policy_version: DF.Data
		purpose: DF.Literal["Service", "Appointment", "Marketing"]
		recorded_at: DF.Datetime
		status: DF.Literal["Unknown", "OptedIn", "OptedOut", "Expired"]
	# end: auto-generated types
	pass
