import frappe


@frappe.whitelist(methods=["GET", "POST"])
def list_connections(company_context=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    rows = frappe.get_all(
        "AIA Connection", filters={"company": company},
        fields=["name", "connection_type", "provider", "display_name", "status", "payer_mode", "error_code"],
        order_by="modified desc",
    )
    return rows


@frappe.whitelist(methods=["POST"])
def create_connection(company_context=None, connection_type=None, provider=None, display_name=None, base_url=None, auth_type=None, payer_mode=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    d = frappe.get_doc({
        "doctype": "AIA Connection",
        "company": company,
        "connection_type": connection_type,
        "provider": provider,
        "display_name": display_name,
        "base_url": base_url,
        "auth_type": auth_type or "None",
        "payer_mode": payer_mode or "Included",
    })
    d.flags.ignore_permissions = True
    d.insert(ignore_permissions=True)
    return {"name": d.name, "status": d.status}

