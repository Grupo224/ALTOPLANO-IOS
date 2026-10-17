import frappe
from frappe.model.document import Document


class AIAWhatsAppTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		category: DF.Data | None
		company: DF.Link
		components_json: DF.Code
		content_hash: DF.Data
		enabled: DF.Check
		language_code: DF.Data
		last_synced_at: DF.Datetime
		provider_status: DF.Data
		template_id: DF.Data
		template_name: DF.Data
		whatsapp_account: DF.Link
	# end: auto-generated types
	pass
