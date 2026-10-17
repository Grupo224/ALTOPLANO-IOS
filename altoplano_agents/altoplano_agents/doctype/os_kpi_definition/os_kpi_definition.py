import frappe
from frappe.model.document import Document


class OSKPIDefinition(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		entity_type: DF.Literal["Company", "Process", "Step", "Agent", "Connector"]
		formula: DF.SmallText | None
		frequency: DF.Data | None
		kpi_code: DF.Data | None
		kpi_title: DF.Data
		owner_user: DF.Link | None
		source: DF.Data | None
		threshold_critical: DF.Data | None
		threshold_warning: DF.Data | None
	# end: auto-generated types
	pass
