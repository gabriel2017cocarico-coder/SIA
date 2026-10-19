<template>
  <div class="layout sigta-role-layout">
    <aside :class="{ abierto: menuAbierto }">
      <div class="brand-row">
        <div class="brand"><b><img src="/img/emi.jpg" alt="EMI"></b><div><strong>SIGTA</strong><small>Soporte Técnico</small></div></div>
        <button type="button" class="menu-toggle" :aria-expanded="menuAbierto" aria-label="Mostrar opciones del menú" @click="menuAbierto = !menuAbierto"><span></span><span></span><span></span></button>
      </div>
      <div class="profile"><i>{{ iniciales }}</i><div><b>{{ nombre }}</b><small>Jefe de UTIC</small></div></div>
      <p>GESTIÓN DE TICKETS</p>
      <button v-for="m in menu" :key="m.id" :class="{active:vista===m.id}" @click="vista=m.id; menuAbierto=false"><span>{{ m.icono }}</span>{{ m.nombre }}<em v-if="m.total!==undefined">{{ m.total }}</em></button>
      <div class="bottom"><button @click="salir"><span>↪</span>Cerrar sesión</button></div>
    </aside>

    <main>
      <header>
        <div><small>SIGTA / SOPORTE / {{ titulo }}</small><h1>{{ titulo }}</h1><p>Recepción, clasificación y asignación de tickets de Soporte Técnico.</p></div>
        <button class="refresh" @click="cargar">↻ Actualizar</button>
      </header>

      <section v-if="vista==='resumen'">
        <div class="hero">
          <div><small>LÍDER DE TI</small><h2>{{ saludo }}, {{ primerNombre }}</h2><p>Tickets que requieren su gestión hoy.</p></div>
          <span>UTIC</span>
        </div>
        <div class="stats">
          <article @click="vista='validacion'"><i class="blue">VA</i><div><small>Por validar</small><b>{{ porValidar.length }}</b><p>tickets nuevos</p></div></article>
          <article @click="vista='clasificacion'"><i class="gold">CL</i><div><small>Por clasificar</small><b>{{ porClasificar.length }}</b><p>prioridad / SLA</p></div></article>
          <article @click="vista='asignacion'"><i class="green">AS</i><div><small>Por asignar</small><b>{{ porAsignar.length }}</b><p>especialista</p></div></article>
          <article @click="vista='compra'"><i class="navy">CO</i><div><small>Compras por validar</small><b>{{ pendientesViabilidad.length }}</b><p>elevar a DAF</p></div></article>
        </div>
        <div class="panels">
          <section class="panel">
            <div class="panel-head"><div><small>FLUJO BPMN</small><h3>Proceso de soporte técnico</h3></div></div>
            <button class="flow" @click="vista='validacion'"><i class="blue">1</i><div><b>Recibir y validar ticket</b><small>Confirmar que el ticket es válido o devolverlo al solicitante</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='clasificacion'"><i class="gold">2</i><div><b>Clasificar prioridad y SLA</b><small>Definir prioridad y calcular el tiempo de atención</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='asignacion'"><i class="green">3</i><div><b>Asignar especialista responsable</b><small>Designar al técnico que atenderá el ticket</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='compra'"><i class="navy">4</i><div><b>Validar y elevar compra</b><small>Revisar el requerimiento del técnico y elevarlo a DAF</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='informe'"><i class="gold">5</i><div><b>Elaborar informe final</b><small>Cerrar el expediente técnico del ticket</small></div><strong>›</strong></button>
          </section>
          <section class="panel">
            <div class="panel-head"><div><small>IDENTIDAD</small><h3>Delegación de aprobación</h3></div></div>
            <p class="copy">Si va a estar ausente, delegue temporalmente su rol de Jefe de UTIC a otro usuario habilitado.</p>
            <button class="wide primary" @click="vista='delegar'">Gestionar delegaciones →</button>
          </section>
        </div>
      </section>

      <section v-else-if="vista==='validacion'">
        <div class="instruction"><b>¿Es válido el ticket?</b><span>Reciba y valide, o devuelva el ticket al solicitante indicando el motivo.</span></div>
        <div class="toolbar"><label>⌕ <input v-model="busqueda" placeholder="Buscar ticket o unidad"></label></div>
        <div v-if="cargando" class="empty">Consultando tickets…</div>
        <div v-else-if="filtrar(porValidar).length" class="cards">
          <article v-for="t in filtrar(porValidar)" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ t.estado_codigo }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <p>{{ (t.descripcion||'').slice(0,130) }}</p>
            <div class="actions">
              <button @click="verTicket(t)">Ver detalle</button>
              <button class="reject" @click="rechazarTicket(t)">Rechazar</button>
              <button class="primary" @click="validarTicket(t)">Validar</button>
            </div>
          </article>
        </div>
        <div v-else class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay tickets pendientes de validación.</p></div>
      </section>

      <section v-else-if="vista==='clasificacion'">
        <div class="instruction"><b>Clasificar prioridad y SLA</b><span>Defina la prioridad y registre el criterio técnico de clasificación.</span></div>
        <div v-if="!ticketActivo" class="cards">
          <article v-for="t in porClasificar" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ t.estado_codigo }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <div class="actions"><button class="primary" @click="ticketActivo=t;formClasificacion.prioridad='';formClasificacion.criterio_tecnico=''">Clasificar</button></div>
          </article>
          <div v-if="!porClasificar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay tickets pendientes de clasificación.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ ticketActivo.codigo }} — {{ ticketActivo.titulo }}</h3>
          <label class="campo">Prioridad
            <select v-model="formClasificacion.prioridad">
              <option value="">Seleccione…</option>
              <option value="BAJA">Baja (48 h)</option>
              <option value="MEDIA">Media (24 h)</option>
              <option value="ALTA">Alta (8 h)</option>
              <option value="CRITICA">Crítica (4 h)</option>
            </select>
          </label>
          <label class="campo">Criterio técnico
            <textarea v-model="formClasificacion.criterio_tecnico" rows="3" placeholder="Justifique la prioridad asignada"></textarea>
          </label>
          <div class="actions">
            <button @click="ticketActivo=null">Cancelar</button>
            <button class="primary" :disabled="procesando||!formClasificacion.prioridad||!formClasificacion.criterio_tecnico.trim()" @click="clasificarTicket">Guardar clasificación</button>
          </div>
        </div>
      </section>

      <section v-else-if="vista==='asignacion'">
        <div class="instruction"><b>Asignar especialista responsable</b><span>Seleccione al Especialista que atenderá el ticket.</span></div>
        <div v-if="!ticketActivo" class="cards">
          <article v-for="t in porAsignar" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ t.prioridad }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <div class="actions"><button class="primary" @click="ticketActivo=t;formAsignacion.tecnico_id=''">Asignar</button></div>
          </article>
          <div v-if="!porAsignar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay tickets pendientes de asignación.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ ticketActivo.codigo }} — {{ ticketActivo.titulo }}</h3>
          <label class="campo">Especialista responsable
            <select v-model="formAsignacion.tecnico_id">
              <option value="">Seleccione…</option>
              <option v-for="e in especialistas" :key="e.id" :value="e.id">{{ e.nombre_completo || e.email }}</option>
            </select>
          </label>
          <small v-if="!especialistas.length">No hay especialistas activos disponibles.</small>
          <div class="actions">
            <button @click="ticketActivo=null">Cancelar</button>
            <button class="primary" :disabled="procesando||!formAsignacion.tecnico_id" @click="designarRevision">Designar especialista</button>
          </div>
        </div>
      </section>

      <section v-else-if="vista==='compra'">
        <div class="instruction"><b>Evaluar viabilidad de compra</b><span>El especialista ya solicitó el componente con su cotización. Confirme si es viable antes de generar el expediente de Compra Caja Chica.</span></div>
        <div v-if="!ticketActivo" class="cards">
          <article v-for="t in pendientesViabilidad" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ t.estado_codigo }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <p>{{ t.componente_requerido }} — Bs. {{ t.costo_estimado || 's/d' }}</p>
            <div class="actions"><button class="primary" @click="ticketActivo=t;formCompra.viable=true;formCompra.motivo_no_viable=''">Evaluar</button></div>
          </article>
          <div v-if="!pendientesViabilidad.length" class="empty"><span>✓</span><h3>Sin pendientes</h3><p>Ningún requerimiento de componente esperando evaluación.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ ticketActivo.codigo }} — {{ ticketActivo.titulo }}</h3>
          <p class="copy"><b>Componente:</b> {{ ticketActivo.componente_requerido }}<br><b>Especificaciones:</b> {{ ticketActivo.especificaciones_tecnicas || 's/d' }}<br><b>Costo estimado:</b> Bs. {{ ticketActivo.costo_estimado || 's/d' }}</p>
          <label class="campo">¿Es viable la compra?
            <select v-model="formCompra.viable">
              <option :value="true">Sí, es viable</option>
              <option :value="false">No es viable</option>
            </select>
          </label>
          <label v-if="formCompra.viable===false" class="campo">Motivo de no viabilidad<textarea v-model="formCompra.motivo_no_viable" rows="2"></textarea></label>
          <div class="actions">
            <button @click="ticketActivo=null">Cancelar</button>
            <button class="primary" :disabled="procesando||(formCompra.viable===false&&!formCompra.motivo_no_viable.trim())" @click="evaluarViabilidad">{{ formCompra.viable===false ? 'Cerrar sin compra' : 'Generar expediente de compra' }}</button>
          </div>
        </div>
      </section>

      <section v-else-if="vista==='informe'">
        <div class="instruction"><b>Elaborar y validar informe final</b><span>Redacte el informe de cierre del expediente técnico.</span></div>
        <div v-if="!ticketActivo" class="cards">
          <article v-for="t in cerradosSinInforme" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>CERRADO</em></div>
            <h3>{{ t.titulo }}</h3>
            <div class="actions"><button class="primary" @click="ticketActivo=t;formInforme.informe_final=''">Elaborar informe</button></div>
          </article>
          <div v-if="!cerradosSinInforme.length" class="empty"><span>✓</span><h3>Sin pendientes</h3><p>No hay tickets cerrados esperando informe final.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ ticketActivo.codigo }} — {{ ticketActivo.titulo }}</h3>
          <label class="campo">Informe final<textarea v-model="formInforme.informe_final" rows="5" placeholder="Resumen técnico del caso, causa raíz y solución aplicada"></textarea></label>
          <div class="actions">
            <button @click="ticketActivo=null">Cancelar</button>
            <button class="primary" :disabled="procesando||!formInforme.informe_final.trim()" @click="elaborarInformeFinal">Guardar informe final</button>
          </div>
        </div>
      </section>

      <section v-else-if="vista==='delegar'">
        <DelegacionesPanel rol-codigo="JEFE_UTIC" rol-nombre="Jefe de UTIC" />
      </section>
    </main>

    <div v-if="ticketDetalle" class="detalle-modal-backdrop" @click.self="ticketDetalle=null">
      <div class="detalle-modal">
        <div class="detalle-modal-header">
          <div><h3>{{ ticketDetalle.codigo }}</h3><small>{{ ticketDetalle.titulo }}</small></div>
          <button class="detalle-modal-close" @click="ticketDetalle=null">✕</button>
        </div>
        <div class="detalle-modal-body">
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Estado</b><span>{{ ticketDetalle.estado_nombre }}</span></div>
            <div class="detalle-campo"><b>Prioridad</b><span>{{ ticketDetalle.prioridad || 's/d' }}</span></div>
          </div>
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Solicitante</b><span>{{ ticketDetalle.solicitante_nombre }}</span></div>
            <div class="detalle-campo"><b>Especialista asignado</b><span>{{ ticketDetalle.tecnico_nombre || 's/d' }}</span></div>
          </div>
          <div class="detalle-campo"><b>Descripción</b><p>{{ ticketDetalle.descripcion || 's/d' }}</p></div>
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Ubicación</b><span>{{ ticketDetalle.ubicacion || 's/d' }}</span></div>
            <div class="detalle-campo"><b>Equipo afectado</b><span>{{ ticketDetalle.equipo_afectado || 's/d' }}</span></div>
          </div>
          <div class="detalle-campo" v-if="ticketDetalle.criterio_tecnico"><b>Criterio de validación</b><p>{{ ticketDetalle.criterio_tecnico }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.diagnostico"><b>Diagnóstico</b><p>{{ ticketDetalle.diagnostico }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.plan_solucion"><b>Plan de solución</b><p>{{ ticketDetalle.plan_solucion }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.componente_requerido"><b>Componente requerido</b><p>{{ ticketDetalle.componente_requerido }} — {{ ticketDetalle.especificaciones_tecnicas || 'sin especificaciones' }} — Bs. {{ ticketDetalle.costo_estimado || 's/d' }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.codigo_compra_vinculada"><b>Expediente de compra</b><span>{{ ticketDetalle.codigo_compra_vinculada }}</span></div>
          <div class="detalle-campo" v-if="ticketDetalle.solucion"><b>Intervención realizada</b><p>{{ ticketDetalle.solucion }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.resultado_pruebas"><b>Resultado de pruebas técnicas</b><p>{{ ticketDetalle.resultado_pruebas }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.observaciones_usuario"><b>Observaciones del solicitante</b><p>{{ ticketDetalle.observaciones_usuario }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.informe_final"><b>Informe final</b><p>{{ ticketDetalle.informe_final }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.evidencia_archivo_url"><b>Evidencia adjunta</b><a :href="ticketDetalle.evidencia_archivo_url" target="_blank">Abrir archivo →</a></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import DelegacionesPanel from '../components/DelegacionesPanel.vue'

const router = useRouter()
const usuario = ref(JSON.parse(localStorage.getItem('sigta_usuario') || '{}'))
const vista = ref('resumen')
const menuAbierto = ref(false)
const tickets = ref([])
const especialistas = ref([])
const cargando = ref(false)
const procesando = ref(false)
const busqueda = ref('')
const ticketActivo = ref(null)

const nombre = computed(() => usuario.value.nombre || usuario.value.nombre_completo || 'Jefe de UTIC')
const primerNombre = computed(() => nombre.value.split(' ')[0])
const iniciales = computed(() => nombre.value.split(' ').slice(0, 2).map(x => x[0]).join('').toUpperCase())
const saludo = computed(() => new Date().getHours() < 12 ? 'Buenos días' : new Date().getHours() < 19 ? 'Buenas tardes' : 'Buenas noches')

const porValidar = computed(() => tickets.value.filter(t => t.estado_codigo === 'NUEVO'))
const porClasificar = computed(() => tickets.value.filter(t => t.estado_codigo === 'EN_ANALISIS' && !t.prioridad))
const porAsignar = computed(() => tickets.value.filter(t => t.estado_codigo === 'EN_ANALISIS' && !!t.prioridad))
const pendientesViabilidad = computed(() => tickets.value.filter(t => t.estado_compra_componente === 'SOLICITADA'))
const cerradosSinInforme = computed(() => tickets.value.filter(t => t.estado_codigo === 'CERRADO' && !t.informe_final))

const menu = computed(() => [
  { id: 'resumen', icono: '⌂', nombre: 'Dashboard' },
  { id: 'validacion', icono: 'VA', nombre: 'Validar tickets', total: porValidar.value.length },
  { id: 'clasificacion', icono: 'CL', nombre: 'Clasificar prioridad', total: porClasificar.value.length },
  { id: 'asignacion', icono: 'AS', nombre: 'Asignar especialista', total: porAsignar.value.length },
  { id: 'compra', icono: 'CO', nombre: 'Validar y elevar compra', total: pendientesViabilidad.value.length },
  { id: 'informe', icono: 'IF', nombre: 'Informe final', total: cerradosSinInforme.value.length },
  { id: 'delegar', icono: 'DL', nombre: 'Delegar aprobación' },
])

const titulo = computed(() => ({
  resumen: 'Dashboard del Jefe de UTIC',
  validacion: 'Validar tickets',
  clasificacion: 'Clasificar prioridad y SLA',
  asignacion: 'Asignar especialista',
  compra: 'Validar y elevar compra',
  informe: 'Elaborar informe final',
  delegar: 'Delegar aprobación temporal',
}[vista.value]))

function filtrar(lista) {
  if (!busqueda.value.trim()) return lista
  return lista.filter(t => JSON.stringify(t).toLowerCase().includes(busqueda.value.toLowerCase()))
}

function headersJson() {
  return { Authorization: `Token ${localStorage.getItem('sigta_token')}`, 'Content-Type': 'application/json' }
}

async function cargar() {
  cargando.value = true
  try {
    const r = await fetch('/api/soporte/tickets/', { headers: { Authorization: `Token ${localStorage.getItem('sigta_token')}` } })
    const d = await r.json()
    tickets.value = Array.isArray(d) ? d : (d.results || [])
    const re = await fetch('/api/usuarios/usuarios-por-rol/?rol=ESPECIALISTA', { headers: { Authorization: `Token ${localStorage.getItem('sigta_token')}` } })
    especialistas.value = re.ok ? await re.json() : []
  } finally {
    cargando.value = false
  }
}

function salir() {
  localStorage.removeItem('sigta_token')
  localStorage.removeItem('sigta_usuario')
  router.push('/login')
}

async function postAccion(ticket, endpoint, body) {
  procesando.value = true
  try {
    const r = await fetch(`/api/soporte/tickets/${ticket.id}/${endpoint}/`, { method: 'POST', headers: headersJson(), body: JSON.stringify(body || {}) })
    const d = await r.json().catch(() => ({}))
    if (!r.ok) throw new Error(d.detalle || Object.values(d)[0] || 'No fue posible completar la acción.')
    await cargar()
    ticketActivo.value = null
    return d
  } finally {
    procesando.value = false
  }
}

const ticketDetalle = ref(null)
function verTicket(t) {
  ticketDetalle.value = t
}

async function validarTicket(t) {
  try {
    await postAccion(t, 'validar-ticket', { es_valido: true })
  } catch (e) { alert(e.message) }
}

async function rechazarTicket(t) {
  const motivo = prompt('Indique el motivo del rechazo:')
  if (!motivo?.trim()) return
  try {
    await postAccion(t, 'validar-ticket', { es_valido: false, motivo_rechazo: motivo.trim() })
  } catch (e) { alert(e.message) }
}

const formClasificacion = reactive({ prioridad: '', criterio_tecnico: '' })
async function clasificarTicket() {
  try {
    await postAccion(ticketActivo.value, 'clasificar-prioridad', { prioridad: formClasificacion.prioridad, criterio_tecnico: formClasificacion.criterio_tecnico.trim() })
  } catch (e) { alert(e.message) }
}

const formAsignacion = reactive({ tecnico_id: '' })
async function designarRevision() {
  try {
    await postAccion(ticketActivo.value, 'designar-revision', { tecnico_id: Number(formAsignacion.tecnico_id), especialistas_apoyo: [] })
  } catch (e) { alert(e.message) }
}

const formCompra = reactive({ viable: true, motivo_no_viable: '' })
async function evaluarViabilidad() {
  try {
    const d = await postAccion(ticketActivo.value, 'evaluar-viabilidad-compra', {
      viable: formCompra.viable,
      motivo_no_viable: formCompra.motivo_no_viable.trim(),
    })
    if (d) {
      if (formCompra.viable) alert(`Expediente de compra ${d.ticket?.codigo_compra_vinculada || ''} generado y vinculado al ticket.`)
      else alert('Compra marcada como no viable. El ticket se cerró sin compra.')
    }
  } catch (e) { alert(e.message) }
}

const formInforme = reactive({ informe_final: '' })
async function elaborarInformeFinal() {
  try {
    await postAccion(ticketActivo.value, 'elaborar-informe-final', { informe_final: formInforme.informe_final.trim() })
  } catch (e) { alert(e.message) }
}

onMounted(cargar)
</script>

<style scoped>
*{box-sizing:border-box}.layout{min-height:100vh;background:#f5f6fa;color:#232f4a;font-family:Inter,Segoe UI,sans-serif}aside{position:fixed;inset:0 auto 0 0;width:278px;background:#222f55;color:white;padding:22px 16px;display:flex;flex-direction:column}.brand,.profile{display:flex;align-items:center;gap:12px}.brand{padding:0 10px 20px;border-bottom:1px solid #ffffff20}.brand>b{background:#e6b941;color:#243155;padding:14px 10px;border-radius:9px}.brand strong,.brand small,.profile b,.profile small{display:block}.brand strong{font-size:23px}.brand small,.profile small{color:#c0c9e1;margin-top:3px}.profile{padding:22px 10px}.profile>i{width:42px;height:42px;border-radius:50%;background:#e6b941;color:#253154;display:grid;place-items:center;font-style:normal;font-weight:900}aside>p{font-size:10px;color:#929fc5;font-weight:800;letter-spacing:1.4px;margin:14px 10px 8px}aside button{border:0;background:transparent;color:#dfe4f2;border-radius:8px;padding:12px;display:flex;gap:11px;align-items:center;text-align:left;cursor:pointer;margin:2px 0;width:100%}aside button>span{font-size:10px;font-weight:900;width:28px}aside button em{margin-left:auto;background:#ffffff1c;padding:2px 8px;border-radius:10px;font-style:normal}aside button.active,aside button:hover{background:#ffffff14;box-shadow:inset 3px 0 #e6b941}.bottom{margin-top:auto;border-top:1px solid #ffffff20;padding-top:10px}.bottom button{width:100%}main{margin-left:278px;padding:30px 38px 55px;max-width:1650px}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:27px}header small{color:#78839e}h1{font-size:29px;margin:6px 0}header p{margin:0;color:#737e96}.refresh{border:1px solid #d9deea;background:white;color:#313e69;padding:10px 14px;border-radius:8px}.hero{background:linear-gradient(120deg,#25335a,#3b4d7d);color:white;border-radius:13px;padding:28px 30px;display:flex;justify-content:space-between;align-items:center}.hero small,.panel-head small{font-size:10px;font-weight:800;letter-spacing:1.4px;color:#edc65a}.hero h2{font-size:24px;margin:7px 0}.hero p{margin:0;color:#dce1ee}.hero>span{width:68px;height:68px;border:1px solid #edc65a88;border-radius:50%;display:grid;place-items:center;font-weight:900}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:18px 0}.stats article{background:white;border:1px solid #e0e3ec;border-radius:10px;padding:19px;display:flex;gap:13px}.stats i,.flow i{font-style:normal;width:37px;height:37px;border-radius:8px;display:grid;place-items:center;color:white;font-size:10px;font-weight:900}.blue{background:#3b7fba}.gold{background:#c89c2d}.green{background:#38936e}.navy{background:#34456e}.stats small,.stats b,.stats p{display:block}.stats b{font-size:25px;margin:3px 0}.stats p{font-size:11px;color:#858da0;margin:0}.panels{display:grid;grid-template-columns:2fr 1fr;gap:18px}.panel{background:white;border:1px solid #e0e3ec;border-radius:11px;padding:22px}.panel-head h3{margin:5px 0 14px}.flow{width:100%;border:0;border-top:1px solid #e9ebf1;background:white;padding:15px 2px;display:flex;gap:13px;align-items:center;text-align:left;cursor:pointer}.flow div{flex:1}.flow b,.flow small{display:block}.flow small{color:#81899b;margin-top:4px}.flow>strong{font-size:20px}.copy{color:#707b91;font-size:12px;line-height:1.7}.wide{width:100%;padding:10px;border-radius:7px}.toolbar{display:flex;justify-content:space-between;margin-bottom:17px}.toolbar label{width:350px;background:white;border:1px solid #d9deea;border-radius:8px;padding:9px 12px}.toolbar input{border:0;outline:0;margin-left:7px;width:88%}.primary{background:#293b67!important;color:white!important;border-color:#293b67!important}.instruction{background:#fff8e7;border-left:4px solid #d4a632;padding:14px 17px;margin-bottom:17px;border-radius:7px}.instruction b,.instruction span{display:block}.instruction span{font-size:12px;color:#766b4d;margin-top:4px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.cards article{background:white;border:1px solid #dfe3eb;border-radius:10px;padding:19px}.top{display:flex;justify-content:space-between}.top span{font-size:12px;font-weight:800;color:#3d5d96}.top em{font-size:10px;background:#eff0f5;padding:4px 8px;border-radius:10px;font-style:normal}.cards h3{font-size:17px;margin:15px 0 7px}.cards article>p{font-size:12px;color:#778096;min-height:42px}.actions{display:flex;gap:7px;border-top:1px solid #e8eaf0;padding-top:13px;margin-top:10px}.actions button{flex:1;padding:9px 6px;border-radius:7px;border:1px solid #cdd3e0;background:white;color:#3e4b69;font-weight:700;cursor:pointer}.reject{color:#af4b4b!important;border-color:#e3bcbc!important}.empty{text-align:center;background:white;border:1px dashed #cbd0dc;padding:65px;border-radius:10px;color:#798196}.empty>span{font-size:31px;color:#38936e}.campo{display:block;margin:14px 0;font-size:12px;font-weight:700;color:#465170}.campo input,.campo select,.campo textarea{display:block;width:100%;margin-top:6px;padding:9px 11px;border:1px solid #d9deea;border-radius:7px;font-family:inherit;font-size:13px;font-weight:400;color:#232f4a}@media(max-width:1050px){.stats{grid-template-columns:1fr 1fr}.panels{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}}@media(max-width:720px){aside{position:static;width:100%}main{margin:0;padding:20px}.stats,.cards{grid-template-columns:1fr}.toolbar,header{align-items:flex-start;flex-direction:column;gap:12px}.toolbar label{width:100%}}
</style>
