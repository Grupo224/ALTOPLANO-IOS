# Resolución de contexto autorizado (company, actor) para servicios internos.

import frappe


def current_user():
    return frappe.session.user


def allowed_companies(user=None):
    """Compañías donde el usuario tiene perfil de acceso habilitado."""
    from altoplano_agents.permissions import _allowed_companies
    return _allowed_companies()


def resolve_company(company_context=None):
    """Devuelve la Company autorizada o lanza FORBIDDEN.

    company_context es una solicitud de ámbito, no autoridad.
    """
    companies = allowed_companies()
    if not companies:
        frappe.throw("No tienes acceso a ninguna empresa.", frappe.PermissionError)
    if company_context:
        if company_context not in companies:
            frappe.throw("No tienes acceso a esa empresa.", frappe.PermissionError)
        return company_context
    if len(companies) == 1:
        return next(iter(companies))
    settings = frappe.get_single("AIA Settings")
    if settings.default_company in companies:
        return settings.default_company
    return next(iter(companies))

