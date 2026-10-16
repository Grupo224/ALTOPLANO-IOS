import frappe
from frappe.model.document import Document


class AIAToolDefinition(Document):
    def validate(self):
        if self.get("adapter_key") and not frappe.db.exists("AIA Tool Definition", self.adapter_key):
            # adapter_key apunta al registro de adaptador del servidor; validado en catálogo.
            pass

