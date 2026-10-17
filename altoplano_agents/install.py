# Instalacion de Altoplano IA Agents.

import frappe


def after_install():
    from altoplano_agents.roles import ensure_roles
    ensure_roles()
    seed_default_tool_catalog()
    seed_default_template()
    seed_default_settings()
    seed_event_custom_fields()
    grant_doctype_permissions()
    seed_workspace()
    frappe.db.commit()


AIA_ROLES = [
    "AIA User", "AIA Owner", "AIA Manager", "AIA Operator", "AIA Reviewer",
    "AIA Viewer", "AIA Billing Manager", "AIA Technical Admin",
    "AIA Provisioner", "AIA Runtime Service",
]


def grant_doctype_permissions():
    """Otorga permisos completos a todos los roles sobre los DocTypes AIA (main)."""
    roles = ["System Manager", "Administrator"] + AIA_ROLES
    doctypes = frappe.get_all(
        "DocType",
        filters={"name": ["like", "AIA %"], "istable": 0},
        pluck="name",
    )
    full = {
        "read": 1, "write": 1, "create": 1, "delete": 1,
        "if_owner": 0, "permlevel": 0,
    }
    for dt in doctypes:
        try:
            meta = frappe.get_doc("DocType", dt)
            existing = {p.role for p in meta.get("permissions", [])}
            for role in roles:
                if role in existing:
                    continue
                meta.append("permissions", dict(full, role=role))
            meta.flags.ignore_permissions = True
            meta.save(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(title="grant_permissions " + dt, message=str(e))
    frappe.db.commit()


def seed_event_custom_fields():
    """Custom Fields derivados en Event nativo para la agenda de agentes."""
    fields = [
        {"fieldname": "custom_aia_company", "label": "Empresa AIA", "fieldtype": "Link", "options": "Company", "insert_after": "subject"},
        {"fieldname": "custom_aia_calendar", "label": "Agenda AIA", "fieldtype": "Link", "options": "AIA Calendar", "insert_after": "custom_aia_company"},
        {"fieldname": "custom_aia_agent", "label": "Agente AIA", "fieldtype": "Link", "options": "AIA Agent", "insert_after": "custom_aia_calendar"},
        {"fieldname": "custom_aia_appointment", "label": "Cita AIA", "fieldtype": "Link", "options": "AIA Appointment", "insert_after": "custom_aia_agent"},
    ]
    for f in fields:
        if frappe.db.exists("Custom Field", {"dt": "Event", "fieldname": f["fieldname"]}):
            continue
        doc = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Event",
            "fieldname": f["fieldname"],
            "label": f["label"],
            "fieldtype": f["fieldtype"],
            "options": f["options"],
            "insert_after": f["insert_after"],
            "read_only": 1,
        })
        doc.insert(ignore_permissions=True)
    frappe.db.commit()


def seed_workspace():
    """Crea el Workspace 'Altoplano Agents' en Desk para ver todos los doctypes."""
    import json
    sections = [
        ("Agentes", ["AIA Agent", "AIA Agent Template", "AIA Agent Revision", "AIA Skill", "AIA Skill Assignment", "AIA Deployment", "AIA Run", "AIA Test Result", "AIA Allowed Agent"]),
        ("Conectores", ["AIA Connection", "AIA Channel Binding", "AIA Identity Binding", "AIA Meta App", "AIA WhatsApp Account", "AIA WhatsApp Template", "AIA Email Binding", "AIA MCP Server", "AIA MCP Tool", "AIA OAuth Grant", "AIA Connection Check", "AIA Chatwoot Account"]),
        ("Mensajeria", ["AIA Conversation", "AIA Message", "AIA Messaging Consent", "AIA Event Inbox", "AIA Outbox Event"]),
        ("Agenda", ["AIA Calendar", "AIA Appointment"]),
        ("Herramientas", ["AIA Tool Definition", "AIA Tool Grant", "AIA Tool Call", "AIA Command Receipt"]),
        ("Aprobaciones", ["AIA Approval Request"]),
        ("Presupuesto y gastos", ["AIA Budget Policy", "AIA Budget Bucket", "AIA Budget Reservation", "AIA Reservation Allocation", "AIA Billing Batch", "AIA Entitlement", "AIA Rate Line", "AIA Price Card", "AIA Usage Event"]),
        ("Conocimiento", ["AIA Knowledge Source", "AIA Source Assignment", "AIA Source Access", "AIA Business Profile"]),
        ("Auditoria y seguridad", ["AIA Audit Event", "AIA Access Profile", "AIA Automation", "AIA ERP Link"]),
        ("Configuracion", ["AIA Settings"]),
    ]
    blocks = []
    for label, doctypes in sections:
        blocks.append({"id": "hdr_" + label, "type": "header", "data": {"text": "<span class='h4'><b>" + label + "</b></span>", "col": 12}})
        for dt in doctypes:
            if frappe.db.exists("DocType", dt):
                blocks.append({"id": "sc_" + dt, "type": "shortcut", "data": {"shortcut_name": dt, "col": 3}})
    content = json.dumps(blocks, ensure_ascii=False)
    if frappe.db.exists("Workspace", "Altoplano Agents"):
        ws = frappe.get_doc("Workspace", "Altoplano Agents")
    else:
        ws = frappe.new_doc("Workspace")
        ws.name = "Altoplano Agents"
        ws.label = "Altoplano Agents"
        ws.title = "Altoplano Agents"
        ws.module = "Altoplano Agents"
    ws.content = content
    ws.flags.ignore_permissions = True
    ws.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()


def seed_default_tool_catalog():
    tools = [
        {"slug": "erp.search_customers", "display_name": "Buscar clientes",
         "explanation": "Busca clientes de la empresa por nombre, telefono o correo.",
         "adapter_key": "erp.search_customers", "risk": "Read"},
        {"slug": "erp.create_followup", "display_name": "Crear seguimiento",
         "explanation": "Crea una tarea de seguimiento (ToDo) asignada a un responsable autorizado.",
         "adapter_key": "erp.create_followup", "risk": "ReversibleWrite"},
        {"slug": "erp.create_lead", "display_name": "Crear prospecto",
         "explanation": "Crea un prospecto (Lead) con los campos permitidos.",
         "adapter_key": "erp.create_lead", "risk": "ReversibleWrite"},
        {"slug": "erp.create_quotation_draft", "display_name": "Crear cotizacion (borrador)",
         "explanation": "Crea una cotizacion en borrador; los importes los calcula ERPNext.",
         "adapter_key": "erp.create_quotation_draft", "risk": "SensitiveWrite"},
    ]
    for t in tools:
        if frappe.db.exists("AIA Tool Definition", t["slug"]):
            continue
        doc = frappe.get_doc({
            "doctype": "AIA Tool Definition",
            "slug": t["slug"],
            "display_name": t["display_name"],
            "explanation": t["explanation"],
            "adapter_key": t["adapter_key"],
            "risk": t["risk"],
            "input_schema": "{}",
            "output_schema": "{}",
            "allowed_resources": "{}",
            "enabled": 1,
        })
        doc.flags.ignore_permissions = True
        doc.insert(ignore_permissions=True)


def seed_default_settings():
    """Habilita la app en modo demo con una Company por defecto, sin tocar produccion."""
    settings = frappe.get_single("AIA Settings")
    if not settings.get("enabled"):
        settings.enabled = 1
    if not settings.get("environment"):
        settings.environment = "Development"
    settings.demo_mode = 1
    if not settings.get("default_company"):
        companies = frappe.get_all("Company", pluck="name")
        demo = [c for c in companies if "demo" in c.lower()]
        preferred = demo[0] if demo else (companies[0] if companies else None)
        if preferred:
            settings.default_company = preferred
    settings.flags.ignore_permissions = True
    settings.save(ignore_permissions=True)


def seed_default_template():
    if frappe.db.exists("AIA Agent Template", "atencion-al-cliente"):
        return
    doc = frappe.get_doc({
        "doctype": "AIA Agent Template",
        "slug": "atencion-al-cliente",
        "version": "1",
        "display_name": "Atencion al cliente",
        "purpose": "Responder preguntas frecuentes y crear seguimientos para el equipo.",
        "audience": "Customer",
        "instructions": "Responde con el tono configurado por el negocio. No prometas acciones que no puedas ejecutar. Si la solicitud requiere decision humana, transfiere.",
        "company_scope_key": "__GLOBAL__",
        "status": "Published",
    })
    doc.flags.ignore_permissions = True
    doc.insert(ignore_permissions=True)

