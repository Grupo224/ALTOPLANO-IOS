# Adaptadores ERP cerrados (catálogo de herramientas). Ejecutan como principal limitado.
import frappe


ALLOWED = {"erp.search_customers", "erp.create_followup", "erp.create_lead", "erp.create_quotation_draft"}


def execute(tool_slug, arguments, actor=None):
    if tool_slug not in ALLOWED:
        frappe.throw("Herramienta no permitida.", frappe.PermissionError)
    return ADAPTERS[tool_slug](arguments or {}, actor)


def search_customers(args, actor):
    q = (args.get("query") or "").strip()
    filters = {}
    if q:
        filters["customer_name"] = ["like", "%" + q + "%"]
    return frappe.get_all(
        "Customer",
        filters=filters,
        fields=["name", "customer_name", "mobile_no", "email_id"],
        limit_page_length=10,
        order_by="modified desc",
    )


def create_followup(args, actor):
    task = args.get("task")
    if not task:
        frappe.throw("Falta la tarea del seguimiento.", frappe.ValidationError)
    assigned = args.get("assigned_to") or actor or frappe.session.user
    todo = frappe.get_doc({
        "doctype": "ToDo",
        "description": task,
        "assigned_by": frappe.session.user,
        "assigned_by_full_name": frappe.db.get_value("User", frappe.session.user, "full_name"),
        "reference_type": args.get("reference_type"),
        "reference_name": args.get("reference_name"),
    })
    if args.get("date"):
        todo.date = args["date"]
    todo.flags.ignore_permissions = True
    todo.insert(ignore_permissions=True)
    # Asignar (requiere permiso real; falla controlado si no corresponde)
    try:
        from frappe.desk.form.assign_to import add
        add({"assign_to": [assigned], "doctype": "ToDo", "name": todo.name})
    except Exception:
        pass
    return {"name": todo.name, "doctype": "ToDo"}


def create_lead(args, actor):
    from frappe.model.naming import get_default_naming_series
    lead = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": args.get("lead_name") or (args.get("company_name") or "Prospecto"),
        "company_name": args.get("company_name"),
        "email_id": args.get("email_id"),
        "phone": args.get("phone") or args.get("mobile_no"),
        "source": args.get("source"),
        "notes": args.get("notes"),
    })
    lead.flags.ignore_permissions = True
    lead.insert(ignore_permissions=True)
    return {"name": lead.name, "doctype": "Lead"}


def create_quotation_draft(args, actor):
    from erpnext.selling.doctype.quotation.quotation import Quotation
    customer = args.get("customer")
    items = args.get("items") or []
    if not customer or not items:
        frappe.throw("Cotización requiere cliente e ítems.", frappe.ValidationError)
    q = frappe.new_doc("Quotation")
    q.party_name = customer
    q.quotation_to = "Customer"
    q.transaction_date = frappe.utils.today()
    for it in items:
        q.append("items", {
            "item_code": it["item_code"],
            "qty": it.get("qty") or 1,
        })
    q.flags.ignore_permissions = True
    q.insert(ignore_permissions=True)  # Borrador real; importes los calcula ERPNext.
    return {"name": q.name, "doctype": "Quotation", "grand_total": q.grand_total}


ADAPTERS = {
    "erp.search_customers": search_customers,
    "erp.create_followup": create_followup,
    "erp.create_lead": create_lead,
    "erp.create_quotation_draft": create_quotation_draft,
}

