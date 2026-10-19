<template>
  <div class="layout sigta-role-layout">
    <aside :class="{ abierto: menuAbierto }">
      <div class="brand-row">
        <div class="brand"><b><img src="/img/emi.jpg" alt="EMI"></b><div><strong>SIGTA</strong><small>Mantenimiento</small></div></div>
        <button type="button" class="menu-toggle" :aria-expanded="menuAbierto" aria-label="Mostrar opciones del menú" @click="menuAbierto = !menuAbierto"><span></span><span></span><span></span></button>
      </div>
      <div class="profile"><i>{{ iniciales }}</i><div><b>{{ nombre }}</b><small>Servicios Generales</small></div></div>
      <p>GESTIÓN DE MANTENIMIENTO</p>
      <button v-for="m in menu" :key="m.id" :class="{active:vista===m.id}" @click="vista=m.id; menuAbierto=false"><span>{{ m.icono }}</span>{{ m.nombre }}<em v-if="m.total!==undefined">{{ m.total }}</em></button>
      <div class="bottom"><button @click="salir"><span>↪</span>Cerrar sesión</button></div>
    </aside>

    <main>
      <header>
        <div><small>SIGTA / MANTENIMIENTO / {{ titulo }}</small><h1>{{ titulo }}</h1><p>Recepción y derivación de requerimientos de mantenimiento.</p></div>
        <button class="refresh" @click="cargar">↻ Actualizar</button>
      </header>

      <section v-if="vista==='resumen'">
        <div class="hero">
          <div><small>SERVICIOS GENERALES</small><h2>{{ saludo }}, {{ primerNombre }}</h2><p>Requerimientos que requieren su gestión hoy.</p></div>
          <span>SG</span>
        </div>
        <div class="stats">
          <article @click="vista='derivar'"><i class="blue">DR</i><div><small>Por derivar</small><b>{{ porDerivar.length }}</b><p>a un auxiliar</p></div></article>
          <article @click="vista='compra'"><i class="gold">CO</i><div><small>Compras por validar</small><b>{{ comprasPorValidar.length }}</b><p>para elevar a DAF</p></div></article>
          <article @click="vista='finalizar'"><i class="green">FI</i><div><small>Por finalizar</small><b>{{ porFinalizar.length }}</b><p>informe registrado</p></div></article>
          <article @click="vista='seguimiento'"><i class="navy">EC</i><div><small>En curso</small><b>{{ enCurso.length }}</b><p>ver seguimiento</p></div></article>
        </div>
        <div class="panels">
          <section class="panel">
            <div class="panel-head"><div><small>FLUJO BPMN</small><h3>Proceso de mantenimiento</h3></div></div>
            <button class="flow" @click="vista='derivar'"><i class="blue">1</i><div><b>Derivar a su auxiliar</b><small>Asignar el requerimiento recibido a un Auxiliar de Servicios Generales</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='finalizar'"><i class="gold">2</i><div><b>Recibir expediente y archivar</b><small>Confirmar el informe del trabajo y finalizar el requerimiento</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='reporte'"><i class="green">3</i><div><b>Reporte mensual</b><small>Consolidado de mantenimientos finalizados en el periodo</small></div><strong>›</strong></button>
          </section>
          <section class="panel">
            <div class="panel-head"><div><small>SEGUIMIENTO</small><h3>Requerimientos en curso</h3></div></div>
            <p class="copy">Requerimientos ya derivados a un auxiliar y todavía no finalizados.</p>
            <button class="wide primary" @click="vista='seguimiento'">Ver requerimientos en curso →</button>
          </section>
        </div>
      </section>

      <section v-else-if="vista==='derivar'">
        <div class="instruction"><b>Derivar a su auxiliar</b><span>Seleccione al Auxiliar de Servicios Generales que atenderá el requerimiento.</span></div>
        <div v-if="!itemActivo" class="cards">
          <article v-for="r in porDerivar" :key="r.id">
            <div class="top"><span>{{ r.codigo }}</span><em>{{ r.estado_codigo }}</em></div>
            <h3>{{ r.titulo }}</h3>
            <p>{{ (r.descripcion||'').slice(0,130) }}</p>
            <div class="actions"><button @click="verItem(r)">Ver detalle</button><button class="primary" @click="abrirDerivacion(r)">Derivar</button></div>
          </article>
          <div v-if="!porDerivar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay requerimientos pendientes de derivación.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ itemActivo.codigo }} — {{ itemActivo.titulo }}</h3>
          <label class="campo">Auxiliar de Servicios Generales
            <select v-model="formDerivar.auxiliar_id">
              <option value="">Seleccione…</option>
              <option v-for="a in auxiliares" :key="a.id" :value="a.id">{{ a.nombre_completo || a.email }}</option>
            </select>
          </label>
          <small v-if="!auxiliares.length">No hay auxiliares activos disponibles.</small>
          <label class="campo">Prioridad
            <select v-model="formDerivar.prioridad">
              <option value="">Seleccione…</option>
              <option value="BAJA">Baja</option>
              <option value="MEDIA">Media</option>
              <option value="ALTA">Alta</option>
              <option value="URGENTE">Urgente</option>
            </select>
          </label>
          <label class="campo">Criterio de prioridad
            <textarea v-model.trim="formDerivar.criterio_prioridad" rows="3" placeholder="Explique por qué se asigna esta prioridad"></textarea>
          </label>
          <div class="actions"><button @click="itemActivo=null">Cancelar</button><button class="primary" :disabled="procesando||!formDerivar.auxiliar_id||!formDerivar.prioridad||!formDerivar.criterio_prioridad" @click="derivarAuxiliar">Derivar requerimiento</button></div>
        </div>
      </section>

      <section v-else-if="vista==='finalizar'">
        <div class="instruction"><b>Recibir expediente y archivar</b><span>Confirme que el informe del trabajo fue registrado y finalice el requerimiento.</span></div>
        <div class="cards">
          <article v-for="r in porFinalizar" :key="r.id">
            <div class="top"><span>{{ r.codigo }}</span><em>{{ r.estado_codigo }}</em></div>
            <h3>{{ r.titulo }}</h3>
            <p>{{ (r.informe_trabajo||'').slice(0,130) }}</p>
            <div class="actions"><button @click="verItem(r)">Ver detalle</button><button class="primary" @click="finalizarRequerimiento(r)">Finalizar y archivar</button></div>
          </article>
          <div v-if="!porFinalizar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay expedientes pendientes de archivar.</p></div>
        </div>
      </section>

      <section v-else-if="vista==='compra'">
        <div class="instruction"><b>Validar y elevar compra</b><span>Revise el requerimiento preparado por el técnico y, si corresponde, elévelo a DAF.</span></div>
        <div class="cards">
          <article v-for="r in comprasPorValidar" :key="r.id">
            <div class="top"><span>{{ r.codigo }}</span><em>PENDIENTE</em></div>
            <h3>{{ r.producto_requerido || r.titulo }}</h3>
            <p>Cantidad: {{ r.cantidad_requerida || 1 }}<br>{{ r.especificacion_producto || 'Sin especificaciones adicionales.' }}</p>
            <div class="actions"><button @click="verItem(r)">Ver documentación</button><button class="primary" :disabled="procesando" @click="elevarCompra(r)">Validar y elevar a DAF</button></div>
          </article>
          <div v-if="!comprasPorValidar.length" class="empty"><span>✓</span><h3>Sin compras pendientes</h3><p>No existen solicitudes esperando validación de la jefatura.</p></div>
        </div>
      </section>

      <section v-else-if="vista==='seguimiento'">
        <div class="instruction"><b>Requerimientos en curso</b><span>Solo lectura: derivados a un auxiliar y todavía no finalizados.</span></div>
        <div class="table" v-if="enCurso.length">
          <div class="thead"><span>Código</span><span>Título</span><span>Auxiliar</span><span>Estado</span><span>Compra vinculada</span></div>
          <div class="row" v-for="r in enCurso" :key="r.id">
            <b>{{ r.codigo }}</b><span>{{ r.titulo }}</span><span>{{ r.auxiliar_asignado_nombre || '—' }}</span><em>{{ r.estado_codigo }}</em>
            <span>{{ r.compra_vinculada ? `${r.compra_vinculada.codigo} (${r.compra_vinculada.estado_nombre})` : '—' }}</span>
          </div>
        </div>
        <div v-else class="empty">No hay requerimientos en curso.</div>
      </section>

      <section v-else-if="vista==='reporte'">
        <div class="instruction"><b>Reporte mensual de mantenimiento</b><span>Consolidado de requerimientos finalizados en el periodo seleccionado.</span></div>
        <div class="toolbar">
          <label class="campo inline">Año<input v-model.number="reporte.anio" type="number"></label>
          <label class="campo inline">Mes<input v-model.number="reporte.mes" type="number" min="1" max="12"></label>
          <button class="primary" @click="cargarReporte">Consultar</button>
        </div>
        <div class="table" v-if="reporte.requerimientos.length">
          <div class="thead"><span>Código</span><span>Título</span><span>Área</span><span>Auxiliar</span><span>Finalizado</span></div>
          <div class="row" v-for="r in reporte.requerimientos" :key="r.id">
            <b>{{ r.codigo }}</b><span>{{ r.titulo }}</span><span>{{ r.area_nombre }}</span><span>{{ r.auxiliar_asignado_nombre || '—' }}</span><em>{{ formatoFecha(r.finalizado_en) }}</em>
          </div>
        </div>
        <div v-else class="empty">No hay mantenimientos finalizados en el periodo consultado.</div>
      </section>
    </main>

    <div v-if="itemDetalle" class="detalle-modal-backdrop" @click.self="itemDetalle=null">
      <div class="detalle-modal">
        <div class="detalle-modal-header">
          <div><h3>{{ itemDetalle.codigo }}</h3><small>{{ itemDetalle.titulo }}</small></div>
          <button class="detalle-modal-close" @click="itemDetalle=null">✕</button>
        </div>
        <div class="detalle-modal-body">
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Estado</b><span>{{ itemDetalle.estado_nombre }}</span></div>
            <div class="detalle-campo"><b>Tipo</b><span>{{ itemDetalle.tipo || 's/d' }}</span></div>
          </div>
          <div class="detalle-fila">
            <div class="detalle-campo"><b>Solicitante</b><span>{{ itemDetalle.solicitante_nombre }}</span></div>
            <div class="detalle-campo"><b>Auxiliar asignado</b><span>{{ itemDetalle.auxiliar_asignado_nombre || 's/d' }}</span></div>
          </div>
          <div class="detalle-campo"><b>Descripción</b><p>{{ itemDetalle.descripcion || 's/d' }}</p></div>
          <div class="detalle-campo"><b>Ubicación</b><span>{{ itemDetalle.ubicacion || 's/d' }}</span></div>
          <div class="detalle-campo" v-if="itemDetalle.requiere_reposicion"><b>Producto requerido de almacén</b><p>{{ itemDetalle.producto_requerido }} — cantidad: {{ itemDetalle.cantidad_requerida || 's/d' }}<br>{{ itemDetalle.especificacion_producto || '' }}</p></div>
          <div class="detalle-campo" v-if="itemDetalle.observacion_almacen"><b>Observación de Almacén</b><p>{{ itemDetalle.observacion_almacen }}</p></div>
          <div class="detalle-campo" v-if="itemDetalle.codigo_compra_vinculada"><b>Expediente de compra</b><span>{{ itemDetalle.codigo_compra_vinculada }}</span></div>
          <div class="detalle-campo" v-if="itemDetalle.trabajo_realizado"><b>Trabajo realizado</b><p>{{ itemDetalle.trabajo_realizado }}</p></div>
          <div class="detalle-campo" v-if="itemDetalle.observaciones_trabajo"><b>Observaciones del trabajo</b><p>{{ itemDetalle.observaciones_trabajo }}</p></div>
          <div class="detalle-campo" v-if="itemDetalle.informe_trabajo"><b>Informe del trabajo</b><p>{{ itemDetalle.informe_trabajo }}</p></div>
          <div class="detalle-campo" v-if="itemDetalle.fotografia_trabajo_url"><b>Fotografía del trabajo</b><a :href="itemDetalle.fotografia_trabajo_url" target="_blank">Abrir imagen →</a></div>
          <div class="detalle-campo" v-if="itemDetalle.evidencia_archivo_url"><b>Evidencia adjunta</b><a :href="itemDetalle.evidencia_archivo_url" target="_blank">Abrir archivo →</a></div>
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
const requerimientos = ref([])
const auxiliares = ref([])
const cargando = ref(false)
const procesando = ref(false)
const itemActivo = ref(null)
const reporte = reactive({ anio: new Date().getFullYear(), mes: new Date().getMonth() + 1, requerimientos: [] })

const nombre = computed(() => usuario.value.nombre || usuario.value.nombre_completo || 'Servicios Generales')
const primerNombre = computed(() => nombre.value.split(' ')[0])
const iniciales = computed(() => nombre.value.split(' ').slice(0, 2).map(x => x[0]).join('').toUpperCase())
const saludo = computed(() => new Date().getHours() < 12 ? 'Buenos días' : new Date().getHours() < 19 ? 'Buenas tardes' : 'Buenas noches')

const porDerivar = computed(() => requerimientos.value.filter(r => r.estado_codigo === 'RECIBIDO'))
const enCurso = computed(() => requerimientos.value.filter(r => ['DERIVADO', 'REVISION_ALMACEN', 'EN_ESPERA_COMPRA', 'EN_MANTENIMIENTO', 'INFORME_REGISTRADO'].includes(r.estado_codigo)))
const porFinalizar = computed(() => requerimientos.value.filter(r => r.estado_codigo === 'INFORME_REGISTRADO'))
const comprasPorValidar = computed(() => requerimientos.value.filter(r => r.estado_codigo === 'EN_ESPERA_COMPRA' && !r.derivado_compra))
const finalizadosMes = computed(() => {
  const ahora = new Date()
  return requerimientos.value.filter(r => r.estado_codigo === 'FINALIZADO' && r.finalizado_en && new Date(r.finalizado_en).getMonth() === ahora.getMonth() && new Date(r.finalizado_en).getFullYear() === ahora.getFullYear())
})

const menu = computed(() => [
  { id: 'resumen', icono: '⌂', nombre: 'Dashboard' },
  { id: 'derivar', icono: 'DR', nombre: 'Derivar a auxiliar', total: porDerivar.value.length },
  { id: 'compra', icono: 'CO', nombre: 'Validar y elevar compra', total: comprasPorValidar.value.length },
  { id: 'seguimiento', icono: 'EC', nombre: 'En curso', total: enCurso.value.length },
  { id: 'finalizar', icono: 'FI', nombre: 'Finalizar y archivar', total: porFinalizar.value.length },
  { id: 'reporte', icono: 'RM', nombre: 'Reporte mensual' },
])

const titulo = computed(() => ({
  resumen: 'Dashboard de Mantenimiento',
  derivar: 'Derivar a auxiliar',
  compra: 'Validar y elevar compra',
  seguimiento: 'Requerimientos en curso',
  finalizar: 'Finalizar y archivar',
  reporte: 'Reporte mensual',
}[vista.value]))

function formatoFecha(v) { return v ? new Date(v).toLocaleDateString('es-BO') : '—' }
function headersJson() { return { Authorization: `Token ${localStorage.getItem('sigta_token')}`, 'Content-Type': 'application/json' } }
function headersAuth() { return { Authorization: `Token ${localStorage.getItem('sigta_token')}` } }

async function cargar() {
  cargando.value = true
  try {
    const r = await fetch('/api/mantenimiento/requerimientos/', { headers: headersAuth() })
    const d = await r.json()
    requerimientos.value = Array.isArray(d) ? d : (d.results || [])
    const ra = await fetch('/api/usuarios/usuarios-por-rol/?rol=AUXILIAR_SERVICIOS_GENERALES', { headers: headersAuth() })
    auxiliares.value = ra.ok ? await ra.json() : []
  } finally {
    cargando.value = false
  }
}

async function cargarReporte() {
  const r = await fetch(`/api/mantenimiento/requerimientos/reporte-mensual/?anio=${reporte.anio}&mes=${reporte.mes}`, { headers: headersAuth() })
  const d = await r.json().catch(() => ({}))
  reporte.requerimientos = d.requerimientos || []
}

function salir() {
  localStorage.removeItem('sigta_token')
  localStorage.removeItem('sigta_usuario')
  router.push('/login')
}

const itemDetalle = ref(null)
function verItem(r) {
  itemDetalle.value = r
}

async function postAccion(item, endpoint, body) {
  procesando.value = true
  try {
    const r = await fetch(`/api/mantenimiento/requerimientos/${item.id}/${endpoint}/`, { method: 'POST', headers: headersJson(), body: JSON.stringify(body || {}) })
    const d = await r.json().catch(() => ({}))
    if (!r.ok) throw new Error(d.detalle || Object.values(d)[0] || 'No fue posible completar la acción.')
    await cargar()
    itemActivo.value = null
    return d
  } finally {
    procesando.value = false
  }
}

const formDerivar = reactive({ auxiliar_id: '', prioridad: 'MEDIA', criterio_prioridad: '' })
function abrirDerivacion(item) {
  itemActivo.value = item
  Object.assign(formDerivar, { auxiliar_id: '', prioridad: 'MEDIA', criterio_prioridad: '' })
}
async function derivarAuxiliar() {
  try { await postAccion(itemActivo.value, 'derivar-auxiliar', { auxiliar_id: Number(formDerivar.auxiliar_id), prioridad: formDerivar.prioridad, criterio_prioridad: formDerivar.criterio_prioridad }) }
  catch (e) { alert(e.message) }
}

async function elevarCompra(item) {
  if (!confirm(`¿Validar y elevar a DAF la compra de ${item.producto_requerido || item.titulo}?`)) return
  try { const data = await postAccion(item, 'validar-elevar-compra', {}); alert(data?.mensaje || 'Solicitud elevada a DAF correctamente.') }
  catch (e) { alert(e.message) }
}

async function finalizarRequerimiento(r) {
  if (!confirm(`¿Finalizar y archivar ${r.codigo}?`)) return
  try { await postAccion(r, 'finalizar', {}) }
  catch (e) { alert(e.message) }
}

onMounted(() => { cargar(); cargarReporte() })
</script>

<style scoped>
*{box-sizing:border-box}.layout{min-height:100vh;background:#f5f6fa;color:#232f4a;font-family:Inter,Segoe UI,sans-serif}aside{position:fixed;inset:0 auto 0 0;width:278px;background:#222f55;color:white;padding:22px 16px;display:flex;flex-direction:column}.brand,.profile{display:flex;align-items:center;gap:12px}.brand{padding:0 10px 20px;border-bottom:1px solid #ffffff20}.brand>b{background:#e6b941;color:#243155;padding:14px 10px;border-radius:9px}.brand strong,.brand small,.profile b,.profile small{display:block}.brand strong{font-size:23px}.brand small,.profile small{color:#c0c9e1;margin-top:3px}.profile{padding:22px 10px}.profile>i{width:42px;height:42px;border-radius:50%;background:#e6b941;color:#253154;display:grid;place-items:center;font-style:normal;font-weight:900}aside>p{font-size:10px;color:#929fc5;font-weight:800;letter-spacing:1.4px;margin:14px 10px 8px}aside button{border:0;background:transparent;color:#dfe4f2;border-radius:8px;padding:12px;display:flex;gap:11px;align-items:center;text-align:left;cursor:pointer;margin:2px 0;width:100%}aside button>span{font-size:10px;font-weight:900;width:28px}aside button em{margin-left:auto;background:#ffffff1c;padding:2px 8px;border-radius:10px;font-style:normal}aside button.active,aside button:hover{background:#ffffff14;box-shadow:inset 3px 0 #e6b941}.bottom{margin-top:auto;border-top:1px solid #ffffff20;padding-top:10px}.bottom button{width:100%}main{margin-left:278px;padding:30px 38px 55px;max-width:1650px}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:27px}header small{color:#78839e}h1{font-size:29px;margin:6px 0}header p{margin:0;color:#737e96}.refresh{border:1px solid #d9deea;background:white;color:#313e69;padding:10px 14px;border-radius:8px}.hero{background:linear-gradient(120deg,#25335a,#3b4d7d);color:white;border-radius:13px;padding:28px 30px;display:flex;justify-content:space-between;align-items:center}.hero small,.panel-head small{font-size:10px;font-weight:800;letter-spacing:1.4px;color:#edc65a}.hero h2{font-size:24px;margin:7px 0}.hero p{margin:0;color:#dce1ee}.hero>span{width:68px;height:68px;border:1px solid #edc65a88;border-radius:50%;display:grid;place-items:center;font-weight:900}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:18px 0}.stats article{background:white;border:1px solid #e0e3ec;border-radius:10px;padding:19px;display:flex;gap:13px}.stats i,.flow i{font-style:normal;width:37px;height:37px;border-radius:8px;display:grid;place-items:center;color:white;font-size:10px;font-weight:900}.blue{background:#3b7fba}.gold{background:#c89c2d}.green{background:#38936e}.navy{background:#34456e}.stats small,.stats b,.stats p{display:block}.stats b{font-size:25px;margin:3px 0}.stats p{font-size:11px;color:#858da0;margin:0}.panels{display:grid;grid-template-columns:2fr 1fr;gap:18px}.panel{background:white;border:1px solid #e0e3ec;border-radius:11px;padding:22px}.panel-head h3{margin:5px 0 14px}.flow{width:100%;border:0;border-top:1px solid #e9ebf1;background:white;padding:15px 2px;display:flex;gap:13px;align-items:center;text-align:left;cursor:pointer}.flow div{flex:1}.flow b,.flow small{display:block}.flow small{color:#81899b;margin-top:4px}.flow>strong{font-size:20px}.copy{color:#707b91;font-size:12px;line-height:1.7}.wide{width:100%;padding:10px;border-radius:7px}.toolbar{display:flex;gap:12px;align-items:flex-end;margin-bottom:17px}.primary{background:#293b67!important;color:white!important;border-color:#293b67!important}.instruction{background:#fff8e7;border-left:4px solid #d4a632;padding:14px 17px;margin-bottom:17px;border-radius:7px}.instruction b,.instruction span{display:block}.instruction span{font-size:12px;color:#766b4d;margin-top:4px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.cards article{background:white;border:1px solid #dfe3eb;border-radius:10px;padding:19px}.top{display:flex;justify-content:space-between}.top span{font-size:12px;font-weight:800;color:#3d5d96}.top em{font-size:10px;background:#eff0f5;padding:4px 8px;border-radius:10px;font-style:normal}.cards h3{font-size:17px;margin:15px 0 7px}.cards article>p{font-size:12px;color:#778096;min-height:42px}.actions{display:flex;gap:7px;border-top:1px solid #e8eaf0;padding-top:13px;margin-top:10px}.actions button{flex:1;padding:9px 6px;border-radius:7px;border:1px solid #cdd3e0;background:white;color:#3e4b69;font-weight:700;cursor:pointer}.empty{text-align:center;background:white;border:1px dashed #cbd0dc;padding:65px;border-radius:10px;color:#798196}.empty>span{font-size:31px;color:#38936e}.campo{display:block;margin:14px 0;font-size:12px;font-weight:700;color:#465170}.campo.inline{margin:0}.campo input,.campo select,.campo textarea{display:block;width:100%;margin-top:6px;padding:9px 11px;border:1px solid #d9deea;border-radius:7px;font-family:inherit;font-size:13px;font-weight:400;color:#232f4a}.table{background:white;border:1px solid #dfe3eb;border-radius:10px;overflow:hidden}.thead,.row{display:grid;grid-template-columns:1fr 1.6fr 1fr .8fr 1.2fr;gap:10px;align-items:center;padding:14px 18px}.thead{background:#eff0f5;color:#737b90;font-size:10px;font-weight:800}.row{border-top:1px solid #e8eaf0;font-size:12px}.row em{font-style:normal;color:#318266}@media(max-width:1050px){.stats{grid-template-columns:1fr 1fr}.panels{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}}@media(max-width:720px){aside{position:static;width:100%}main{margin:0;padding:20px}.stats,.cards{grid-template-columns:1fr}header,.toolbar{align-items:flex-start;flex-direction:column;gap:12px}.table{overflow:auto}.thead,.row{min-width:760px}}
</style>
