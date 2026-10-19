<template>
  <div class="layout">
    <SolicitanteMenu />
    <main>
      <header class="head">
        <div>
          <p class="eyebrow">MI PORTAL SIGTA</p>
          <h1>{{ saludo }}, {{ nombre }}</h1>
          <p>Consulte el avance cuando lo necesite y atienda las solicitudes que requieren su validación.</p>
        </div>
        <div class="head-actions">
          <button class="bell" title="Validaciones pendientes" @click="irAValidaciones">
            🔔<b v-if="porValidar.length">{{ porValidar.length }}</b>
          </button>
          <button class="primary" @click="mostrarCrear = !mostrarCrear">＋ Nueva solicitud</button>
        </div>
      </header>

      <section v-if="mostrarCrear" class="create-panel">
        <button @click="router.push('/usuario/soporte')">
          <span>🖥️</span><div><strong>Soporte Técnico</strong><small>Equipos, redes, sistemas y dispositivos.</small></div>
        </button>
        <button @click="router.push('/usuario/mantenimiento')">
          <span>🛠️</span><div><strong>Mantenimiento</strong><small>Infraestructura, instalaciones y servicios.</small></div>
        </button>
      </section>

      <section class="summary">
        <article><span>Solicitudes activas</span><strong>{{ activas }}</strong></article>
        <article><span>En proceso</span><strong>{{ columnas[1].items.length }}</strong></article>
        <article class="attention"><span>Requieren mi validación</span><strong>{{ porValidar.length }}</strong></article>
        <article><span>Finalizadas</span><strong>{{ columnas[3].items.length }}</strong></article>
      </section>

      <section class="board-head">
        <div><h2>Mis solicitudes</h2><p>Seleccione una columna para abrir su listado filtrado o una tarjeta para consultar el detalle.</p></div>
        <button class="refresh" :disabled="cargando" @click="cargar">↻ Actualizar</button>
      </section>

      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="cargando" class="loading">Cargando solicitudes...</div>
      <section v-else class="kanban">
        <div v-for="columna in columnas" :key="columna.codigo" class="column" :class="columna.clase">
          <button class="column-title" @click="abrirColumna(columna.codigo)">
            <span>{{ columna.titulo }}</span><b>{{ columna.items.length }}</b>
          </button>
          <div class="cards">
            <button v-for="item in columna.items" :key="`${item.proceso}-${item.id}`" class="ticket" @click="abrirDetalle(item)">
              <div class="ticket-top"><span :class="['module', item.proceso.toLowerCase()]">{{ item.modulo }}</span><small>{{ fecha(item.fecha) }}</small></div>
              <strong>{{ item.titulo || 'Solicitud institucional' }}</strong>
              <p>{{ item.codigo || `#${item.id}` }} · {{ item.ubicacion || 'Sin ubicación' }}</p>
              <div class="progress"><i :style="{ width: `${progreso(item.estado_codigo)}%` }"></i></div>
              <footer><span>{{ item.estado_nombre || item.estado_codigo }}</span><span>Ver detalle →</span></footer>
            </button>
            <div v-if="!columna.items.length" class="empty">No hay solicitudes</div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import SolicitanteMenu from '../components/SolicitanteMenu.vue'

const router = useRouter()
const cargando = ref(true), error = ref(''), mostrarCrear = ref(false), solicitudes = ref([])
const usuario = JSON.parse(localStorage.getItem('sigta_usuario') || '{}')
const nombre = computed(() => usuario.nombre_completo || usuario.nombre || 'Usuario')
const saludo = computed(() => new Date().getHours() < 12 ? 'Buenos días' : new Date().getHours() < 19 ? 'Buenas tardes' : 'Buenas noches')
const token = () => localStorage.getItem('sigta_token')
const lista = data => Array.isArray(data) ? data : (data?.results || [])

function bucket(codigo) {
  const e = String(codigo || '').toUpperCase()
  if (e === 'PENDIENTE_CONFORMIDAD') return 'POR_VALIDAR'
  if (/ANUL|RECHAZ/.test(e)) return 'CANCELADAS'
  if (/CERRADO|RESUELTO|FINALIZADO/.test(e)) return 'FINALIZADAS'
  if (/BORRADOR|NUEVO|RECIBIDO/.test(e)) return 'PENDIENTES'
  return 'EN_PROCESO'
}

const porValidar = computed(() => solicitudes.value.filter(x => bucket(x.estado_codigo) === 'POR_VALIDAR'))
const activas = computed(() => solicitudes.value.filter(x => !['FINALIZADAS','CANCELADAS'].includes(bucket(x.estado_codigo))).length)
const definiciones = [
  ['PENDIENTES','Pendientes','pending'], ['EN_PROCESO','En proceso','process'],
  ['POR_VALIDAR','Por validar','validate'], ['FINALIZADAS','Finalizadas','done'], ['CANCELADAS','Canceladas','cancelled'],
]
const columnas = computed(() => definiciones.map(([codigo,titulo,clase]) => ({ codigo,titulo,clase,items: solicitudes.value.filter(x => bucket(x.estado_codigo) === codigo) })))

async function endpoint(url) {
  const r = await fetch(url, { headers: { Authorization: `Token ${token()}`, Accept: 'application/json' } })
  if (!r.ok) throw new Error(`No se pudo consultar ${url.includes('soporte') ? 'Soporte Técnico' : 'Mantenimiento'}.`)
  return lista(await r.json())
}
async function cargar() {
  cargando.value = true; error.value = ''
  try {
    const [soporte,mantenimiento] = await Promise.all([endpoint('/api/soporte/tickets/'),endpoint('/api/mantenimiento/requerimientos/')])
    solicitudes.value = [
      ...soporte.map(x => ({...x,proceso:'SOPORTE',modulo:'Soporte Técnico',estado_codigo:x.estado_codigo||x.estado,estado_nombre:x.estado_nombre||x.estado_codigo,fecha:x.creado_en||x.created_at})),
      ...mantenimiento.map(x => ({...x,proceso:'MANTENIMIENTO',modulo:'Mantenimiento',estado_codigo:x.estado_codigo||x.estado,estado_nombre:x.estado_nombre||x.estado_codigo,fecha:x.creado_en||x.created_at})),
    ].sort((a,b) => new Date(b.fecha||0)-new Date(a.fecha||0))
  } catch (e) { error.value = e.message } finally { cargando.value = false }
}
function abrirColumna(estado) { router.push({path:'/usuario/mis-solicitudes',query:{estado}}) }
function abrirDetalle(item) { router.push({path:'/usuario/mis-solicitudes',query:{proceso:item.proceso,id:item.id}}) }
function irAValidaciones() { router.push({path:'/usuario/mis-solicitudes',query:{estado:'POR_VALIDAR'}}) }
function fecha(value) { return value ? new Date(value).toLocaleDateString('es-BO',{day:'2-digit',month:'short'}) : '' }
function progreso(estado) { return {PENDIENTES:18,EN_PROCESO:58,POR_VALIDAR:85,FINALIZADAS:100,CANCELADAS:100}[bucket(estado)] }
onMounted(cargar)
</script>

<style scoped>
*{box-sizing:border-box}.layout{display:flex;min-height:100vh;background:#f3f6f9;color:#17324a;font-family:Inter,Arial,sans-serif}.layout main{flex:1;min-width:0;padding:28px}.head{display:flex;justify-content:space-between;gap:24px;align-items:center;background:linear-gradient(120deg,#073b6f,#155f91);color:#fff;padding:25px 28px;border-radius:16px;box-shadow:0 12px 30px #073b6f24}.head h1{margin:4px 0 6px;font-size:28px}.head p{margin:0;color:#dceaf6}.eyebrow{font-size:11px!important;font-weight:800;letter-spacing:1.2px;color:#f5cf34!important}.head-actions{display:flex;gap:10px}.head button,.create-panel button,.column-title,.ticket,.refresh{cursor:pointer}.primary,.bell{border:0;border-radius:10px;height:44px;padding:0 17px;font-weight:800}.primary{background:#f2c400;color:#17324a}.bell{position:relative;background:#ffffff18;color:#fff;font-size:19px}.bell b{position:absolute;right:-4px;top:-6px;background:#e74c3c;color:white;border-radius:12px;padding:2px 6px;font-size:10px}.create-panel{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px}.create-panel button{display:flex;gap:14px;text-align:left;border:1px solid #dbe4eb;background:white;padding:18px;border-radius:12px}.create-panel button>span{font-size:28px}.create-panel strong,.create-panel small{display:block}.create-panel small{margin-top:4px;color:#71818f}.summary{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}.summary article{background:#fff;border:1px solid #e1e8ee;border-radius:12px;padding:16px}.summary span{font-size:12px;color:#687b8b}.summary strong{display:block;margin-top:7px;font-size:25px}.summary .attention{border-color:#f2c400;background:#fffdf1}.board-head{display:flex;justify-content:space-between;align-items:center;margin:22px 0 12px}.board-head h2{margin:0}.board-head p{margin:5px 0 0;color:#71818f;font-size:13px}.refresh{border:1px solid #ccd8e1;background:#fff;padding:9px 13px;border-radius:8px}.kanban{display:grid;grid-template-columns:repeat(5,minmax(230px,1fr));gap:13px;overflow-x:auto;padding-bottom:14px}.column{background:#e9eef3;border-radius:13px;min-height:390px;border-top:4px solid #8d9cab}.column.process{border-color:#3182ce}.column.validate{border-color:#f2c400}.column.done{border-color:#2e9d64}.column.cancelled{border-color:#d66b6b}.column-title{width:100%;display:flex;justify-content:space-between;border:0;background:transparent;padding:14px;font-weight:800;color:#263f52}.column-title b{background:white;border-radius:12px;padding:2px 8px}.cards{padding:0 9px 10px}.ticket{width:100%;border:1px solid #dde5eb;background:#fff;border-radius:10px;padding:13px;margin-bottom:9px;text-align:left;box-shadow:0 3px 9px #17324a0d}.ticket:hover{transform:translateY(-2px);box-shadow:0 8px 18px #17324a1a}.ticket-top,.ticket footer{display:flex;justify-content:space-between;gap:8px}.ticket strong{display:block;margin:10px 0 6px;font-size:13px}.ticket p,.ticket small,.ticket footer{font-size:10px;color:#71818f}.module{padding:3px 6px;border-radius:5px;font-size:9px;font-weight:800}.module.soporte{background:#e4f1ff;color:#1762a4}.module.mantenimiento{background:#fff1dc;color:#9a5b00}.progress{height:4px;background:#e7edf2;border-radius:4px;margin:11px 0}.progress i{display:block;height:100%;background:#1d75ae;border-radius:4px}.empty,.loading,.error{padding:28px;text-align:center;color:#788895}.error{background:#fff0f0;color:#b13c3c;border-radius:10px}@media(max-width:900px){.layout{display:block}.layout main{padding:15px}.head{align-items:flex-start;flex-direction:column}.summary{grid-template-columns:1fr 1fr}.kanban{grid-template-columns:repeat(5,270px)}.create-panel{grid-template-columns:1fr}}
</style>
