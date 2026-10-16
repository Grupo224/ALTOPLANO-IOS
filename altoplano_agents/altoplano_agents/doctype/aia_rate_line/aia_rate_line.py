# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIARateLine(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		condition_json: DF.Code | None
		currency: DF.Link
		metric_key: DF.Literal["InputTokens", "OutputTokens", "CachedReadTokens", "CacheWriteTokens", "AudioSeconds", "Messages", "Requests", "StorageGBMonth"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		unit_basis: DF.Int
		unit_price: DF.Currency
	# end: auto-generated types
	pass
