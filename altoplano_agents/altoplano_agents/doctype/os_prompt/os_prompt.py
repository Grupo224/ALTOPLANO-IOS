import frappe
from frappe.model.document import Document


class OSPrompt(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		approval_policy: DF.SmallText | None
		context_template: DF.TextEditor | None
		docs: DF.Attach | None
		fallback: DF.SmallText | None
		output_schema: DF.Code | None
		owner_user: DF.Link | None
		prompt_code: DF.Data | None
		prompt_title: DF.Data
		status: DF.Literal["Draft", "Tested", "Approved", "Deprecated"]
		system_instruction: DF.TextEditor | None
		task_template: DF.Code | None
		tool_policy: DF.SmallText | None
		version_label: DF.Data | None
	# end: auto-generated types
	pass
