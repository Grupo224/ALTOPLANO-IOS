# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIABudgetBucket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		base_currency: DF.Link
		bucket_key: DF.Data
		committed_amount: DF.Currency
		company: DF.Link
		last_reconciled: DF.Datetime | None
		limit_snapshot: DF.Currency
		period_end: DF.Datetime
		period_start: DF.Datetime
		policy: DF.Link
		reserved_amount: DF.Currency
		uncertain_amount: DF.Currency
	# end: auto-generated types
	pass
