<template>
  <AppLayout>
    <div class="flex h-full">
      <div class="w-80 shrink-0 border-r border-outline-gray-2 bg-surface-base">
        <div class="border-b border-outline-gray-2 px-4 py-3">
          <h1 class="text-base font-semibold">Conversaciones</h1>
        </div>
        <div v-if="loading" class="p-4 text-sm text-ink-gray-5">Cargando…</div>
        <div v-else-if="!conversations.length" class="p-4 text-sm text-ink-gray-5">Sin conversaciones aún.</div>
        <button v-else v-for="c in conversations" :key="c.name" @click="select(c)"
          class="block w-full border-b border-outline-gray-2 px-4 py-3 text-left hover:bg-surface-gray-2"
          :class="selected && selected.name === c.name ? 'bg-surface-blue-2' : ''">
          <div class="text-sm font-medium">{{ c.customer || c.channel }}</div>
          <div class="text-[12px] text-ink-gray-5">{{ c.agent || c.name }}</div>
        </button>
      </div>

      <div class="flex min-w-0 flex-1 flex-col">
        <div v-if="!selected" class="flex flex-1 items-center justify-center text-sm text-ink-gray-5">Selecciona una conversación.</div>
        <template v-else>
          <div class="flex items-center justify-between border-b border-outline-gray-2 px-4 py-3">
            <div>
              <div class="text-sm font-medium">{{ selected.customer || selected.channel }}</div>
              <div class="text-[12px] text-ink-gray-5">{{ selected.agent || selected.name }}</div>
            </div>
            <Button variant="subtle" label="Transferir" @click="showHandoff = true" />
          </div>
          <div class="scroll-area flex-1 px-4 py-3">
            <div v-if="!messages.length" class="text-sm text-ink-gray-5">Sin mensajes.</div>
            <div v-else class="flex flex-col gap-2">
              <div v-for="(m, i) in messages" :key="i" class="max-w-[75%] rounded-xl px-3 py-2 text-sm"
                :class="m.sender === 'agent' ? 'self-start bg-surface-base border border-outline-gray-2' : 'self-end bg-surface-blue-2'">
                {{ m.content }}
              </div>
            </div>
          </div>
        </template>
      </div>
    </div>

    <Dialog v-model:open="showHandoff" title="Transferir conversación" size="md">
      <div class="flex flex-col gap-3">
        <TextInput v-model="handoffUser" label="Asignar a (usuario)" placeholder="usuario@ejemplo.com" />
      </div>
      <template #actions="{ close }">
        <Button variant="ghost" label="Cancelar" @click="close()" />
        <Button variant="solid" theme="blue" label="Transferir" :loading="handing" @click="handoff" />
      </template>
    </Dialog>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Button, Dialog, TextInput } from 'frappe-ui'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const conversations = ref([])
const messages = ref([])
const selected = ref(null)
const loading = ref(true)
const showHandoff = ref(false)
const handoffUser = ref('')
const handing = ref(false)

async function load() {
  loading.value = true
  try { conversations.value = await api.listConversations() } catch (e) { toast.error(humanError(e)) } finally { loading.value = false }
}
async function select(c) {
  selected.value = c
  messages.value = []
  try { messages.value = await api.getMessages(c.name) } catch (e) { toast.error(humanError(e)) }
}
async function handoff() {
  handing.value = true
  try { await api.handoff(selected.value.name, handoffUser.value); toast.success('Conversación transferida.'); showHandoff.value = false }
  catch (e) { toast.error(humanError(e)) } finally { handing.value = false }
}
onMounted(load)
</script>
