import frappe
from frappe.model.document import Document


class AIAToolCall(Document):
    def validate(self):
        if self.is_new() and not self.get("operation_key"):
            frappe.throw("operation_key es obligatoria y única.")
        if self.is_new() and not self.get("status"):
            self.status = "Queued"

