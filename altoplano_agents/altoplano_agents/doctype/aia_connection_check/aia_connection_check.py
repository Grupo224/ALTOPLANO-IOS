import frappe
from frappe.model.document import Document


class AIAConnectionCheck(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		capability: DF.Data
		check_key: DF.Data
		company: DF.Link
		config_version: DF.Int
		connection: DF.Link
		credential_version: DF.Int
		diagnostic_code: DF.Data | None
		effect_level: DF.Literal["ReadOnly; AuthorizedSend; AuthorizedWrite"]
		evidence_json: DF.Code | None
		finished_at: DF.Datetime | None
		latency_ms: DF.Int
		provider_error_code: DF.Data | None
		requested_by: DF.Link
		started_at: DF.Datetime | None
		status: DF.Literal["Queued; Running; Pass; Fail; Blocked; Unknown"]
		summary: DF.Text
		trace_id: DF.Data
		valid_until: DF.Datetime | None
	# end: auto-generated types
	pass
