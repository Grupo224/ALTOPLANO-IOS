import frappe
from frappe.model.document import Document


class AIAAgentRevision(Document):
    """Instantánea inmutable: no se permite reescribir una revisión existente."""

    def on_update(self):
        if not self.is_new() and self.get_doc_before_save():
            prev = self.get_doc_before_save()
            immutable = {"manifest_json", "manifest_hash", "agent", "revision_no", "created_by", "created_at"}
            for f in immutable:
                if prev.get(f) != self.get(f):
                    frappe.throw("La revisión es inmutable: no se puede modificar " + f)

