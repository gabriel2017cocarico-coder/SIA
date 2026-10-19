<template>
  <div class="layout sigta-role-layout">
    <aside :class="{ abierto: menuAbierto }">
      <div class="brand-row">
        <div class="brand"><b><img src="/img/emi.jpg" alt="EMI"></b><div><strong>SIGTA</strong><small>Mantenimiento</small></div></div>
        <button type="button" class="menu-toggle" :aria-expanded="menuAbierto" aria-label="Mostrar opciones del menú" @click="menuAbierto = !menuAbierto"><span></span><span></span><span></span></button>
      </div>
      <div class="profile"><i>{{ iniciales }}</i><div><b>{{ nombre }}</b><small>Auxiliar de Servicios Generales</small></div></div>
      <p>MIS REQUERIMIENTOS</p>
      <button v-for="m in menu" :key="m.id" :class="{active:vista===m.id}" @click="vista=m.id; menuAbierto=false"><span>{{ m.icono }}</span>{{ m.nombre }}<em v-if="m.total!==undefined">{{ m.total }}</em></button>
      <div class="bottom"><button @click="salir"><span>↪</span>Cerrar sesión</button></div>
    </aside>

    <main>
      <header>
        <div><small>SIGTA / MANTENIMIENTO / {{ titulo }}</small><h1>{{ titulo }}</h1><p>Ejecución de los requerimientos de mantenimiento que le fueron derivados.</p></div>
        <button class="refresh" @click="cargar">↻ Actualizar</button>
      </header>

      <section v-if="vista==='resumen'">
        <div class="hero">
          <div><small>AUXILIAR</small><h2>{{ saludo }}, {{ primerNombre }}</h2><p>Requerimientos derivados que requieren su atención.</p></div>
          <span>SG</span>
        </div>
        <div class="stats">
          <article><i class="blue">RP</i><div><small>Por verificar reposición</small><b>{{ porVerificar.length }}</b><p>recién derivados</p></div></article>
          <article><i class="gold">MT</i><div><small>Por realizar</small><b>{{ porRealizar.length }}</b><p>mantenimiento</p></div></article>
          <article><i class="green">IF</i><div><small>Por informar</small><b>{{ porInformar.length }}</b><p>informe y fotograma</p></div></article>
          <article><i class="navy">EC</i><div><small>Esperando compra</small><b>{{ esperandoCompra.length }}</b><p>Caja Chica</p></div></article>
        </div>
        <div class="panels">
          <section class="panel">
            <div class="panel-head"><div><small>FLUJO BPMN</small><h3>Ejecución del mantenimiento</h3></div></div>
            <button class="flow" @click="vista='reposicion'"><i class="blue">1</i><div><b>¿Requiere reposición de almacén?</b><small>Determinar si falta un producto para el mantenimiento</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='realizar'"><i class="gold">2</i><div><b>Realizar el mantenimiento</b><small>Registrar el trabajo realizado</small></div><strong>›</strong></button>
            <button class="flow" @click="vista='informar'"><i class="green">3</i><div><b>Realizar informe y fotograma</b><small>Documentar el trabajo con informe y evidencia fotográfica</small></div><strong>›</strong></button>
          </section>
          <section class="panel">
            <div class="panel-head"><div><small>SEGUIMIENTO</small><h3>Esperando Compra Caja Chica</h3></div></div>
            <p class="copy">Requerimientos donde reportó que no había producto en almacén; el mantenimiento continuará cuando Compras cierre el expediente.</p>
            <button class="wide primary" @click="vista='compra'">Ver estado de la compra →</button>
          </section>
        </div>
      </section>

      <section v-else-if="vista==='reposicion'">
        <div class="instruction"><b>¿Requiere reposición de almacén?</b><span>Indique si necesita un producto de almacén para realizar el mantenimiento.</span></div>
        <div v-if="!itemActivo" class="cards">
          <article v-for="r in porVerificar" :key="r.id">
            <div class="top"><span>{{ r.codigo }}</span><em>{{ r.estado_codigo }}</em></div>
            <h3>{{ r.titulo }}</h3>
            <p>{{ (r.descripcion||'').slice(0,130) }}</p>
            <div class="actions"><button @click="verItem(r)">Ver detalle</button><button class="primary" @click="abrirReposicion(r)">Verificar</button></div>
          </article>
          <div v-if="!porVerificar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay requerimientos pendientes de verificación.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ itemActivo.codigo }} — {{ itemActivo.titulo }}</h3>
          <label class="campo"><input type="checkbox" v-model="formReposicion.requiere"> Requiere reposición de almacén</label>
          <template v-if="formReposicion.requiere">
            <label class="campo">Producto requerido<input v-model="formReposicion.producto_requerido"></label>
            <label class="campo">Cantidad requerida<input v-model.number="formReposicion.cantidad_requerida" type="number" min="1"></label>
            <label class="campo">Especificación<textarea v-model="formReposicion.especificacion_producto" rows="2"></textarea></label>
          </template>
          <div class="actions"><button @click="itemActivo=null">Cancelar</button><button class="primary" :disabled="procesando" @click="verificarReposicion">Guardar</button></div>
        </div>
      </section>

      <section v-else-if="vista==='realizar'">
        <div class="instruction"><b>Realizar el mantenimiento</b><span>Registre el trabajo realizado sobre el equipo o instalación.</span></div>
        <div v-if="!itemActivo" class="cards">
          <article v-for="r in porRealizar" :key="r.id">
            <div class="top"><span>{{ r.codigo }}</span><em>{{ r.estado_codigo }}</em></div>
            <h3>{{ r.titulo }}</h3>
            <div class="actions"><button @click="verItem(r)">Ver detalle</button><button class="primary" @click="itemActivo=r;formTrabajo.trabajo_realizado='';formTrabajo.observaciones_trabajo=''">Registrar trabajo</button></div>
          </article>
          <div v-if="!porRealizar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay requerimientos en mantenimiento pendientes.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ itemActivo.codigo }} — {{ itemActivo.titulo }}</h3>
          <label class="campo">Trabajo realizado<textarea v-model="formTrabajo.trabajo_realizado" rows="4"></textarea></label>
          <label class="campo">Observaciones (opcional)<textarea v-model="formTrabajo.observaciones_trabajo" rows="2"></textarea></label>
          <div class="actions"><button @click="itemActivo=null">Cancelar</button><button class="primary" :disabled="procesando||!formTrabajo.trabajo_realizado.trim()" @click="realizarMantenimiento">Guardar trabajo realizado</button></div>
        </div>
      </section>

      <section v-else-if="vista==='informar'">
        <div class="instruction"><b>Realizar informe y fotograma</b><span>Documente el trabajo con un informe y, si corresponde, una fotografía.</span></div>
        <div v-if="!itemActivo" class="cards">
          <article v-for="r in porInformar" :key="r.id">
            <div class="top"><span>{{ r.codigo }}</span><em>{{ r.estado_codigo }}</em></div>
            <h3>{{ r.titulo }}</h3>
            <p>{{ (r.trabajo_realizado||'').slice(0,130) }}</p>
            <div class="actions"><button @click="verItem(r)">Ver detalle</button><button class="primary" @click="itemActivo=r;formInforme.informe_trabajo='';archivoFoto=null">Registrar informe</button></div>
          </article>
          <div v-if="!porInformar.length" class="empty"><span>✓</span><h3>Bandeja al día</h3><p>No hay trabajos pendientes de informe.</p></div>
        </div>
        <div v-else class="panel">
          <h3>{{ itemActivo.codigo }} — {{ itemActivo.titulo }}</h3>
          <label class="campo">Informe del trabajo<textarea v-model="formInforme.informe_trabajo" rows="4"></textarea></label>
          <label class="campo">Fotografía del trabajo (opcional)<input type="file" accept="image/*,.pdf" @change="e=>archivoFoto=e.target.files?.[0]||null"></label>
          <div class="actions"><button @click="itemActivo=null">Cancelar</button><button class="primary" :disabled="procesando||!formInforme.informe_trabajo.trim()" @click="registrarInforme">Guardar informe</button></div>
        </div>
      </section>

      <section v-else-if="vista==='compra'">
        <div class="instruction"><b>Esperando Compra Caja Chica</b><span>Solo lectura: el mantenimiento continúa automáticamente cuando Compras cierra y archiva el expediente.</span></div>
        <div class="table" v-if="esperandoCompra.length">
          <div class="thead"><span>Código</span><span>Producto requerido</span><span>Compra vinculada</span><span>Estado</span></div>
          <div class="row" v-for="r in esperandoCompra" :key="r.id">
            <b>{{ r.codigo }}</b><span>{{ r.producto_requerido }}</span><span>{{ r.compra_vinculada?.codigo || '—' }}</span><em>{{ r.compra_vinculada?.estado_nombre || 'Sin expediente' }}</em>
          </div>
        </div>
        <div v-else class="empty">No hay requerimientos esperando una compra.</div>
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
            <div class="detalle-campo"><b>Responsable Servicios Generales</b><span>{{ itemDetalle.responsable_servicios_generales_nombre || 's/d' }}</span></div>
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
const cargando = ref(false)
const procesando = ref(false)
const itemActivo = ref(null)
const archivoFoto = ref(null)

const nombre = computed(() => usuario.value.nombre || usuario.value.nombre_completo || 'Auxiliar')
const primerNombre = computed(() => nombre.value.split(' ')[0])
const iniciales = computed(() => nombre.value.split(' ').slice(0, 2).map(x => x[0]).join('').toUpperCase())
const saludo = computed(() => new Date().getHours() < 12 ? 'Buenos días' : new Date().getHours() < 19 ? 'Buenas tardes' : 'Buenas noches')

const misRequerimientos = computed(() => requerimientos.value.filter(r => Number(r.auxiliar_asignado) === Number(usuario.value.id)))
const porVerificar = computed(() => misRequerimientos.value.filter(r => r.estado_codigo === 'DERIVADO'))
const porRealizar = computed(() => misRequerimientos.value.filter(r => r.estado_codigo === 'EN_MANTENIMIENTO' && !r.trabajo_realizado))
const porInformar = computed(() => misRequerimientos.value.filter(r => r.estado_codigo === 'EN_MANTENIMIENTO' && !!r.trabajo_realizado))
const esperandoCompra = computed(() => misRequerimientos.value.filter(r => r.estado_codigo === 'EN_ESPERA_COMPRA'))

const menu = computed(() => [
  { id: 'resumen', icono: '⌂', nombre: 'Resumen' },
  { id: 'reposicion', icono: 'RP', nombre: 'Verificar reposición', total: porVerificar.value.length },
  { id: 'realizar', icono: 'MT', nombre: 'Realizar mantenimiento', total: porRealizar.value.length },
  { id: 'informar', icono: 'IF', nombre: 'Informe y fotograma', total: porInformar.value.length },
  { id: 'compra', icono: 'EC', nombre: 'Esperando compra', total: esperandoCompra.value.length },
])

const titulo = computed(() => ({
  resumen: 'Panel del Auxiliar de Servicios Generales',
  reposicion: 'Verificar reposición de almacén',
  realizar: 'Realizar mantenimiento',
  informar: 'Informe y fotograma',
  compra: 'Esperando Compra Caja Chica',
}[vista.value]))

function headersJson() { return { Authorization: `Token ${localStorage.getItem('sigta_token')}`, 'Content-Type': 'application/json' } }
function headersAuth() { return { Authorization: `Token ${localStorage.getItem('sigta_token')}` } }

async function cargar() {
  cargando.value = true
  try {
    const r = await fetch('/api/mantenimiento/requerimientos/', { headers: headersAuth() })
    const d = await r.json()
    requerimientos.value = Array.isArray(d) ? d : (d.results || [])
  } finally {
    cargando.value = false
  }
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

function abrirReposicion(r) {
  itemActivo.value = r
  formReposicion.requiere = false
  formReposicion.producto_requerido = ''
  formReposicion.cantidad_requerida = 1
  formReposicion.especificacion_producto = ''
}

async function postAccion(endpoint, body, multipart = false) {
  procesando.value = true
  try {
    const opciones = multipart
      ? { method: 'POST', headers: headersAuth(), body }
      : { method: 'POST', headers: headersJson(), body: JSON.stringify(body || {}) }
    const r = await fetch(`/api/mantenimiento/requerimientos/${itemActivo.value.id}/${endpoint}/`, opciones)
    const d = await r.json().catch(() => ({}))
    if (!r.ok) throw new Error(d.detalle || Object.values(d)[0] || 'No fue posible completar la acción.')
    await cargar()
    itemActivo.value = null
    return d
  } finally {
    procesando.value = false
  }
}

const formReposicion = reactive({ requiere: false, producto_requerido: '', cantidad_requerida: 1, especificacion_producto: '' })
async function verificarReposicion() {
  try {
    await postAccion('verificar-reposicion', {
      requiere_reposicion: formReposicion.requiere,
      ...(formReposicion.requiere ? {
        producto_requerido: formReposicion.producto_requerido,
        cantidad_requerida: formReposicion.cantidad_requerida,
        especificacion_producto: formReposicion.especificacion_producto,
      } : {}),
    })
  } catch (e) { alert(e.message) }
}

const formTrabajo = reactive({ trabajo_realizado: '', observaciones_trabajo: '' })
async function realizarMantenimiento() {
  try { await postAccion('realizar-mantenimiento', { trabajo_realizado: formTrabajo.trabajo_realizado.trim(), observaciones_trabajo: formTrabajo.observaciones_trabajo.trim() }) }
  catch (e) { alert(e.message) }
}

const formInforme = reactive({ informe_trabajo: '' })
async function registrarInforme() {
  try {
    const fd = new FormData()
    fd.append('informe_trabajo', formInforme.informe_trabajo.trim())
    if (archivoFoto.value) fd.append('fotografia_trabajo', archivoFoto.value)
    await postAccion('registrar-informe', fd, true)
  } catch (e) { alert(e.message) }
}

onMounted(cargar)
</script>

<style scoped>
*{box-sizing:border-box}.layout{min-height:100vh;background:#f5f6fa;color:#232f4a;font-family:Inter,Segoe UI,sans-serif}aside{position:fixed;inset:0 auto 0 0;width:278px;background:#222f55;color:white;padding:22px 16px;display:flex;flex-direction:column}.brand,.profile{display:flex;align-items:center;gap:12px}.brand{padding:0 10px 20px;border-bottom:1px solid #ffffff20}.brand>b{background:#e6b941;color:#243155;padding:14px 10px;border-radius:9px}.brand strong,.brand small,.profile b,.profile small{display:block}.brand strong{font-size:23px}.brand small,.profile small{color:#c0c9e1;margin-top:3px}.profile{padding:22px 10px}.profile>i{width:42px;height:42px;border-radius:50%;background:#e6b941;color:#253154;display:grid;place-items:center;font-style:normal;font-weight:900}aside>p{font-size:10px;color:#929fc5;font-weight:800;letter-spacing:1.4px;margin:14px 10px 8px}aside button{border:0;background:transparent;color:#dfe4f2;border-radius:8px;padding:12px;display:flex;gap:11px;align-items:center;text-align:left;cursor:pointer;margin:2px 0;width:100%}aside button>span{font-size:10px;font-weight:900;width:28px}aside button em{margin-left:auto;background:#ffffff1c;padding:2px 8px;border-radius:10px;font-style:normal}aside button.active,aside button:hover{background:#ffffff14;box-shadow:inset 3px 0 #e6b941}.bottom{margin-top:auto;border-top:1px solid #ffffff20;padding-top:10px}.bottom button{width:100%}main{margin-left:278px;padding:30px 38px 55px;max-width:1650px}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:27px}header small{color:#78839e}h1{font-size:29px;margin:6px 0}header p{margin:0;color:#737e96}.refresh{border:1px solid #d9deea;background:white;color:#313e69;padding:10px 14px;border-radius:8px}.hero{background:linear-gradient(120deg,#25335a,#3b4d7d);color:white;border-radius:13px;padding:28px 30px;display:flex;justify-content:space-between;align-items:center}.hero small,.panel-head small{font-size:10px;font-weight:800;letter-spacing:1.4px;color:#edc65a}.hero h2{font-size:24px;margin:7px 0}.hero p{margin:0;color:#dce1ee}.hero>span{width:68px;height:68px;border:1px solid #edc65a88;border-radius:50%;display:grid;place-items:center;font-weight:900}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin:18px 0}.stats article{background:white;border:1px solid #e0e3ec;border-radius:10px;padding:19px;display:flex;gap:13px}.stats i,.flow i{font-style:normal;width:37px;height:37px;border-radius:8px;display:grid;place-items:center;color:white;font-size:10px;font-weight:900}.blue{background:#3b7fba}.gold{background:#c89c2d}.green{background:#38936e}.navy{background:#34456e}.stats small,.stats b,.stats p{display:block}.stats b{font-size:25px;margin:3px 0}.stats p{font-size:11px;color:#858da0;margin:0}.panels{display:grid;grid-template-columns:2fr 1fr;gap:18px}.panel{background:white;border:1px solid #e0e3ec;border-radius:11px;padding:22px}.panel-head h3{margin:5px 0 14px}.flow{width:100%;border:0;border-top:1px solid #e9ebf1;background:white;padding:15px 2px;display:flex;gap:13px;align-items:center;text-align:left;cursor:pointer}.flow div{flex:1}.flow b,.flow small{display:block}.flow small{color:#81899b;margin-top:4px}.flow>strong{font-size:20px}.copy{color:#707b91;font-size:12px;line-height:1.7}.wide{width:100%;padding:10px;border-radius:7px}.primary{background:#293b67!important;color:white!important;border-color:#293b67!important}.instruction{background:#fff8e7;border-left:4px solid #d4a632;padding:14px 17px;margin-bottom:17px;border-radius:7px}.instruction b,.instruction span{display:block}.instruction span{font-size:12px;color:#766b4d;margin-top:4px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.cards article{background:white;border:1px solid #dfe3eb;border-radius:10px;padding:19px}.top{display:flex;justify-content:space-between}.top span{font-size:12px;font-weight:800;color:#3d5d96}.top em{font-size:10px;background:#eff0f5;padding:4px 8px;border-radius:10px;font-style:normal}.cards h3{font-size:17px;margin:15px 0 7px}.cards article>p{font-size:12px;color:#778096;min-height:42px}.actions{display:flex;gap:7px;border-top:1px solid #e8eaf0;padding-top:13px;margin-top:10px}.actions button{flex:1;padding:9px 6px;border-radius:7px;border:1px solid #cdd3e0;background:white;color:#3e4b69;font-weight:700;cursor:pointer}.empty{text-align:center;background:white;border:1px dashed #cbd0dc;padding:65px;border-radius:10px;color:#798196}.empty>span{font-size:31px;color:#38936e}.campo{display:block;margin:14px 0;font-size:12px;font-weight:700;color:#465170}.campo input,.campo select,.campo textarea{display:block;width:100%;margin-top:6px;padding:9px 11px;border:1px solid #d9deea;border-radius:7px;font-family:inherit;font-size:13px;font-weight:400;color:#232f4a}.campo input[type=checkbox]{display:inline-block;width:auto;margin:0 8px 0 0}.table{background:white;border:1px solid #dfe3eb;border-radius:10px;overflow:hidden}.thead,.row{display:grid;grid-template-columns:1fr 1.6fr 1fr 1fr;gap:10px;align-items:center;padding:14px 18px}.thead{background:#eff0f5;color:#737b90;font-size:10px;font-weight:800}.row{border-top:1px solid #e8eaf0;font-size:12px}.row em{font-style:normal;color:#318266}@media(max-width:1050px){.stats{grid-template-columns:1fr 1fr}.panels{grid-template-columns:1fr}.cards{grid-template-columns:1fr 1fr}}@media(max-width:720px){aside{position:static;width:100%}main{margin:0;padding:20px}.stats,.cards{grid-template-columns:1fr}header{align-items:flex-start;flex-direction:column;gap:12px}.table{overflow:auto}.thead,.row{min-width:640px}}
</style>
