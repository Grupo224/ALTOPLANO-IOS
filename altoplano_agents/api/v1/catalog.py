import frappe

from altoplano_agents.api.v1.common import require_app_access


@frappe.whitelist(methods=["GET"])
def templates(company_context=None, limit=50):
    require_app_access()
    filters = {"status": "Published"}
    rows = frappe.get_all(
        "AIA Agent Template", filters=filters,
        fields=["name", "slug", "version", "display_name", "purpose", "audience"],
        limit_page_length=int(limit) if limit else 50, order_by="display_name",
    )
    return rows


@frappe.whitelist(methods=["GET"])
def skills(company_context=None, limit=50):
    require_app_access()
    filters = {"status": "Published"}
    rows = frappe.get_all(
        "AIA Skill", filters=filters,
        fields=["name", "slug", "version", "display_name", "kind"],
        limit_page_length=int(limit) if limit else 50, order_by="display_name",
    )
    return rows


@frappe.whitelist(methods=["GET"])
def tools(company_context=None):
    require_app_access()
    rows = frappe.get_all(
        "AIA Tool Definition", filters={"enabled": 1},
        fields=["slug", "display_name", "explanation", "risk"],
        order_by="display_name",
    )
    return rows

