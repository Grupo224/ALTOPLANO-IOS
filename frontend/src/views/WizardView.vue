<template>
  <AppLayout>
    <div class="mx-auto w-full max-w-3xl p-6">
      <div class="mb-8">
        <h1 class="text-xl font-semibold">Crear tu agente</h1>
        <p class="text-sm text-ink-gray-5">Completa estos pasos para desplegar tu agente de IA.</p>

        <div class="mt-5 flex items-center">
          <template v-for="(s, i) in steps" :key="i">
            <div class="flex shrink-0 items-center gap-2">
              <div class="flex h-8 w-8 items-center justify-center rounded-full text-sm font-semibold" :class="i < current ? 'bg-surface-blue-7 text-white' : i === current ? 'bg-surface-blue-2 text-ink-blue-7' : 'bg-surface-gray-2 text-ink-gray-5'">
                <span v-if="i < current" class="lucide-check size-4"></span>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span class="hidden text-sm sm:block" :class="i <= current ? 'font-medium text-ink-gray-7' : 'text-ink-gray-4'">{{ s }}</span>
            </div>
            <div v-if="i < steps.length - 1" class="mx-2 h-px flex-1 bg-outline-gray-2"></div>
          </template>
        </div>
      </div>

      <div class="rounded-xl border border-outline-gray-2 bg-surface-base p-6">
        <!-- Paso 1: Negocio -->
        <div v-if="current === 0" class="flex flex-col gap-3">
          <TextInput v-model="profile.display_name" label="Nombre del negocio" placeholder="Mi negocio" />
          <Textarea v-model="profile.offering" label="¿Qué ofreces?" placeholder="Productos o servicios que vendes" />
          <TextInput v-model="profile.audience" label="¿A quién atiendes?" placeholder="Clientes, prospectos, etc." />
          <Select v-model="profile.tone" label="Tono de comunicación" :options="tones" />
          <TextInput v-model="profile.timezone" label="Zona horaria" placeholder="America/Mexico_City" />
        </div>

        <!-- Paso 2: Plantilla -->
        <div v-else-if="current === 1" class="flex flex-col gap-2">
          <div v-if="!templates.length" class="rounded-lg border border-dashed border-outline-gray-2 p-6 text-center text-sm text-ink-gray-5">
            No hay plantillas publicadas. Continúa y personaliza tu agente manualmente.
          </div>
          <button v-for="t in templates" :key="t.name" class="rounded-lg border p-3 text-left transition" :class="selectedTemplate === t.slug ? 'border-outline-blue-4 bg-surface-blue-2' : 'border-outline-gray-2 hover:bg-surface-gray-1'" @click="selectedTemplate = t.slug">
            <div class="font-medium">{{ t.display_name }}</div>
            <div class="text-sm text-ink-gray-5">{{ t.purpose }}</div>
          </button>
        </div>

        <!-- Paso 3: Personalidad -->
        <div v-else-if="current === 2" class="flex flex-col gap-3">
          <TextInput v-model="agent.display_name" label="Nombre del agente" placeholder="Asistente de ventas" />
          <TextInput v-model="agent.summary" label="Resumen" placeholder="Qué hace tu agente" />
          <Select v-model="agent.audience" label="Audiencia" :options="['Customer', 'Internal', 'Prospect']" />
          <Textarea v-model="agent.instructions" label="Instrucciones" placeholder="Cómo debe responder y actuar" />
        </div>

        <!-- Paso 4: Canales -->
        <div v-else-if="current === 3" class="flex flex-col gap-3">
          <div class="text-sm text-ink-gray-6">Conecta un canal para que tu agente atienda clientes.</div>
          <div v-if="!connections.length" class="rounded-lg border border-dashed border-outline-gray-2 p-6 text-center text-sm text-ink-gray-5">Aún no tienes conexiones.</div>
          <div v-for="c in connections" :key="c.name" class="flex items-center justify-between rounded-lg border border-outline-gray-2 px-3 py-2">
            <span class="truncate">{{ c.display_name || c.name }}</span>
            <Badge :label="c.status || 'Pendiente'" variant="subtle" theme="gray" />
          </div>
          <div class="flex gap-2">
            <Select v-model="newConn.type" :options="['WhatsApp', 'Email', 'Chatwoot', 'MCP']" class="w-40 shrink-0" />
            <TextInput v-model="newConn.display_name" placeholder="Nombre de la conexión" class="flex-1" />
            <Button variant="subtle" label="Agregar" @click="addConnection" />
          </div>
        </div>

        <!-- Paso 5: Revisar -->
        <div v-else class="flex flex-col gap-3">
          <div class="rounded-lg bg-surface-gray-1 p-4">
            <div class="mb-2 font-medium">Resumen</div>
            <div class="text-sm"><b>Negocio:</b> {{ profile.display_name || '—' }}</div>
            <div class="text-sm"><b>Plantilla:</b> {{ templateLabel }}</div>
            <div class="text-sm"><b>Agente:</b> {{ agent.display_name || '—' }}</div>
            <div class="text-sm"><b>Canales:</b> {{ connections.length }}</div>
          </div>
          <Button variant="solid" theme="blue" size="lg" label="Crear y desplegar agente" :loading="creating" @click="createAgent" />
        </div>
      </div>

      <div class="mt-4 flex justify-between">
        <Button variant="subtle" label="Anterior" :disabled="current === 0" @click="current--" />
        <Button v-if="current < steps.length - 1" variant="solid" theme="blue" label="Siguiente" @click="next" />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Badge, Select, TextInput, Textarea, toast } from 'frappe-ui'
import AppLayout from '../components/AppLayout.vue'
import { api, humanError } from '../resources/api'

const router = useRouter()
const steps = ['Negocio', 'Plantilla', 'Personalidad', 'Canales', 'Revisar']
const current = ref(0)

const profile = reactive({ display_name: '', offering: '', audience: '', tone: 'Profesional', timezone: 'America/Mexico_City' })
const templates = ref([])
const selectedTemplate = ref('')
const agent = reactive({ display_name: '', summary: '', audience: 'Customer', instructions: '' })
const connections = ref([])
const newConn = reactive({ type: 'WhatsApp', display_name: '' })
const creating = ref(false)

const tones = ['Profesional', 'Amigable', 'Formal', 'Cercano', 'Técnico']

const templateLabel = computed(() => templates.value.find((t) => t.slug === selectedTemplate.value)?.display_name || '—')

async function load() {
  try {
    const [p, t, c] = await Promise.all([api.getProfile(), api.templates(), api.listConnections()])
    if (p) Object.assign(profile, { display_name: p.display_name || '', offering: p.offering || '', audience: p.audience || '', tone: p.tone || 'Profesional', timezone: p.timezone || 'America/Mexico_City' })
    templates.value = t || []
    connections.value = c || []
  } catch (e) { toast.error(humanError(e)) }
}

async function saveProfile() {
  await api.saveProfile({ display_name: profile.display_name, offering: profile.offering, audience: profile.audience, tone: profile.tone, timezone: profile.timezone })
}

function next() {
  if (current.value === 0 && !profile.display_name.trim()) { toast.warning('Escribe el nombre de tu negocio.'); return }
  if (current.value === 2 && !agent.display_name.trim()) { toast.warning('Escribe el nombre de tu agente.'); return }
  current.value++
}

async function addConnection() {
  if (!newConn.display_name.trim()) { toast.warning('Escribe un nombre para la conexión.'); return }
  try {
    await api.createConnection({ connection_type: newConn.type, display_name: newConn.display_name })
    toast.success('Conexión agregada.')
    newConn.display_name = ''
    connections.value = await api.listConnections()
  } catch (e) { toast.error(humanError(e)) }
}

async function createAgent() {
  creating.value = true
  try {
    await saveProfile()
    await api.createAgent({ display_name: agent.display_name || 'Mi agente', summary: agent.summary, audience: agent.audience, template: selectedTemplate.value || null, instructions: agent.instructions })
    toast.success('Agente creado.')
    router.push('/agents')
  } catch (e) { toast.error(humanError(e)) } finally { creating.value = false }
}

onMounted(load)
</script>
