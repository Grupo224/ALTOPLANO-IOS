import frappe


@frappe.whitelist(methods=["GET"])
def boot(company_context=None):
    from altoplano_agents.api.v1.common import require_app_access
    require_app_access()
    from altoplano_agents.services.context import resolve_company, allowed_companies
    roles = frappe.get_roles()
    companies = allowed_companies()
    company = resolve_company(company_context) if companies else None
    return {
        "user": frappe.session.user,
        "full_name": frappe.db.get_value("User", frappe.session.user, "full_name"),
        "roles": roles,
        "companies": sorted(companies),
        "company": company,
        "app_route": "/ai-agents",
        "capabilities": {
            "manage_agents": bool({"AIA Owner", "AIA Manager", "AIA Technical Admin"} & set(roles)),
            "manage_business": bool({"AIA Manager"} & set(roles)),
            "review": bool({"AIA Reviewer"} & set(roles)),
            "billing": bool({"AIA Billing Manager"} & set(roles)),
            "technical": bool({"AIA Technical Admin"} & set(roles)),
        },
    }

