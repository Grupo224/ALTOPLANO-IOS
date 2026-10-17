from frappe.model.document import Document

class ASKnowledge(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        content: DF.LongText | None
        enabled: DF.Check
        kind: DF.Literal["Context", "Skill"]
        revision: DF.Int
        title: DF.Data
    # end: auto-generated types
    pass
