import frappe
from frappe.model.document import Document


class OSKPIDefinition(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		designation: DF.Link | None
		entity_type: DF.Literal["Company", "Process", "Step", "Agent", "Connector", "Position", "RoleCard"]
		formula: DF.SmallText | None
		frequency: DF.Data | None
		kpi_code: DF.Data | None
		kpi_title: DF.Data
		org_node: DF.Link | None
		owner_user: DF.Link | None
		role_card: DF.Link | None
		source: DF.Data | None
		threshold_critical: DF.Data | None
		threshold_warning: DF.Data | None
	# end: auto-generated types
	pass
