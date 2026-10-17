from frappe.model.document import Document

class ASBudgetLedger(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agent: DF.Link
        amount: DF.Currency
        deduplication_key: DF.Data | None
        execution: DF.Link
        kind: DF.Literal["Reserve", "Settle", "Release"]
        period: DF.Data
    # end: auto-generated types
    pass
