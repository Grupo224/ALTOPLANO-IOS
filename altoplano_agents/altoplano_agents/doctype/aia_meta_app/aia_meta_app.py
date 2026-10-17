import frappe
from frappe.model.document import Document


class AIAMetaApp(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allowed_origin: DF.Data
		app_mode: DF.Literal["Unknown; Development; Live"]
		app_secret_ref: DF.Data | None
		company: DF.Link
		config_version: DF.Int
		display_name: DF.Data
		embedded_signup_config_id: DF.Data | None
		embedded_signup_enabled: DF.Check
		enabled: DF.Check
		graph_api_version: DF.Data
		meta_app_id: DF.Data
		oauth_redirect_uri: DF.Data | None
		signup_contract_version: DF.Data | None
		verify_token_ref: DF.Data
		webhook_callback_url: DF.Data
		webhook_fields_json: DF.Code
		webhook_route_key: DF.Data
		webhook_verified_at: DF.Datetime | None
	# end: auto-generated types
	pass
