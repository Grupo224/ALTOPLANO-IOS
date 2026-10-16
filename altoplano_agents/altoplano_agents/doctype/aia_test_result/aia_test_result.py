# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIATestResult(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link
		company: DF.Link
		connection_versions_json: DF.Code
		execution_mode: DF.Literal["Mock", "Sandbox", "LiveReadOnly", "Live"]
		policy_hash: DF.Data
		revision: DF.Link
		scenario: DF.Data
		status: DF.Literal["Pass", "Fail", "Blocked"]
		summary: DF.SmallText
		tested_at: DF.Datetime
		tested_by: DF.Link
		trace_id: DF.Data
	# end: auto-generated types
	pass
