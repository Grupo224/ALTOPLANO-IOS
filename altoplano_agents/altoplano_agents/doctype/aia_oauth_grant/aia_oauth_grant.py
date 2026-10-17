import frappe
from frappe.model.document import Document


class AIAOAuthGrant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		authorization_endpoint: DF.Data
		authorized_at: DF.Datetime | None
		client_id: DF.Data
		client_secret_ref: DF.Data | None
		company: DF.Link
		connection: DF.Link
		expires_at: DF.Datetime | None
		granted_scopes_json: DF.Code | None
		issuer: DF.Data
		last_refreshed_at: DF.Datetime | None
		pkce_method: DF.Literal["S256"]
		principal_kind: DF.Literal["OwnerUser; CompanyService"]
		protected_resource_metadata_url: DF.Data | None
		redirect_uri: DF.Data
		refresh_available: DF.Check
		registration_method: DF.Literal["PreRegistered; ClientIDMetadata; DynamicRegistration"]
		requested_scopes_json: DF.Code
		resource_uri: DF.Data
		revocation_endpoint: DF.Data | None
		status: DF.Literal["Pending; Active; Expired; Revoked; Failed"]
		subject_user: DF.Link | None
		token_bundle_ref: DF.Data | None
		token_endpoint: DF.Data
		token_version: DF.Int
	# end: auto-generated types
	pass
