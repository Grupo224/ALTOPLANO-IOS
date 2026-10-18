import json

import frappe

SKIP_META = {"name", "owner", "creation", "modified", "modified_by", "docstatus", "idx",
             "parent", "parentfield", "parenttype", "_user_tags", "_comments", "_assign",
             "_liked_by", "naming_series"}


@frappe.whitelist(methods=["GET", "POST"])
def get_doctype_meta(doctype=None):
    """Devuelve los campos editables de un doctype (label/fieldtype/options/reqd)
    para que el frontend renderice formularios completos sin hardcodear campos."""
    if not doctype:
        return {"fields": []}
    meta = frappe.get_meta(doctype)
    fields = []
    for f in meta.fields:
        if f.fieldname in SKIP_META:
            continue
        if f.fieldtype in ("Section Break", "Column Break", "Heading", "Fold", "Read Only", "Table"):
            continue
        if getattr(f, "read_only", 0):
            continue
        entry = {
            "fieldname": f.fieldname,
            "label": f.label or f.fieldname,
            "fieldtype": f.fieldtype,
            "options": f.options or "",
            "reqd": 1 if f.reqd else 0,
            "description": f.description or "",
        }
        if f.fieldtype == "Link":
            entry["link_doctype"] = f.options or ""
            try:
                entry["link_title_field"] = frappe.get_meta(f.options).title_field or "name"
            except Exception:
                entry["link_title_field"] = "name"
        fields.append(entry)
    return {"doctype": doctype, "fields": fields}


@frappe.whitelist(methods=["GET", "POST"])
def get_process(name):
    d = frappe.get_doc("OS Process", name)
    return {
        "name": d.name,
        "process_title": d.process_title,
        "status": d.status,
        "steps": [dict(s.as_dict(), x=float(s.x or 0), y=float(s.y or 0)) for s in d.get("steps", [])],
        "edges": [{"edge_key": e.edge_key, "source_step_key": e.source_step_key, "target_step_key": e.target_step_key, "relation_type": e.relation_type} for e in d.get("edges", [])],
    }


@frappe.whitelist(methods=["POST"])
def save_process_canvas(name, steps, edges):
    if isinstance(steps, str):
        steps = json.loads(steps)
    if isinstance(edges, str):
        edges = json.loads(edges)
    d = frappe.get_doc("OS Process", name)
    by_key = {s.step_key: s for s in d.get("steps", [])}
    for s in steps or []:
        row = by_key.get(s.get("step_key"))
        if row:
            row.x = float(s.get("x") or 0)
            row.y = float(s.get("y") or 0)
    d.set("edges", [])
    for e in edges or []:
        d.append("edges", {"edge_key": e.get("edge_key") or frappe.generate_hash(length=8), "source_step_key": e.get("source_step_key"), "target_step_key": e.get("target_step_key"), "relation_type": e.get("relation_type") or "NEXT"})
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"name": d.name}


@frappe.whitelist(methods=["POST"])
def add_process_step(name, step_title=None, step_type=None):
    d = frappe.get_doc("OS Process", name)
    key = frappe.generate_hash(length=8)
    d.append("steps", {"step_key": key, "step_title": step_title or "Nuevo paso", "step_type": step_type or "HUMAN", "execution_type": "H", "x": 40, "y": 40})
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"step_key": key}


@frappe.whitelist(methods=["POST"])
def save_process_step(name, step_key=None, values=None):
    """Edita los campos de un paso (child table OS Process Step) dentro del proceso padre."""
    if isinstance(values, str):
        values = json.loads(values)
    d = frappe.get_doc("OS Process", name)
    for s in d.get("steps", []):
        if s.step_key == step_key:
            for k, v in (values or {}).items():
                s.set(k, v)
            break
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"ok": 1}


@frappe.whitelist(methods=["POST"])
def delete_process_step(name, step_key=None):
    d = frappe.get_doc("OS Process", name)
    keep = [s for s in d.get("steps", []) if s.step_key != step_key]
    d.set("steps", keep)
    d.set("edges", [e for e in d.get("edges", []) if e.source_step_key != step_key and e.target_step_key != step_key])
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"ok": 1}


@frappe.whitelist(methods=["GET", "POST"])
def get_org():
    nodes = frappe.get_all("OS Org Node", fields=["name", "title", "node_type", "x", "y"], order_by="title")
    relations = frappe.get_all("OS Org Relation", fields=["name", "from_node", "to_node", "relation_type", "label"])
    return {"nodes": nodes, "relations": relations}


@frappe.whitelist(methods=["POST"])
def add_org_node(title=None, node_type=None, x=None, y=None):
    d = frappe.get_doc({"doctype": "OS Org Node", "title": title or "Nuevo nodo", "node_type": node_type or "Custom", "x": float(x or 100), "y": float(y or 100), "is_active": 1})
    d.flags.ignore_permissions = True
    d.insert(ignore_permissions=True)
    return {"name": d.name}


@frappe.whitelist(methods=["POST"])
def save_org_node(name, x=None, y=None):
    frappe.db.set_value("OS Org Node", name, {"x": float(x or 0), "y": float(y or 0)})
    return {"name": name}


@frappe.whitelist(methods=["POST"])
def create_process(process_title=None, process_code=None, purpose=None, risk_level=None, trigger_type=None):
    d = frappe.get_doc({
        "doctype": "OS Process",
        "process_title": process_title or "Nuevo proceso",
        "process_code": process_code or process_title or "Nuevo proceso",
        "purpose": purpose or process_title or "",
        "company": frappe.defaults.get_user_default("Company"),
        "owner_user": frappe.session.user,
        "status": "Draft",
        "trigger_type": trigger_type or "Manual",
        "max_autonomy": "L1",
        "risk_level": risk_level or "Medium",
        "version_label": "1",
    })
    d.flags.ignore_permissions = True
    d.insert(ignore_permissions=True)
    return {"name": d.name}


@frappe.whitelist(methods=["POST"])
def update_doc(doctype, name, values):
    if isinstance(values, str):
        values = json.loads(values)
    d = frappe.get_doc(doctype, name)
    for k, v in (values or {}).items():
        d.set(k, v)
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"name": d.name}


@frappe.whitelist(methods=["POST"])
def save_process_meta(name=None, values=None, goals=None):
    """Guarda los DATOS del proceso (wizard SIPOC/RACI/metas) y su child table goals.
    Los pasos/edges se manejan por separado en save_process_canvas."""
    if isinstance(values, str):
        values = json.loads(values)
    if isinstance(goals, str):
        goals = json.loads(goals)
    values = values or {}
    if name:
        d = frappe.get_doc("OS Process", name)
    else:
        if not values.get("process_code"):
            base = (values.get("process_title") or "PROC").upper()
            slug = "".join(c for c in base if c.isalnum())[:20] or "PROC"
            values["process_code"] = slug + "-" + frappe.generate_hash(length=4).upper()
        values.setdefault("status", "Draft")
        values.setdefault("trigger_type", "Manual")
        values.setdefault("max_autonomy", "L1")
        values.setdefault("risk_level", "Medium")
        values.setdefault("version_label", "v0.1")
        d = frappe.get_doc({"doctype": "OS Process"})
    for k, v in values.items():
        if k in ("steps", "edges"):
            continue
        d.set(k, v)
    if goals is not None:
        d.set("goals", [])
        for g in goals or []:
            try:
                target = float(g.get("target")) if g.get("target") not in (None, "") else 0
            except (TypeError, ValueError):
                target = 0
            d.append("goals", {
                "cadence": g.get("cadence") or "Monthly",
                "metric": g.get("metric"),
                "target": target,
                "unit": g.get("unit"),
                "tolerance": g.get("tolerance"),
                "direction": g.get("direction") or "More is better",
                "responsible": g.get("responsible"),
            })
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"name": d.name}


@frappe.whitelist(methods=["POST"])
def delete_org_node(name):
    """Elimina un nodo del organigrama y limpia sus relaciones (from/to)."""
    frappe.db.delete("OS Org Relation", {"from_node": name})
    frappe.db.delete("OS Org Relation", {"to_node": name})
    frappe.delete_doc("OS Org Node", name, ignore_permissions=True, force=True)
    return {"ok": 1}


@frappe.whitelist(methods=["POST"])
def delete_org_relation(name):
    """Elimina una conexión (OS Org Relation) del organigrama."""
    frappe.delete_doc("OS Org Relation", name, ignore_permissions=True, force=True)
    return {"ok": 1}


@frappe.whitelist(methods=["GET", "POST"])
def add_org_relation(from_node=None, to_node=None, relation_type=None):
    """Crea una conexión entre dos nodos (idempotente)."""
    if not from_node or not to_node or from_node == to_node:
        return {"error": "Selecciona dos nodos distintos."}
    exists = frappe.db.exists("OS Org Relation", {"from_node": from_node, "to_node": to_node})
    if exists:
        return {"name": exists}
    d = frappe.get_doc({
        "doctype": "OS Org Relation",
        "from_node": from_node,
        "to_node": to_node,
        "relation_type": relation_type or "REPORTS_TO",
    })
    d.flags.ignore_permissions = True
    d.insert(ignore_permissions=True)
    return {"name": d.name}


@frappe.whitelist(methods=["POST"])
def add_process_edge(name, source_step_key=None, target_step_key=None, relation_type=None):
    """Agrega una conexión entre dos pasos (idempotente)."""
    d = frappe.get_doc("OS Process", name)
    keys = {s.step_key for s in d.get("steps", [])}
    if source_step_key not in keys or target_step_key not in keys:
        return {"error": "Los pasos no pertenecen a este proceso."}
    exists = any(e.source_step_key == source_step_key and e.target_step_key == target_step_key for e in d.get("edges", []))
    if exists:
        return {"ok": 1}
    d.append("edges", {
        "edge_key": frappe.generate_hash(length=8),
        "source_step_key": source_step_key,
        "target_step_key": target_step_key,
        "relation_type": relation_type or "NEXT",
    })
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"ok": 1}


@frappe.whitelist(methods=["POST"])
def delete_process_edge(name, source_step_key=None, target_step_key=None):
    """Elimina una conexión entre dos pasos."""
    d = frappe.get_doc("OS Process", name)
    d.set("edges", [e for e in d.get("edges", []) if not (e.source_step_key == source_step_key and e.target_step_key == target_step_key)])
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"ok": 1}


@frappe.whitelist(methods=["POST"])
def save_process_step_position(name, step_key=None, x=None, y=None):
    """Guarda la posición de un paso en el lienzo."""
    d = frappe.get_doc("OS Process", name)
    for s in d.get("steps", []):
        if s.step_key == step_key:
            s.x = float(x or 0)
            s.y = float(y or 0)
            break
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"ok": 1}
