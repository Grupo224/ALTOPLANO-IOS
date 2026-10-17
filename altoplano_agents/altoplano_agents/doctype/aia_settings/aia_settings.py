import frappe
from frappe.model.document import Document


class AIASettings(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        base_currency: DF.Link
        default_company: DF.Link
        demo_mode: DF.Check
        enabled: DF.Check
        environment: DF.Literal["Development", "Staging", "Production"]
        operating_mode: DF.Literal["SelfManaged", "ManagedClient", "ProviderControl"]
        platform_account_id: DF.Data | None
        retention_days: DF.Int
        runtime_connection: DF.Link | None
        schema_version: DF.Data
        support_contact: DF.Data | None
    # end: auto-generated types
    def validate(self):
        if not self.get("enabled"):
            self.enabled = 0
        if self.get("environment") == "Production" and self.get("demo_mode"):
            frappe.throw("No se permiten datos de demostración en producción.")
        if not self.get("schema_version"):
            self.schema_version = "1"

