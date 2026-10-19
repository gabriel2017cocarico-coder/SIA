<template>
  <div class="layout sigta-role-layout">
    <aside :class="{ abierto: menuAbierto }">
      <div class="brand-row">
        <div class="brand"><b><img src="/img/emi.jpg" alt="EMI"></b><div><strong>SIGTA</strong><small>Soporte Técnico</small></div></div>
        <button type="button" class="menu-toggle" :aria-expanded="menuAbierto" aria-label="Mostrar opciones del menú" @click="menuAbierto = !menuAbierto"><span></span><span></span><span></span></button>
      </div>
      <div class="profile"><i>{{ iniciales }}</i><div><b>{{ nombre }}</b><small>Especialista</small></div></div>
      <p>MI TRABAJO</p>
      <button v-for="m in menu" :key="m.id" :class="{active:vista===m.id}" @click="irA(m.id)"><span>{{ m.icono }}</span>{{ m.nombre }}<em v-if="m.total!==undefined">{{ m.total }}</em></button>
      <div class="bottom"><button @click="salir"><span>↪</span>Cerrar sesión</button></div>
    </aside>

    <main>
      <header>
        <div><small>SIGTA / SOPORTE / {{ titulo }}</small><h1>{{ titulo }}</h1><p>{{ subtitulo }}</p></div>
        <button class="refresh" :disabled="cargando" @click="cargar">↻ Actualizar</button>
      </header>

      <!-- ============================================================
           RESUMEN
      ============================================================= -->
      <section v-if="vista==='resumen'">
        <div class="hero">
          <div><small>ESPECIALISTA</small><h2>{{ saludo }}, {{ primerNombre }}</h2><p>Órdenes de trabajo que requieren su atención.</p></div>
          <span>TI</span>
        </div>

        <div v-if="conRetorno.length" class="alerta">
          <b>⚠ {{ conRetorno.length }} orden(es) devuelta(s): pruebas de usuario fallidas</b>
          <span>{{ conRetorno.map(t=>t.codigo).join(', ') }} — re-evalúe el equipo y repita la reparación.</span>
        </div>

        <div class="stats">
          <article @click="irA('ordenes')"><i class="blue">OT</i><div><small>Órdenes por recibir</small><b>{{ porRecibir.length }}</b><p>asignadas por la jefatura</p></div></article>
          <article @click="irA('trabajo')"><i class="gold">RP</i><div><small>En reparación</small><b>{{ porIntervenir.length }}</b><p>hoja de trabajo abierta</p></div></article>
          <article @click="irA('trabajo')"><i class="green">PB</i><div><small>Por probar</small><b>{{ porProbar.length }}</b><p>pruebas e informe</p></div></article>
          <article @click="irA('compras')"><i class="navy">CO</i><div><small>En espera de compra</small><b>{{ esperandoCompra.length }}</b><p>flujo en pausa</p></div></article>
        </div>

        <div class="panels">
          <section class="panel">
            <div class="panel-head"><div><small>FLUJO BPMN</small><h3>Atención técnica</h3></div></div>
            <button class="flow" @click="irA('ordenes')"><i class="blue">1</i><div><b>Recibir orden de trabajo</b><small>Tomar conocimiento del ticket asignado por la jefatura</small></div><strong>›</strong></button>
            <button class="flow" @click="irA('ordenes')"><i class="blue">2</i><div><b>Realizar inspección técnica y diagnóstico</b><small>Registrar el diagnóstico y definir si requiere compra</small></div><strong>›</strong></button>
            <button class="flow" @click="irA('compras')"><i class="navy">3</i><div><b>Realizar requerimiento de componente</b><small>Características y cotización, si el diagnóstico lo exige</small></div><strong>›</strong></button>
            <button class="flow" @click="irA('trabajo')"><i class="gold">4</i><div><b>Reparar o instalar y registrar</b><small>Documentar la intervención técnica aplicada</small></div><strong>›</strong></button>
            <button class="flow" @click="irA('trabajo')"><i class="green">5</i><div><b>Pruebas técnicas e informe a jefatura</b><small>Verificar el equipo y elevar el descargo técnico</small></div><strong>›</strong></button>
          </section>
          <section class="panel">
            <div class="panel-head"><div><small>APOYO</small><h3>Tickets donde participo</h3></div></div>
            <p class="copy">Además de sus órdenes como responsable, puede colaborar como especialista de apoyo en otros tickets.</p>
            <button class="wide primary" @click="irA('apoyo')">Ver tickets de apoyo →</button>
          </section>
        </div>
      </section>

      <!-- ============================================================
           A. BANDEJA DE ÓRDENES DE TRABAJO
      ============================================================= -->
      <section v-else-if="vista==='ordenes' && !ordenAbierta">
        <div class="instruction"><b>Recibir orden de trabajo</b><span>Revise los datos y la evidencia cargados por el solicitante, y abra la hoja de trabajo para registrar el diagnóstico.</span></div>
        <div v-if="cargando" class="empty">Consultando órdenes…</div>
        <div v-else-if="porRecibir.length" class="cards">
          <article v-for="t in porRecibir" :key="t.id" :class="{ retorno: Number(t.rework_count) > 0 }">
            <div class="top"><span>{{ t.codigo }}</span><em :class="claseSla(t)">{{ etiquetaEstado(t) }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <ul class="datos">
              <li><b>Asignada</b><span>{{ fecha(t.asignado_en) }}</span></li>
              <li><b>Prioridad</b><span>{{ t.prioridad || 's/d' }}</span></li>
              <li><b>SLA</b><span>{{ textoSla(t) }}</span></li>
              <li><b>Ubicación</b><span>{{ t.ubicacion || 's/d' }}</span></li>
              <li><b>Equipo</b><span>{{ t.equipo_afectado || 's/d' }}</span></li>
            </ul>
            <p>{{ (t.descripcion||'').slice(0,150) }}</p>
            <a v-if="t.evidencia_archivo_url" class="adjunto" :href="t.evidencia_archivo_url" target="_blank">📎 Evidencia del solicitante</a>
            <div class="actions">
              <button @click="verTicket(t)">Ver detalle</button>
              <button class="primary" @click="recibirOrden(t)">Recibir orden de trabajo</button>
            </div>
          </article>
        </div>
        <div v-else class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No tiene órdenes de trabajo pendientes de recibir.</p></div>
      </section>

      <!-- ============================================================
           B / C. HOJA DE TRABAJO: DIAGNÓSTICO Y REQUERIMIENTO
      ============================================================= -->
      <section v-else-if="vista==='ordenes' && ordenAbierta" class="panel hoja">
        <div class="hoja-head">
          <div><small>ORDEN DE TRABAJO</small><h3>{{ ordenAbierta.codigo }} — {{ ordenAbierta.titulo }}</h3></div>
          <button class="refresh" @click="cerrarOrden">Cerrar hoja</button>
        </div>

        <div v-if="Number(ordenAbierta.rework_count) > 0" class="alerta">
          <b>⚠ Pruebas de usuario fallidas: re-evaluar equipo</b>
          <span>{{ ordenAbierta.observaciones_usuario || 'El solicitante reportó que el problema no fue resuelto.' }}</span>
        </div>

        <template v-if="!modoComponente">
          <label class="campo">Diagnóstico técnico inicial
            <textarea v-model="formDiagnostico.diagnostico" rows="4" placeholder="Resultado de la inspección técnica del equipo"></textarea>
          </label>
          <label class="campo">Plan de solución
            <textarea v-model="formDiagnostico.plan_solucion" rows="3" placeholder="Acciones previstas para resolver el problema"></textarea>
          </label>

          <fieldset class="compuerta">
            <legend>¿Requiere compra de repuestos o insumos?</legend>
            <label><input v-model="formDiagnostico.requiere_compra" type="radio" :value="false"> No</label>
            <label><input v-model="formDiagnostico.requiere_compra" type="radio" :value="true"> Sí</label>
          </fieldset>

          <div class="actions">
            <button @click="cerrarOrden">Cancelar</button>
            <button class="primary" :disabled="procesando || !formDiagnostico.diagnostico.trim() || !formDiagnostico.plan_solucion.trim()" @click="guardarDiagnostico">
              {{ formDiagnostico.requiere_compra ? 'Guardar y realizar requerimiento' : 'Guardar diagnóstico' }}
            </button>
          </div>
        </template>

        <template v-else>
          <div class="instruction"><b>Realizar requerimiento de componente</b><span>El flujo técnico quedará en pausa hasta que la jefatura evalúe la viabilidad y Almacén entregue el componente.</span></div>
          <label class="campo">Informe de requerimiento
            <textarea v-model="formComponente.componente_requerido" rows="2" placeholder="Componente o insumo solicitado"></textarea>
          </label>
          <label class="campo">Características del componente
            <textarea v-model="formComponente.especificaciones_tecnicas" rows="3" placeholder="Marca, modelo, capacidad y demás especificaciones técnicas"></textarea>
          </label>
          <label class="campo">Costo estimado (Bs.)
            <input v-model="formComponente.costo_estimado" type="number" min="0" step="0.01">
          </label>
          <label class="campo">Cotización / proforma
            <input type="file" accept="application/pdf,image/*" @change="onCotizacion">
          </label>
          <div class="actions">
            <button @click="cerrarOrden">Cancelar</button>
            <button class="primary" :disabled="procesando || !formComponente.componente_requerido.trim()" @click="enviarRequerimiento">Enviar requerimiento</button>
          </div>
        </template>
      </section>

      <!-- ============================================================
           EN ESPERA DE COMPRA
      ============================================================= -->
      <section v-else-if="vista==='compras'">
        <div class="instruction"><b>Requerimientos en curso</b><span>El flujo técnico está en pausa: se reanuda cuando Almacén registra la entrega del componente.</span></div>
        <div v-if="esperandoCompra.length" class="cards">
          <article v-for="t in esperandoCompra" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ etiquetaEstado(t) }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <ul class="datos">
              <li><b>Componente</b><span>{{ t.componente_requerido || 's/d' }}</span></li>
              <li><b>Costo estimado</b><span>{{ t.costo_estimado ? `Bs. ${t.costo_estimado}` : 's/d' }}</span></li>
              <li><b>Expediente</b><span>{{ t.codigo_compra_vinculada || 'aún no generado' }}</span></li>
            </ul>
            <p>{{ textoEspera(t) }}</p>
            <a v-if="t.cotizacion_archivo_url" class="adjunto" :href="t.cotizacion_archivo_url" target="_blank">📎 Cotización enviada</a>
            <div class="actions"><button @click="verTicket(t)">Ver detalle</button></div>
          </article>
        </div>
        <div v-else class="empty"><span>✓</span><h3>Sin requerimientos en curso</h3><p>Ninguna orden suya está esperando una compra.</p></div>
      </section>

      <!-- ============================================================
           D. REPARACIÓN, PRUEBAS E INFORME
      ============================================================= -->
      <section v-else-if="vista==='trabajo'">
        <div class="instruction"><b>Reparación, pruebas e informe técnico</b><span>Documente la intervención, registre las pruebas y eleve el descargo a la jefatura.</span></div>

        <div v-if="!ticketActivo" class="cards">
          <article v-for="t in enTrabajo" :key="t.id" :class="{ retorno: Number(t.rework_count) > 0 }">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ etiquetaEstado(t) }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <div v-if="Number(t.rework_count) > 0" class="mini-alerta">⚠ Pruebas de usuario fallidas: re-evaluar equipo</div>
            <ul class="datos">
              <li><b>Prioridad</b><span>{{ t.prioridad || 's/d' }}</span></li>
              <li><b>SLA</b><span>{{ textoSla(t) }}</span></li>
              <li v-if="t.componente_entregado_en"><b>Componente</b><span>entregado {{ fecha(t.componente_entregado_en) }}</span></li>
            </ul>
            <p>{{ (t.diagnostico||t.descripcion||'').slice(0,150) }}</p>
            <div class="actions">
              <button @click="verTicket(t)">Ver detalle</button>
              <button class="primary" @click="abrirTrabajo(t)">{{ t.solucion ? 'Pruebas e informe' : 'Registrar reparación' }}</button>
            </div>
          </article>
          <div v-if="!enTrabajo.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay órdenes en reparación ni pendientes de pruebas.</p></div>
        </div>

        <div v-else class="panel hoja">
          <div class="hoja-head">
            <div><small>HOJA DE TRABAJO</small><h3>{{ ticketActivo.codigo }} — {{ ticketActivo.titulo }}</h3></div>
            <button class="refresh" @click="ticketActivo=null">Volver</button>
          </div>

          <div v-if="Number(ticketActivo.rework_count) > 0" class="alerta">
            <b>⚠ Pruebas de usuario fallidas: re-evaluar equipo</b>
            <span>{{ ticketActivo.observaciones_usuario || 'El solicitante reportó que el problema no fue resuelto.' }}</span>
          </div>

          <template v-if="!ticketActivo.solucion">
            <label class="campo">Detalles de la reparación o instalación realizada
              <textarea v-model="formIntervencion.solucion" rows="5" placeholder="Acciones correctivas aplicadas sobre el equipo"></textarea>
            </label>
            <div class="actions">
              <button @click="ticketActivo=null">Cancelar</button>
              <button class="primary" :disabled="procesando || !formIntervencion.solucion.trim()" @click="registrarIntervencion">Guardar reparación</button>
            </div>
          </template>

          <template v-else>
            <p class="copy"><b>Reparación registrada:</b> {{ ticketActivo.solucion }}</p>
            <label class="campo">Resultados de las pruebas técnicas
              <textarea v-model="formPruebas.resultado_pruebas" rows="4" placeholder="Pruebas efectuadas y comportamiento del equipo"></textarea>
            </label>
            <label class="campo">Informe técnico dirigido a la jefatura
              <textarea v-model="formPruebas.informe_tecnico" rows="4" placeholder="Descargo técnico del trabajo realizado"></textarea>
            </label>
            <div class="actions">
              <button @click="ticketActivo=null">Cancelar</button>
              <button class="primary" :disabled="procesando || !formPruebas.resultado_pruebas.trim() || !formPruebas.informe_tecnico.trim()" @click="enviarInformeTecnico">Enviar informe técnico</button>
            </div>
          </template>
        </div>
      </section>

      <!-- ============================================================
           APOYO
      ============================================================= -->
      <section v-else-if="vista==='apoyo'">
        <div class="instruction"><b>Tickets de apoyo</b><span>Órdenes donde usted colabora como especialista de apoyo; el responsable es otro técnico.</span></div>
        <div v-if="ticketsApoyo.length" class="cards">
          <article v-for="t in ticketsApoyo" :key="t.id">
            <div class="top"><span>{{ t.codigo }}</span><em>{{ etiquetaEstado(t) }}</em></div>
            <h3>{{ t.titulo }}</h3>
            <p>{{ (t.descripcion||'').slice(0,150) }}</p>
            <div class="actions"><button @click="verTicket(t)">Ver detalle</button></div>
          </article>
        </div>
        <div v-else class="empty"><span>✓</span><h3>Sin tickets de apoyo</h3><p>No participa como apoyo en ninguna orden.</p></div>
      </section>
    </main>

    <!-- ==============================================================
         DETALLE
    =============================================================== -->
    <div v-if="ticketDetalle" class="detalle-modal-backdrop" @click.self="ticketDetalle=null">
      <div class="detalle-modal">
        <div class="detalle-modal-header">
          <div><h3>{{ ticketDetalle.codigo }}</h3><small>{{ ticketDetalle.titulo }}</small></div>
          <button class="detalle-modal-close" @click="ticketDetalle=null">✕</button>
        </div>
        <div class="detalle-modal-body">
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Estado</b><span>{{ etiquetaEstado(ticketDetalle) }}</span></div>
            <div class="detalle-campo"><b>Prioridad</b><span>{{ ticketDetalle.prioridad || 's/d' }}</span></div>
          </div>
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Solicitante</b><span>{{ ticketDetalle.solicitante_nombre }}</span></div>
            <div class="detalle-campo"><b>SLA</b><span>{{ textoSla(ticketDetalle) }}</span></div>
          </div>
          <div class="detalle-campo"><b>Descripción</b><p>{{ ticketDetalle.descripcion || 's/d' }}</p></div>
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Ubicación</b><span>{{ ticketDetalle.ubicacion || 's/d' }}</span></div>
            <div class="detalle-campo"><b>Equipo afectado</b><span>{{ ticketDetalle.equipo_afectado || 's/d' }}</span></div>
          </div>
          <div class="detalle-campo" v-if="ticketDetalle.diagnostico"><b>Diagnóstico</b><p>{{ ticketDetalle.diagnostico }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.plan_solucion"><b>Plan de solución</b><p>{{ ticketDetalle.plan_solucion }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.componente_requerido"><b>Componente requerido</b><p>{{ ticketDetalle.componente_requerido }} — {{ ticketDetalle.especificaciones_tecnicas || 'sin especificaciones' }} — Bs. {{ ticketDetalle.costo_estimado || 's/d' }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.motivo_no_viable"><b>Compra no viable</b><p>{{ ticketDetalle.motivo_no_viable }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.codigo_compra_vinculada"><b>Expediente de compra</b><span>{{ ticketDetalle.codigo_compra_vinculada }}</span></div>
          <div class="detalle-campo" v-if="ticketDetalle.solucion"><b>Intervención realizada</b><p>{{ ticketDetalle.solucion }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.resultado_pruebas"><b>Resultado de pruebas técnicas</b><p>{{ ticketDetalle.resultado_pruebas }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.informe_tecnico"><b>Informe técnico</b><p>{{ ticketDetalle.informe_tecnico }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.observaciones_usuario"><b>Observaciones del solicitante</b><p>{{ ticketDetalle.observaciones_usuario }}</p></div>
          <div class="detalle-campo" v-if="ticketDetalle.evidencia_archivo_url"><b>Evidencia adjunta</b><a :href="ticketDetalle.evidencia_archivo_url" target="_blank">Abrir archivo →</a></div>
          <div class="detalle-campo" v-if="ticketDetalle.cotizacion_archivo_url"><b>Cotización</b><a :href="ticketDetalle.cotizacion_archivo_url" target="_blank">Abrir archivo →</a></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const usuario = ref(JSON.parse(localStorage.getItem('sigta_usuario') || '{}'))
const vista = ref('resumen')
const menuAbierto = ref(false)
const tickets = ref([])
const cargando = ref(false)
const procesando = ref(false)
const ticketActivo = ref(null)
const ordenAbierta = ref(null)
const modoComponente = ref(false)
const ticketDetalle = ref(null)

const nombre = computed(() => usuario.value.nombre || usuario.value.nombre_completo || 'Especialista')
const primerNombre = computed(() => nombre.value.split(' ')[0])
const iniciales = computed(() => nombre.value.split(' ').slice(0, 2).map(x => x[0]).join('').toUpperCase())
const saludo = computed(() => new Date().getHours() < 12 ? 'Buenos días' : new Date().getHours() < 19 ? 'Buenas tardes' : 'Buenas noches')

/* ==========================================================
   BANDEJAS

   Los estados del BPMN se muestran como etiquetas sobre los
   estados reales del ticket: no existe un EN_DIAGNOSTICO ni un
   EN_ESPERA_DE_COMPRA en la base de datos, sino ASIGNADO y
   EN_EJECUCION combinados con el estado del requerimiento de
   componente (SOLICITADA / VIABLE / ENTREGADA).
========================================================== */

const misTickets = computed(() => tickets.value.filter(t => Number(t.tecnico_asignado) === Number(usuario.value.id)))

// "Esperando compra": el requerimiento fue enviado y todavía no llega el
// componente. Mientras tanto el backend rechaza registrar la intervención.
const enEsperaDeCompra = t => ['SOLICITADA', 'VIABLE'].includes(t.estado_compra_componente)

const porRecibir = computed(() => misTickets.value.filter(t => t.estado_codigo === 'ASIGNADO'))
const esperandoCompra = computed(() => misTickets.value.filter(t => t.estado_codigo === 'EN_EJECUCION' && enEsperaDeCompra(t)))
const porIntervenir = computed(() => misTickets.value.filter(t => t.estado_codigo === 'EN_EJECUCION' && !t.solucion && !enEsperaDeCompra(t)))
const porProbar = computed(() => misTickets.value.filter(t => t.estado_codigo === 'EN_EJECUCION' && !!t.solucion))
const enTrabajo = computed(() => [...porIntervenir.value, ...porProbar.value])
const conRetorno = computed(() => misTickets.value.filter(t => Number(t.rework_count) > 0 && t.estado_codigo === 'EN_EJECUCION'))
const ticketsApoyo = computed(() => tickets.value.filter(t => (t.especialistas_apoyo || []).map(Number).includes(Number(usuario.value.id))))

const menu = computed(() => [
  { id: 'resumen', icono: '⌂', nombre: 'Resumen' },
  { id: 'ordenes', icono: 'OT', nombre: 'Órdenes de trabajo', total: porRecibir.value.length },
  { id: 'trabajo', icono: 'RP', nombre: 'Reparación y pruebas', total: enTrabajo.value.length },
  { id: 'compras', icono: 'CO', nombre: 'En espera de compra', total: esperandoCompra.value.length },
  { id: 'apoyo', icono: 'AP', nombre: 'Tickets de apoyo', total: ticketsApoyo.value.length },
])

const titulo = computed(() => ({
  resumen: 'Panel del Especialista',
  ordenes: ordenAbierta.value ? 'Inspección y diagnóstico' : 'Bandeja de órdenes de trabajo',
  trabajo: 'Reparación, pruebas e informe',
  compras: 'Requerimientos en espera de compra',
  apoyo: 'Tickets de apoyo',
}[vista.value]))

const subtitulo = computed(() => ({
  resumen: 'Diagnóstico, reparación y pruebas técnicas de las órdenes asignadas a usted.',
  ordenes: 'Órdenes designadas por la jefatura tras clasificar prioridad y SLA.',
  trabajo: 'Intervención técnica y descargo dirigido a la jefatura.',
  compras: 'Órdenes cuyo flujo técnico está en pausa hasta recibir el componente.',
  apoyo: 'Órdenes donde colabora como especialista de apoyo.',
}[vista.value]))

/* ==========================================================
   ETIQUETAS DEL BPMN
========================================================== */

function etiquetaEstado(t) {
  if (!t) return ''
  if (t.estado_codigo === 'ASIGNADO') return Number(t.rework_count) > 0 ? 'Reasignada' : 'Orden asignada'
  if (t.estado_codigo === 'EN_EJECUCION') {
    if (t.estado_compra_componente === 'SOLICITADA') return 'Requiere compra'
    if (t.estado_compra_componente === 'VIABLE') return 'En espera de compra'
    if (t.estado_compra_componente === 'ENTREGADA' && !t.solucion) return 'Repuestos entregados'
    return t.solucion ? 'Por probar' : 'En reparación'
  }
  if (t.estado_codigo === 'EN_VERIFICACION') return 'En verificación de jefatura'
  return t.estado_nombre || t.estado_codigo
}

function textoEspera(t) {
  if (t.estado_compra_componente === 'SOLICITADA') return 'Pendiente de que la jefatura evalúe la viabilidad de la compra.'
  return 'Compra en curso: el componente será entregado por Almacén.'
}

function textoSla(t) {
  if (!t?.sla_horas) return 's/d'
  const minutos = Number(t.sla_restante_minutos)
  if (!Number.isFinite(minutos)) return `${t.sla_horas} h`
  if (minutos <= 0) return `${t.sla_horas} h · vencido`
  return `${t.sla_horas} h · quedan ${Math.floor(minutos / 60)}h ${minutos % 60}m`
}

function claseSla(t) {
  return Number(t?.sla_restante_minutos) <= 0 ? 'vencido' : ''
}

function fecha(valor) {
  return valor ? new Date(valor).toLocaleDateString('es-BO', { day: '2-digit', month: 'short', year: 'numeric' }) : 's/d'
}

/* ==========================================================
   DATOS
========================================================== */

function token() { return localStorage.getItem('sigta_token') }

async function cargar() {
  cargando.value = true
  try {
    const r = await fetch('/api/soporte/tickets/', { headers: { Authorization: `Token ${token()}` } })
    const d = await r.json()
    tickets.value = Array.isArray(d) ? d : (d.results || [])
    // Mantiene sincronizada la orden abierta tras cada acción.
    if (ordenAbierta.value) ordenAbierta.value = tickets.value.find(t => t.id === ordenAbierta.value.id) || null
    if (ticketActivo.value) ticketActivo.value = tickets.value.find(t => t.id === ticketActivo.value.id) || null
  } finally {
    cargando.value = false
  }
}

async function postAccion(ticket, endpoint, body, esFormData = false) {
  procesando.value = true
  try {
    const headers = { Authorization: `Token ${token()}` }
    if (!esFormData) headers['Content-Type'] = 'application/json'
    const r = await fetch(`/api/soporte/tickets/${ticket.id}/${endpoint}/`, {
      method: 'POST',
      headers,
      body: esFormData ? body : JSON.stringify(body || {}),
    })
    const d = await r.json().catch(() => ({}))
    if (!r.ok) throw new Error(d.detalle || Object.values(d)[0] || 'No fue posible completar la acción.')
    await cargar()
    return d
  } finally {
    procesando.value = false
  }
}

function irA(id) {
  vista.value = id
  menuAbierto.value = false
  ordenAbierta.value = null
  ticketActivo.value = null
  modoComponente.value = false
}

function salir() {
  localStorage.removeItem('sigta_token')
  localStorage.removeItem('sigta_usuario')
  router.push('/login')
}

function verTicket(t) { ticketDetalle.value = t }

/* ==========================================================
   A. RECIBIR ORDEN DE TRABAJO
========================================================== */

const formDiagnostico = reactive({ diagnostico: '', plan_solucion: '', requiere_compra: false })
const formComponente = reactive({ componente_requerido: '', especificaciones_tecnicas: '', costo_estimado: '', archivo: null })
const formIntervencion = reactive({ solucion: '' })
const formPruebas = reactive({ resultado_pruebas: '', informe_tecnico: '' })

function recibirOrden(t) {
  ordenAbierta.value = t
  modoComponente.value = false
  formDiagnostico.diagnostico = ''
  formDiagnostico.plan_solucion = ''
  formDiagnostico.requiere_compra = false
  formComponente.componente_requerido = ''
  formComponente.especificaciones_tecnicas = ''
  formComponente.costo_estimado = ''
  formComponente.archivo = null
}

function cerrarOrden() {
  ordenAbierta.value = null
  modoComponente.value = false
}

/* ==========================================================
   B. DIAGNÓSTICO Y COMPUERTA "¿REQUIERE COMPRA?"
========================================================== */

async function guardarDiagnostico() {
  try {
    await postAccion(ordenAbierta.value, 'registrar-diagnostico', {
      diagnostico: formDiagnostico.diagnostico.trim(),
      plan_solucion: formDiagnostico.plan_solucion.trim(),
    })
    if (formDiagnostico.requiere_compra) {
      // El requerimiento se registra sobre el ticket ya en ejecución.
      modoComponente.value = true
    } else {
      cerrarOrden()
      vista.value = 'trabajo'
    }
  } catch (e) { alert(e.message) }
}

/* ==========================================================
   C. REQUERIMIENTO DE COMPONENTE
========================================================== */

function onCotizacion(evento) {
  formComponente.archivo = evento.target.files?.[0] || null
}

async function enviarRequerimiento() {
  try {
    const datos = new FormData()
    datos.append('componente_requerido', formComponente.componente_requerido.trim())
    datos.append('especificaciones_tecnicas', formComponente.especificaciones_tecnicas.trim())
    if (formComponente.costo_estimado) datos.append('costo_estimado', formComponente.costo_estimado)
    if (formComponente.archivo) datos.append('cotizacion_archivo', formComponente.archivo)
    await postAccion(ordenAbierta.value, 'solicitar-requerimiento-componente', datos, true)
    cerrarOrden()
    vista.value = 'compras'
    alert('Requerimiento enviado. El flujo técnico queda en pausa hasta la entrega del componente.')
  } catch (e) { alert(e.message) }
}

/* ==========================================================
   D. REPARACIÓN, PRUEBAS E INFORME TÉCNICO
========================================================== */

function abrirTrabajo(t) {
  ticketActivo.value = t
  formIntervencion.solucion = ''
  formPruebas.resultado_pruebas = ''
  formPruebas.informe_tecnico = ''
}

async function registrarIntervencion() {
  try {
    await postAccion(ticketActivo.value, 'registrar-intervencion', { solucion: formIntervencion.solucion.trim() })
  } catch (e) { alert(e.message) }
}

async function enviarInformeTecnico() {
  try {
    await postAccion(ticketActivo.value, 'pruebas-tecnicas', {
      resultado_pruebas: formPruebas.resultado_pruebas.trim(),
      informe_tecnico: formPruebas.informe_tecnico.trim(),
    })
    ticketActivo.value = null
    alert('Informe técnico enviado. La jefatura verificará el funcionamiento.')
  } catch (e) { alert(e.message) }
}

onMounted(cargar)
</script>

<style scoped>
*{box-sizing:border-box}.layout{min-height:100vh;background:#f5f6fa;color:#232f4a;font-family:Inter,Segoe UI,sans-serif}aside{position:fixed;inset:0 auto 0 0;width:278px;background:#222f55;color:white;padding:22px 16px;display:flex;flex-direction:column}.brand,.profile{display:flex;align-items:center;gap:12px}.brand{padding:0 10px 20px;border-bottom:1px solid #ffffff20}.brand>b{background:#e6b941;color:#243155;padding:14px 10px;border-radius:9px}.brand strong,.brand small,.profile b,.profile small{display:block}.brand strong{font-size:23px}.brand small,.profile small{color:#c0c9e1;margin-top:3px}.profile{padding:22px 10px}.profile>i{width:42px;height:42px;border-radius:50%;background:#e6b941;color:#253154;display:grid;place-items:center;font-style:normal;font-weight:900}aside>p{font-size:10px;color:#929fc5;font-weight:800;letter-spacing:1.4px;margin:14px 10px 8px}aside button{border:0;background:transparent;color:#dfe4f2;border-radius:8px;padding:12px;display:flex;gap:11px;align-items:center;text-align:left;cursor:pointer;margin:2px 0;width:100%}aside button>span{font-size:10px;font-weight:900;width:28px}aside button em{margin-left:auto;background:#ffffff1c;padding:2px 8px;border-radius:10px;font-style:normal}aside button.active,aside button:hover{background:#ffffff14;box-shadow:inset 3px 0 #e6b941}.bottom{margin-top:auto;border-top:1px solid #ffffff20;padding-top:10px}.bottom button{width:100%}main{margin-left:278px;padding:30px 38px 55px;max-width:1650px}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:27px}header small{color:#78839e}h1{font-size:29px;margin:6px 0}header p{margin:0;color:#737e96}.refresh{border:1px solid #d9deea;background:white;color:#313e69;padding:10px 14px;border-radius:8px;cursor:pointer}.hero{background:linear-gradient(120deg,#25335a,#3b4d7d);color:white;border-radius:13px;padding:28px 30px;display:flex;justify-content:space-between;align-items:center}.hero small,.panel-head small,.hoja-head small{font-size:10px;font-weight:800;letter-spacing:1.4px;color:#edc65a}.hero h2{font-size:24px;margin:7px 0}.hero p{margin:0;color:#dce1ee}.hero>span{width:68px;height:68px;border:1px solid #edc65a88;border-radius:50%;display:grid;place-items:center;font-weight:900}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:18px 0}.stats article{background:white;border:1px solid #e0e3ec;border-radius:10px;padding:19px;display:flex;gap:13px;cursor:pointer}.stats i,.flow i{font-style:normal;width:37px;height:37px;border-radius:8px;display:grid;place-items:center;color:white;font-size:10px;font-weight:900}.blue{background:#3b7fba}.gold{background:#c89c2d}.green{background:#38936e}.navy{background:#34456e}.stats small,.stats b,.stats p{display:block}.stats b{font-size:25px;margin:3px 0}.stats p{font-size:11px;color:#858da0;margin:0}.panels{display:grid;grid-template-columns:2fr 1fr;gap:18px}.panel{background:white;border:1px solid #e0e3ec;border-radius:11px;padding:22px}.panel-head h3{margin:5px 0 14px}.flow{width:100%;border:0;border-top:1px solid #e9ebf1;background:white;padding:15px 2px;display:flex;gap:13px;align-items:center;text-align:left;cursor:pointer}.flow div{flex:1}.flow b,.flow small{display:block}.flow small{color:#81899b;margin-top:4px}.flow>strong{font-size:20px}.copy{color:#707b91;font-size:12px;line-height:1.7}.wide{width:100%;padding:10px;border-radius:7px;border:1px solid #cdd3e0;cursor:pointer}.primary{background:#293b67!important;color:white!important;border-color:#293b67!important}.instruction{background:#fff8e7;border-left:4px solid #d4a632;padding:14px 17px;margin-bottom:17px;border-radius:7px}.instruction b,.instruction span{display:block}.instruction span{font-size:12px;color:#766b4d;margin-top:4px}.alerta{background:#fdeceb;border-left:4px solid #c0392b;padding:14px 17px;margin:0 0 17px;border-radius:7px}.alerta b,.alerta span{display:block}.alerta b{color:#96271b}.alerta span{font-size:12px;color:#7d453e;margin-top:4px}.mini-alerta{background:#fdeceb;color:#96271b;font-size:11px;font-weight:700;padding:7px 9px;border-radius:6px;margin-bottom:10px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.cards article{background:white;border:1px solid #dfe3eb;border-radius:10px;padding:19px}.cards article.retorno{border-color:#e2b4ae;box-shadow:inset 3px 0 #c0392b}.top{display:flex;justify-content:space-between;gap:8px}.top span{font-size:12px;font-weight:800;color:#3d5d96}.top em{font-size:10px;background:#eff0f5;padding:4px 8px;border-radius:10px;font-style:normal;white-space:nowrap}.top em.vencido{background:#fdeceb;color:#96271b}.cards h3{font-size:17px;margin:15px 0 7px}.cards article>p{font-size:12px;color:#778096;min-height:42px}.datos{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:4px}.datos li{display:flex;justify-content:space-between;gap:10px;font-size:11px;border-bottom:1px dashed #edf0f5;padding-bottom:3px}.datos b{color:#5c6883}.datos span{color:#79839a;text-align:right}.adjunto{display:inline-block;font-size:11px;color:#3d5d96;margin-bottom:10px;text-decoration:none}.actions{display:flex;gap:7px;border-top:1px solid #e8eaf0;padding-top:13px;margin-top:10px}.actions button{flex:1;padding:9px 6px;border-radius:7px;border:1px solid #cdd3e0;background:white;color:#3e4b69;font-weight:700;cursor:pointer}.actions button:disabled{opacity:.55;cursor:not-allowed}.empty{text-align:center;background:white;border:1px dashed #cbd0dc;padding:65px;border-radius:10px;color:#798196}.empty>span{font-size:31px;color:#38936e}.campo{display:block;margin:14px 0;font-size:12px;font-weight:700;color:#465170}.campo input,.campo select,.campo textarea{display:block;width:100%;margin-top:6px;padding:9px 11px;border:1px solid #d9deea;border-radius:7px;font-family:inherit;font-size:13px;font-weight:400;color:#232f4a}.hoja{max-width:820px}.hoja-head{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:16px}.hoja-head h3{margin:5px 0 0}.compuerta{border:1px solid #e0e3ec;border-radius:8px;padding:12px 15px;margin:16px 0;display:flex;gap:22px;align-items:center}.compuerta legend{font-size:12px;font-weight:700;color:#465170;padding:0 6px}.compuerta label{font-size:13px;display:flex;align-items:center;gap:6px;font-weight:600}.compuerta input{margin:0}.detalle-modal-backdrop{position:fixed;inset:0;background:#0d1a31aa;display:grid;place-items:center;padding:20px;z-index:20}.detalle-modal{background:white;border-radius:14px;width:min(700px,100%);max-height:88vh;display:flex;flex-direction:column}.detalle-modal-header{display:flex;justify-content:space-between;align-items:center;padding:20px 24px;border-bottom:1px solid #e8eaf0}.detalle-modal-header h3{margin:0}.detalle-modal-header small{color:#78839e}.detalle-modal-close{border:0;background:transparent;font-size:20px;cursor:pointer;color:#78839e}.detalle-modal-body{padding:20px 24px;overflow-y:auto;display:grid;gap:14px}.detalle-fila{display:grid;grid-template-columns:1fr 1fr;gap:14px}.detalle-campo b{display:block;font-size:11px;color:#5c6883;margin-bottom:4px}.detalle-campo span,.detalle-campo p{font-size:13px;color:#39445c;margin:0}@media(max-width:1050px){.stats{grid-template-columns:1fr 1fr}.panels{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}}@media(max-width:720px){aside{position:static;width:100%}main{margin:0;padding:20px}.stats,.cards{grid-template-columns:1fr}header{align-items:flex-start;flex-direction:column;gap:12px}.detalle-fila{grid-template-columns:1fr}}
</style>
