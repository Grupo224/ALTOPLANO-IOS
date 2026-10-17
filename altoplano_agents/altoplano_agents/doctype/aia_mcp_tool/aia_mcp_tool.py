import frappe
from frappe.model.document import Document


class AIAMCPTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		annotations_json: DF.Code | None
		approved_schema_hash: DF.Data | None
		company: DF.Link
		description: DF.Text | None
		display_title: DF.Data | None
		enabled: DF.Check
		input_schema_json: DF.Code
		last_seen_at: DF.Datetime
		mcp_server: DF.Link
		observed_schema_hash: DF.Data
		output_schema_json: DF.Code | None
		remote_name: DF.Data
		requires_approval: DF.Check
		review_status: DF.Literal["Pending; Approved; Changed; Blocked; Retired"]
		reviewed_at: DF.Datetime | None
		reviewed_by: DF.Link | None
		risk_level: DF.Literal["Read; Write; Destructive; ExternalMessage; Financial"]
		tool_definition: DF.Link | None
	# end: auto-generated types
	pass
