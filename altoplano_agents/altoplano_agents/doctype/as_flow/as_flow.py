from frappe.model.document import Document

class ASFlow(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        graph_json: DF.Code
        revision: DF.Int
        status: DF.Literal["Draft", "Published", "Archived"]
        title: DF.Data
    # end: auto-generated types
    pass
