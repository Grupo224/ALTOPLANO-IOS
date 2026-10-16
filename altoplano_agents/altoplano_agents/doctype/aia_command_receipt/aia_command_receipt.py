import frappe
from frappe.model.document import Document


class AIACommandReceipt(Document):
    """Recibo durable de comandos UI. command_key es único (reintento idempotente)."""
    pass

