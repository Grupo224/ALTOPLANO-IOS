from frappe.model.document import Document

class ASConnector(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        email_account: DF.Link | None
        enabled: DF.Check
        endpoint: DF.Data | None
        graph_api_version: DF.Data | None
        kind: DF.Literal["MCP", "WhatsApp", "Email", "ERPNext", "OpenClaw"]
        phone_number_id: DF.Data | None
        secret_reference: DF.Data | None
        title: DF.Data
        transport: DF.Literal["Streamable HTTP", "HTTP API"]
        waba_id: DF.Data | None
    # end: auto-generated types
    pass
