# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIASkill(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_tool_grant.aia_tool_grant import AIAToolGrant
		from frappe.types import DF

		company: DF.Link | None
		company_scope_key: DF.Data
		digest: DF.Data | None
		display_name: DF.Data
		instructions: DF.TextEditor | None
		kind: DF.Literal["Instruction", "ReviewedPackage"]
		package_ref: DF.Data | None
		provenance: DF.SmallText
		required_tools: DF.Table[AIAToolGrant]
		reviewed_by: DF.Link | None
		runtime_version_constraint: DF.Data | None
		slug: DF.Data
		status: DF.Literal["Draft", "Published", "Retired"]
		version: DF.Data
	# end: auto-generated types
	pass
