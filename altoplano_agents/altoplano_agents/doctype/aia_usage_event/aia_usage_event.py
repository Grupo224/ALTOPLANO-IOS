import frappe
from frappe.model.document import Document


class AIAUsageEvent(Document):
    """Hecho de consumo inmutable. Correcciones mediante nuevo evento (correction_of)."""

    def on_update(self):
        if not self.is_new() and self.get_doc_before_save():
            prev = self.get_doc_before_save()
            immutable = {"event_key", "run", "connection", "occurred_at"}
            for f in immutable:
                if prev.get(f) != self.get(f):
                    frappe.throw("El evento de consumo es append-only: no se puede modificar " + f)

