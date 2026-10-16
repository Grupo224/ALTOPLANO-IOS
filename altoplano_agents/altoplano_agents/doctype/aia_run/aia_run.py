import frappe
from frappe.model.document import Document


class AIARun(Document):
    def validate(self):
        if self.is_new() and not self.get("status"):
            self.status = "Queued"
        if self.is_new() and not self.get("trace_id"):
            self.trace_id = frappe.generate_hash(length=24)

