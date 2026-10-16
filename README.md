# Altoplano IA Agents

Custom App de Grupo Altoplano sobre Frappe Framework / ERPNext para administrar
agentes de IA integrados a los datos, permisos y procesos reales de ERPNext.

**Frontend:** Vue 3 + Vite + Frappe UI (experiencia tipo Frappe CRM) en `/ai-agents`.
**Backend:** DocTypes propios + API v1 (`@frappe.whitelist`) + servicios autorizados.

## Instalación

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench --site SITE install-app altoplano_agents
# compilar frontend
cd apps/altoplano_agents/frontend && npm install && npm run build
```

## Dominio de datos

40 DocTypes en el módulo `Altoplano Agents` (`custom=0`), 10 roles `AIA *`,
y catálogo de herramientas sembrado en `AIA Tool Definition`:

- `erp.search_customers`
- `erp.create_followup`
- `erp.create_lead`
- `erp.create_quotation_draft`

## Cerebro

Chat de la app para consultar el ERP y ejecutar acciones autorizadas. Ver
[docs/cerebro.md](docs/cerebro.md).

## API v1

`altoplano_agents.api.v1.*` — `boot`, `dashboard`, `business`, `catalog`,
`agents`, `connections`, `conversations`, `approvals`, `usage`, `erp`, `cerebro`.
Ver [docs/api.md](docs/api.md).

## Pruebas

```bash
bench --site SITE run-tests --app altoplano_agents
```

## License

mit
