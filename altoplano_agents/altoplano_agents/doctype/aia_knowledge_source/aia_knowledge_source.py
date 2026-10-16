# Copyright (c) 2026, Altoplano and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AIAKnowledgeSource(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_source_access.aia_source_access import AIASourceAccess
		from frappe.types import DF

		access_list: DF.Table[AIASourceAccess]
		approved_url: DF.Data | None
		company: DF.Link
		content_hash: DF.Data | None
		display_name: DF.Data
		error_code: DF.Data | None
		file: DF.Link | None
		index_version: DF.Data | None
		processed_at: DF.Datetime | None
		query_tool: DF.Link | None
		source_type: DF.Literal["File", "Text", "ERPQuery", "ApprovedURL"]
		status: DF.Literal["Uploaded", "Queued", "Processing", "Ready", "Failed", "Archived"]
		text_content: DF.TextEditor | None
		visibility: DF.Literal["Public", "Internal", "Restricted"]
	# end: auto-generated types
	pass
