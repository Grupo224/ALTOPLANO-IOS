from frappe.model.document import Document

class ASApproval(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        action_hash: DF.Data
        approver: DF.Link
        decided_at: DF.Datetime | None
        execution: DF.Link
        expires_at: DF.Datetime | None
        status: DF.Literal["Pending", "Approved", "Rejected", "Expired"]
    # end: auto-generated types
    pass
