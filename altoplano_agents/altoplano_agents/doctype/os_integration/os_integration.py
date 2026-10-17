import frappe
from frappe.model.document import Document


class OSIntegration(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		category: DF.Literal["CRM", "Comms", "Docs", "Calendar", "Finance", "Automation", "CustomAPI"]
		depends: DF.SmallText | None
		external_connection_id: DF.Data | None
		health_notes: DF.SmallText | None
		integration_name: DF.Data
		last_sync_at: DF.Datetime | None
		owner_user: DF.Link | None
		provider: DF.Data | None
		scopes_declared: DF.SmallText | None
		status: DF.Literal["Connected", "Degraded", "Disconnected"]
	# end: auto-generated types
	pass
