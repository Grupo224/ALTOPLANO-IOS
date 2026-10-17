from frappe.model.document import Document

class ASSchedule(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        cron_expression: DF.Data | None
        enabled: DF.Check
        flow: DF.Link
        next_run: DF.Datetime | None
        timezone: DF.Data | None
        title: DF.Data
    # end: auto-generated types
    pass
