# Jobs de scheduler de Altoplano IA Agents.

import frappe


def process_outbox():
    now = frappe.utils.now_datetime()
    events = frappe.get_all(
        "AIA Outbox Event",
        filters={"state": ["in", ["Queued", "Failed"]], "next_attempt": ["<=", now]},
        order_by="creation",
        limit_page_length=50,
        pluck="name",
    )
    for name in events:
        frappe.enqueue(
            "altoplano_agents.services.outbox.deliver_event",
            event_name=name,
            queue="long",
            timeout=300,
            job_id="aia-outbox-" + name,
        )


def expire_approvals():
    now = frappe.utils.now_datetime()
    frappe.db.sql(
        "UPDATE tabAIA Approval Request SET status='Expired' WHERE status='Pending' AND expires_at < %(now)s",
        {"now": now},
    )


def reconcile_budgets():
    for bucket in frappe.get_all("AIA Budget Bucket", pluck="name", order_by="period_start"):
        frappe.enqueue(
            "altoplano_agents.services.budgets.reconcile_bucket",
            bucket_name=bucket,
            queue="long",
            timeout=300,
            job_id="aia-reconcile-" + bucket,
        )


def retire_expired_connections():
    now = frappe.utils.now_datetime()
    frappe.db.sql(
        "UPDATE tabAIA Connection SET status='Expired' WHERE status IN ('Ready','Checking') AND expires_at < %(now)s",
        {"now": now},
    )

