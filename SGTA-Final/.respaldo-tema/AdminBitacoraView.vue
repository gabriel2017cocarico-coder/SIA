<template>

  <div class="layout">

    <!-- ================================================
         MENÚ: cada portal conserva su propio sidebar
         (esta pantalla se comparte entre Director y
         Superusuario, pero cada uno accede por su
         propia ruta).
    ================================================= -->

    <SuperuserMenu v-if="esRutaSuperuser" />
    <AdminMenu v-else />


    <!-- ================================================
         CONTENIDO
    ================================================= -->

    <main class="content">

      <!-- ==============================================
           ENCABEZADO
      =============================================== -->

      <header class="topbar">

        <div>

          <h1>
            Auditoría del sistema
          </h1>

          <p>
            Auditoría de accesos y actividades
            realizadas dentro de SIGTA.
          </p>

        </div>


        <div class="security-box">

          <span>
            REGISTRO ACTIVO
          </span>

          <strong>
            {{ registros.length }} eventos
          </strong>

        </div>

      </header>


      <!-- ==============================================
           RESUMEN
      =============================================== -->

      <section class="summary">

        <article>

          <span>
            Total de eventos
          </span>

          <strong>
            {{ registros.length }}
          </strong>

          <small>
            Registros almacenados
          </small>

        </article>


        <article>

          <span>
            Seguridad
          </span>

          <strong>
            {{ cantidad('SECURITY') }}
          </strong>

          <small>
            Eventos de seguridad
          </small>

        </article>


        <article>

          <span>
            Advertencias
          </span>

          <strong>
            {{ cantidad('WARNING') }}
          </strong>

          <small>
            Eventos que requieren atención
          </small>

        </article>


        <article>

          <span>
            Errores
          </span>

          <strong>
            {{ cantidad('ERROR') }}
          </strong>

          <small>
            Errores registrados
          </small>

        </article>

      </section>


      <!-- ==============================================
           FILTROS
      =============================================== -->

      <section class="filters-card">

        <div class="filters-header">

          <div>

            <span class="section-label">
              CONSULTA DE AUDITORÍA
            </span>

            <h2>
              Buscar registros
            </h2>

            <p>
              Consulte las acciones realizadas
              por los usuarios dentro del sistema.
            </p>

          </div>


          <button
            class="refresh-button"
            type="button"
            :disabled="cargando"
            @click="cargar"
          >
            {{
              cargando
                ? 'Actualizando...'
                : 'Actualizar'
            }}
          </button>

        </div>


        <div class="filters">

          <div class="search-box">

            <label>
              Buscar registro
            </label>

            <input
              v-model="buscar"
              type="text"
              placeholder="Usuario, acción, módulo o detalle..."
            />

          </div>


          <div>

            <label>
              Nivel
            </label>

            <select
              v-model="nivel"
            >

              <option value="">
                Todos los niveles
              </option>

              <option value="INFO">
                Información
              </option>

              <option value="SECURITY">
                Seguridad
              </option>

              <option value="WARNING">
                Advertencia
              </option>

              <option value="ERROR">
                Error
              </option>

            </select>

          </div>

        </div>

      </section>


      <!-- ==============================================
           TABLA
      =============================================== -->

      <section class="table-card">

        <div class="table-title">

          <div>

            <span class="section-label">
              HISTORIAL DE AUDITORÍA
            </span>

            <h2>
              Registros del sistema
            </h2>

          </div>


          <span class="result-count">
            {{ filtrados.length }}
            registro(s)
          </span>

        </div>


        <div class="table-scroll">

          <div class="table-content">

            <!-- ========================================
                 CABECERA
            ========================================= -->

            <div class="table-header">

              <span>
                Fecha y hora
              </span>

              <span>
                Usuario
              </span>

              <span>
                Acción
              </span>

              <span>
                Módulo
              </span>

              <span>
                Nivel
              </span>

              <span>
                IP
              </span>

            </div>


            <!-- ========================================
                 CARGANDO
            ========================================= -->

            <div
              v-if="cargando"
              class="empty"
            >

              <strong>
                Cargando auditoría...
              </strong>

              <span>
                Espere mientras se consultan
                los registros del sistema.
              </span>

            </div>


            <!-- ========================================
                 SIN RESULTADOS
            ========================================= -->

            <div
              v-else-if="filtrados.length === 0"
              class="empty"
            >

              <strong>
                No existen registros para este filtro.
              </strong>

              <span>
                Los accesos y operaciones de SIGTA
                se registran automáticamente.
              </span>

            </div>


            <!-- ========================================
                 FILAS
            ========================================= -->

            <div
              v-for="item in filtrados"
              :key="item.id"
              class="table-row"
            >

              <!-- FECHA -->

              <div>

                <strong>
                  {{ fecha(item.fecha) }}
                </strong>

              </div>


              <!-- USUARIO -->

              <div>

                <strong>
                  {{
                    item.usuario_nombre
                    || 'Sistema'
                  }}
                </strong>

                <small>
                  {{
                    item.usuario_email
                    || '-'
                  }}
                </small>

              </div>


              <!-- ACCIÓN -->

              <div>

                <strong>
                  {{
                    item.accion
                    || '-'
                  }}
                </strong>

                <small>
                  {{
                    item.detalle
                    || 'Sin detalle adicional'
                  }}
                </small>

              </div>


              <!-- MÓDULO -->

              <div>

                <span class="module-badge">
                  {{
                    item.modulo
                    || 'Sistema'
                  }}
                </span>

              </div>


              <!-- NIVEL -->

              <div>

                <span
                  :class="[
                    'level',
                    claseNivel(item.nivel)
                  ]"
                >
                  {{
                    item.nivel_nombre
                    || item.nivel
                    || 'INFO'
                  }}
                </span>

              </div>


              <!-- IP -->

              <div>

                {{
                  item.ip
                  || '-'
                }}

              </div>

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
  ref
} from 'vue'

import {
  useRoute,
  useRouter
} from 'vue-router'

import AdminMenu
  from '../components/AdminMenu.vue'

import SuperuserMenu
  from '../components/SuperuserMenu.vue'


const router =
  useRouter()

const route =
  useRoute()

const esRutaSuperuser =
  computed(() =>
    route.path.startsWith('/superuser')
  )


// ==========================================================
// DATOS
// ==========================================================

const registros =
  ref([])

const cargando =
  ref(true)

const buscar =
  ref('')

const nivel =
  ref('')


// ==========================================================
// TOKEN
// ==========================================================

function token() {

  return localStorage.getItem(
    'sigta_token'
  )
}


// ==========================================================
// INICIO
// ==========================================================

onMounted(
  async () => {

    if (!token()) {

      router.push(
        '/login'
      )

      return
    }


    await cargar()
  }
)


// ==========================================================
// NORMALIZAR LISTA
// ==========================================================

function normalizarLista(
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


// ==========================================================
// CARGAR BITÁCORA
// ==========================================================

async function cargar() {

  cargando.value =
    true


  try {

    const respuesta =
      await fetch(
        '/api/auditoria/bitacora/',
        {
          headers: {

            Authorization:
              `Token ${token()}`,

            Accept:
              'application/json',
          }
        }
      )


    // ------------------------------------------------------
    // SESIÓN EXPIRADA
    // ------------------------------------------------------

    if (
      respuesta.status === 401
      ||
      respuesta.status === 403
    ) {

      cerrarSesion()

      return
    }


    if (!respuesta.ok) {

      console.error(
        'Auditoría:',
        respuesta.status
      )

      registros.value = []

      return
    }


    const datos =
      await respuesta.json()


    registros.value =
      normalizarLista(
        datos
      )


  } catch (error) {

    console.error(
      'Error cargando auditoría:',
      error
    )


    registros.value = []


  } finally {

    cargando.value =
      false
  }
}


// ==========================================================
// FILTROS
// ==========================================================

const filtrados =
  computed(() => {

    const q =
      buscar.value
        .toLowerCase()
        .trim()


    return registros.value.filter(
      item => {

        const nivelActual =
          String(
            item.nivel
            || ''
          )
            .toUpperCase()


        const nivelOk =
          !nivel.value
          ||
          nivelActual === nivel.value


        const texto =
          [
            item.usuario_nombre,
            item.usuario_email,
            item.accion,
            item.modulo,
            item.detalle,
            item.ip,
          ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase()


        const textoOk =
          !q
          ||
          texto.includes(q)


        return (
          nivelOk
          &&
          textoOk
        )
      }
    )
  })


// ==========================================================
// CANTIDAD POR NIVEL
// ==========================================================

function cantidad(
  valor
) {

  return registros.value.filter(
    item =>
      String(
        item.nivel
        || ''
      )
        .toUpperCase()
      ===
      valor
  ).length
}


// ==========================================================
// FECHA
// ==========================================================

function fecha(
  valor
) {

  if (!valor) {

    return '-'
  }


  try {

    return new Intl.DateTimeFormat(
      'es-BO',
      {
        dateStyle:
          'short',

        timeStyle:
          'medium',
      }
    ).format(
      new Date(valor)
    )

  } catch {

    return valor
  }
}


// ==========================================================
// CLASE NIVEL
// ==========================================================

function claseNivel(
  valor
) {

  return String(
    valor
    || 'INFO'
  )
    .trim()
    .toLowerCase()
}


// ==========================================================
// CERRAR SESIÓN
// ==========================================================

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

.layout {
  min-height: 100vh;
  display: flex;
  background: #f2f5f9;
  font-family: Arial, Helvetica, sans-serif;
}


.content {
  flex: 1;
  min-width: 0;
  padding: 27px;
  overflow-x: hidden;
}


/* =========================================================
   ENCABEZADO
========================================================= */

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}


.topbar h1 {
  margin: 0;
  color: #17324a;
  font-size: 33px;
}


.topbar p {
  margin: 5px 0 0;
  color: #718294;
  font-size: 17px;
  line-height: 1.45;
}


/* =========================================================
   CAJA REGISTRO
========================================================= */

.security-box {
  min-width: 145px;
  padding: 11px 15px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 3px 12px rgba(0,0,0,.05);
}


.security-box span,
.security-box strong {
  display: block;
}


.security-box span {
  color: #237345;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .5px;
}


.security-box strong {
  margin-top: 4px;
  color: #29475e;
  font-size: 17px;
}


/* =========================================================
   RESUMEN
========================================================= */

.summary {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 13px;
  margin-bottom: 17px;
}


.summary article {
  min-height: 105px;
  padding: 17px;
  border-top: 4px solid #f2c400;
  border-radius: 9px;
  background: white;
  box-shadow: 0 3px 12px rgba(0,0,0,.05);
}


.summary span,
.summary small {
  display: block;
}


.summary span {
  color: #718294;
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
}


.summary strong {
  display: block;
  margin: 7px 0 4px;
  color: #073b6f;
  font-size: 32px;
}


.summary small {
  color: #8593a0;
  font-size: 14px;
}


/* =========================================================
   FILTROS
========================================================= */

.filters-card {
  margin-bottom: 17px;
  padding: 17px;
  border-radius: 9px;
  background: white;
  box-shadow: 0 3px 12px rgba(0,0,0,.04);
}


.filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 14px;
}


.section-label {
  display: block;
  margin-bottom: 4px;
  color: #07518d;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .8px;
}


.filters-header h2,
.table-title h2 {
  margin: 0;
  color: #17324a;
  font-size: 21px;
}


.filters-header p {
  margin: 4px 0 0;
  color: #778895;
  font-size: 14px;
}


.refresh-button {
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid #ccd6de;
  border-radius: 6px;
  background: white;
  color: #526777;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}


.refresh-button:hover {
  border-color: #073b6f;
  color: #073b6f;
}


.refresh-button:disabled {
  opacity: .6;
  cursor: not-allowed;
}


.filters {
  display: grid;
  grid-template-columns: 1fr 230px;
  gap: 12px;
}


.filters > div {
  display: flex;
  flex-direction: column;
  gap: 5px;
}


.filters label {
  color: #536575;
  font-size: 14px;
  font-weight: 800;
}


.filters input,
.filters select {
  width: 100%;
  height: 39px;
  padding: 0 11px;
  border: 1px solid #d0dae2;
  border-radius: 6px;
  background: white;
  color: #344b5e;
  font-family: inherit;
  font-size: 15px;
  outline: none;
}


.filters input:focus,
.filters select:focus {
  border-color: #07518d;
}


/* =========================================================
   TABLA
========================================================= */

.table-card {
  overflow: hidden;
  border-radius: 9px;
  background: white;
  box-shadow: 0 4px 14px rgba(0,0,0,.04);
}


.table-title {
  min-height: 62px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  padding: 14px 16px;
  border-bottom: 1px solid #e8edf1;
}


.result-count {
  padding: 5px 8px;
  border-radius: 20px;
  background: #edf4fa;
  color: #07518d;
  font-size: 13px;
  font-weight: 800;
}


.table-scroll {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
}


.table-content {
  min-width: 1050px;
}


.table-header,
.table-row {
  display: grid;
  grid-template-columns:
    150px
    180px
    minmax(300px,1fr)
    150px
    120px
    120px;

  gap: 12px;

  align-items: center;
}


.table-header {
  min-height: 43px;
  padding: 0 16px;
  background: #f7f9fb;
  color: #607383;
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
}


.table-row {
  min-height: 66px;
  padding: 11px 16px;
  border-top: 1px solid #edf0f2;
  color: #536777;
  font-size: 15px;
}


.table-row:hover {
  background: #fafcfd;
}


.table-row strong,
.table-row small {
  display: block;
}


.table-row strong {
  color: #29475e;
  font-size: 15px;
}


.table-row small {
  margin-top: 3px;
  color: #84919b;
  font-size: 13px;
  line-height: 1.4;
}


/* =========================================================
   MÓDULO
========================================================= */

.module-badge {
  display: inline-block;
  padding: 5px 7px;
  border-radius: 5px;
  background: #edf3f7;
  color: #587183;
  font-size: 13px;
  font-weight: 700;
}


/* =========================================================
   NIVEL
========================================================= */

.level {
  display: inline-block;
  padding: 5px 8px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 800;
}


.level.info {
  background: #eaf3fb;
  color: #07518d;
}


.level.security {
  background: #f1ebfa;
  color: #633c89;
}


.level.warning {
  background: #fff5d9;
  color: #856500;
}


.level.error {
  background: #fdeaea;
  color: #a53232;
}


/* =========================================================
   VACÍO
========================================================= */

.empty {
  padding: 45px 20px;
  text-align: center;
  color: #758491;
}


.empty strong,
.empty span {
  display: block;
}


.empty strong {
  color: #526777;
  font-size: 16px;
}


.empty span {
  margin-top: 6px;
  font-size: 14px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1000px) {

  .summary {
    grid-template-columns: repeat(2,1fr);
  }
}


@media (max-width: 760px) {

  .layout {
    display: block;
  }


  .content {
    padding: 16px;
  }


  .topbar {
    align-items: flex-start;
    flex-direction: column;
  }


  .filters-header {
    align-items: flex-start;
    flex-direction: column;
  }


  .filters {
    grid-template-columns: 1fr;
  }


  .summary {
    grid-template-columns: 1fr;
  }
}

</style>
