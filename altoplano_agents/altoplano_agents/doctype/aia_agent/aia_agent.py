import frappe
from frappe.model.document import Document


class AIAAgent(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from altoplano_agents.altoplano_agents.doctype.aia_allowed_agent.aia_allowed_agent import AIAAllowedAgent
        from altoplano_agents.altoplano_agents.doctype.aia_skill_assignment.aia_skill_assignment import AIASkillAssignment
        from altoplano_agents.altoplano_agents.doctype.aia_source_assignment.aia_source_assignment import AIASourceAssignment
        from altoplano_agents.altoplano_agents.doctype.aia_tool_grant.aia_tool_grant import AIAToolGrant
        from frappe.types import DF

        applied_revision: DF.Link | None
        audience: DF.Literal["Customer", "Internal"]
        budget_policy: DF.Link | None
        business_profile: DF.Link | None
        company: DF.Link
        configuration_hash: DF.Data | None
        context_notes: DF.TextEditor | None
        current_revision: DF.Link | None
        delegates: DF.Table[AIAAllowedAgent]
        desired_state: DF.Literal["Draft", "Active", "Paused", "Archived"]
        display_name: DF.Data
        draft_version: DF.Int
        instructions: DF.TextEditor | None
        knowledge_sources: DF.Table[AIASourceAssignment]
        last_heartbeat: DF.Datetime | None
        model_connection: DF.Link | None
        model_id: DF.Data | None
        observed_state: DF.Literal["NeedsSetup", "Validating", "Queued", "Deploying", "Active", "Degraded", "Failed", "Paused", "Suspended", "Archived"]
        owner_user: DF.Link
        skills: DF.Table[AIASkillAssignment]
        summary: DF.SmallText | None
        template: DF.Link | None
        tested_revision: DF.Link | None
        tools: DF.Table[AIAToolGrant]
    # end: auto-generated types
    def validate(self):
        self._set_company()
        if not self.get("observed_state"):
            self.observed_state = "NeedsSetup"

    def _set_company(self):
        if self.get("company"):
            return
        from altoplano_agents.services.context import resolve_company
        self.company = resolve_company(None)
        if not self.get("owner_user"):
            self.owner_user = frappe.session.user

