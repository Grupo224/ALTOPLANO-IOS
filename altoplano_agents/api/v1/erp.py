import frappe


@frappe.whitelist(methods=["GET"])
def resolve_link(erp_link):
    from altoplano_agents.permissions import has_agent_permission
    link = frappe.get_doc("AIA ERP Link", erp_link)
    # El acceso al vínculo no concede acceso al documento destino.
    if not frappe.has_permission(link.erp_doctype, "read", link.erp_document):
        frappe.throw("No tienes permiso sobre el documento vinculado.", frappe.PermissionError)
    return {"doctype": link.erp_doctype, "name": link.erp_document, "action": link.action}


@frappe.whitelist(methods=["GET"])
def activity(company_context=None, limit=50):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    return frappe.get_all(
        "AIA Audit Event", filters={"company": company},
        fields=["name", "event_type", "object_doctype", "object_name", "summary", "created_at"],
        limit_page_length=int(limit) if limit else 50, order_by="creation desc",
    )

