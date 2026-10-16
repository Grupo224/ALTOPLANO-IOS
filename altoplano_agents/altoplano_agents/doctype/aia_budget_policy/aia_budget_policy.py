# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIABudgetPolicy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link | None
		base_currency: DF.Link
		company: DF.Link
		cost_basis: DF.Literal["SupplierCost", "CustomerCharge"]
		enabled: DF.Check
		enforcement: DF.Literal["Hard", "Soft"]
		limit_amount: DF.Currency
		max_concurrent: DF.Int
		max_duration: DF.Int
		max_tool_calls: DF.Int
		max_turns: DF.Int
		period: DF.Literal["Daily", "Monthly"]
		policy_version: DF.Int
		safety_margin_percent: DF.Percent
		scope: DF.Literal["Company", "Agent", "User"]
		timezone: DF.Data
		user: DF.Link | None
		warning_percent: DF.Percent
	# end: auto-generated types
	pass
