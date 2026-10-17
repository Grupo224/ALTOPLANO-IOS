import frappe
from frappe.model.document import Document


class OSOrgNode(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link | None
		company: DF.Link | None
		custom_ref: DF.Data | None
		department: DF.Link | None
		designation: DF.Link | None
		employee: DF.Link | None
		is_active: DF.Check
		node_type: DF.Literal["Company", "Department", "Designation", "Employee", "Agent", "Custom"]
		title: DF.Data
		x: DF.Float
		y: DF.Float
	# end: auto-generated types
	pass
