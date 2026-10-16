import frappe


@frappe.whitelist(methods=["GET"])
def get_profile(company_context=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    name = frappe.db.get_value("AIA Business Profile", {"company": company}, "name")
    if not name:
        return None
    d = frappe.get_doc("AIA Business Profile", name)
    return {
        "name": d.name, "company": d.company, "display_name": d.display_name,
        "offering": d.offering, "audience": d.audience, "tone": d.tone,
        "opening_hours": d.opening_hours, "timezone": d.timezone,
        "handoff_instructions": d.handoff_instructions, "public_contact": d.public_contact,
        "status": d.status, "config_version": d.config_version,
    }


@frappe.whitelist(methods=["POST"])
def save_profile(company_context=None, **fields):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    editable = {"display_name", "offering", "audience", "tone", "opening_hours", "timezone", "handoff_instructions", "public_contact"}
    name = frappe.db.get_value("AIA Business Profile", {"company": company}, "name")
    d = frappe.get_doc("AIA Business Profile", name) if name else frappe.new_doc("AIA Business Profile")
    if not name:
        d.company = company
        d.status = "Active"
        d.config_version = 0
    for k, val in fields.items():
        if k in editable and val is not None:
            d.set(k, val)
    if not d.get("config_version"):
        d.config_version = 0
    d.config_version = int(d.config_version or 0) + 1
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"name": d.name, "config_version": d.config_version}

