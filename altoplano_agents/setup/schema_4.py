# Child tables canónicas (33-40). istable=1.
SCHEMA_4 = [
{
 "name": "AIA Allowed Agent", "istable": 1,
 "fields": [
  ("agent", "Agente", "Link", "AIA Agent", 1, "User"),
 ],
},
{
 "name": "AIA Skill Assignment", "istable": 1,
 "fields": [
  ("skill", "Habilidad", "Link", "AIA Skill", 1, "User"),
  ("skill_version", "Versión fijada", "Data", None, 1, "Server"),
  ("enabled", "Activa", "Check", None, 1, "User"),
  ("parameters_json", "Parámetros", "Code", None, 0, "User"),
 ],
},
{
 "name": "AIA Tool Grant", "istable": 1,
 "fields": [
  ("tool", "Herramienta", "Link", "AIA Tool Definition", 1, "User"),
  ("access_level", "Nivel", "Select", "Read\nCreateDraft\nExecuteScoped", 1, "User"),
  ("requires_approval", "Requiere aprobación", "Check", None, 1, "Server"),
  ("scope_json", "Alcance", "Code", None, 1, "User"),
  ("max_calls_per_run", "Máximo por ejecución", "Int", None, 1, "User"),
 ],
},
{
 "name": "AIA Source Assignment", "istable": 1,
 "fields": [
  ("source", "Fuente", "Link", "AIA Knowledge Source", 1, "User"),
  ("version_policy", "Versión", "Select", "Pinned\nLiveAuthorized", 1, "User"),
  ("source_version", "Versión fijada", "Data", None, 0, "Server"),
 ],
},
{
 "name": "AIA Source Access", "istable": 1,
 "fields": [
  ("principal_type", "Tipo", "Select", "User\nRole", 1, "Admin"),
  ("principal", "Principal", "Dynamic Link", "principal_type", 1, "Admin"),
 ],
},
{
 "name": "AIA Rate Line", "istable": 1,
 "fields": [
  ("metric_key", "Métrica", "Select", "InputTokens\nOutputTokens\nCachedReadTokens\nCacheWriteTokens\nAudioSeconds\nMessages\nRequests\nStorageGBMonth", 1, "Admin"),
  ("unit_basis", "Unidades por tarifa", "Int", None, 1, "Admin"),
  ("unit_price", "Precio por unidad de tarifa", "Currency", "currency", 1, "Admin"),
  ("currency", "Moneda", "Link", "Currency", 1, "Server"),
  ("condition_json", "Condiciones", "Code", None, 0, "Admin"),
 ],
},
{
 "name": "AIA Reservation Allocation", "istable": 1,
 "fields": [
  ("bucket", "Presupuesto del período", "Link", "AIA Budget Bucket", 1, "Server"),
  ("amount", "Importe", "Currency", "base_currency", 1, "Server"),
  ("base_currency", "Moneda", "Link", "Currency", 1, "Server"),
 ],
},
{
 "name": "AIA Billing Line", "istable": 1,
 "fields": [
  ("usage_event", "Evento local", "Link", "AIA Usage Event", 0, "Server"),
  ("event_key", "Referencia de consumo", "Data", None, 1, "Server"),
  ("service_item", "Servicio ERP", "Link", "Item", 1, "Admin"),
  ("qty", "Cantidad", "Float", None, 1, "Server"),
  ("uom", "Unidad", "Link", "UOM", 1, "Admin"),
  ("rate", "Tarifa", "Currency", "currency", 1, "Server"),
  ("amount", "Importe", "Currency", "currency", 1, "Server"),
  ("currency", "Moneda", "Link", "Currency", 1, "Server"),
  ("pricing_snapshot_json", "Detalle de precio", "Code", None, 1, "Server"),
  ("billing_key", "Clave de cobro", "Data", None, 1, "Server"),
 ],
},
]
