<template>

  <div class="layout">

    <!-- ================================================
         MENÚ ÚNICO DEL ADMINISTRADOR
    ================================================= -->

    <SuperuserMenu />


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
            Preferencias del sistema
          </h1>

          <p>
            Parámetros institucionales,
            operativos y de seguridad de SIGTA.
          </p>

        </div>


        <button
          class="save-top"
          type="button"
          :disabled="guardando"
          @click="guardar"
        >
          {{
            guardando
              ? 'Guardando...'
              : 'Guardar cambios'
          }}
        </button>

      </header>


      <!-- ==============================================
           MENSAJES
      =============================================== -->

      <div
        v-if="mensaje"
        class="success"
      >
        {{ mensaje }}
      </div>


      <div
        v-if="error"
        class="error"
      >
        {{ error }}
      </div>


      <!-- ==============================================
           CONFIGURACIONES
      =============================================== -->

      <section class="settings-grid">

        <!-- ============================================
             IDENTIDAD
        ============================================= -->

        <article class="setting-card">

          <div class="card-header">

            <span>
              01
            </span>

            <div>

              <h2>
                Identidad institucional
              </h2>

              <p>
                Información general visible
                dentro de SIGTA.
              </p>

            </div>

          </div>


          <div class="fields">

            <div class="field">

              <label>
                Nombre del sistema
              </label>

              <input
                v-model="form.nombre_sistema"
                type="text"
                placeholder="SIGTA"
              />

            </div>


            <div class="field">

              <label>
                Institución
              </label>

              <input
                v-model="form.institucion"
                type="text"
                placeholder="Escuela Militar de Ingeniería"
              />

            </div>


            <div class="field full">

              <label>
                Unidad académica
              </label>

              <input
                v-model="form.unidad_academica"
                type="text"
                placeholder="Unidad Académica Santa Cruz"
              />

            </div>

          </div>

        </article>


        <!-- ============================================
             PROCESOS
        ============================================= -->

        <article class="setting-card">

          <div class="card-header">

            <span>
              02
            </span>

            <div>

              <h2>
                Configuración operativa
              </h2>

              <p>
                Identificadores y parámetros
                generales de los procesos.
              </p>

            </div>

          </div>


          <div class="fields">

            <div class="field">

              <label>
                Prefijo Soporte Técnico
              </label>

              <input
                v-model="form.prefijo_soporte"
                type="text"
                placeholder="SOP"
              />

              <small>
                Ejemplo: SOP-2026-0001.
              </small>

            </div>


            <div class="field">

              <label>
                Prefijo Compras
              </label>

              <input
                v-model="form.prefijo_compras"
                type="text"
                placeholder="CMP"
              />

              <small>
                Ejemplo: CMP-2026-0001.
              </small>

            </div>


            <div class="field full">

              <label>
                Límite de Caja Chica (Bs)
              </label>

              <input
                v-model.number="form.limite_caja_chica"
                type="number"
                min="0"
              />

              <small>
                Valor utilizado para determinar
                la vía de adquisición correspondiente.
              </small>

            </div>

          </div>

        </article>


        <!-- ============================================
             SEGURIDAD
        ============================================= -->

        <article class="setting-card">

          <div class="card-header">

            <span>
              03
            </span>

            <div>

              <h2>
                Seguridad de acceso
              </h2>

              <p>
                Parámetros relacionados con
                intentos fallidos y bloqueo temporal.
              </p>

            </div>

          </div>


          <div class="fields">

            <div class="field">

              <label>
                Intentos máximos
              </label>

              <input
                v-model.number="form.intentos_login"
                type="number"
                min="1"
              />

              <small>
                Cantidad de intentos fallidos
                permitidos antes del bloqueo.
              </small>

            </div>


            <div class="field">

              <label>
                Tiempo de bloqueo
              </label>

              <div class="input-unit">

                <input
                  v-model.number="
                    form.tiempo_bloqueo_minutos
                  "
                  type="number"
                  min="1"
                />

                <span>
                  min
                </span>

              </div>

              <small>
                Duración del bloqueo temporal
                de la cuenta.
              </small>

            </div>

          </div>

        </article>

      </section>


      <!-- ==============================================
           NOTA INSTITUCIONAL
      =============================================== -->

      <section class="system-note">

        <div>

          <span class="section-label">
            CONFIGURACIÓN CENTRAL
          </span>

          <strong>
            Preferencias generales de SIGTA
          </strong>

          <p>
            Los cambios efectuados en esta sección
            modifican parámetros generales del sistema
            y deben quedar registrados en la auditoría.
          </p>

        </div>


        <span class="admin-badge">
          ADMIN
        </span>

      </section>

    </main>

  </div>

</template>


<script setup>

import {
  onMounted,
  reactive,
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'

import SuperuserMenu
  from '../components/SuperuserMenu.vue'


const router =
  useRouter()


// ==========================================================
// ESTADO
// ==========================================================

const mensaje =
  ref('')

const error =
  ref('')

const guardando =
  ref(false)


// ==========================================================
// FORMULARIO
// ==========================================================

const form =
  reactive({

    nombre_sistema:
      'SIGTA',

    institucion:
      'Escuela Militar de Ingeniería',

    unidad_academica:
      'Unidad Académica Santa Cruz',

    prefijo_soporte:
      'SOP',

    prefijo_compras:
      'CMP',

    limite_caja_chica:
      1500,

    intentos_login:
      5,

    tiempo_bloqueo_minutos:
      15,
  })


// ==========================================================
// TOKEN
// ==========================================================

function token() {

  return localStorage.getItem(
    'sigta_token'
  )
}


// ==========================================================
// HEADERS
// ==========================================================

function headersJson() {

  return {

    'Content-Type':
      'application/json',

    Accept:
      'application/json',

    Authorization:
      `Token ${token()}`,
  }
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


    await cargarPreferencias()
  }
)


// ==========================================================
// CARGAR
// ==========================================================

async function cargarPreferencias() {

  error.value =
    ''


  try {

    const respuesta =
      await fetch(
        '/api/auditoria/preferencias/',
        {
          headers:
            headersJson()
        }
      )


    if (
      respuesta.status === 401
      ||
      respuesta.status === 403
    ) {

      cerrarSesion()

      return
    }


    if (!respuesta.ok) {

      error.value =
        'No fue posible cargar las preferencias del sistema.'

      return
    }


    const datos =
      await respuesta.json()


    Object.assign(
      form,
      datos
    )


  } catch (err) {

    console.error(
      'Error cargando preferencias:',
      err
    )


    error.value =
      'No fue posible conectar con el servicio de preferencias.'
  }
}


// ==========================================================
// GUARDAR
// ==========================================================

async function guardar() {

  mensaje.value =
    ''

  error.value =
    ''

  guardando.value =
    true


  try {

    const respuesta =
      await fetch(
        '/api/auditoria/preferencias/',
        {
          method:
            'PUT',

          headers:
            headersJson(),

          body:
            JSON.stringify(
              form
            ),
        }
      )


    if (
      respuesta.status === 401
      ||
      respuesta.status === 403
    ) {

      cerrarSesion()

      return
    }


    let datos = {}


    try {

      datos =
        await respuesta.json()

    } catch {

      datos = {}
    }


    if (!respuesta.ok) {

      error.value =
        datos?.detalle
        ||
        datos?.detail
        ||
        'No fue posible guardar las preferencias.'

      return
    }


    Object.assign(
      form,
      datos
    )


    mensaje.value =
      'Preferencias actualizadas correctamente.'


    setTimeout(
      () => {

        mensaje.value =
          ''

      },
      3500
    )


  } catch (err) {

    console.error(
      'Error guardando preferencias:',
      err
    )


    error.value =
      'No fue posible guardar las preferencias del sistema.'


  } finally {

    guardando.value =
      false
  }
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


.breadcrumb {
  display: block;
  margin-bottom: 6px;
  color: #8493a0;
  font-size: 15px;
}


.topbar h1 {
  margin: 0;
  color: #17324a;
  font-size: 27px;
}


.topbar p {
  margin: 5px 0 0;
  color: #718294;
  font-size: 17px;
  line-height: 1.45;
}


/* =========================================================
   GUARDAR
========================================================= */

.save-top {
  min-height: 39px;
  padding: 0 15px;
  border: none;
  border-radius: 7px;
  background: #f2c400;
  color: #17324a;
  font-family: inherit;
  font-size: 15px;
  font-weight: 900;
  cursor: pointer;
}


.save-top:hover {
  background: #e4b900;
}


.save-top:disabled {
  opacity: .6;
  cursor: not-allowed;
}


/* =========================================================
   MENSAJES
========================================================= */

.success,
.error {
  margin-bottom: 15px;
  padding: 10px 12px;
  border-radius: 7px;
  font-size: 14px;
}


.success {
  background: #e8f7ef;
  color: #237345;
}


.error {
  background: #fdeaea;
  color: #a53232;
}


/* =========================================================
   TARJETAS
========================================================= */

.settings-grid {
  display: grid;
  grid-template-columns:
    repeat(3,minmax(0,1fr));
  gap: 14px;
}


.setting-card {
  min-height: 310px;
  padding: 18px;
  border-top: 4px solid #f2c400;
  border-radius: 9px;
  background: white;
  box-shadow: 0 4px 14px rgba(0,0,0,.04);
}


/* =========================================================
   HEADER TARJETAS
========================================================= */

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 18px;
}


.card-header > span {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  background: #edf4fa;
  color: #07518d;
  font-size: 14px;
  font-weight: 900;
}


.card-header h2 {
  margin: 0;
  color: #29475e;
  font-size: 20px;
}


.card-header p {
  margin: 4px 0 0;
  color: #7a8995;
  font-size: 14px;
  line-height: 1.45;
}


/* =========================================================
   CAMPOS
========================================================= */

.fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}


.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}


.field.full {
  grid-column: 1 / -1;
}


.field label {
  color: #43596b;
  font-size: 14px;
  font-weight: 800;
}


.field input {
  width: 100%;
  height: 39px;
  padding: 0 10px;
  border: 1px solid #ccd6de;
  border-radius: 6px;
  background: white;
  color: #344b5e;
  font-family: inherit;
  font-size: 15px;
  outline: none;
}


.field input:focus {
  border-color: #0b5795;
  box-shadow: 0 0 0 3px rgba(11,87,149,.08);
}


.field small {
  color: #87949e;
  font-size: 13px;
  line-height: 1.4;
}


/* =========================================================
   UNIDAD
========================================================= */

.input-unit {
  display: flex;
  align-items: center;
}


.input-unit input {
  border-radius: 6px 0 0 6px;
}


.input-unit span {
  height: 39px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  border: 1px solid #ccd6de;
  border-left: none;
  border-radius: 0 6px 6px 0;
  background: #f1f4f6;
  color: #687986;
  font-size: 14px;
}


/* =========================================================
   NOTA
========================================================= */

.system-note {
  margin-top: 17px;
  padding: 15px 17px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  border-left: 4px solid #07518d;
  border-radius: 8px;
  background: #edf4fa;
}


.section-label {
  display: block;
  margin-bottom: 4px;
  color: #07518d;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .8px;
}


.system-note strong {
  display: block;
  color: #07518d;
  font-size: 16px;
}


.system-note p {
  margin: 4px 0 0;
  color: #678092;
  font-size: 14px;
  line-height: 1.45;
}


.admin-badge {
  flex-shrink: 0;
  padding: 5px 8px;
  border-radius: 5px;
  background: white;
  color: #07518d;
  font-size: 14px;
  font-weight: 900;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 1100px) {

  .settings-grid {
    grid-template-columns: 1fr;
  }


  .setting-card {
    min-height: auto;
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


  .fields {
    grid-template-columns: 1fr;
  }


  .field.full {
    grid-column: auto;
  }


  .system-note {
    align-items: flex-start;
    flex-direction: column;
  }
}

</style>
