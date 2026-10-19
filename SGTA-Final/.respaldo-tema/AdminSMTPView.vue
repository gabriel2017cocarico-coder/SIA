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
            Correo y notificaciones
          </h1>

          <p>
            Configuración del canal SMTP secundario
            utilizado por SIGTA.
          </p>

        </div>


        <span
          :class="[
            'status',
            form.activo
              ? 'enabled'
              : 'disabled'
          ]"
        >
          {{
            form.activo
              ? 'SMTP ACTIVO'
              : 'SMTP INACTIVO'
          }}
        </span>

      </header>


      <!-- ==============================================
           INFORMACIÓN
      =============================================== -->

      <section class="info-grid">

        <article class="info-card">

          <span class="number">
            01
          </span>

          <div>

            <strong>
              Recuperación de contraseña
            </strong>

            <p>
              Envío del código de recuperación
              solicitado por el usuario.
            </p>

          </div>

        </article>


        <article class="info-card">

          <span class="number">
            02
          </span>

          <div>

            <strong>
              Notificaciones de requerimientos
            </strong>

            <p>
              Avisos relacionados con cambios de estado,
              asignaciones y cierre de procesos.
            </p>

          </div>

        </article>


        <article class="info-card">

          <span class="number">
            03
          </span>

          <div>

            <strong>
              Canal secundario
            </strong>

            <p>
              SIGTA mantiene autenticación local;
              el correo se utiliza únicamente
              como medio de notificación.
            </p>

          </div>

        </article>

      </section>


      <!-- ==============================================
           CONFIGURACIÓN
      =============================================== -->

      <section class="configuration">

        <div class="configuration-header">

          <div>

            <span class="section-label">
              CONFIGURACIÓN DE CORREO
            </span>

            <h2>
              Configuración SMTP
            </h2>

            <p>
              Datos del servidor de correo autorizado
              para enviar mensajes desde SIGTA.
            </p>

          </div>


          <div class="provider">
            OUTLOOK / MICROSOFT
          </div>

        </div>


        <!-- ============================================
             FORMULARIO
        ============================================= -->

        <form
          @submit.prevent="guardar"
        >

          <div class="form-grid">

            <!-- ========================================
                 NOMBRE
            ========================================= -->

            <div class="field full">

              <label>
                Nombre de configuración
              </label>

              <input
                v-model="form.nombre"
                type="text"
                placeholder="Correo institucional EMI"
              />

            </div>


            <!-- ========================================
                 HOST
            ========================================= -->

            <div class="field">

              <label>
                Servidor SMTP
              </label>

              <input
                v-model="form.host"
                type="text"
                placeholder="smtp-mail.outlook.com"
              />

              <small>
                Servidor proporcionado por el
                proveedor de correo.
              </small>

            </div>


            <!-- ========================================
                 PUERTO
            ========================================= -->

            <div class="field">

              <label>
                Puerto
              </label>

              <input
                v-model.number="form.puerto"
                type="number"
                min="1"
                placeholder="587"
              />

              <small>
                Normalmente 587 con STARTTLS.
              </small>

            </div>


            <!-- ========================================
                 USUARIO
            ========================================= -->

            <div class="field">

              <label>
                Cuenta de envío
              </label>

              <input
                v-model="form.usuario"
                type="email"
                placeholder="sigta@emi.edu.bo"
              />

              <small>
                Cuenta autorizada para enviar
                mensajes desde SIGTA.
              </small>

            </div>


            <!-- ========================================
                 REMITENTE
            ========================================= -->

            <div class="field">

              <label>
                Remitente visible
              </label>

              <input
                v-model="form.remitente"
                type="email"
                placeholder="sigta@emi.edu.bo"
              />

              <small>
                Dirección que visualizará
                el destinatario.
              </small>

            </div>

          </div>


          <!-- ==========================================
               SEGURIDAD
          =========================================== -->

          <section class="security-section">

            <div class="security-header">

              <span class="section-label">
                SEGURIDAD
              </span>

              <h3>
                Seguridad de conexión
              </h3>

              <p>
                La credencial secreta no se guarda
                en esta pantalla ni se expone
                desde la interfaz.
              </p>

            </div>


            <!-- ========================================
                 TLS
            ========================================= -->

            <label class="switch-row">

              <input
                v-model="form.usar_tls"
                type="checkbox"
              />

              <div>

                <strong>
                  STARTTLS / TLS
                </strong>

                <span>
                  Proteger la conexión con
                  el servidor SMTP.
                </span>

              </div>

            </label>


            <!-- ========================================
                 ACTIVO
            ========================================= -->

            <label class="switch-row">

              <input
                v-model="form.activo"
                type="checkbox"
              />

              <div>

                <strong>
                  Habilitar notificaciones
                </strong>

                <span>
                  Permitir que SIGTA utilice
                  este canal de correo.
                </span>

              </div>

            </label>

          </section>


          <!-- ==========================================
               MENSAJE
          =========================================== -->

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


          <!-- ==========================================
               BOTONES
          =========================================== -->

          <div class="footer-actions">

            <button
              type="button"
              class="secondary"
              @click="
                router.push('/admin/dashboard')
              "
            >
              Cancelar
            </button>


            <button
              type="submit"
              class="primary"
              :disabled="guardando"
            >
              {{
                guardando
                  ? 'Guardando...'
                  : 'Guardar configuración'
              }}
            </button>

          </div>

        </form>

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

    nombre:
      'Correo institucional',

    host:
      '',

    puerto:
      587,

    usuario:
      '',

    remitente:
      '',

    usar_tls:
      true,

    activo:
      false,
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


    await cargarConfiguracion()
  }
)


// ==========================================================
// CARGAR CONFIGURACIÓN
// ==========================================================

async function cargarConfiguracion() {

  error.value =
    ''


  try {

    const respuesta =
      await fetch(
        '/api/auditoria/smtp/',
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
        'No fue posible cargar la configuración SMTP.'

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
      'Error cargando SMTP:',
      err
    )


    error.value =
      'No fue posible conectar con el servicio SMTP.'
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
        '/api/auditoria/smtp/',
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
        'No fue posible guardar la configuración.'

      return
    }


    Object.assign(
      form,
      datos
    )


    mensaje.value =
      'Configuración SMTP actualizada correctamente.'


    setTimeout(
      () => {

        mensaje.value =
          ''

      },
      3500
    )


  } catch (err) {

    console.error(
      'Error guardando SMTP:',
      err
    )


    error.value =
      'No fue posible guardar la configuración SMTP.'


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
  justify-content: space-between;
  align-items: center;
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
   ESTADO
========================================================= */

.status {
  padding: 7px 11px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: .3px;
}


.status.enabled {
  background: #e8f7ef;
  color: #237345;
}


.status.disabled {
  background: #f0f2f4;
  color: #687986;
}


/* =========================================================
   TARJETAS DE INFORMACIÓN
========================================================= */

.info-grid {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 13px;
  margin-bottom: 17px;
}


.info-card {
  min-height: 100px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border-top: 4px solid #f2c400;
  border-radius: 9px;
  background: white;
  box-shadow: 0 3px 12px rgba(0,0,0,.04);
}


.number {
  width: 33px;
  height: 33px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 7px;
  background: #edf4fa;
  color: #07518d;
  font-size: 15px;
  font-weight: 900;
}


.info-card strong {
  color: #29475e;
  font-size: 16px;
}


.info-card p {
  margin: 5px 0 0;
  color: #788894;
  font-size: 14px;
  line-height: 1.5;
}


/* =========================================================
   CONFIGURACIÓN
========================================================= */

.configuration {
  padding: 20px;
  border-top: 4px solid #f2c400;
  border-radius: 9px;
  background: white;
  box-shadow: 0 4px 14px rgba(0,0,0,.04);
}


.configuration-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 15px;
  border-bottom: 1px solid #edf0f2;
}


.section-label {
  display: block;
  margin-bottom: 4px;
  color: #07518d;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .8px;
}


.configuration-header h2 {
  margin: 0;
  color: #17324a;
  font-size: 17px;
}


.configuration-header p {
  margin: 5px 0 0;
  color: #788894;
  font-size: 15px;
}


.provider {
  flex-shrink: 0;
  padding: 6px 9px;
  border-radius: 5px;
  background: #edf4fa;
  color: #07518d;
  font-size: 14px;
  font-weight: 800;
}


/* =========================================================
   FORMULARIO
========================================================= */

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  max-width: 1100px;
  margin-top: 18px;
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
  color: #344b5e;
  font-size: 15px;
  font-weight: 800;
}


.field input {
  width: 100%;
  height: 40px;
  padding: 0 11px;
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
  color: #84919b;
  font-size: 13px;
}


/* =========================================================
   SEGURIDAD
========================================================= */

.security-section {
  max-width: 1100px;
  margin-top: 20px;
  padding: 15px;
  border-radius: 8px;
  background: #f7f9fb;
}


.security-header h3 {
  margin: 0;
  color: #29475e;
  font-size: 18px;
}


.security-header p {
  margin: 4px 0 13px;
  color: #788894;
  font-size: 14px;
}


.switch-row {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 10px 0;
  border-top: 1px solid #e6ebef;
  cursor: pointer;
}


.switch-row input {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
}


.switch-row strong,
.switch-row span {
  display: block;
}


.switch-row strong {
  color: #344b5e;
  font-size: 15px;
}


.switch-row span {
  margin-top: 3px;
  color: #84919b;
  font-size: 13px;
}


/* =========================================================
   MENSAJES
========================================================= */

.success,
.error {
  max-width: 1100px;
  margin-top: 14px;
  padding: 10px 12px;
  border-radius: 6px;
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
   ACCIONES
========================================================= */

.footer-actions {
  max-width: 1100px;
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  margin-top: 18px;
}


.footer-actions button {
  min-height: 38px;
  padding: 0 15px;
  border-radius: 6px;
  font-family: inherit;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}


.secondary {
  border: 1px solid #ccd6de;
  background: white;
  color: #506273;
}


.primary {
  border: none;
  background: #073b6f;
  color: white;
}


.primary:disabled {
  opacity: .6;
  cursor: not-allowed;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

  .info-grid {
    grid-template-columns: 1fr;
  }


  .form-grid {
    grid-template-columns: 1fr;
  }


  .field.full {
    grid-column: auto;
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


  .configuration-header {
    flex-direction: column;
  }
}

</style>