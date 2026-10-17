import frappe
from frappe.model.document import Document


class OSRoleCard(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		competencies: DF.TextEditor | None
		designation: DF.Link | None
		expected_results: DF.SmallText | None
		functions: DF.TextEditor | None
		kpis: DF.SmallText | None
		mission: DF.SmallText | None
		objectives: DF.TextEditor | None
		org_node: DF.Link | None
		owner_user: DF.Link | None
		process_refs: DF.SmallText | None
		purpose: DF.SmallText | None
		responsibilities: DF.TextEditor | None
		role_title: DF.Data
		sop_refs: DF.SmallText | None
		tools: DF.SmallText | None
	# end: auto-generated types
	pass
