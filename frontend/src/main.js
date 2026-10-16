import './style.css'
import { createApp } from 'vue'
import { FrappeUI, setConfig, frappeRequest } from 'frappe-ui'
import router from './router'
import App from './App.vue'

setConfig('resourceFetcher', frappeRequest)

// Evita pantalla en blanco silenciosa: muestra el error real si falla el arranque.
function showFatal(err) {
  const el = document.getElementById('app')
  const msg = (err && (err.message || err.reason?.message || String(err))) || 'Error desconocido'
  if (el) {
    el.innerHTML = '<div style="padding:24px;font-family:ui-sans-serif,system-ui,sans-serif;color:#b91c1c;background:#fff;min-height:100vh"><b style="font-size:16px">Error al cargar Altoplano IA Agents</b><pre style="white-space:pre-wrap;margin-top:8px;font-size:13px">' + msg.replace(/</g,'&lt;') + '</pre><p style="margin-top:12px;color:#6b7280;font-size:13px">Recarga con Ctrl+Shift+R. Si persiste, repórtalo.</p></div>'
  }
}
window.addEventListener('error', (e) => showFatal(e.error || e))
window.addEventListener('unhandledrejection', (e) => showFatal(e.reason || e))

const app = createApp(App)
app.use(FrappeUI)
app.use(router)
app.config.errorHandler = (err) => showFatal(err)
app.mount('#app')
