from frappe.model.document import Document

class ASExecution(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agent: DF.Link | None
        cost: DF.Currency
        finished_at: DF.Datetime | None
        flow: DF.Link | None
        idempotency_key: DF.Data | None
        input_tokens: DF.Int
        output_tokens: DF.Int
        redacted_error: DF.SmallText | None
        started_at: DF.Datetime | None
        status: DF.Literal["Queued", "Running", "Awaiting Approval", "Succeeded", "Failed", "Cancelled"]
    # end: auto-generated types
    pass
