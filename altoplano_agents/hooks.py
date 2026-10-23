app_name = "altoplano_agents"
app_title = "IOS"
app_publisher = "Altoplano"
app_description = "LivingOrg OS: sistema operativo vivo de tu empresa"
app_email = "ia@altoplano.com"
app_license = "mit"

required_apps = ["erpnext"]

add_to_apps_screen = [
	{
		"name": "altoplano_agents",
		"logo": "/assets/altoplano_agents/images/logo.svg",
		"title": "IOS",
		"route": "/ios",
		"has_permission": "altoplano_agents.permissions.can_access_app",
	}
]

website_route_rules = [
	{"from_route": "/ios/<path:app_path>", "to_route": "ios"},
]

after_install = "altoplano_agents.install.after_install"

# ===== LivingOrg OS runtime (portado de livingorg_bridge) =====
# Reglas críticas que no deben depender del navegador.
doc_events = {
	"OS Process": {
		"validate": "altoplano_agents.bridge.governance.validate_process",
	},
	"OS Org Relation": {
		"validate": "altoplano_agents.bridge.governance.validate_org_relation",
	},
	"OS Step Run": {
		"validate": "altoplano_agents.bridge.governance.validate_step_run",
	},
	"OS Approval": {
		"validate": "altoplano_agents.bridge.events.validate_approval",
	},
	"OS Evidence": {
		"validate": "altoplano_agents.bridge.governance.validate_evidence",
	},
}

# Aislamiento documental para operadores/aprobadores.
permission_query_conditions = {
	"OS Step Run": "altoplano_agents.bridge.permissions.step_run_query",
	"OS Approval": "altoplano_agents.bridge.permissions.approval_query",
	"OS Document Link": "altoplano_agents.bridge.permissions.document_link_query",
	"OS Evidence": "altoplano_agents.bridge.evidence_permissions.evidence_query",
}

has_permission = {
	"OS Step Run": "altoplano_agents.bridge.permissions.step_run_has_permission",
	"OS Approval": "altoplano_agents.bridge.permissions.approval_has_permission",
	"OS Document Link": "altoplano_agents.bridge.permissions.document_link_has_permission",
	"OS Evidence": "altoplano_agents.bridge.evidence_permissions.evidence_has_permission",
}

export_python_type_annotations = True
