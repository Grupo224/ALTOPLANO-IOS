import frappe
from frappe.model.document import Document


class AIAChatwootAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		account_id: DF.Data
		agent_bot_id: DF.Data | None
		api_token_ref: DF.Data | None
		auth_header_mode: DF.Literal["ApiAccessToken", "Bearer"]
		base_url: DF.Data
		chatwoot_version: DF.Data | None
		company: DF.Link
		config_version: DF.Int
		connection: DF.Link
		handoff_team_id: DF.Data | None
		last_event_at: DF.Datetime | None
		webhook_auth_mode: DF.Literal["ProviderSignature", "PrivateRelay"]
		webhook_route_key: DF.Data
		webhook_secret_ref: DF.Data | None
		webhook_url: DF.Data
	# end: auto-generated types
	pass
