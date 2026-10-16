# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAAgentTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_skill_assignment.aia_skill_assignment import AIASkillAssignment
		from altoplano_agents.altoplano_agents.doctype.aia_tool_grant.aia_tool_grant import AIAToolGrant
		from frappe.types import DF

		audience: DF.Literal["Customer", "Internal"]
		company: DF.Link | None
		company_scope_key: DF.Data
		display_name: DF.Data
		instructions: DF.TextEditor
		published_at: DF.Datetime | None
		purpose: DF.SmallText
		reviewed_by: DF.Link | None
		skills: DF.Table[AIASkillAssignment]
		slug: DF.Data
		status: DF.Literal["Draft", "Published", "Retired"]
		tools: DF.Table[AIAToolGrant]
		version: DF.Data
	# end: auto-generated types
	pass
