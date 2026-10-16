# Outbox: entrega de efectos externos tras commit.
import frappe


def deliver_event(event_name):
    ev = frappe.get_doc("AIA Outbox Event", event_name)
    # Sin adaptador externo conectado, queda en Failed con error claro (no ficticio Active).
    ev.state = "Failed"
    ev.attempt_count = (ev.attempt_count or 0) + 1
    ev.flags.ignore_permissions = True
    ev.save(ignore_permissions=True)

