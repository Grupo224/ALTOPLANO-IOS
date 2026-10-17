import frappe
from frappe.model.document import Document


class AIAToolDefinition(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        adapter_key: DF.Data
        allowed_resources: DF.Code
        display_name: DF.Data
        enabled: DF.Check
        explanation: DF.SmallText
        input_schema: DF.Code
        output_schema: DF.Code
        risk: DF.Literal["Read", "ReversibleWrite", "SensitiveWrite"]
        slug: DF.Data
    # end: auto-generated types
    def validate(self):
        if self.get("adapter_key") and not frappe.db.exists("AIA Tool Definition", self.adapter_key):
            # adapter_key apunta al registro de adaptador del servidor; validado en catálogo.
            pass

