import frappe
from frappe.model.document import Document


class AIAAgentRevision(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        agent: DF.Link
        based_on_revision: DF.Link | None
        company: DF.Link
        created_at: DF.Datetime
        created_by: DF.Link
        manifest_hash: DF.Data
        manifest_json: DF.Code
        manifest_schema: DF.Data
        revision_no: DF.Int
        template_version: DF.Data | None
    # end: auto-generated types
    """Instantánea inmutable: no se permite reescribir una revisión existente."""

    def on_update(self):
        if not self.is_new() and self.get_doc_before_save():
            prev = self.get_doc_before_save()
            immutable = {"manifest_json", "manifest_hash", "agent", "revision_no", "created_by", "created_at"}
            for f in immutable:
                if prev.get(f) != self.get(f):
                    frappe.throw("La revisión es inmutable: no se puede modificar " + f)

