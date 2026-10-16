import json
import uuid

import frappe
from frappe import _


def _get(agent_name):
    from altoplano_agents.permissions import has_agent_permission
    doc = frappe.get_doc("AIA Agent", agent_name)
    if not has_agent_permission(doc):
        frappe.throw(_("No tienes acceso a este agente."), frappe.PermissionError)
    return doc


def _dto(doc):
    return {
        "name": doc.name,
        "display_name": doc.display_name,
        "summary": doc.summary,
        "audience": doc.audience,
        "company": doc.company,
        "observed_state": doc.observed_state,
        "desired_state": doc.desired_state,
        "modified": str(doc.modified),
        "model_id": doc.model_id,
    }


@frappe.whitelist(methods=["GET", "POST"])
def list_agents(company_context=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    names = frappe.get_all(
        "AIA Agent",
        filters={"company": company},
        fields=["name"],
        order_by="modified desc",
    )
    return [_dto(frappe.get_doc("AIA Agent", n.name)) for n in names]


@frappe.whitelist(methods=["GET", "POST"])
def get_agent(agent):
    return _dto(_get(agent))


@frappe.whitelist(methods=["POST"])
def create_agent(company_context=None, display_name=None, summary=None, audience=None, template=None, instructions=None):
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    if template:
        template_name = frappe.db.get_value("AIA Agent Template", {"slug": template}, "name")
        template = template_name or None
    doc = frappe.get_doc({
        "doctype": "AIA Agent",
        "company": company,
        "display_name": display_name or "Nuevo agente",
        "summary": summary,
        "audience": audience or "Customer",
        "template": template,
        "instructions": instructions,
        "desired_state": "Draft",
        "owner_user": frappe.session.user,
        "draft_version": 0,
    })
    doc.flags.ignore_permissions = True
    doc.insert(ignore_permissions=True)
    return _dto(doc)


@frappe.whitelist(methods=["POST"])
def update_agent(agent, display_name=None, summary=None, audience=None, instructions=None, context_notes=None):
    doc = _get(agent)
    if display_name is not None:
        doc.display_name = display_name
    if summary is not None:
        doc.summary = summary
    if audience is not None:
        doc.audience = audience
    if instructions is not None:
        doc.instructions = instructions
    if context_notes is not None:
        doc.context_notes = context_notes
    doc.flags.ignore_permissions = True
    doc.save(ignore_permissions=True)
    return _dto(doc)


@frappe.whitelist(methods=["POST"])
def create_revision(agent):
    """Crea una revisión inmutable del borrador actual."""
    doc = _get(agent)
    import hashlib
    manifest = {
        "agent": doc.name,
        "display_name": doc.display_name,
        "summary": doc.summary,
        "audience": doc.audience,
        "instructions": doc.instructions,
        "context_notes": doc.context_notes,
        "model_id": doc.model_id,
    }
    payload = json.dumps(manifest, sort_keys=True, ensure_ascii=False, default=str)
    revision_no = (doc.draft_version or 0) + 1
    rev = frappe.get_doc({
        "doctype": "AIA Agent Revision",
        "company": doc.company,
        "agent": doc.name,
        "revision_no": revision_no,
        "manifest_schema": "1",
        "manifest_json": payload,
        "manifest_hash": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "created_by": frappe.session.user,
        "created_at": frappe.utils.now_datetime(),
    })
    rev.flags.ignore_permissions = True
    rev.insert(ignore_permissions=True)
    doc.draft_version = revision_no
    doc.current_revision = rev.name
    doc.flags.ignore_permissions = True
    doc.save(ignore_permissions=True)
    return {"name": rev.name, "revision_no": revision_no, "manifest_hash": rev.manifest_hash}

