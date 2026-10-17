import frappe
from frappe.model.document import Document


class OSRoleCard(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		designation: DF.Link | None
		expected_results: DF.SmallText | None
		kpis: DF.SmallText | None
		mission: DF.SmallText | None
		owner_user: DF.Link | None
		responsibilities: DF.TextEditor | None
		role_title: DF.Data
	# end: auto-generated types
	pass
