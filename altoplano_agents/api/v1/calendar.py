import frappe


@frappe.whitelist(methods=["GET", "POST"])
def list_calendars():
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(None)
    return frappe.get_all(
        "AIA Calendar",
        filters={"company": company},
        fields=["name", "display_name", "agent", "timezone", "slot_minutes", "enabled", "sync_mode"],
        order_by="modified desc",
    )


@frappe.whitelist(methods=["GET", "POST"])
def list_appointments():
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(None)
    return frappe.get_all(
        "AIA Appointment",
        filters={"company": company},
        fields=["name", "calendar", "customer", "agent", "status", "timezone", "source", "booking_key", "revision"],
        order_by="modified desc",
    )


@frappe.whitelist(methods=["POST"])
def create_calendar(display_name=None, timezone=None, slot_minutes=None, agent=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(None)
    d = frappe.get_doc({
        "doctype": "AIA Calendar",
        "company": company,
        "display_name": display_name or "Mi agenda",
        "owner_user": frappe.session.user,
        "timezone": timezone or "America/Mexico_City",
        "slot_minutes": int(slot_minutes or 30),
        "slot_step_minutes": 30,
        "buffer_before_minutes": 0,
        "buffer_after_minutes": 0,
        "minimum_notice_minutes": 0,
        "booking_horizon_days": 14,
        "max_bookings_per_day": 20,
        "sync_mode": "LocalOnly",
        "enabled": 1,
        "config_version": 1,
    })
    if agent:
        d.agent = agent
    # Horario semanal por defecto: L-V 09:00-18:00
    for wd in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday"):
        d.append("availability", {"weekday": wd, "start_time": "09:00:00", "end_time": "18:00:00"})
    d.flags.ignore_permissions = True
    d.insert(ignore_permissions=True)
    return {"name": d.name, "display_name": d.display_name}
