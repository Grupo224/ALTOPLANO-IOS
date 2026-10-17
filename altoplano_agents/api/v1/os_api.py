import json

import frappe


@frappe.whitelist(methods=["GET", "POST"])
def get_process(name):
    d = frappe.get_doc("OS Process", name)
    return {
        "name": d.name,
        "process_title": d.process_title,
        "status": d.status,
        "steps": [{"name": s.name, "step_key": s.step_key, "step_title": s.step_title, "step_type": s.step_type, "x": float(s.x or 0), "y": float(s.y or 0)} for s in d.get("steps", [])],
        "edges": [{"name": e.name, "source_step_key": e.source_step_key, "target_step_key": e.target_step_key, "relation_type": e.relation_type} for e in d.get("edges", [])],
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
