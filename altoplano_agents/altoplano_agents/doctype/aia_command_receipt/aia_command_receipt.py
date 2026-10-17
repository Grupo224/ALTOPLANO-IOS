import frappe
from frappe.model.document import Document


class AIACommandReceipt(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        actor: DF.Link
        command_id: DF.Data
        command_key: DF.Data
        company: DF.Link
        expires_at: DF.Datetime | None
        method: DF.Data
        payload_hash: DF.Data
        result_json: DF.Code | None
        status: DF.Literal["Processing", "Succeeded", "Failed", "Unknown"]
        trace_id: DF.Data
    # end: auto-generated types
    """Recibo durable de comandos UI. command_key es único (reintento idempotente)."""
    pass

