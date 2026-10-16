import frappe


@frappe.whitelist(methods=["GET"])
def dashboard(company_context=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    agents = frappe.get_all(
        "AIA Agent", filters={"company": company},
        fields=["name", "observed_state", "modified"], order_by="modified desc",
    )
    active = [a for a in agents if a.observed_state == "Active"]
    needs_setup = [a for a in agents if a.observed_state in ("NeedsSetup", "Draft")]
    pending_approvals = frappe.db.count("AIA Approval Request", {"company": company, "status": "Pending"})
    return {
        "total_agents": len(agents),
        "active_agents": len(active),
        "needs_setup": len(needs_setup),
        "pending_approvals": pending_approvals,
        "recent": agents[:10],
    }

