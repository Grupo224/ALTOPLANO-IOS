<template>
  <Dialog :open="open" @update:open="onOpenChange" :title="title" size="xl" :dismissible="false">
    <div v-if="!mode" class="os-mode-choice">
      <p style="color: var(--os-steel); font-size: 13px; margin: 0 0 14px">Puedes empezar rápido y enriquecer después — nunca se pierde lo ya capturado.</p>
      <div class="flex gap-3">
        <div class="os-mode-card" role="button" tabindex="0" @click="start('quick')">
          <span>Modo Rápido</span>
          <b>7 campos · &lt;2 min</b>
          <p>Proceso mínimo viable: nombre, propósito, empresa, dueño, disparador, riesgo, autonomía y KPI.</p>
        </div>
        <div class="os-mode-card" role="button" tabindex="0" @click="start('full')">
          <span>Modo Completo</span>
          <b>6 pasos · 8–12 min</b>
          <p>SIPOC, RACI, controles, metas por cadencia y mejora continua — el esquema completo.</p>
        </div>
      </div>
    </div>

    <div v-else>
      <div class="os-wizard-steps">
        <button v-for="(s, i) in SECTIONS" :key="i" type="button"
          class="os-wizard-step" :class="{ on: i === stepIdx, done: i < stepIdx }"
          :disabled="i > maxReached" @click="goto(i)">
          <span class="os-wizard-num">{{ i < stepIdx ? '✓' : i + 1 }}</span>{{ s.title }}
        </button>
      </div>

      <div class="os-form-body" style="padding-top: 14px; max-height: 55vh; overflow-y: auto">
        <template v-if="mode === 'quick'">
          <p style="color: var(--os-steel); font-size: 12.5px; margin: 0 0 10px">Con esto ya es un proceso utilizable. Podrás enriquecerlo después con SIPOC, RACI y más metas.</p>
          <div v-for="f in quickFields" :key="f.name" class="mb-3">
            <FieldInput :field="f" v-model="form[f.name]" />
          </div>
        </template>

        <template v-else>
          <div v-for="f in SECTIONS[stepIdx].fields" :key="f.name" class="mb-3">
            <FieldInput :field="f" v-model="form[f.name]" />
          </div>

          <div v-if="SECTIONS[stepIdx].stepsSummary">
            <div class="os-section-title">Resumen de pasos</div>
            <p v-if="isEdit && (stepsCount > 0)" style="font-size: 13px; color: var(--os-steel)">{{ stepsCount }} paso(s) definidos en el lienzo.</p>
            <p v-else style="font-size: 13px; color: var(--os-steel)">Los pasos y sus conexiones se dibujan en el lienzo de procesos — podrás agregarlos justo después de guardar.</p>
            <Button v-if="isEdit" variant="ghost" label="↗ Ir al lienzo de pasos" @click="goCanvas" />
          </div>

          <div v-if="SECTIONS[stepIdx].goals">
            <div class="os-section-title">Metas por cadencia</div>
            <div v-if="!goals.length" class="muted" style="font-size: 12px; padding: 4px 0 8px">Sin metas capturadas. Empieza por la meta mensual.</div>
            <div v-for="(g, gi) in goals" :key="gi" class="flex items-end gap-2 mb-2">
              <Select v-model="g.cadence" :options="cadenceOptions" style="width: 110px" />
              <TextInput v-model="g.metric" placeholder="Métrica / KPI" style="min-width: 130px" />
              <TextInput v-model="g.target" type="number" placeholder="Objetivo" style="max-width: 90px" />
              <TextInput v-model="g.unit" placeholder="Unidad" style="max-width: 80px" />
              <TextInput v-model="g.tolerance" placeholder="Tolerancia" style="max-width: 90px" />
              <TextInput v-model="g.responsible" placeholder="Responsable" style="min-width: 110px" />
              <Button variant="ghost" theme="red" label="✕" @click="goals.splice(gi, 1)" />
            </div>
            <div class="flex gap-2">
              <Button variant="ghost" label="＋ Agregar meta" @click="goals.push({ cadence: 'Monthly', direction: 'More is better' })" />
              <Button variant="ghost" label="✨ Sugerir cascada" @click="cascadeGoals" />
            </div>
          </div>
        </template>
      </div>
    </div>

    <template #actions="{ close }">
      <Button variant="ghost" label="Cancelar" @click="close()" />
      <template v-if="mode">
        <Button variant="ghost" label="Guardar borrador y salir" @click="saveDraft" />
        <Button v-if="mode === 'full' && stepIdx > 0" variant="ghost" label="Atrás" @click="stepIdx--" />
        <Button variant="solid" theme="blue" :label="isLast ? 'Guardar proceso' : 'Siguiente'" :loading="saving" @click="next" />
      </template>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, Button, TextInput, Select, call, toast } from 'frappe-ui'
import FieldInput from './FieldInput.vue'
import { osApi, humanError } from '../resources/os'

const props = defineProps({
  open: Boolean,
  name: { type: String, default: null },
})
const emit = defineEmits(['update:open', 'saved'])
const router = useRouter()

const isEdit = computed(() => !!props.name)
const title = computed(() => (isEdit.value ? 'Editar proceso' : 'Nuevo proceso'))

const SECTIONS = [
  { title: 'Identidad y propósito', fields: [
    { name: 'process_title', label: 'Nombre del proceso', type: 'text', required: true, hint: 'Ej. Lead → Cotización' },
    { name: 'process_code', label: 'Código / ID', type: 'text', hint: 'Se genera solo si lo dejas vacío.' },
    { name: 'company', label: 'Empresa', type: 'link', linkDoctype: 'Company', required: true },
    { name: 'org_area', label: 'Área (Organigrama Vivo)', type: 'link', linkDoctype: 'OS Org Node' },
    { name: 'department', label: 'Departamento (ERPNext)', type: 'link', linkDoctype: 'Department' },
    { name: 'owner_user', label: 'Dueño / responsable (Aprobador)', type: 'link', linkDoctype: 'User', required: true },
    { name: 'priority', label: 'Criticidad', type: 'select', options: ['Low', 'Medium', 'High', 'Critical'] },
    { name: 'purpose', label: 'Propósito', type: 'textarea', required: true, hint: 'Por qué existe y qué valor entrega.' },
    { name: 'outcome', label: 'Resultado esperado', type: 'textarea' },
  ] },
  { title: 'Alcance y disparador (SIPOC)', fields: [
    { name: 'trigger_type', label: 'Tipo de disparador', type: 'select', options: ['Manual', 'ERP Event', 'Webhook', 'Schedule', 'External'], required: true },
    { name: 'trigger_reference', label: 'Disparador (detalle)', type: 'text' },
    { name: 'suppliers', label: 'Proveedores', type: 'text', hint: 'Separados por coma.' },
    { name: 'inputs', label: 'Entradas / insumos', type: 'text', required: true, hint: 'Separadas por coma.' },
    { name: 'outputs', label: 'Salidas / entregables', type: 'text', required: true, hint: 'Separadas por coma.' },
    { name: 'clients', label: 'Cliente del proceso', type: 'text' },
    { name: 'scope', label: 'Incluye / no incluye', type: 'textarea' },
    { name: 'frequency', label: 'Frecuencia de ejecución', type: 'select', options: ['On Demand', 'Daily', 'Weekly', 'Biweekly', 'Monthly'] },
  ] },
  { title: 'Pasos y ejecución', stepsSummary: true, fields: [
    { name: 'max_autonomy', label: 'Autonomía máxima de la IA', type: 'select', options: ['L0', 'L1', 'L2', 'L3', 'L4'], required: true },
    { name: 'rules', label: 'Reglas de decisión', type: 'textarea', hint: 'Bifurcaciones: si pasa X, entonces Y.' },
    { name: 'exceptions', label: 'Excepciones y manejo', type: 'textarea' },
  ] },
  { title: 'Roles y gobierno (RACI)', fields: [
    { name: 'raci_responsible', label: 'Responsable (R)', type: 'link', linkDoctype: 'User' },
    { name: 'raci_consulted', label: 'Consultado (C)', type: 'text', hint: 'Separados por coma.' },
    { name: 'raci_informed', label: 'Informado (I)', type: 'text', hint: 'Separados por coma.' },
    { name: 'responsible_node', label: 'Responsable vinculado (organigrama)', type: 'link', linkDoctype: 'OS Org Node' },
    { name: 'risk_level', label: 'Riesgo', type: 'select', options: ['Low', 'Medium', 'High', 'Critical'], required: true },
    { name: 'gates', label: 'Puntos de aprobación (gates)', type: 'textarea' },
    { name: 'policy', label: 'Política aplicable', type: 'link', linkDoctype: 'OS Policy' },
    { name: 'controls', label: 'Controles', type: 'textarea', hint: 'Obligatorio en la práctica si el riesgo es alto.' },
    { name: 'sop', label: 'SOP vinculado', type: 'link', linkDoctype: 'OS SOP' },
  ] },
  { title: 'Metas y medición', goals: true, fields: [
    { name: 'kpis', label: 'KPIs del proceso', type: 'text', required: true, hint: 'Separados por coma.' },
    { name: 'sla_minutes', label: 'SLA objetivo (min)', type: 'number' },
    { name: 'definition_of_done', label: 'Definición de Hecho (DoD)', type: 'textarea', required: true },
    { name: 'evidence_required', label: 'Evidencia requerida', type: 'textarea' },
  ] },
  { title: 'Mejora continua', fields: [
    { name: 'version_label', label: 'Versión', type: 'text' },
    { name: 'next_review_on', label: 'Próxima revisión', type: 'text', hint: 'YYYY-MM-DD' },
    { name: 'changelog', label: 'Historial de cambios', type: 'textarea' },
    { name: 'kaizen', label: 'Oportunidades de mejora', type: 'textarea' },
  ] },
]

const QUICK_FIELD_NAMES = ['process_title', 'purpose', 'owner_user', 'company', 'trigger_reference', 'risk_level', 'max_autonomy', 'kpis']
const quickFields = QUICK_FIELD_NAMES.map((n) => SECTIONS.flatMap((s) => s.fields).find((f) => f.name === n)).filter(Boolean)

const cadenceOptions = ['Daily', 'Weekly', 'Biweekly', 'Monthly'].map((c) => ({ label: c, value: c }))

const mode = ref(null)
const stepIdx = ref(0)
const maxReached = ref(0)
const form = reactive({})
const goals = ref([])
const saving = ref(false)
const stepsCount = ref(0)

const isLast = computed(() => mode.value === 'quick' || stepIdx.value === SECTIONS.length - 1)

function onOpenChange(v) { emit('update:open', v) }

function start(m) {
  mode.value = m
  stepIdx.value = 0
  maxReached.value = 0
}

function goto(i) {
  if (i > maxReached.value || i === stepIdx.value || i < 0 || i >= SECTIONS.length) return
  stepIdx.value = i
}

function next() {
  if (mode.value === 'quick') return save()
  const sec = SECTIONS[stepIdx.value]
  const missing = sec.fields.filter((f) => f.required && !String(form[f.name] || '').trim())
  if (missing.length) { toast.warning('Falta capturar: ' + missing.map((f) => f.label).join(', ')); return }
  if (!isLast.value) { stepIdx.value++; if (stepIdx.value > maxReached.value) maxReached.value = stepIdx.value }
  else save()
}

function goCanvas() {
  emit('update:open', false)
  if (props.name) router.push('/processes/' + props.name)
}

function buildValues() {
  const out = {}
  const all = SECTIONS.flatMap((s) => s.fields)
  for (const f of all) {
    const v = form[f.name]
    if (v !== undefined && v !== null && v !== '') out[f.name] = v
  }
  return out
}

async function save() {
  saving.value = true
  try {
    const values = buildValues()
    const g = goals.value.filter((x) => x.metric && x.target != null)
    const r = await osApi.saveProcessMeta(props.name, values, g)
    toast.success(isEdit.value ? 'Cambios guardados ✓' : 'Proceso creado en Draft ✓')
    emit('saved', { name: r.name })
    emit('update:open', false)
  } catch (e) { toast.error(humanError(e)) } finally { saving.value = false }
}

function saveDraft() { save() }

watch(() => props.open, async (v) => {
  if (!v) return
  mode.value = isEdit.value ? 'full' : null
  stepIdx.value = 0
  maxReached.value = 0
  goals.value = []
  stepsCount.value = 0
  for (const k in form) delete form[k]
  if (props.name) {
    try {
      const doc = await call('frappe.client.get', { doctype: 'OS Process', name: props.name })
      for (const f of SECTIONS.flatMap((s) => s.fields)) form[f.name] = doc[f.name] ?? ''
      goals.value = (doc.goals || []).map((g) => ({ cadence: g.cadence, metric: g.metric, target: g.target, unit: g.unit, tolerance: g.tolerance, direction: g.direction, responsible: g.responsible }))
      stepsCount.value = (doc.steps || []).length
    } catch (e) { toast.error(humanError(e)) }
  } else {
    form.status = 'Draft'
    form.version_label = 'v0.1'
    form.trigger_type = 'Manual'
    form.max_autonomy = 'L1'
    form.risk_level = 'Medium'
  }
})

function cascadeGoals() {
  const base = goals.value.find((g) => g.cadence === 'Monthly' && g.target != null)
  if (!base) { toast.warning('Captura primero una meta mensual con objetivo numérico.'); return }
  const factor = { Daily: 22, Weekly: 4.33, Biweekly: 2 }
  for (const c of ['Daily', 'Weekly', 'Biweekly']) {
    const val = Math.round((base.target / factor[c]) * 10) / 10
    let row = goals.value.find((g) => g.cadence === c && g.metric === base.metric)
    if (!row) { row = { cadence: c, metric: base.metric, unit: base.unit, responsible: base.responsible, direction: base.direction, tolerance: base.tolerance }; goals.value.unshift(row) }
    row.target = val
  }
  toast.success('Cascada propuesta. Ajusta lo que necesites.')
}
</script>
