import frappe
from frappe.model.document import Document


class AIAUsageEvent(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agent: DF.Link
        base_amount: DF.Currency
        base_currency: DF.Link
        company: DF.Link
        connection: DF.Link
        correction_of: DF.Link | None
        customer_amount: DF.Currency
        customer_currency: DF.Link | None
        customer_price_card: DF.Link | None
        event_key: DF.Data
        fx_at: DF.Datetime | None
        fx_rate: DF.Float
        fx_source: DF.Data | None
        measurement_state: DF.Literal["Estimated", "Reported", "Reconciled", "Unpriced", "Corrected"]
        metrics_json: DF.Code
        occurred_at: DF.Datetime
        pricing_snapshot_json: DF.Code
        provider_event_id: DF.Data | None
        run: DF.Link
        supplier_amount: DF.Currency
        supplier_currency: DF.Link | None
        supplier_price_card: DF.Link | None
    # end: auto-generated types
    """Hecho de consumo inmutable. Correcciones mediante nuevo evento (correction_of)."""

    def on_update(self):
        if not self.is_new() and self.get_doc_before_save():
            prev = self.get_doc_before_save()
            immutable = {"event_key", "run", "connection", "occurred_at"}
            for f in immutable:
                if prev.get(f) != self.get(f):
                    frappe.throw("El evento de consumo es append-only: no se puede modificar " + f)

