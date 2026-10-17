from frappe.model.document import Document

class ASCredential(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        expires_on: DF.Datetime | None
        title: DF.Data
        token: DF.Password
    # end: auto-generated types
    pass
