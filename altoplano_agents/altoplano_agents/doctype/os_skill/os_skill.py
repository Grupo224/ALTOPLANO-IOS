import frappe
from frappe.model.document import Document


class OSSkill(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.SmallText | None
		inputs: DF.SmallText | None
		outputs: DF.SmallText | None
		owner_user: DF.Link | None
		reusable_by: DF.Literal["Agent", "Process", "Both"]
		skill_code: DF.Data | None
		skill_title: DF.Data
		status: DF.Literal["Draft", "Active", "Deprecated"]
	# end: auto-generated types
	pass
