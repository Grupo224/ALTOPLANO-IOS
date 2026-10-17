<template>
  <AppLayout>
    <div class="p-6">
      <div class="mb-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold">Conexiones</h1>
          <p class="text-sm text-ink-gray-5">Canales e integraciones autorizadas de tus agentes.</p>
        </div>
        <Button variant="solid" theme="blue" label="Nueva conexión" @click="openCreate()" />
      </div>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!connections.length" class="rounded-lg border border-outline-gray-2 p-8 text-center">
        <div class="mb-2 text-sm font-medium">Sin conexiones</div>
        <div class="text-sm text-ink-gray-5">Conecta un canal para que tu agente atienda clientes.</div>
      </div>
      <div v-else class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <div v-for="c in connections" :key="c.name" class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
          <div class="mb-1 flex items-center justify-between gap-2">
            <span class="truncate text-sm font-medium">{{ c.display_name || c.name }}</span>
            <Badge :label="statusLabel(c.status)" variant="subtle" :theme="statusTheme(c.status)" />
          </div>
          <div class="text-[12px] text-ink-gray-5">{{ typeLabel(c.connection_type) }}<span v-if="c.provider"> · {{ c.provider }}</span></div>
        </div>
      </div>

      <Dialog v-model:open="showCreate" title="Nueva conexión" size="md">
        <div class="flex flex-col gap-3">
          <Select v-model="form.connection_type" label="Tipo de canal" :options="typeOptions" />
          <TextInput v-model="form.display_name" label="Nombre" placeholder="WhatsApp Atención" />
          <TextInput v-model="form.provider" label="Proveedor (opcional)" placeholder="meta_whatsapp_cloud" />
        </div>
        <template #actions="{ close }">
          <Button variant="ghost" label="Cancelar" @click="close()" />
          <Button variant="solid" theme="blue" label="Crear" :loading="saving" @click="create" />
        </template>
      </Dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, Badge, Dialog, Select, TextInput, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const connections = ref([])
const loading = ref(true)
const showCreate = ref(false)
const saving = ref(false)
const form = ref({ connection_type: 'WhatsApp', display_name: '', provider: '' })

const typeOptions = ['WhatsApp', 'Email', 'MCP', 'Chatwoot', 'Telegram', 'LLM', 'ERP', 'Runtime']

const TYPE_LABELS = { WhatsApp: 'WhatsApp Cloud', Email: 'Correo', MCP: 'MCP', Chatwoot: 'Chatwoot', Telegram: 'Telegram', LLM: 'Modelo LLM', ERP: 'ERPNext', Runtime: 'Runtime' }
const STATUS_LABELS = { PendingAuthorization: 'Pendiente', Authorized: 'Autorizada', Checking: 'Verificando', Ready: 'Lista', Expired: 'Expirada', Degraded: 'Degradada', Revoked: 'Revocada', Failed: 'Fallida' }

function typeLabel(t) { return TYPE_LABELS[t] || t || '—' }
function statusLabel(s) { return STATUS_LABELS[s] || s || 'Pendiente' }
function statusTheme(s) {
  return { Ready: 'green', Authorized: 'green', Checking: 'amber', Degraded: 'amber', Expired: 'red', Revoked: 'red', Failed: 'red' }[s] || 'gray'
}

async function load() {
  loading.value = true
  try { connections.value = await api.listConnections() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
function openCreate() { form.value = { connection_type: 'WhatsApp', display_name: '', provider: '' }; showCreate.value = true }
async function create() {
  if (!form.value.display_name.trim()) { toast.warning('Escribe un nombre para la conexión.'); return }
  saving.value = true
  try {
    await api.createConnection({ connection_type: form.value.connection_type, display_name: form.value.display_name, provider: form.value.provider || null })
    toast.success('Conexión creada.')
    showCreate.value = false
    await load()
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}
onMounted(load)
</script>
