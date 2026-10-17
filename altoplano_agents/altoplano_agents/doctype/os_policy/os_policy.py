import frappe
from frappe.model.document import Document


class OSPolicy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		docs: DF.Attach | None
		owner_user: DF.Link | None
		policy_title: DF.Data
		rules: DF.LongText | None
		scope: DF.Data | None
		status: DF.Literal["Draft", "Active", "Retired"]
	# end: auto-generated types
	pass
