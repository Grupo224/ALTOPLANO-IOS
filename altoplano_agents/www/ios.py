# Bootstrap de la SPA /ios (página no cacheable con sesión + CSRF).
import frappe

no_cache = 1


def get_context(context):
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/ios"
        raise frappe.Redirect

    from altoplano_agents.permissions import can_access_app
    if not can_access_app():
        frappe.local.flags.redirect_location = "/app"
        raise frappe.Redirect

    context.boot = {
        "csrf_token": frappe.sessions.get_csrf_token(),
        "user": frappe.session.user,
        "full_name": frappe.db.get_value("User", frappe.session.user, "full_name"),
    }
    return context

