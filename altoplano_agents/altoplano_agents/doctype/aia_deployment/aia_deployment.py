# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIADeployment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		agent: DF.Link
		attempt_count: DF.Int
		company: DF.Link
		desired_state: DF.Literal["Active", "Paused", "Archived"]
		error_code: DF.Data | None
		expected_applied_revision: DF.Link | None
		fencing_token: DF.Int
		finished_at: DF.Datetime | None
		lease_owner: DF.Data | None
		lease_until: DF.Datetime | None
		manifest_hash: DF.Data
		observed_revision: DF.Link | None
		request_key: DF.Data
		requested_at: DF.Datetime
		requested_by: DF.Link
		revision: DF.Link
		runtime_connection: DF.Link
		status: DF.Literal["Queued", "Applying", "Verifying", "Active", "Failed", "Paused", "Superseded"]
		trace_id: DF.Data
	# end: auto-generated types
	pass
