import frappe
from frappe.model.document import Document


class AIAWhatsAppAccount(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		access_token_ref: DF.Data | None
		business_portfolio_id: DF.Data | None
		coexistence_status: DF.Literal["NotRequested", "Unverified", "Supported", "Unsupported"]
		company: DF.Link
		config_version: DF.Int
		connection: DF.Link
		data_access_expires_at: DF.Datetime | None
		default_template: DF.Link | None
		granted_permissions_json: DF.Code | None
		last_delivery_at: DF.Datetime | None
		last_inbound_webhook_at: DF.Datetime | None
		last_status_webhook_at: DF.Datetime | None
		messaging_policy_version: DF.Data
		meta_app: DF.Link
		onboarding_method: DF.Literal["Manual", "EmbeddedSignup"]
		phone_number_e164: DF.Data | None
		phone_number_id: DF.Data
		platform_type: DF.Data | None
		quality_rating: DF.Data | None
		registration_status: DF.Literal["Unknown", "Pending", "Registered", "Failed"]
		service_window_hours: DF.Int
		token_expires_at: DF.Datetime | None
		token_kind: DF.Literal["Unknown", "User", "SystemUser", "BusinessIntegration"]
		verified_name: DF.Data | None
		waba_id: DF.Data
		waba_subscribed: DF.Check
	# end: auto-generated types
	pass
