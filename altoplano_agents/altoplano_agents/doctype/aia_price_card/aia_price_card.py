# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAPriceCard(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_rate_line.aia_rate_line import AIARateLine
		from frappe.types import DF

		company: DF.Link | None
		currency: DF.Link
		effective_from: DF.Datetime
		effective_to: DF.Datetime | None
		match_dimensions: DF.Code
		model_id: DF.Data
		pricing_side: DF.Literal["Supplier", "Customer"]
		provider: DF.Data
		rate_lines: DF.Table[AIARateLine]
		service_kind: DF.Literal["LLM", "Embedding", "Audio", "Channel", "Tool", "Storage"]
		source_url: DF.Data
		status: DF.Literal["Draft", "Active", "Retired"]
		verified_at: DF.Datetime | None
		verified_by: DF.Link | None
	# end: auto-generated types
	pass
