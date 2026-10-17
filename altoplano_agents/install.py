# Instalacion de Altoplano IA Agents (LivingOrg OS).

import frappe


def after_install():
    from altoplano_agents.roles import ensure_roles
    ensure_roles()
    grant_doctype_permissions()
    seed_workspace()
    frappe.db.commit()


AIA_ROLES = [
    "AIA User", "AIA Owner", "AIA Manager", "AIA Operator", "AIA Reviewer",
    "AIA Viewer", "AIA Billing Manager", "AIA Technical Admin",
    "AIA Provisioner", "AIA Runtime Service",
]


def grant_doctype_permissions():
    """Otorga permisos completos a todos los roles sobre los DocTypes del modulo."""
    roles = ["System Manager", "Administrator"] + AIA_ROLES
    doctypes = frappe.get_all(
        "DocType",
        filters={"module": "Altoplano Agents", "istable": 0},
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


def seed_workspace():
    """Crea el Workspace 'Altoplano Agents' en Desk con los doctypes OS."""
    import json
    sections = [
        ("Organizacion", ["OS Org Node", "OS Org Relation", "OS Role Card"]),
        ("Procesos", ["OS Process", "OS SOP", "OS Policy"]),
        ("Agentes IA", ["OS Agent", "OS Prompt", "OS Skill"]),
        ("Ejecucion", ["OS Run", "OS Step Run", "OS Approval", "OS Evidence"]),
        ("Gobierno", ["OS KPI Definition", "OS Integration", "OS Knowledge Source"]),
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
