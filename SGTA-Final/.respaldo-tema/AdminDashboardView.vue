<template>

  <div class="dashboard-layout">

    <!-- =====================================================
         MENÚ ÚNICO DEL ADMINISTRADOR
    ====================================================== -->

    <AdminMenu />


    <!-- =====================================================
         CONTENIDO PRINCIPAL
    ====================================================== -->

    <main class="main-content">


      <!-- =================================================
           ENCABEZADO
      ================================================== -->

      <header class="topbar">

        <div>

          <h1>
            Panel de Administración
          </h1>

          <p>
            Supervisión general de los procesos y
            configuración del Sistema Integral de Gestión.
          </p>

        </div>


        <div class="user-box">

          <div class="user-avatar">
            {{ inicialesUsuario }}
          </div>

          <div>

            <strong>
              {{
                usuario?.nombre
                ||
                usuario?.nombre_completo
                ||
                'Administrador'
              }}
            </strong>

            <span>
              {{
                usuario?.email
                ||
                'admin@emi.edu.bo'
              }}
            </span>

          </div>

        </div>

      </header>


      <!-- =================================================
           RESUMEN GENERAL
      ================================================== -->

      <section class="stats-grid">


        <!-- USUARIOS -->

        <article
          class="stat-card"
          @click="abrirStatModal('usuarios')"
        >

          <span>
            Usuarios
          </span>

          <strong>
            {{ resumen.usuarios }}
          </strong>

          <small>
            Registrados en SIGTA
          </small>

        </article>


        <!-- TICKETS -->

        <article
          class="stat-card"
          @click="abrirStatModal('tickets')"
        >

          <span>
            Requerimientos de soporte
          </span>

          <strong>
            {{ resumen.tickets }}
          </strong>

          <small>
            Registrados en Soporte Técnico
          </small>

        </article>


        <!-- NUEVOS -->

        <article
          class="stat-card"
          @click="abrirStatModal('nuevos')"
        >

          <span>
            Requerimientos nuevos
          </span>

          <strong>
            {{ resumen.nuevos }}
          </strong>

          <small>
            Solicitudes registradas pendientes de atención UTIC
          </small>

        </article>


        <!-- COMPRAS -->

        <article
          class="stat-card"
          @click="abrirStatModal('compras')"
        >

          <span>
            Solicitudes de compra
          </span>

          <strong>
            {{ resumen.compras }}
          </strong>

          <small>
            Registradas en el proceso de Compras
          </small>

        </article>

      </section>


      <!-- =================================================
           MENSAJE
      ================================================== -->

      <div
        v-if="mensaje"
        class="dashboard-message"
      >
        {{ mensaje }}
      </div>


      <!-- =================================================
           DETALLE DEL PANEL (aparece al hacer clic
           en una de las tarjetas de arriba)
      ================================================== -->

      <section
        v-if="statCategoria"
        class="content-card"
      >

        <div class="section-header">

          <div>

            <span class="section-kicker">
              DETALLE
            </span>

            <h2>
              {{ statTitulo }}
            </h2>

            <p>
              {{ statItems.length }} de {{ statItemsBase.length }} registro(s)
            </p>

          </div>

          <button
            class="close-panel"
            type="button"
            @click="cerrarStatModal"
          >✕</button>

        </div>


        <input
          v-model="statBusqueda"
          type="text"
          class="stat-search"
          :placeholder="statPlaceholder"
        />


        <p
          v-if="statItems.length === 0"
          class="detalle-vacio"
        >
          No se encontraron registros.
        </p>

        <div
          v-else
          class="stat-list"
        >
          <div
            v-for="item in statItems"
            :key="item.id"
            class="stat-item"
          >
            <div class="stat-item-main">
              <strong>{{ item.titulo }}</strong>
              <span v-if="item.subtitulo">{{ item.subtitulo }}</span>
            </div>

            <div class="stat-item-side">

              <small v-if="item.meta">{{ item.meta }}</small>

              <button
                v-if="statCategoria === 'compras'"
                type="button"
                class="stat-item-revisar"
                @click="router.push('/admin/compras')"
              >
                Ir a revisar
              </button>

            </div>
          </div>
        </div>

      </section>


    </main>

  </div>

</template>


<script setup>

import {
  computed,
  onMounted,
  reactive,
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'


/* =========================================================
   MENÚ ÚNICO
========================================================= */

import AdminMenu
  from '../components/AdminMenu.vue'


const router =
  useRouter()


/* =========================================================
   USUARIO
========================================================= */

const usuario =
  ref(null)


/* =========================================================
   RESUMEN
========================================================= */

const resumen =
  reactive({

    usuarios: 0,

    tickets: 0,

    nuevos: 0,

    compras: 0,
  })


/* =========================================================
   REGISTROS COMPLETOS (PARA LOS MODALES DE DETALLE)
========================================================= */

const usuariosLista =
  ref([])

const ticketsLista =
  ref([])

const comprasLista =
  ref([])


/* =========================================================
   MENSAJE
========================================================= */

const mensaje =
  ref('')


/* =========================================================
   TOKEN
========================================================= */

const obtenerToken = () =>
  localStorage.getItem(
    'sigta_token'
  )


/* =========================================================
   INICIALES
========================================================= */

const inicialesUsuario =
  computed(() => {

    const nombre =
      usuario.value?.nombre
      ||
      usuario.value?.nombre_completo
      ||
      'Administrador'


    return nombre
      .trim()
      .split(/\s+/)
      .slice(0, 2)
      .map(
        palabra =>
          palabra
            .charAt(0)
            .toUpperCase()
      )
      .join('')
  })


/* =========================================================
   INICIO
========================================================= */

onMounted(
  async () => {

    const usuarioGuardado =
      localStorage.getItem(
        'sigta_usuario'
      )


    const token =
      obtenerToken()


    if (
      !usuarioGuardado
      ||
      !token
    ) {

      router.push(
        '/login'
      )

      return
    }


    try {

      usuario.value =
        JSON.parse(
          usuarioGuardado
        )

    } catch (error) {

      console.error(
        'Error leyendo usuario:',
        error
      )


      cerrarSesion()

      return
    }


    await cargarResumen()
  }
)


/* =========================================================
   HEADERS
========================================================= */

function headersAuth() {

  return {

    Authorization:
      `Token ${obtenerToken()}`,

    Accept:
      'application/json',
  }
}


/* =========================================================
   NORMALIZAR RESPUESTAS
========================================================= */

function convertirLista(
  datos
) {

  if (
    Array.isArray(datos)
  ) {

    return datos
  }


  if (
    Array.isArray(
      datos?.results
    )
  ) {

    return datos.results
  }


  return []
}


/* =========================================================
   CARGAR RESUMEN
========================================================= */

async function cargarResumen() {

  mensaje.value = ''


  try {

    const [
      usuariosRes,
      ticketsRes,
      comprasRes
    ] =
      await Promise.all([


        /* USUARIOS */

        fetch(
          '/api/usuarios/usuarios/',
          {
            headers:
              headersAuth()
          }
        ),


        /* SOPORTE TÉCNICO */

        fetch(
          '/api/soporte/tickets/',
          {
            headers:
              headersAuth()
          }
        ),


        /* COMPRAS */

        fetch(
          '/api/compras/solicitudes/',
          {
            headers:
              headersAuth()
          }
        ),

      ])


    /* =====================================================
       SESIÓN VENCIDA
    ====================================================== */

    const respuestas = [

      usuariosRes,

      ticketsRes,

      comprasRes
    ]


    const sinAutorizacion =
      respuestas.some(
        respuesta =>
          respuesta.status === 401
          ||
          respuesta.status === 403
      )


    if (
      sinAutorizacion
    ) {

      cerrarSesion()

      return
    }


    /* =====================================================
       LEER DATOS
    ====================================================== */

    const usuariosDatos =
      usuariosRes.ok
        ? await usuariosRes.json()
        : []


    const ticketsDatos =
      ticketsRes.ok
        ? await ticketsRes.json()
        : []


    const comprasDatos =
      comprasRes.ok
        ? await comprasRes.json()
        : []


    /* =====================================================
       NORMALIZAR
    ====================================================== */

    const usuarios =
      convertirLista(
        usuariosDatos
      )


    const tickets =
      convertirLista(
        ticketsDatos
      )


    const compras =
      convertirLista(
        comprasDatos
      )


    /* =====================================================
       GUARDAR REGISTROS COMPLETOS
       (para los modales de detalle de cada panel)
    ====================================================== */

    usuariosLista.value =
      usuarios


    ticketsLista.value =
      tickets


    comprasLista.value =
      compras


    /* =====================================================
       CONTADORES
    ====================================================== */

    resumen.usuarios =
      usuarios.length


    resumen.tickets =
      tickets.length


    resumen.compras =
      compras.length


    resumen.nuevos =
      tickets.filter(
        ticket => {

          const codigo =
            normalizarEstado(
              ticket.estado_codigo
            )


          const nombre =
            normalizarEstado(
              ticket.estado_nombre
            )


          return (
            codigo === 'NUEVO'
            ||
            nombre === 'NUEVO'
          )
        }
      ).length


    /* =====================================================
       AVISO SI UN ENDPOINT NO RESPONDE
    ====================================================== */

    const errores = []


    if (!usuariosRes.ok) {
      errores.push('usuarios')
    }


    if (!ticketsRes.ok) {
      errores.push('soporte técnico')
    }


    if (!comprasRes.ok) {
      errores.push('compras')
    }


    if (
      errores.length > 0
    ) {

      mensaje.value =
        `No fue posible cargar completamente: ${errores.join(', ')}.`

    }


    /* =====================================================
       DEBUG
    ====================================================== */

    console.log(
      'Dashboard usuarios:',
      usuarios
    )


    console.log(
      'Dashboard tickets:',
      tickets
    )


    console.log(
      'Dashboard expedientes de compra:',
      compras
    )


  } catch (error) {

    console.error(
      'Error cargando Dashboard:',
      error
    )


    mensaje.value =
      'No fue posible cargar todos los indicadores del panel.'
  }
}


/* =========================================================
   NORMALIZAR ESTADO
========================================================= */

function normalizarEstado(
  valor
) {

  return String(
    valor
    ||
    ''
  )
    .trim()
    .toUpperCase()
    .replace(/\s+/g, '_')
}


/* =========================================================
   MODAL DE DETALLE POR PANEL
========================================================= */

const statCategoria =
  ref('')

const statBusqueda =
  ref('')


const statConfig = {

  usuarios: {
    titulo: 'Usuarios',
    placeholder: 'Buscar por nombre o correo...',
  },

  tickets: {
    titulo: 'Requerimientos de soporte',
    placeholder: 'Buscar por código o título...',
  },

  nuevos: {
    titulo: 'Requerimientos nuevos',
    placeholder: 'Buscar por código o título...',
  },

  compras: {
    titulo: 'Solicitudes de compra',
    placeholder: 'Buscar por código o título...',
  },
}


const statTitulo =
  computed(() =>
    statConfig[statCategoria.value]?.titulo
    || ''
  )


const statPlaceholder =
  computed(() =>
    statConfig[statCategoria.value]?.placeholder
    || 'Buscar...'
  )


const statItemsBase =
  computed(() => {

    if (statCategoria.value === 'usuarios') {

      return usuariosLista.value.map(
        u => ({
          id: u.id,
          titulo: u.nombre_completo || u.username || u.email || 'Usuario',
          subtitulo: u.email || '',
          meta: u.roles?.[0]?.nombre || u.roles?.[0]?.rol_nombre || 'Sin rol',
        })
      )
    }


    if (statCategoria.value === 'tickets') {

      return ticketsLista.value.map(
        t => ({
          id: t.id,
          titulo: `${t.codigo || 'S/C'} · ${t.titulo || 'Sin título'}`,
          subtitulo: t.estado_nombre || t.estado_codigo || t.estado || '',
          meta: t.area_nombre || '',
        })
      )
    }


    if (statCategoria.value === 'nuevos') {

      return ticketsLista.value
        .filter(
          t => {

            const codigo =
              normalizarEstado(t.estado_codigo)

            const nombre =
              normalizarEstado(t.estado_nombre)

            return (
              codigo === 'NUEVO'
              ||
              nombre === 'NUEVO'
            )
          }
        )
        .map(
          t => ({
            id: t.id,
            titulo: `${t.codigo || 'S/C'} · ${t.titulo || 'Sin título'}`,
            subtitulo: t.estado_nombre || t.estado_codigo || t.estado || '',
            meta: t.area_nombre || '',
          })
        )
    }


    if (statCategoria.value === 'compras') {

      return comprasLista.value.map(
        c => ({
          id: c.id,
          titulo: `${c.codigo || 'S/C'} · ${c.titulo || 'Sin título'}`,
          subtitulo: c.estado_nombre || c.estado || '',
          meta: c.area_nombre || '',
        })
      )
    }


    return []
  })


const statItems =
  computed(() => {

    const texto =
      statBusqueda.value
        .trim()
        .toLowerCase()


    if (!texto) {
      return statItemsBase.value
    }


    return statItemsBase.value.filter(
      item =>
        [item.titulo, item.subtitulo, item.meta]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()
          .includes(texto)
    )
  })


function abrirStatModal(
  categoria
) {

  statCategoria.value =
    categoria

  statBusqueda.value =
    ''
}


function cerrarStatModal() {

  statCategoria.value =
    ''

  statBusqueda.value =
    ''
}


/* =========================================================
   CERRAR SESIÓN
========================================================= */

function cerrarSesion() {

  localStorage.removeItem(
    'sigta_token'
  )


  localStorage.removeItem(
    'sigta_usuario'
  )


  router.push(
    '/login'
  )
}

</script>


<style scoped>

* {
  box-sizing: border-box;
}


/* =========================================================
   LAYOUT
========================================================= */

.dashboard-layout {

  min-height: 100vh;

  display: flex;

  background: #f2f5f9;

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}


.main-content {

  flex: 1;

  min-width: 0;

  padding: 28px;

  overflow-x: hidden;
}


/* =========================================================
   TOPBAR
========================================================= */

.topbar {

  display: flex;

  justify-content:
    space-between;

  align-items: center;

  gap: 20px;

  margin-bottom: 24px;
}


.topbar h1 {

  margin: 0;

  color: #17324a;

  font-size: 34px;
}


.topbar p {

  margin:
    5px
    0
    0;

  color: #758391;

  font-size: 18px;
}


/* =========================================================
   USUARIO
========================================================= */

.user-box {

  min-width: 205px;

  display: flex;

  align-items: center;

  justify-content: flex-end;

  gap: 9px;

  padding:
    10px
    14px;

  background: #ffffff;

  border-radius: 9px;

  box-shadow:
    0
    3px
    10px
    rgba(0,0,0,.07);
}


.user-avatar {

  width: 35px;

  height: 35px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #f2c400;

  color: #073b6f;

  font-size: 15px;

  font-weight: 900;
}


.user-box strong,
.user-box span {

  display: block;
}


.user-box strong {

  color: #1c3449;

  font-size: 17px;
}


.user-box span {

  margin-top: 2px;

  color: #788693;

  font-size: 15px;
}


/* =========================================================
   ESTADÍSTICAS
========================================================= */

.stats-grid {

  display: grid;

  grid-template-columns:
    repeat(4,1fr);

  gap: 14px;

  margin-bottom: 22px;
}


.stat-card {

  min-width: 0;

  min-height: 120px;

  padding: 18px;

  background: #ffffff;

  border-top:
    4px solid #f2c400;

  border-radius: 10px;

  box-shadow:
    0
    4px
    14px
    rgba(0,0,0,.05);

  cursor: pointer;

  transition:
    transform .15s ease,
    box-shadow .15s ease;
}


.stat-card:hover {

  transform: scale(1.04);

  box-shadow:
    0
    8px
    20px
    rgba(0,0,0,.1);
}


.stat-card span {

  display: block;

  margin-bottom: 7px;

  color: #647484;

  font-size: 15px;

  font-weight: 800;

  text-transform: uppercase;
}


.stat-card strong {

  display: block;

  margin-bottom: 6px;

  color: #073b6f;

  font-size: 34px;
}


.stat-card small {

  color: #8995a0;

  font-size: 14px;

  line-height: 1.35;
}


/* =========================================================
   MENSAJE
========================================================= */

.dashboard-message {

  margin-bottom: 18px;

  padding:
    11px
    13px;

  border-radius: 7px;

  background: #fff2d9;

  color: #775600;

  font-size: 16px;
}


/* =========================================================
   CONTENEDORES
========================================================= */

.content-card {

  margin-bottom: 20px;

  padding: 22px;

  background: #ffffff;

  border-radius: 10px;

  box-shadow:
    0
    4px
    14px
    rgba(0,0,0,.05);
}


.section-kicker {

  display: block;

  margin-bottom: 5px;

  color: #0b5795;

  font-size: 14px;

  font-weight: 900;

  letter-spacing: .8px;
}


.section-header {

  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  gap: 14px;
}


.section-header h2 {

  margin: 0;

  color: #1b3449;

  font-size: 24px;
}


.section-header p {

  margin:
    5px
    0
    18px;

  color: #778590;

  font-size: 16px;
}


.close-panel {

  flex-shrink: 0;

  width: 32px;

  height: 32px;

  border: none;

  border-radius: 50%;

  background: #f1f3f6;

  color: #4a5a6a;

  font-size: 15px;

  line-height: 1;

  cursor: pointer;
}


.close-panel:hover {

  background: #e5e8ee;
}


/* =========================================================
   DETALLE DEL PANEL
========================================================= */

.stat-search {

  width: 100%;

  padding:
    12px
    14px;

  border:
    1px solid #d0dae2;

  border-radius: 8px;

  background: white;

  color: #17324a;

  font-family: inherit;

  font-size: 15px;

  outline: none;
}


.stat-search:focus {

  border-color: #0a5794;
}


.stat-list {

  margin-top: 14px;

  display: flex;

  flex-direction: column;
}


.content-card > .detalle-vacio {

  display: block;

  margin-top: 14px;
}


.stat-item {

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 12px;

  padding: 12px 4px;

  border-bottom: 1px solid #edf0f2;
}


.stat-item:last-child {

  border-bottom: none;
}


.stat-item-main {

  min-width: 0;
}


.stat-item-main strong {

  display: block;

  color: #17324a;

  font-size: 15px;
}


.stat-item-main span {

  display: block;

  margin-top: 2px;

  color: #71818f;

  font-size: 13px;
}


.stat-item-side {

  flex-shrink: 0;

  display: flex;

  flex-direction: column;

  align-items: flex-end;

  gap: 6px;
}


.stat-item-side > small {

  padding: 4px 8px;

  border-radius: 12px;

  background: #edf3f7;

  color: #557185;

  font-size: 12px;
  font-weight: 700;
}


.stat-item-revisar {

  padding: 0;

  border: none;

  background: transparent;

  color: #07518d;

  font-size: 13px;
  font-weight: 700;

  text-decoration: underline;

  cursor: pointer;
}


.stat-item-revisar:hover {

  color: #073b6f;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (
  max-width: 1200px
) {

  .stats-grid {

    grid-template-columns:
      repeat(3,1fr);
  }

}


@media (
  max-width: 900px
) {

  .stats-grid {

    grid-template-columns:
      repeat(2,1fr);
  }

}


@media (
  max-width: 760px
) {

  .dashboard-layout {

    display: block;
  }


  .main-content {

    padding: 18px;
  }


  .topbar {

    flex-direction: column;

    align-items: flex-start;
  }


  .user-box {

    justify-content:
      flex-start;
  }

}


@media (
  max-width: 520px
) {

  .stats-grid {

    grid-template-columns:
      1fr;
  }

}

</style>