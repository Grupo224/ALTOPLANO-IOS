import frappe
from frappe.model.document import Document


class AIAConnection(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        adapter_key: DF.Data
        adapter_schema_version: DF.Data
        auth_type: DF.Literal["None", "APIKey", "OAuth", "ServiceAccount", "SecretRef"]
        authorization_scope: DF.Literal["OwnerUser", "CompanyService"]
        base_url: DF.Data | None
        capabilities_json: DF.Code | None
        company: DF.Link
        config_fingerprint: DF.Data
        config_json: DF.Code | None
        config_version: DF.Int
        connection_type: DF.Literal["LLM", "ERP", "MCP", "Telegram", "WhatsApp", "Chatwoot", "Email", "Runtime"]
        credential_ref: DF.Data | None
        credential_version: DF.Int
        display_name: DF.Data
        enabled: DF.Check
        environment: DF.Literal["Sandbox", "Production"]
        error_code: DF.Data | None
        expires_at: DF.Datetime | None
        external_account_id: DF.Data | None
        granted_scopes: DF.Code | None
        health_status: DF.Literal["Unknown", "Healthy", "Degraded", "Down"]
        last_check: DF.Link | None
        last_checked: DF.Datetime | None
        last_success_at: DF.Datetime | None
        next_check_at: DF.Datetime | None
        owner_user: DF.Link
        payer_mode: DF.Literal["Included", "BYOK", "Managed"]
        provider: DF.Data
        reconnect_required: DF.Check
        required_capabilities_json: DF.Code
        status: DF.Literal["PendingAuthorization", "Authorized", "Checking", "Ready", "Expired", "Degraded", "Revoked", "Failed"]
    # end: auto-generated types
    def validate(self):
        if self.is_new() and not self.get("company"):
            from altoplano_agents.services.context import resolve_company
            self.company = resolve_company(None)
        if self.is_new() and not self.get("owner_user"):
            self.owner_user = frappe.session.user
        if self.is_new() and not self.get("status"):
            self.status = "PendingAuthorization"

    def before_save(self):
        # Nunca exponer credenciales: credential_ref es opaca; nada de secretos aquí.
        if self.get("credential_ref") and len(str(self.credential_ref)) > 200:
            frappe.throw("credential_ref debe ser una referencia opaca corta.")

