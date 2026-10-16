# Autorización central de Altoplano IA Agents.
# La visibilidad de la app y el alcance por Company se resuelven aquí.

import frappe

APP_ROLE = "AIA User"
ADMIN_ROLES = {"AIA Manager", "AIA Technical Admin"}


def _roles():
    return set(frappe.get_all("Has Role", filters={"parent": frappe.session.user}, pluck="role"))


def can_access_app():
    """Hook add_to_apps_screen: decide si la app es visible para este usuario."""
    if frappe.session.user == "Guest":
        return False
    enabled = frappe.db.get_value("User", frappe.session.user, "enabled")
    if not enabled:
        return False
    roles = _roles()
    app_roles = {
        APP_ROLE, "AIA Owner", "AIA Manager", "AIA Operator", "AIA Reviewer",
        "AIA Viewer", "AIA Billing Manager", "AIA Technical Admin",
        "AIA Provisioner", "AIA Runtime Service",
    }
    return bool(roles & app_roles)


def _allowed_companies():
    """Compañías donde el usuario tiene perfil de acceso habilitado."""
    roles = _roles()
    if roles & ADMIN_ROLES or "System Manager" in roles:
        profiles = frappe.get_all(
            "AIA Access Profile", filters={"user": frappe.session.user, "enabled": 1}, pluck="company"
        )
        if profiles:
            return set(profiles)
        settings = frappe.get_single("AIA Settings")
        return {settings.default_company} if settings.default_company else set()
    return set(
        frappe.get_all(
            "AIA Access Profile", filters={"user": frappe.session.user, "enabled": 1}, pluck="company"
        )
    )


def _in_list(companies):
    return ", ".join(frappe.db.escape(c) for c in companies)


def agent_query_conditions(user=None):
    if "System Manager" in _roles():
        return ""
    companies = _allowed_companies()
    if not companies:
        return "1=0"
    return "tabAIA Agent.company in ({})".format(_in_list(companies))


def conversation_query_conditions(user=None):
    if "System Manager" in _roles():
        return ""
    companies = _allowed_companies()
    if not companies:
        return "1=0"
    return "tabAIA Conversation.company in ({})".format(_in_list(companies))


def message_query_conditions(user=None):
    if "System Manager" in _roles():
        return ""
    companies = _allowed_companies()
    if not companies:
        return "1=0"
    return "tabAIA Message.company in ({})".format(_in_list(companies))


def has_agent_permission(doc, ptype=None, user=None):
    if "System Manager" in _roles():
        return True
    return doc.company in _allowed_companies()


def has_conversation_permission(doc, ptype=None, user=None):
    if "System Manager" in _roles():
        return True
    return doc.company in _allowed_companies()


def has_message_permission(doc, ptype=None, user=None):
    if "System Manager" in _roles():
        return True
    return doc.company in _allowed_companies()
