# Roles de Altoplano IA Agents (creacion idempotente).

ROLES = [
    {"role": "AIA User", "desk_access": 0},
    {"role": "AIA Owner", "desk_access": 1},
    {"role": "AIA Manager", "desk_access": 1},
    {"role": "AIA Operator", "desk_access": 1},
    {"role": "AIA Reviewer", "desk_access": 1},
    {"role": "AIA Viewer", "desk_access": 1},
    {"role": "AIA Billing Manager", "desk_access": 1},
    {"role": "AIA Technical Admin", "desk_access": 1},
    {"role": "AIA Provisioner", "desk_access": 0},
    {"role": "AIA Runtime Service", "desk_access": 0},
]


def ensure_roles():
    import frappe
    for spec in ROLES:
        if frappe.db.exists("Role", spec["role"]):
            continue
        r = frappe.get_doc({"doctype": "Role", "role_name": spec["role"], "desk_access": spec["desk_access"]})
        r.flags.ignore_permissions = True
        r.insert(ignore_permissions=True)
