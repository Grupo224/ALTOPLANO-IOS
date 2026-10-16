# Generador de DocTypes de Altoplano IA Agents (dos pasadas).
# 1) Crea los esqueletos (custom=0, módulo "Altoplano Agents").
# 2) Añade campos, cuando ya existen todos los Link destino.

import frappe
from .helpers import MODULE, FIELDTYPE_MAP
from .schema_1 import SCHEMA_1
from .schema_2 import SCHEMA_2
from .schema_3 import SCHEMA_3
from .schema_4 import SCHEMA_4

ALL_SCHEMAS = SCHEMA_1 + SCHEMA_2 + SCHEMA_3 + SCHEMA_4


def _ensure_module_def():
    if frappe.db.exists("Module Def", "Altoplano Agents"):
        return
    md = frappe.get_doc({"doctype": "Module Def", "module_name": "Altoplano Agents", "app_name": "altoplano_agents"})
    md.flags.ignore_permissions = True
    md.insert(ignore_permissions=True)


def _build_fields(spec):
    fields = []
    for (fieldname, label, ftype, options, reqd, authority) in spec["fields"]:
        fields.append(frappe._dict({
            "fieldname": fieldname,
            "label": label,
            "fieldtype": FIELDTYPE_MAP.get(ftype, ftype),
            "options": options,
            "reqd": 1 if reqd else 0,
            "read_only": 1 if authority == "Server" else 0,
        }))
    return fields


def _pass_1_skeletons():
    for spec in ALL_SCHEMAS:
        name = spec["name"]
        is_table = spec.get("istable", 0)
        is_single = spec.get("issingle", 0)
        if frappe.db.exists("DocType", name):
            dt = frappe.get_doc("DocType", name)
        else:
            dt = frappe.new_doc("DocType")
            dt.name = name
            dt.module = MODULE
            dt.custom = 0
            dt.istable = is_table
            dt.issingle = is_single
            dt.autoname = "hash"
            dt.permissions = []
            dt.fields = []
            dt.flags.ignore_permissions = True
            dt.flags.ignore_mandatory = True
            dt.insert(ignore_permissions=True)


def _pass_2_fields():
    for spec in ALL_SCHEMAS:
        name = spec["name"]
        is_table = spec.get("istable", 0)
        is_single = spec.get("issingle", 0)
        dt = frappe.get_doc("DocType", name)
        if dt.istable != is_table:
            dt.istable = is_table
        if dt.issingle != is_single:
            dt.issingle = is_single
        existing = {f.fieldname for f in dt.fields}
        changed = False
        for f in _build_fields(spec):
            if f.fieldname in existing:
                continue
            dt.append("fields", {
                "fieldname": f.fieldname,
                "label": f.label,
                "fieldtype": f.fieldtype,
                "options": f.options,
                "reqd": f.reqd,
                "read_only": f.read_only,
            })
            changed = True
        if changed:
            dt.flags.ignore_permissions = True
            dt.flags.ignore_mandatory = True
            dt.save(ignore_permissions=True)


def create_all():
    _ensure_module_def()
    frappe.clear_cache(doctype="DocType")
    _pass_1_skeletons()
    frappe.clear_cache(doctype="DocType")
    _pass_2_fields()
    frappe.clear_cache(doctype="DocType")
    frappe.db.commit()
    return [s["name"] for s in ALL_SCHEMAS]
