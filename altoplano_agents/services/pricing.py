# Tarifas y valorización de consumo (doc 13). Decimal, monedas explícitas.
import frappe
from decimal import Decimal


def price_event(event):
    """Valoriza un Usage Event con la Price Card vigente en la fecha del consumo.

    Sin tarifa válida -> measurement_state 'Unpriced' (nunca $0 ficticio).
    """
    if not event.supplier_price_card:
        event.measurement_state = "Unpriced"
        return event
    card = frappe.get_doc("AIA Price Card", event.supplier_price_card)
    metrics = frappe.parse_json(event.metrics_json) if isinstance(event.metrics_json, str) else (event.metrics_json or {})
    total = Decimal("0")
    for line in card.rate_lines:
        units = Decimal(str(metrics.get(line.metric_key, 0) or 0))
        if units <= 0:
            continue
        total += units / Decimal(str(line.unit_basis)) * Decimal(str(line.unit_price))
    event.supplier_amount = float(total)
    event.measurement_state = "Reported"
    return event

