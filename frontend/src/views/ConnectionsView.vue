<template>
  <AppLayout>
    <div class="p-6">
      <div class="mb-4 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold">Conexiones</h1>
          <p class="text-sm text-ink-gray-5">Canales e integraciones autorizadas de tus agentes.</p>
        </div>
        <Button variant="solid" theme="blue" label="Nueva conexión" @click="showCreate = true" />
      </div>

      <div v-if="loading" class="py-8 text-center text-ink-gray-5">Cargando…</div>
      <div v-else-if="!connections.length" class="rounded-lg border border-outline-gray-2 p-8 text-center">
        <div class="mb-2 text-sm font-medium">Sin conexiones</div>
        <div class="text-sm text-ink-gray-5">Conecta un canal para que tu agente atienda clientes.</div>
      </div>
      <div v-else class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <div v-for="c in connections" :key="c.name" class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
          <div class="mb-1 flex items-center justify-between">
            <span class="text-sm font-medium">{{ c.channel || c.name }}</span>
            <Badge :label="c.connection_state || 'Pending'" variant="subtle" theme="gray" />
          </div>
          <div class="text-[12px] text-ink-gray-5">{{ c.agent || c.external_id || '—' }}</div>
        </div>
      </div>

      <Dialog v-model:open="showCreate" title="Nueva conexión" size="md">
        <div class="flex flex-col gap-3">
          <Select v-model="form.channel" label="Canal" :options="['WhatsApp','Chatwoot','Email','API']" />
          <TextInput v-model="form.agent" label="Agente" placeholder="Nombre del agente" />
          <TextInput v-model="form.external_id" label="ID externo (opcional)" />
          <TextInput v-model="form.credential" label="Credencial (nombre de Secret)" placeholder="Ref, nunca el valor" />
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
import { Button, Badge, Dialog, Select, TextInput } from 'frappe-ui'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const connections = ref([])
const loading = ref(true)
const showCreate = ref(false)
const saving = ref(false)
const form = ref({ channel: 'WhatsApp', agent: '', external_id: '', credential: '' })

async function load() {
  loading.value = true
  try { connections.value = await api.listConnections() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
async function create() {
  saving.value = true
  try { await api.createConnection(form.value); toast.success('Conexión creada.'); showCreate.value = false; await load() }
  catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}
onMounted(load)
</script>
