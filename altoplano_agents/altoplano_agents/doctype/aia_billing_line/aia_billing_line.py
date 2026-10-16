# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIABillingLine(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount: DF.Currency
		billing_key: DF.Data
		currency: DF.Link
		event_key: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		pricing_snapshot_json: DF.Code
		qty: DF.Float
		rate: DF.Currency
		service_item: DF.Link
		uom: DF.Link
		usage_event: DF.Link | None
	# end: auto-generated types
	pass
