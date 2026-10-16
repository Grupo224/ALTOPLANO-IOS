# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAAutomation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link
		company: DF.Link
		condition_json: DF.Code | None
		enabled: DF.Check
		event_doctype: DF.Link | None
		event_name: DF.Literal["after_insert", "on_update", "on_submit"]
		execution_principal: DF.Link
		last_run: DF.Link | None
		max_runs_period: DF.Int
		next_run: DF.Datetime | None
		schedule_rule: DF.Data | None
		timezone: DF.Data
		trigger: DF.Literal["Manual", "Schedule", "DocumentEvent"]
	# end: auto-generated types
	pass
