import frappe
from frappe.model.document import Document


class AIARun(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agent: DF.Link
        budget_reservation: DF.Link | None
        company: DF.Link
        conversation: DF.Link | None
        execution_mode: DF.Literal["Mock", "Sandbox", "LiveReadOnly", "Live"]
        execution_principal: DF.Link
        finished_at: DF.Datetime | None
        identity_binding: DF.Link | None
        policy_snapshot_json: DF.Code
        requested_by: DF.Link | None
        revision: DF.Link
        started_at: DF.Datetime | None
        status: DF.Literal["Queued", "Running", "WaitingApproval", "Succeeded", "Failed", "Cancelled", "TimedOut", "Unknown"]
        trace_id: DF.Data
        trigger_type: DF.Literal["Manual", "Schedule", "Event", "Channel", "Test"]
    # end: auto-generated types
    def validate(self):
        if self.is_new() and not self.get("status"):
            self.status = "Queued"
        if self.is_new() and not self.get("trace_id"):
            self.trace_id = frappe.generate_hash(length=24)

