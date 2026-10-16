<template>
  <AppLayout>
    <div class="flex h-full flex-col">
      <div class="border-b border-outline-gray-2 px-6 py-4">
        <h1 class="text-xl font-semibold">Cerebro</h1>
        <p class="text-sm text-ink-gray-5">Asistente de ERPNext. Consulta y ejecuta acciones autorizadas con aprobación.</p>
      </div>
      <div ref="logRef" class="scroll-area flex-1 px-6 py-4">
        <div v-if="!messages.length" class="flex h-full flex-col items-center justify-center gap-2 text-center">
          <div class="text-2xl">🧠</div>
          <div class="text-sm font-medium">¿En qué te ayudo?</div>
          <div class="max-w-sm text-sm text-ink-gray-5">Puedo buscar clientes, crear seguimientos, leads o borradores de cotización. Te mostraré el documento real antes de cualquier cambio.</div>
          <div class="mt-2 flex flex-wrap justify-center gap-2">
            <Button v-for="s in suggestions" :key="s" variant="subtle" :label="s" @click="send(s)" />
          </div>
        </div>
        <div v-else class="flex flex-col gap-3">
          <div v-for="(m, i) in messages" :key="i" class="flex" :class="m.role === 'user' ? 'justify-end' : 'justify-start'">
            <div class="max-w-[75%] rounded-xl px-3 py-2 text-sm" :class="m.role === 'user' ? 'bg-surface-blue-2 text-ink-blue-9' : 'bg-surface-base text-ink-gray-9 border border-outline-gray-2'">
              <div class="whitespace-pre-wrap">{{ m.text }}</div>
              <div v-if="m.actions && m.actions.length" class="mt-2 flex flex-wrap gap-2">
                <Button v-for="a in m.actions" :key="a.label" size="sm" :variant="a.danger ? 'solid' : 'subtle'" :theme="a.danger ? 'red' : 'blue'" :label="a.label" @click="confirm(m, a)" />
              </div>
            </div>
          </div>
          <div v-if="busy" class="text-sm text-ink-gray-5">Pensando…</div>
        </div>
      </div>
      <div class="border-t border-outline-gray-2 p-4">
        <div class="flex gap-2">
          <TextInput v-model="draft" class="flex-1" placeholder="Escribe tu consulta…" @keydown.enter.prevent="send()" />
          <Button variant="solid" theme="blue" label="Enviar" :loading="busy" @click="send()" />
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { Button, TextInput } from 'frappe-ui'
import { toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const messages = ref([])
const draft = ref('')
const busy = ref(false)
const conversation = ref(null)
const logRef = ref(null)

const suggestions = ['Mis pendientes', '¿Qué prospectos requieren atención?', '¿Cómo va la venta?', 'Crea una tarea para…']

async function ensure() {
  if (conversation.value) return conversation.value
  conversation.value = await api.cerebroStart()
  return conversation.value
}

async function send(text) {
  const msg = (text || draft.value || '').trim()
  if (!msg || busy.value) return
  draft.value = ''
  messages.value.push({ role: 'user', text: msg })
  busy.value = true
  scrollDown()
  try {
    const c = await ensure()
    const reply = await api.cerebroAsk(c.name, msg)
    messages.value.push({ role: 'assistant', text: reply.text, actions: reply.actions || [] })
  } catch (e) {
    messages.value.push({ role: 'assistant', text: '⚠️ ' + humanError(e), actions: [] })
  } finally {
    busy.value = false
    scrollDown()
  }
}

async function confirm(msgRow, action) {
  msgRow.actions = []
  busy.value = true
  try {
    const c = await ensure()
    const reply = await api.cerebroAsk(c.name, action.value || action.label, { execute: true })
    messages.value.push({ role: 'assistant', text: reply.text, actions: reply.actions || [] })
  } catch (e) {
    messages.value.push({ role: 'assistant', text: '⚠️ ' + humanError(e), actions: [] })
  } finally {
    busy.value = false
    scrollDown()
  }
}

function scrollDown() { nextTick(() => { if (logRef.value) logRef.value.scrollTop = logRef.value.scrollHeight }) }
onMounted(() => scrollDown())
</script>
