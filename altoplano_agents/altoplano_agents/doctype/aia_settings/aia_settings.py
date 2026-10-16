import frappe
from frappe.model.document import Document


class AIASettings(Document):
    def validate(self):
        if not self.get("enabled"):
            self.enabled = 0
        if self.get("environment") == "Production" and self.get("demo_mode"):
            frappe.throw("No se permiten datos de demostración en producción.")
        if not self.get("schema_version"):
            self.schema_version = "1"

