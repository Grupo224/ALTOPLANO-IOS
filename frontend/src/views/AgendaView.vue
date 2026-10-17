<template>
  <div class="p-6">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-xl font-semibold">Agenda</h1>
        <p class="text-sm text-ink-gray-5">Agendas de citas de agentes y reservas.</p>
      </div>
      <Button variant="solid" theme="blue" label="Nueva agenda" @click="openNew = true" />
    </div>

    <div v-if="loading" class="flex justify-center py-16"><Spinner /></div>
    <div v-else-if="error" class="rounded-lg bg-surface-red-2 px-4 py-3 text-sm text-ink-red-7">{{ error }}</div>

    <template v-else>
      <div class="mb-6">
        <div class="mb-2 text-sm font-medium text-ink-gray-6">Agendas</div>
        <div v-if="!calendars.length" class="rounded-lg border border-dashed border-outline-gray-2 px-4 py-10 text-center text-sm text-ink-gray-5">
          Aún no hay agendas. Crea la primera para empezar a reservar citas.
        </div>
        <div v-else class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="c in calendars" :key="c.name" class="rounded-xl border border-outline-gray-2 bg-surface-base p-4">
            <div class="flex items-center justify-between gap-2">
              <div class="truncate font-medium">{{ c.display_name }}</div>
              <Badge :label="c.enabled ? 'Activa' : 'Pausada'" variant="subtle" :theme="c.enabled ? 'green' : 'gray'" />
            </div>
            <div class="mt-1 text-sm text-ink-gray-5">{{ c.timezone }}</div>
            <div class="text-xs text-ink-gray-4">Citas de {{ c.slot_minutes }} min · {{ c.sync_mode }}</div>
          </div>
        </div>
      </div>

      <div>
        <div class="mb-2 text-sm font-medium text-ink-gray-6">Citas</div>
        <div v-if="!appointments.length" class="rounded-lg border border-dashed border-outline-gray-2 px-4 py-10 text-center text-sm text-ink-gray-5">
          Aún no hay citas registradas.
        </div>
        <div v-else class="overflow-hidden rounded-xl border border-outline-gray-2 bg-surface-base">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-outline-gray-2 text-left text-xs uppercase text-ink-gray-5">
                <th class="px-4 py-2 font-medium">Cita</th>
                <th class="px-4 py-2 font-medium">Cliente</th>
                <th class="px-4 py-2 font-medium">Agenda</th>
                <th class="px-4 py-2 font-medium">Origen</th>
                <th class="px-4 py-2 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in appointments" :key="a.name" class="border-b border-outline-gray-2 last:border-0">
                <td class="px-4 py-2 font-medium">{{ a.name }}</td>
                <td class="px-4 py-2 text-ink-gray-7">{{ a.customer || '—' }}</td>
                <td class="px-4 py-2 text-ink-gray-7">{{ a.calendar }}</td>
                <td class="px-4 py-2 text-ink-gray-7">{{ a.source || '—' }}</td>
                <td class="px-4 py-2"><Badge :label="a.status || '—'" variant="subtle" :theme="statusTheme(a.status)" /></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <Dialog v-model:open="openNew" title="Nueva agenda" size="sm">
      <div class="flex flex-col gap-3">
        <TextInput v-model="form.display_name" label="Nombre de la agenda" placeholder="Atención al cliente" />
        <TextInput v-model="form.slot_minutes" type="number" label="Duración de cita (min)" />
        <TextInput v-model="form.timezone" label="Zona horaria" placeholder="America/Mexico_City" />
      </div>
      <template #actions="{ close }">
        <Button variant="ghost" label="Cancelar" @click="close()" />
        <Button variant="solid" theme="blue" label="Crear agenda" @click="create()" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Button, Badge, Dialog, TextInput, Spinner, toast } from 'frappe-ui'
import { api, humanError } from '../resources/api'

const loading = ref(true)
const error = ref('')
const calendars = ref([])
const appointments = ref([])
const openNew = ref(false)
const form = reactive({ display_name: '', slot_minutes: 30, timezone: 'America/Mexico_City' })

function statusTheme(s) {
  return { Confirmed: 'green', Held: 'amber', Cancelled: 'gray', Completed: 'green', NoShow: 'red' }[s] || 'gray'
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    const [c, a] = await Promise.all([api.calendars(), api.appointments()])
    calendars.value = c || []
    appointments.value = a || []
  } catch (e) {
    error.value = humanError(e)
  } finally {
    loading.value = false
  }
}

async function create() {
  if (!form.display_name.trim()) { toast.warning('Escribe un nombre para la agenda.'); return }
  try {
    await api.createCalendar({ ...form })
    toast.success('Agenda creada.')
    openNew.value = false
    form.display_name = ''
    load()
  } catch (e) {
    toast.error(humanError(e))
  }
}

onMounted(load)
</script>
