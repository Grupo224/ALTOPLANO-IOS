# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIABudgetReservation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_reservation_allocation.aia_reservation_allocation import AIAReservationAllocation
		from frappe.types import DF

		allocations: DF.Table[AIAReservationAllocation]
		base_currency: DF.Link
		company: DF.Link
		expires_at: DF.Datetime
		provider_request_id: DF.Data | None
		reservation_key: DF.Data
		reserved_amount: DF.Currency
		run: DF.Link
		settled_amount: DF.Currency
		state: DF.Literal["Active", "Settled", "Released", "Uncertain"]
		uncertain_amount: DF.Currency
	# end: auto-generated types
	pass
