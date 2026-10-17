import frappe
from frappe.model.document import Document


class AIAToolCall(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        approval_request: DF.Link | None
        argument_hash: DF.Data
        arguments_json: DF.Code
        arguments_redacted_json: DF.Code
        company: DF.Link
        error_code: DF.Data | None
        execution_actor: DF.Link
        finished_at: DF.Datetime | None
        operation_key: DF.Data
        result_summary: DF.SmallText | None
        run: DF.Link
        started_at: DF.Datetime | None
        status: DF.Literal["PendingApproval", "Queued", "Running", "Succeeded", "Failed", "Unknown", "Denied"]
        target_doctype: DF.Link | None
        target_name: DF.DynamicLink | None
        tool: DF.Link
    # end: auto-generated types
    def validate(self):
        if self.is_new() and not self.get("operation_key"):
            frappe.throw("operation_key es obligatoria y única.")
        if self.is_new() and not self.get("status"):
            self.status = "Queued"

