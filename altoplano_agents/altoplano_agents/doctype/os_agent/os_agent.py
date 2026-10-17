import frappe
from frappe.model.document import Document


class OSAgent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent_code: DF.Data | None
		agent_title: DF.Data
		autonomy_max: DF.Literal["L0", "L1", "L2", "L3", "L4"]
		budget_limit: DF.Data | None
		department: DF.Link | None
		docs: DF.Attach | None
		escalation_policy: DF.SmallText | None
		knowledge_sources: DF.SmallText | None
		model_policy: DF.Data | None
		output_schema: DF.Code | None
		owner_user: DF.Link | None
		prompt: DF.Link | None
		purpose: DF.SmallText | None
		skills: DF.SmallText | None
		status: DF.Literal["Draft", "Active", "Disabled"]
		tools_allowed: DF.SmallText | None
	# end: auto-generated types
	pass
