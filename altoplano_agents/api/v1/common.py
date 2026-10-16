# Helpers comunes de la API v1 (roles, idempotencia, DTO).
import json
import uuid

import frappe
from frappe import _


def require_app_access():
    """Niega el acceso a toda la API a usuarios sin ningún rol AIA."""
    from altoplano_agents.permissions import can_access_app
    if not can_access_app():
        frappe.throw(_("No tienes acceso a Altoplano IA Agents."), frappe.PermissionError)


def require_role(role):
    if "System Manager" in frappe.get_roles():
        return
    if role not in frappe.get_roles():
        frappe.throw(_("No tienes el rol {0}.").format(role), frappe.PermissionError)


def parse_command_id(command_id):
    if command_id:
        try:
            return str(uuid.UUID(command_id))
        except (ValueError, TypeError, AttributeError):
            frappe.throw(_("command_id inválido."), frappe.ValidationError)
    return None


def receipt_lookup(command_key):
    if not command_key:
        return None
    rows = frappe.get_all(
        "AIA Command Receipt",
        filters={"command_key": command_key},
        fields=["name", "status", "result_json"],
        limit=1,
    )
    return rows[0] if rows else None


def make_receipt(command_key, command_id, method, payload_hash, status="Processing"):
    doc = frappe.get_doc({
        "doctype": "AIA Command Receipt",
        "command_key": command_key,
        "command_id": command_id,
        "actor": frappe.session.user,
        "method": method,
        "payload_hash": payload_hash,
        "status": status,
        "trace_id": frappe.generate_hash(length=24),
    })
    doc.flags.ignore_permissions = True
    doc.insert(ignore_permissions=True)
    return doc.name


def resolve_company(company_context=None):
    from altoplano_agents.services.context import resolve_company as rc
    return rc(company_context)


def company_guard(doc, company):
    if doc.get("company") and doc.get("company") != company:
        frappe.throw(_("El documento no pertenece a tu empresa."), frappe.PermissionError)


def paginate(get_list_result):
    return get_list_result

