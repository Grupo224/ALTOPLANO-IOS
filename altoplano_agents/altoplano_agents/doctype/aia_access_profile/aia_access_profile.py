# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAAccessProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_allowed_agent.aia_allowed_agent import AIAAllowedAgent
		from frappe.types import DF

		agent_scope: DF.Literal["All", "Assigned"]
		allowed_agents: DF.Table[AIAAllowedAgent]
		company: DF.Link
		enabled: DF.Check
		user: DF.Link
	# end: auto-generated types
	pass
