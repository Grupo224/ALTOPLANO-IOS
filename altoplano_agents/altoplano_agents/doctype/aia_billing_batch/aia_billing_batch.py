# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIABillingBatch(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_billing_line.aia_billing_line import AIABillingLine
		from frappe.types import DF

		batch_key: DF.Data
		billing_mode: DF.Literal["Included", "BYOK", "PassThrough", "Managed"]
		company: DF.Link
		currency: DF.Link
		customer: DF.Link
		lines: DF.Table[AIABillingLine]
		period_from: DF.Date
		period_to: DF.Date
		sales_invoice: DF.Link | None
		status: DF.Literal["Open", "Priced", "ReadyForReview", "Invoiced", "Reconciled"]
		total: DF.Currency
	# end: auto-generated types
	pass
