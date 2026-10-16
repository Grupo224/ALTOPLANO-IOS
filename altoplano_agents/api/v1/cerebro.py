# Cerebro: chat que consulta ERP y ejecuta acciones autorizadas (con aprobación).

import json
import uuid

import frappe
from frappe import _


TOOL_PREFIX = "__cerebo_tool__"


@frappe.whitelist(methods=["GET", "POST"])
def start(company_context=None):
    """Inicia/recupera una conversación de Cerebro para el usuario actual."""
    from altoplano_agents.services.context import resolve_company
    company = resolve_company(company_context)
    scope = "cerebo:" + company + ":" + frappe.session.user
    conv = frappe.get_all(
        "AIA Conversation", filters={"company": company, "memory_scope": scope, "handler_state": ["!=", "Closed"]},
        pluck="name", limit=1, order_by="creation desc",
    )
    if not conv:
        d = frappe.get_doc({
            "doctype": "AIA Conversation",
            "company": company,
            "session_key": frappe.generate_hash(length=20),
            "memory_scope": scope,
            "audience": "Internal",
            "handler_state": "Bot",
            "last_activity": frappe.utils.now_datetime(),
        })
        d.flags.ignore_permissions = True
        d.insert(ignore_permissions=True)
        return {"conversation": d.name, "messages": []}
    name = conv[0]
    msgs = frappe.get_all(
        "AIA Message", filters={"conversation": name},
        fields=["name", "actor", "body", "created_at"], order_by="creation asc", limit_page_length=200,
    )
    return {"conversation": name, "messages": msgs}


@frappe.whitelist(methods=["POST"])
def ask(conversation, message):
    """Procesa un mensaje de Cerebro. Responde consultas Read y propone acciones que requieren aprobación."""
    from altoplano_agents.permissions import has_conversation_permission
    conv = frappe.get_doc("AIA Conversation", conversation)
    if not has_conversation_permission(conv):
        frappe.throw(_("No tienes acceso a esta conversación."), frappe.PermissionError)

    # Registrar mensaje del usuario
    m = frappe.get_doc({
        "doctype": "AIA Message",
        "company": conv.company,
        "conversation": conv.name,
        "actor": "User",
        "direction": "Inbound",
        "body": message,
        "delivery_state": "Delivered",
        "event_key": frappe.generate_hash(length=20),
        "created_at": frappe.utils.now_datetime(),
    })
    m.flags.ignore_permissions = True
    m.insert(ignore_permissions=True)

    reply = _route(message, conv)
    r = frappe.get_doc({
        "doctype": "AIA Message",
        "company": conv.company,
        "conversation": conv.name,
        "actor": "Agent",
        "direction": "Outbound",
        "body": reply,
        "delivery_state": "Delivered",
        "event_key": frappe.generate_hash(length=20),
        "created_at": frappe.utils.now_datetime(),
    })
    r.flags.ignore_permissions = True
    r.insert(ignore_permissions=True)

    conv.last_activity = frappe.utils.now_datetime()
    conv.flags.ignore_permissions = True
    conv.save(ignore_permissions=True)

    return {"reply": reply, "conversation": conv.name}


def _route(message, conv):
    """Router determinista de Cerebro. Sin LLM conectado: responde con acciones reales disponibles."""
    text = (message or "").strip().lower()

    # Consulta de clientes (Read)
    if any(k in text for k in ("cliente", "clientes", "buscar cliente")):
        from altoplano_agents.services.erp import search_customers
        q = _extract_query(text)
        rows = search_customers({"query": q}, actor=frappe.session.user)
        if not rows:
            return "No encontré clientes" + ((" para " + q) if q else "") + ". Escribe un nombre, teléfono o correo."
        lines = ["Clientes encontrados:"]
        for c in rows[:5]:
            lines.append("• " + (c.customer_name or c.name) + ((" — " + (c.mobile_no or c.email_id)) if (c.mobile_no or c.email_id) else ""))
        return "\n".join(lines)

    # Propuesta de acción que requiere aprobación (SensitiveWrite)
    if "cotización" in text or "cotizacion" in text:
        return "Puedo crear una cotización en borrador, pero requiere tu aprobación. Indícame el cliente y los ítems (código y cantidad) y te pediré confirmar antes de guardar."

    if "prospecto" in text or "crear lead" in text:
        return "Puedo crear un prospecto (Lead). Dime el nombre y los datos de contacto, y te pediré confirmación antes de guardarlo."

    if "seguimiento" in text or "tarea" in text:
        return "Puedo crear un seguimiento (ToDo). Dime la tarea y a quién asignarla, y te pediré confirmación antes de crearlo."

    if any(k in text for k in ("hola", "buenos días", "buenas tardes", "ayuda")):
        return "Hola. Soy Cerebro, tu asistente de Altoplano IA Agents. Puedo buscar clientes, crear seguimientos, prospectos y cotizaciones en borrador. ¿Qué necesitas?"

    return "Entiendo tu mensaje, pero aún no tengo un modelo de IA conectado para responderlo. Mientras tanto puedo ayudarte con: buscar clientes, crear seguimientos, prospectos y cotizaciones en borrador."


def _extract_query(text):
    for k in ("cliente ", "clientes ", "buscar cliente "):
        if k in text:
            return text.split(k, 1)[1].strip()
    return ""

