app_name = "altoplano_agents"
app_title = "Altoplano IA Agents"
app_publisher = "Altoplano"
app_description = "LivingOrg OS: sistema operativo vivo de tu empresa"
app_email = "ia@altoplano.com"
app_license = "mit"

required_apps = ["erpnext"]

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

after_install = "altoplano_agents.install.after_install"

export_python_type_annotations = True
