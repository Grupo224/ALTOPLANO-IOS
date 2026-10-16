import frappe
from frappe.model.document import Document


class AIAConnection(Document):
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

