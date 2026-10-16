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
          <div class="max-w-sm text-sm text-ink-gray-5">Puedo buscar clientes, crear seguimientos, prospectos o cotizaciones en borrador.</div>
          <div class="mt-2 flex flex-wrap justify-center gap-2">
            <Button v-for="s in suggestions" :key="s" variant="subtle" :label="s" @click="send(s)" />
          </div>
        </div>
        <div v-else class="flex flex-col gap-3">
          <div v-for="(m, i) in messages" :key="i" class="flex" :class="m.role === 'user' ? 'justify-end' : 'justify-start'">
            <div class="max-w-[75%] rounded-xl px-3 py-2 text-sm" :class="m.role === 'user' ? 'bg-surface-blue-2 text-ink-blue-9' : 'bg-surface-base text-ink-gray-9 border border-outline-gray-2'">
              <div class="whitespace-pre-wrap">{{ m.text }}</div>
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
const conversationName = ref(null)
const logRef = ref(null)

const suggestions = ['buscar clientes', 'crear un prospecto', 'crear un seguimiento', 'crear una cotización']

async function ensure() {
  if (conversationName.value) return conversationName.value
  const res = await api.cerebroStart()
  conversationName.value = res.conversation
  return conversationName.value
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
    const res = await api.cerebroAsk(c, msg)
    messages.value.push({ role: 'assistant', text: res.reply || 'Sin respuesta.' })
  } catch (e) {
    messages.value.push({ role: 'assistant', text: '⚠️ ' + humanError(e) })
  } finally {
    busy.value = false
    scrollDown()
  }
}

function scrollDown() { nextTick(() => { if (logRef.value) logRef.value.scrollTop = logRef.value.scrollHeight }) }
onMounted(() => scrollDown())
</script>
