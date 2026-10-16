import frappe


@frappe.whitelist(methods=["GET"])
def list_approvals(company_context=None, limit=50):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    rows = frappe.get_all(
        "AIA Approval Request", filters={"company": company},
        fields=["name", "run", "tool_call", "reviewer", "status", "expires_at", "payload_snapshot_json", "reason"],
        limit_page_length=int(limit) if limit else 50, order_by="creation desc",
    )
    return rows


@frappe.whitelist(methods=["POST"])
def decide(approval, decision, reason=None):
    d = frappe.get_doc("AIA Approval Request", approval)
    if d.status != "Pending":
        frappe.throw("La aprobación ya no está pendiente.", frappe.ValidationError)
    if decision not in ("Approved", "Rejected"):
        frappe.throw("Decisión inválida.", frappe.ValidationError)
    d.status = decision
    d.decided_by = frappe.session.user
    d.decided_at = frappe.utils.now_datetime()
    if reason:
        d.reason = reason
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"name": d.name, "status": d.status}

