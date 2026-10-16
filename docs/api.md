# API v1 — Altoplano IA Agents

Todos los endpoints son `@frappe.whitelist` (POST salvo `boot` que es GET) y
corren con la sesión y permisos del usuario actual.

## Módulos

| Módulo | Endpoints |
|---|---|
| `boot` | `boot` |
| `dashboard` | `dashboard` |
| `business` | `get_profile`, `save_profile` |
| `catalog` | `templates`, `skills`, `tools` |
| `agents` | `list_agents`, `get_agent`, `create_agent`, `update_agent`, `create_revision` |
| `connections` | `list_connections`, `create_connection` |
| `conversations` | `list_conversations`, `get_messages`, `handoff` |
| `approvals` | `list_approvals`, `decide` |
| `usage` | `summary`, `events` |
| `erp` | `activity` |
| `cerebro` | `start`, `ask` |

## Autorización

- `services/context.py` resuelve la Company autorizada (`allowed_companies`).
- `permissions.py` aplica condiciones por Company a los DocTypes (`query_conditions`)
  y validación por documento (`has_*_permission`).
- El frontend nunca envía `company`, `owner` o roles como autoridad; el backend decide.
