import frappe
from frappe.model.document import Document


class OSOrgRelation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from_node: DF.Link
		label: DF.Data | None
		metadata: DF.Code | None
		relation_type: DF.Literal["REPORTS_TO", "COLLABORATES_WITH", "SUPPORTS", "OWNS", "APPROVES", "EXECUTES", "USES", "READS", "WRITES", "TRIGGERS", "HANDOFF_TO", "DEPENDS_ON", "MEASURES"]
		to_node: DF.Link
	# end: auto-generated types
	pass
