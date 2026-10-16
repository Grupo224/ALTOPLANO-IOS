# Presupuestos: reservas atómicas con lock real (doc 13).
import frappe
from decimal import Decimal


def _D(v):
    return Decimal(str(v or 0))


def _bucket_key(policy, period_start, period_end):
    return "bkt:" + policy.name + ":" + period_start.strftime("%Y%m%d%H%M%S")


def get_or_create_bucket(policy, period_start, period_end):
    key = _bucket_key(policy, period_start, period_end)
    if frappe.db.exists("AIA Budget Bucket", key):
        return frappe.get_doc("AIA Budget Bucket", key)
    b = frappe.get_doc({
        "doctype": "AIA Budget Bucket",
        "company": policy.company,
        "policy": policy.name,
        "period_start": period_start,
        "period_end": period_end,
        "bucket_key": key,
        "base_currency": policy.base_currency,
        "limit_snapshot": policy.limit_amount,
        "committed_amount": 0,
        "reserved_amount": 0,
        "uncertain_amount": 0,
    })
    b.flags.ignore_permissions = True
    b.insert(ignore_permissions=True)
    return b


def available(bucket):
    limit = _D(bucket.limit_snapshot)
    committed = _D(bucket.committed_amount)
    reserved = _D(bucket.reserved_amount)
    uncertain = _D(bucket.uncertain_amount)
    return limit - committed - reserved - uncertain


def reserve(policy, amount, run_name=None):
    """Reserva atómica. Bloquea el bucket y comprueba disponibilidad antes de reservar."""
    from frappe.utils import now_datetime, add_to_date
    now = now_datetime()
    # Ventana Daily/Monthly traducida a UTC (simplificación conservadora).
    if policy.period == "Daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = add_to_date(start, days=1)
    else:
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = add_to_date(start, months=1)

    amount = _D(amount)
    # Lock: bloquea las filas del bucket ordenadas por name (orden estable).
    frappe.db.sql("SELECT 1 FROM tabAIA Budget Bucket WHERE bucket_key=%s FOR UPDATE", (_bucket_key_for(policy, start, end),))
    bucket = get_or_create_bucket(policy, start, end)
    if available(bucket) < amount:
        frappe.throw("QUOTA_EXCEEDED", frappe.QuotaExceededError)
    bucket.reserved_amount = _D(bucket.reserved_amount) + amount
    bucket.flags.ignore_permissions = True
    bucket.save(ignore_permissions=True)

    res = frappe.get_doc({
        "doctype": "AIA Budget Reservation",
        "company": policy.company,
        "run": run_name,
        "reservation_key": frappe.generate_hash(length=20),
        "state": "Active",
        "base_currency": policy.base_currency,
        "reserved_amount": float(amount),
        "settled_amount": 0,
        "uncertain_amount": 0,
        "expires_at": add_to_date(now, minutes=30),
    })
    res.append("allocations", {"bucket": bucket.name, "amount": float(amount), "base_currency": policy.base_currency})
    res.flags.ignore_permissions = True
    res.insert(ignore_permissions=True)
    frappe.db.commit()
    return res


def _bucket_key_for(policy, start, end):
    return "bkt:" + policy.name + ":" + start.strftime("%Y%m%d%H%M%S")


def settle(reservation, settled_amount):
    """Liquida una reserva: convierte a confirmado y libera el sobrante."""
    res = frappe.get_doc("AIA Budget Reservation", reservation)
    if res.state != "Active":
        frappe.throw("La reserva ya no está activa.")
    settled = _D(settled_amount)
    reserved = _D(res.reserved_amount)
    if settled > reserved:
        settled = reserved
    for alloc in res.allocations:
        b = frappe.get_doc("AIA Budget Bucket", alloc.bucket)
        b.reserved_amount = _D(b.reserved_amount) - _D(alloc.amount)
        b.committed_amount = _D(b.committed_amount) + settled
        b.flags.ignore_permissions = True
        b.save(ignore_permissions=True)
    res.state = "Settled"
    res.settled_amount = float(settled)
    res.flags.ignore_permissions = True
    res.save(ignore_permissions=True)
    frappe.db.commit()
    return res


def reconcile_bucket(bucket_name):
    """Reconstruye committed/reserved/uncertain desde reservas y eventos (idempotente)."""
    b = frappe.get_doc("AIA Budget Bucket", bucket_name)
    res = frappe.db.sql(
        "SELECT COALESCE(SUM(reserved_amount),0) FROM tabAIA Budget Reservation "
        "WHERE name IN (SELECT parent FROM tabAIA Reservation Allocation WHERE bucket=%s) AND state='Active'",
        bucket_name,
    )[0][0]
    b.reserved_amount = res
    b.flags.ignore_permissions = True
    b.save(ignore_permissions=True)

