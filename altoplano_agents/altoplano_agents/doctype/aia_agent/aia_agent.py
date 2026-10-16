import frappe
from frappe.model.document import Document


class AIAAgent(Document):
    def validate(self):
        self._set_company()
        if not self.get("observed_state"):
            self.observed_state = "NeedsSetup"

    def _set_company(self):
        if self.get("company"):
            return
        from altoplano_agents.services.context import resolve_company
        self.company = resolve_company(None)
        if not self.get("owner_user"):
            self.owner_user = frappe.session.user

