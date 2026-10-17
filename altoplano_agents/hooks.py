app_name = "altoplano_agents"
app_title = "Altoplano IA Agents"
app_publisher = "Altoplano"
app_description = "Administra agentes de IA integrados con ERPNext"
app_email = "ia@altoplano.com"
app_license = "mit"

required_apps = ["erpnext"]

# Campos derivados por servidor en Event nativo (agenda de agentes).
custom_fields = {
	"Event": [
		{"fieldname": "custom_aia_company", "label": "Empresa AIA", "fieldtype": "Link", "options": "Company", "insert_after": "subject", "read_only": 1},
		{"fieldname": "custom_aia_calendar", "label": "Agenda AIA", "fieldtype": "Link", "options": "AIA Calendar", "insert_after": "custom_aia_company", "read_only": 1},
		{"fieldname": "custom_aia_agent", "label": "Agente AIA", "fieldtype": "Link", "options": "AIA Agent", "insert_after": "custom_aia_calendar", "read_only": 1},
		{"fieldname": "custom_aia_appointment", "label": "Cita AIA", "fieldtype": "Link", "options": "AIA Appointment", "insert_after": "custom_aia_agent", "read_only": 1},
	],
}

add_to_apps_screen = [
	{
		"name": "altoplano_agents",
		"logo": "/assets/altoplano_agents/images/logo.svg",
		"title": "Altoplano IA Agents",
		"route": "/ai-agents",
		"has_permission": "altoplano_agents.permissions.can_access_app",
	}
]

website_route_rules = [
	{"from_route": "/ai-agents/<path:app_path>", "to_route": "ai-agents"},
]

scheduler_events = {
	"all": [
		"altoplano_agents.jobs.process_outbox",
	],
	"hourly": [
		"altoplano_agents.jobs.expire_approvals",
		"altoplano_agents.jobs.reconcile_budgets",
	],
	"daily": [
		"altoplano_agents.jobs.retire_expired_connections",
	],
}

after_install = "altoplano_agents.install.after_install"

permission_query_conditions = {
	"AIA Agent": "altoplano_agents.permissions.agent_query_conditions",
	"AIA Conversation": "altoplano_agents.permissions.conversation_query_conditions",
	"AIA Message": "altoplano_agents.permissions.message_query_conditions",
}

has_permission = {
	"AIA Agent": "altoplano_agents.permissions.has_agent_permission",
	"AIA Conversation": "altoplano_agents.permissions.has_conversation_permission",
	"AIA Message": "altoplano_agents.permissions.has_message_permission",
}

export_python_type_annotations = True
