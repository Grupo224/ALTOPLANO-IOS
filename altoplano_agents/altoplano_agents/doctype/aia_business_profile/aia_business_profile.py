# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIABusinessProfile(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		audience: DF.SmallText | None
		company: DF.Link
		config_version: DF.Int
		display_name: DF.Data
		handoff_instructions: DF.SmallText | None
		offering: DF.TextEditor
		opening_hours: DF.SmallText | None
		public_contact: DF.Data | None
		status: DF.Literal["Active", "Archived"]
		timezone: DF.Data | None
		tone: DF.Literal["Cercano", "Profesional", "Breve"]
	# end: auto-generated types
	pass
