# Instalacion de Altoplano IA Agents.

import frappe


def after_install():
    from altoplano_agents.roles import ensure_roles
    ensure_roles()
    seed_default_tool_catalog()
    seed_default_template()
    seed_default_settings()
    frappe.db.commit()


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

