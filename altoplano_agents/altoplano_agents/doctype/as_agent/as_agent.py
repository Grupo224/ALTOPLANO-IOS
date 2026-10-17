from frappe.model.document import Document

class ASAgent(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from altoplano_agents.altoplano_agents.doctype.as_knowledge_grant.as_knowledge_grant import ASKnowledgeGrant
        from altoplano_agents.altoplano_agents.doctype.as_tool_grant.as_tool_grant import ASToolGrant
        from frappe.types import DF

        agent_name: DF.Data
        instructions: DF.LongText | None
        knowledge: DF.Table[ASKnowledgeGrant]
        max_output_tokens: DF.Int
        model_profile: DF.Data
        monthly_budget: DF.Currency
        purpose: DF.SmallText | None
        status: DF.Literal["Draft", "Active", "Paused"]
        timeout_seconds: DF.Int
        tool_grants: DF.Table[ASToolGrant]
    # end: auto-generated types
    pass
