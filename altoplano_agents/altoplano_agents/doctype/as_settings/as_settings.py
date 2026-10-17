from frappe.model.document import Document

class ASSettings(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        gateway_credential: DF.Link | None
        gateway_url: DF.Data | None
        kill_switch: DF.Check
        retention_days: DF.Int
    # end: auto-generated types
    pass
