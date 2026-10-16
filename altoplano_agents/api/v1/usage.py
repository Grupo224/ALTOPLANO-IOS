import frappe


@frappe.whitelist(methods=["GET", "POST"])
def summary(company_context=None, agent=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    filters = {"company": company}
    if agent:
        filters["agent"] = agent
    events = frappe.get_all(
        "AIA Usage Event", filters=filters,
        fields=["measurement_state", "supplier_amount", "supplier_currency", "base_amount", "base_currency", "occurred_at"],
        order_by="occurred_at desc", limit_page_length=500,
    )
    total = 0.0
    states = {}
    for e in events:
        states[e.measurement_state] = states.get(e.measurement_state, 0) + 1
        try:
            total += float(e.base_amount or 0)
        except (TypeError, ValueError):
            pass
    return {"count": len(events), "base_total": total, "by_state": states, "currency": frappe.get_single("AIA Settings").base_currency}


@frappe.whitelist(methods=["GET", "POST"])
def events(company_context=None, agent=None, limit=50):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    filters = {"company": company}
    if agent:
        filters["agent"] = agent
    return frappe.get_all(
        "AIA Usage Event", filters=filters,
        fields=["name", "agent", "measurement_state", "supplier_amount", "supplier_currency", "base_amount", "base_currency", "occurred_at"],
        limit_page_length=int(limit) if limit else 50, order_by="occurred_at desc",
    )

