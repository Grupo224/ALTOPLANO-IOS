import frappe


@frappe.whitelist(methods=["GET", "POST"])
def list_conversations(company_context=None, limit=50):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    rows = frappe.get_all(
        "AIA Conversation", filters={"company": company},
        fields=["name", "agent", "summary", "handler_state", "last_activity", "assigned_user"],
        limit_page_length=int(limit) if limit else 50, order_by="last_activity desc",
    )
    return rows


@frappe.whitelist(methods=["GET", "POST"])
def get_messages(conversation, limit=100):
    from altoplano_agents.permissions import has_conversation_permission
    conv = frappe.get_doc("AIA Conversation", conversation)
    if not has_conversation_permission(conv):
        frappe.throw("No tienes acceso a esta conversación.", frappe.PermissionError)
    rows = frappe.get_all(
        "AIA Message", filters={"conversation": conversation},
        fields=["name", "actor", "direction", "body", "delivery_state", "created_at"],
        limit_page_length=int(limit) if limit else 100, order_by="creation asc",
    )
    return rows


@frappe.whitelist(methods=["POST"])
def handoff(conversation, assigned_user=None):
    from altoplano_agents.permissions import has_conversation_permission
    conv = frappe.get_doc("AIA Conversation", conversation)
    if not has_conversation_permission(conv):
        frappe.throw("No tienes acceso.", frappe.PermissionError)
    conv.handler_state = "Human"
    if assigned_user:
        conv.assigned_user = assigned_user
    conv.flags.ignore_permissions = True
    conv.save(ignore_permissions=True)
    return {"name": conv.name, "handler_state": conv.handler_state}

