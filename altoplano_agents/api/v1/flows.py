import json

import frappe


@frappe.whitelist(methods=["GET", "POST"])
def list_flows():
    return frappe.get_all(
        "AS Flow",
        fields=["name", "title", "status", "revision", "modified"],
        order_by="modified desc",
        limit_page_length=100,
    )


@frappe.whitelist(methods=["GET", "POST"])
def get_flow(name):
    d = frappe.get_doc("AS Flow", name)
    return {
        "name": d.name, "title": d.title, "status": d.status,
        "revision": d.revision, "graph_json": d.graph_json,
    }


@frappe.whitelist(methods=["POST"])
def create_flow(title=None):
    d = frappe.get_doc({
        "doctype": "AS Flow",
        "title": title or "Nuevo flujo",
        "status": "Draft",
        "revision": 1,
        "graph_json": json.dumps({
            "schema_version": "altoplano.flow/1",
            "nodes": [{"id": "inicio", "type": "trigger", "config": {"trigger": "inbound_message"}}],
            "edges": [],
            "limits": {"max_steps": 20, "timeout_seconds": 120},
        }),
    })
    d.flags.ignore_permissions = True
    d.insert(ignore_permissions=True)
    return {"name": d.name, "title": d.title, "status": d.status, "revision": d.revision}


@frappe.whitelist(methods=["POST"])
def save_flow(name, title=None, graph_json=None, status=None):
    d = frappe.get_doc("AS Flow", name)
    if title is not None:
        d.title = title
    if status is not None:
        d.status = status
    if graph_json is not None:
        d.graph_json = graph_json if isinstance(graph_json, str) else json.dumps(graph_json)
    d.flags.ignore_permissions = True
    d.save(ignore_permissions=True)
    return {"name": d.name, "title": d.title, "status": d.status, "revision": d.revision}
