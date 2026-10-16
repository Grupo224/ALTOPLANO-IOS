# Cerebro

Cerebro es el chat central de Altoplano IA Agents: permite consultar el ERP y
ejecutar acciones autorizadas desde la propia Custom App, con confirmación
explícita y auditoría para escrituras.

## Principios

- **Identidad real:** usa `frappe.session.user`; nunca actúa como administrador omnipotente.
- **Separación consulta/escritura:** las lecturas se resuelven al momento; las
  escrituras se proponen con vista previa y requieren aprobación.
- **Sin SQL arbitrario:** solo servicios aprobados y consultas acotadas por permiso.
- **Anti prompt-injection:** todo texto de documentos, canales o herramientas se
  trata como no confiable.

## Flujo

1. `cerebro.start` crea (o reutiliza) una `AIA Conversation` con alcance autorizado.
2. `cerebro.ask` clasifica la intención:
   - **Consulta** → ejecuta herramientas `Read` y devuelve documentos reales.
   - **Acción** → devuelve una propuesta con `actions` y espera confirmación.
3. El usuario confirma (`execute: true`) y el backend ejecuta la escritura,
   registrando el tool call y su consumo en `AIA Usage Event`.

## Límites de autorización

- Escrituras financieras, permisos, borrado, mensajes masivos o cambios de
  infraestructura exigen autorización adicional.
- Cada `AIA Tool Definition` declara un `risk` (`Read`, `ReversibleWrite`,
  `SensitiveWrite`, `Irreversible`).
- La idempotencia se garantiza con `AIA Command Receipt` (`command_key`).

## Consumo

Cada ejecución registra `AIA Usage Event` (modelo, tokens, costo estimado) contra
el presupuesto de `AIA Settings` / `AIA Access Profile`, con reserva atómica en
`services/budgets.py`.

## Estado

- Lectura (`search_customers`) y escrituras ERP (`create_followup`,
  `create_lead`, `create_quotation_draft`) implementadas y verificadas contra
  ERPNext.
- Conectores externos (WhatsApp, Chatwoot, Mautic, servicios IA) requieren
  credenciales del cliente: quedan **Pending** hasta que se provean.
