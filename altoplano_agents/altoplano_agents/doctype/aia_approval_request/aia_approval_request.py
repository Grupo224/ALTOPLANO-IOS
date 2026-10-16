import frappe
from frappe.model.document import Document


class AIAApprovalRequest(Document):
    def validate(self):
        if self.is_new() and not self.get("expires_at"):
            from frappe.utils import add_to_date, now_datetime
            self.expires_at = add_to_date(now_datetime(), hours=24)

