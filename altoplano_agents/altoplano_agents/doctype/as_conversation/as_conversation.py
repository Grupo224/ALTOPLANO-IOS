from frappe.model.document import Document

class ASConversation(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agent: DF.Link
        channel: DF.Literal["Portal", "WhatsApp", "Email"]
        external_reference: DF.Data | None
        retention_days: DF.Int
    # end: auto-generated types
    pass
