import frappe
from frappe.model.document import Document


class AIACalendar(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from altoplano_agents.altoplano_agents.doctype.aia_availability_window.aia_availability_window import AIAAvailabilityWindow
		from altoplano_agents.altoplano_agents.doctype.aia_calendar_exception.aia_calendar_exception import AIACalendarException
		from frappe.types import DF

		agent: DF.Link | None
		availability: DF.Table[AIAAvailabilityWindow]
		booking_horizon_days: DF.Int
		buffer_after_minutes: DF.Int
		buffer_before_minutes: DF.Int
		company: DF.Link
		config_version: DF.Int
		display_name: DF.Data
		enabled: DF.Check
		exceptions: DF.Table[AIACalendarException]
		max_bookings_per_day: DF.Int
		minimum_notice_minutes: DF.Int
		native_google_calendar: DF.Link | None
		owner_user: DF.Link
		slot_minutes: DF.Int
		slot_step_minutes: DF.Int
		sync_mode: DF.Literal["LocalOnly", "NativeGoogle"]
		timezone: DF.Data
	# end: auto-generated types
	pass
