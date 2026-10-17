import frappe
from frappe.model.document import Document


class AIAMCPServer(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_mcp_header.aia_mcp_header import AIAMCPHeader
		from frappe.types import DF

		allow_elicitation: DF.Check
		allow_prompts: DF.Check
		allow_resources: DF.Check
		allow_sampling: DF.Check
		auth_header_name: DF.Data | None
		auth_mode: DF.Literal["None; Bearer; APIKeyHeader; OAuth"]
		capabilities_json: DF.Code | None
		catalog_digest: DF.Data | None
		client_sdk_name: DF.Data
		client_sdk_version: DF.Data
		client_supported_versions_json: DF.Code
		company: DF.Link
		config_version: DF.Int
		connect_timeout_seconds: DF.Int
		connection: DF.Link
		discovery_complete: DF.Check
		headers: DF.Table[AIAMCPHeader]
		last_discovered_at: DF.Datetime | None
		managed_stdio_profile: DF.Data | None
		max_response_bytes: DF.Int
		max_tools: DF.Int
		oauth_grant: DF.Link | None
		protocol_mode: DF.Literal["Unknown; RequestMetadata2026; SessionLegacy"]
		protocol_version: DF.Data | None
		request_timeout_seconds: DF.Int
		resource_uri: DF.Data | None
		server_name: DF.Data | None
		server_supported_versions_json: DF.Code | None
		server_url: DF.Data | None
		server_version: DF.Data | None
		transport: DF.Literal["StreamableHTTP; LegacySSE; ManagedStdio"]
	# end: auto-generated types
	pass
