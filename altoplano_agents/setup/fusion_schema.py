# Fusion LivingOrg OS v2 -> altoplano_agents (etapa B: schema).
# Idempotente: no crea nada que ya exista, no borra datos ni campos.

import frappe

OS_ROLES = [
    "OS Admin", "OS Architect", "OS Publisher", "OS AI Supervisor",
    "OS Manager", "OS Operator", "OS Auditor", "OS Viewer",
]

OS_DOCUMENT_LINK_FIELDS = [
    {"fieldname": "run", "label": "Run", "fieldtype": "Link", "options": "OS Run", "reqd": 1, "in_list_view": 1},
    {"fieldname": "step_run", "label": "Step Run", "fieldtype": "Link", "options": "OS Step Run", "in_list_view": 1},
    {"fieldname": "process_ref", "label": "Process", "fieldtype": "Link", "options": "OS Process", "in_list_view": 1},
    {"fieldname": "step_key", "label": "Step Key", "fieldtype": "Data"},
    {"fieldname": "action_key", "label": "Action Key", "fieldtype": "Data"},
    {"fieldname": "link_role", "label": "Link Role", "fieldtype": "Select", "options": "Source\nTarget\nResult\nRelated", "default": "Result", "in_list_view": 1},
    {"fieldname": "reference_doctype", "label": "Reference DocType", "fieldtype": "Link", "options": "DocType", "reqd": 1, "in_list_view": 1},
    {"fieldname": "reference_name", "label": "Reference Name", "fieldtype": "Dynamic Link", "options": "reference_doctype", "reqd": 1, "in_list_view": 1},
    {"fieldname": "label", "label": "Label", "fieldtype": "Data"},
    {"fieldname": "is_primary", "label": "Primary Result", "fieldtype": "Check", "default": "0"},
    {"fieldname": "document_status_snapshot", "label": "Document Status Snapshot", "fieldtype": "Data", "description": "Estado/docstatus observado al vincular el documento."},
]

OS_PROCESS_ACTION_FIELDS = [
    {"fieldname": "action_key", "label": "Action Key", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
    {"fieldname": "step_key", "label": "Step Key", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
    {"fieldname": "action_label", "label": "Action Label", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
    {"fieldname": "system", "label": "System", "fieldtype": "Select", "options": "ERPNext\nExternal", "default": "ERPNext", "reqd": 1, "in_list_view": 1},
    {"fieldname": "action_type", "label": "Action Type", "fieldtype": "Select", "options": "OPEN_DOCUMENT\nCREATE_DOCUMENT\nUPDATE_DOCUMENT\nCREATE_FROM_SOURCE\nSUBMIT_DOCUMENT\nLINK_DOCUMENT", "reqd": 1, "in_list_view": 1},
    {"fieldname": "source_doctype", "label": "Source DocType", "fieldtype": "Link", "options": "DocType"},
    {"fieldname": "target_doctype", "label": "Target DocType", "fieldtype": "Link", "options": "DocType", "in_list_view": 1},
    {"fieldname": "required_role", "label": "Required Role", "fieldtype": "Link", "options": "Role", "description": "Rol adicional necesario para ejecutar esta acción."},
    {"fieldname": "completion_rule", "label": "Completion Rule", "fieldtype": "Select", "options": "Manual\nDocument Linked\nDocument Exists\nDocument Submitted", "default": "Document Linked"},
    {"fieldname": "is_required", "label": "Required Before Step Completion", "fieldtype": "Check", "default": "1"},
    {"fieldname": "submit_after_create", "label": "Submit After Create", "fieldtype": "Check", "default": "0"},
    {"fieldname": "field_mapping_json", "label": "Field Mapping JSON", "fieldtype": "Code", "options": "JSON"},
    {"fieldname": "defaults_json", "label": "Defaults JSON", "fieldtype": "Code", "options": "JSON"},
    {"fieldname": "description", "label": "Description", "fieldtype": "Small Text"},
    {"fieldname": "sort_order", "label": "Sort Order", "fieldtype": "Int", "default": "0"},
]

FULL_PERMS = {"read": 1, "write": 1, "create": 1, "delete": 1, "report": 1, "export": 1}


def ensure_roles():
    for role in OS_ROLES:
        if frappe.db.exists("Role", role):
            continue
        frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 0}).insert(ignore_permissions=True)
    frappe.db.commit()


def ensure_doctype(name, istable, fields):
    if frappe.db.exists("DocType", name):
        return
    perms = []
    for role in ["OS Admin", "System Manager"]:
        perms.append(dict(FULL_PERMS, role=role))
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": name,
        "module": "Altoplano Agents",
        "istable": 1 if istable else 0,
        "editable_grid": 1,
        "track_changes": 0 if istable else 1,
        "engine": "InnoDB",
        "autoname": "hash",
        "fields": fields,
        "permissions": perms,
    })
    doc.flags.ignore_permissions = True
    doc.insert(ignore_permissions=True)
    frappe.db.commit()


def add_fields(doctype, specs):
    if not frappe.db.exists("DocType", doctype):
        return
    dt = frappe.get_doc("DocType", doctype)
    existing = {f.fieldname for f in dt.fields}
    changed = False
    for spec in specs:
        if spec["fieldname"] in existing:
            continue
        dt.append("fields", spec)
        changed = True
    if changed:
        dt.flags.ignore_permissions = True
        dt.save(ignore_permissions=True)
        frappe.db.commit()


def patch_select_options(doctype, fieldname, options):
    if not frappe.db.exists("DocType", doctype):
        return
    dt = frappe.get_doc("DocType", doctype)
    for f in dt.fields:
        if f.fieldname == fieldname and f.options != options:
            f.options = options
            dt.flags.ignore_permissions = True
            dt.save(ignore_permissions=True)
            frappe.db.commit()
            break


def grant_os_permissions():
    doctypes = frappe.get_all(
        "DocType",
        filters={"module": "Altoplano Agents", "name": ["like", "OS %"], "istable": 0},
        pluck="name",
    )
    for dt_name in doctypes:
        meta = frappe.get_doc("DocType", dt_name)
        existing = {p.role for p in meta.get("permissions", [])}
        for role in ["OS Admin", "System Manager"]:
            if role in existing:
                continue
            meta.append("permissions", dict(FULL_PERMS, role=role))
        meta.flags.ignore_permissions = True
        meta.save(ignore_permissions=True)
    frappe.db.commit()


def run():
    ensure_roles()
    ensure_doctype("OS Document Link", False, OS_DOCUMENT_LINK_FIELDS)
    ensure_doctype("OS Process Action", True, OS_PROCESS_ACTION_FIELDS)

    # Overlays (schema_overlays.py de livingorg_bridge)
    add_fields("OS Process", [
        {"fieldname": "actions", "label": "System Actions", "fieldtype": "Table", "options": "OS Process Action", "description": "Acciones estructuradas por step_key."},
    ])
    add_fields("OS Run", [
        {"fieldname": "run_mode", "label": "Run Mode", "fieldtype": "Select", "options": "Test\nLive", "default": "Live", "in_list_view": 1},
        {"fieldname": "context_json", "label": "Runtime Context JSON", "fieldtype": "Code", "options": "JSON"},
    ])
    add_fields("OS Step Run", [
        {"fieldname": "step_type_snapshot", "label": "Step Type Snapshot", "fieldtype": "Data"},
        {"fieldname": "process_version_snapshot", "label": "Process Version Snapshot", "fieldtype": "Data"},
        {"fieldname": "instructions_snapshot", "label": "Instructions Snapshot", "fieldtype": "Long Text"},
        {"fieldname": "sop_snapshot", "label": "SOP Snapshot", "fieldtype": "Data"},
        {"fieldname": "prompt_snapshot", "label": "Prompt Snapshot", "fieldtype": "Data"},
        {"fieldname": "policy_snapshot", "label": "Policy Snapshot", "fieldtype": "Data"},
        {"fieldname": "actor_role", "label": "Actor Role", "fieldtype": "Link", "options": "Role"},
        {"fieldname": "approval_role_snapshot", "label": "Approval Role Snapshot", "fieldtype": "Link", "options": "Role"},
        {"fieldname": "action_status", "label": "System Action Status", "fieldtype": "Select", "options": "Not Required\nReady\nExecuted\nFailed\nSkipped", "default": "Not Required", "in_list_view": 1},
        {"fieldname": "action_snapshot_json", "label": "System Actions Snapshot JSON", "fieldtype": "Code", "options": "JSON"},
        {"fieldname": "source_doctype", "label": "Primary Source DocType", "fieldtype": "Link", "options": "DocType"},
        {"fieldname": "source_name", "label": "Primary Source Name", "fieldtype": "Dynamic Link", "options": "source_doctype"},
        {"fieldname": "reference_doctype", "label": "Primary Result DocType", "fieldtype": "Link", "options": "DocType"},
        {"fieldname": "reference_name", "label": "Primary Result Name", "fieldtype": "Dynamic Link", "options": "reference_doctype"},
        {"fieldname": "last_action_at", "label": "Last System Action At", "fieldtype": "Datetime", "read_only": 1},
    ])
    patch_select_options("OS Step Run", "status", "Blocked\nQueued\nRunning\nWaiting\nApproved\nCompleted\nFailed\nSkipped\nCancelled")

    # Organigrama Vivo 2.0 (manifest additive_schema)
    add_fields("OS SOP", [
        {"fieldname": "responsible_node", "label": "Responsible Organization Node", "fieldtype": "Link", "options": "OS Org Node", "description": "Organigrama Vivo 2.0: puesto responsable del SOP."},
    ])
    add_fields("OS Role Card", [
        {"fieldname": "org_node", "label": "Organization Node", "fieldtype": "Link", "options": "OS Org Node", "in_list_view": 1},
        {"fieldname": "purpose", "label": "Purpose", "fieldtype": "Small Text"},
        {"fieldname": "objectives", "label": "Objectives", "fieldtype": "Text Editor"},
        {"fieldname": "functions", "label": "Functions", "fieldtype": "Text Editor"},
        {"fieldname": "competencies", "label": "Competencies", "fieldtype": "Text Editor"},
        {"fieldname": "tools", "label": "Tools", "fieldtype": "Small Text"},
        {"fieldname": "process_refs", "label": "Process References (Legacy Summary)", "fieldtype": "Small Text"},
        {"fieldname": "sop_refs", "label": "SOP References (Legacy Summary)", "fieldtype": "Small Text"},
    ])
    add_fields("OS KPI Definition", [
        {"fieldname": "org_node", "label": "Organization Node", "fieldtype": "Link", "options": "OS Org Node"},
        {"fieldname": "role_card", "label": "Role Card", "fieldtype": "Link", "options": "OS Role Card"},
        {"fieldname": "designation", "label": "Designation", "fieldtype": "Link", "options": "Designation"},
    ])
    patch_select_options("OS KPI Definition", "entity_type", "Company\nProcess\nStep\nAgent\nConnector\nPosition\nRoleCard")

    grant_os_permissions()
    frappe.clear_cache()
    return {"ok": 1}
