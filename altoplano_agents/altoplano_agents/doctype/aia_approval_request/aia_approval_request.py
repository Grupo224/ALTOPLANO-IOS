import frappe
from frappe.model.document import Document


class AIAApprovalRequest(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        action_hash: DF.Data
        company: DF.Link
        consumed_at: DF.Datetime | None
        decided_at: DF.Datetime | None
        decided_by: DF.Link | None
        expected_doc_modified: DF.Datetime | None
        expires_at: DF.Datetime
        payload_snapshot_json: DF.Code
        reason: DF.SmallText | None
        reviewer: DF.Link
        run: DF.Link
        status: DF.Literal["Pending", "Approved", "Rejected", "Expired", "Invalidated", "Consumed"]
        tool_call: DF.Link
    # end: auto-generated types
    def validate(self):
        if self.is_new() and not self.get("expires_at"):
            from frappe.utils import add_to_date, now_datetime
            self.expires_at = add_to_date(now_datetime(), hours=24)

