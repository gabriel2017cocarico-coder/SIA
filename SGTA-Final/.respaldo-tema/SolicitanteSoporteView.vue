<template>

  <div class="layout">

    <!-- =====================================================
         MENÚ ÚNICO DEL SOLICITANTE
    ====================================================== -->

    <SolicitanteMenu />


    <main class="main">

      <!-- =================================================
           ENCABEZADO
      ================================================== -->

      <header class="topbar">

        <div>

          <h1>
            Registrar solicitud de soporte
          </h1>

          <p>
            Registre el problema detectado para que
            el equipo de UTIC pueda atenderlo.
          </p>

        </div>

      </header>


      <!-- =================================================
           FORMULARIO
      ================================================== -->

      <section class="form-card">


        <!-- =================================================
             PASO 1
        ================================================== -->

        <div class="form-section">

          <div class="section-heading">

            <span class="number">
              1
            </span>

            <div>

              <h2>
                Información del problema
              </h2>

              <p>
                Describa claramente la incidencia detectada.
              </p>

            </div>

          </div>


          <div class="grid">

            <!-- TÍTULO -->

            <div class="field full">

              <label>
                Título del problema
                <span>*</span>
              </label>

              <input
                v-model="form.titulo"
                type="text"
                maxlength="150"
                placeholder="Ej.: Computadora no enciende"
                required
              />

            </div>


            <!-- DESCRIPCIÓN -->

            <div class="field full">

              <label>
                Descripción
                <span>*</span>
              </label>

              <textarea
                v-model="form.descripcion"
                maxlength="1000"
                placeholder="Explique qué sucede, desde cuándo ocurre y cómo afecta su trabajo..."
                required
              ></textarea>

              <small class="counter">
                {{ form.descripcion.length }} / 1000 caracteres
              </small>

            </div>

          </div>

        </div>


        <!-- =================================================
             PASO 2
        ================================================== -->

        <div class="form-section">

          <div class="section-heading">

            <span class="number">
              2
            </span>

            <div>

              <h2>
                Ubicación y equipo afectado
              </h2>

              <p>
                Indique dónde se encuentra el problema.
              </p>

            </div>

          </div>


          <div class="grid">


            <!-- UBICACIÓN -->

            <div class="field">

              <label>
                Ubicación
                <span>*</span>
              </label>

              <input
                v-model="form.ubicacion"
                type="text"
                maxlength="200"
                placeholder="Ej.: Laboratorio de Redes - Aula C0-07"
                required
              />

            </div>


            <!-- EQUIPO -->

            <div class="field">

              <label>
                Equipo afectado
                <span>*</span>
              </label>

              <input
                v-model="form.equipo_afectado"
                type="text"
                maxlength="200"
                placeholder="Ej.: PC, proyector, router, aire acondicionado"
                required
              />

            </div>

          </div>

        </div>


        <!-- =================================================
             PASO 4 - EVIDENCIA REAL
        ================================================== -->

        <div class="form-section">

          <div class="section-heading">

            <span class="number">
              3
            </span>

            <div>

              <h2>
                Evidencia
              </h2>

              <p>
                Puede cargar una fotografía o documento
                que ayude a identificar el problema.
              </p>

            </div>

          </div>


          <!-- DESCRIPCIÓN EVIDENCIA -->

          <div class="field full">

            <label>
              Descripción de la evidencia
              <span class="optional">
                Opcional
              </span>
            </label>

            <textarea
              v-model="form.evidencia"
              class="evidence-text"
              maxlength="500"
              placeholder="Ej.: El equipo muestra una pantalla azul al encender..."
            ></textarea>

          </div>


          <!-- =================================================
               CARGA DE ARCHIVO
          ================================================== -->

          <div class="upload-container">


            <!-- INPUT OCULTO -->

            <input
              id="evidencia-archivo"
              ref="inputArchivo"
              class="file-input"
              type="file"
              accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf"
              @change="seleccionarArchivo"
            />


            <!-- CAJA PARA SELECCIONAR -->

            <label
              v-if="!archivoSeleccionado"
              for="evidencia-archivo"
              class="upload-box"
            >

              <div class="upload-icon">
                ↑
              </div>


              <strong>
                Cargar evidencia
              </strong>


              <span>
                Haga clic para seleccionar una imagen
                o documento
              </span>


              <small>
                JPG, JPEG, PNG o PDF · Máximo 5 MB
              </small>

            </label>


            <!-- =================================================
                 ARCHIVO SELECCIONADO
            ================================================== -->

            <div
              v-else
              class="selected-file-card"
            >


              <!-- PREVISUALIZACIÓN IMAGEN -->

              <div
                v-if="vistaPrevia"
                class="preview-wrapper"
              >

                <img
                  :src="vistaPrevia"
                  alt="Vista previa de evidencia"
                  class="preview-image"
                />

              </div>


              <!-- PDF -->

              <div
                v-else
                class="pdf-preview"
              >

                <div class="pdf-icon">
                  PDF
                </div>

              </div>


              <!-- DATOS -->

              <div class="file-information">

                <span class="file-label">
                  Archivo seleccionado
                </span>

                <strong>
                  {{ archivoSeleccionado.name }}
                </strong>

                <small>
                  {{
                    formatearTamano(
                      archivoSeleccionado.size
                    )
                  }}
                </small>

              </div>


              <!-- QUITAR -->

              <button
                type="button"
                class="remove-file"
                @click="quitarArchivo"
              >
                Quitar
              </button>

            </div>

          </div>

        </div>


        <!-- =================================================
             PRIORIDAD
        ================================================== -->

        <div class="priority-notice">

          <div class="notice-icon">
            i
          </div>


          <div>

            <strong>
              La prioridad será clasificada por UTIC
            </strong>

            <p>
              El Jefe de UTIC revisará la solicitud de soporte,
              clasificará su prioridad y posteriormente
              asignará al especialista responsable.
            </p>

          </div>

        </div>


        <!-- =================================================
             MENSAJE
        ================================================== -->

        <div
          v-if="mensaje"
          :class="[
            'message',
            esError
              ? 'message-error'
              : 'message-success'
          ]"
        >
          {{ mensaje }}
        </div>


        <!-- =================================================
             ACCIONES
        ================================================== -->

        <footer class="actions">

          <button
            type="button"
            class="cancel"
            :disabled="guardando"
            @click="
              router.push(
                '/usuario/dashboard'
              )
            "
          >
            Cancelar
          </button>


          <button
            type="button"
            class="secondary"
            :disabled="guardando"
            @click="limpiarFormulario"
          >
            Limpiar
          </button>


          <button
            type="button"
            class="primary"
            :disabled="guardando"
            @click="crearTicket"
          >

            {{
              guardando
                ? 'Enviando...'
                : 'Enviar solicitud'
            }}

          </button>

        </footer>

      </section>

    </main>

  </div>

</template>


<script setup>

import {
  onBeforeUnmount,
  onMounted,
  reactive,
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'

import SolicitanteMenu
  from '../components/SolicitanteMenu.vue'


/* =========================================================
   ROUTER
========================================================= */

const router =
  useRouter()


/* =========================================================
   CATÁLOGOS
========================================================= */

const areas =
  ref([])

const categorias =
  ref([])


/* =========================================================
   ESTADOS
========================================================= */

const mensaje =
  ref('')

const esError =
  ref(false)

const guardando =
  ref(false)


/* =========================================================
   ARCHIVO
========================================================= */

const archivoSeleccionado =
  ref(null)

const inputArchivo =
  ref(null)

const vistaPrevia =
  ref(null)


/* =========================================================
   FORMULARIO
========================================================= */

const form =
  reactive({

    titulo: '',

    descripcion: '',

    area: '',

    categoria: '',

    ubicacion: '',

    equipo_afectado: '',

    evidencia: '',
  })


/* =========================================================
   TOKEN
========================================================= */

const token = () =>
  localStorage.getItem(
    'sigta_token'
  )


/* =========================================================
   HEADERS PARA GET
========================================================= */

function headersAuth() {

  return {

    Authorization:
      `Token ${token()}`,

    Accept:
      'application/json',
  }
}


/* =========================================================
   INICIO
========================================================= */

onMounted(
  async () => {

    if (
      !token()
    ) {

      router.push(
        '/login'
      )

      return
    }


    await cargarCatalogos()
  }
)


/* =========================================================
   LIMPIAR URL DE PREVISUALIZACIÓN
========================================================= */

onBeforeUnmount(
  () => {

    liberarVistaPrevia()
  }
)


/* =========================================================
   CARGAR CATÁLOGOS
========================================================= */

async function cargarCatalogos() {

  try {

    const [
      areasRespuesta,
      categoriasRespuesta
    ] =
      await Promise.all([


        fetch(
          '/api/usuarios/areas/',
          {
            headers:
              headersAuth()
          }
        ),


        fetch(
          '/api/soporte/categorias/',
          {
            headers:
              headersAuth()
          }
        ),

      ])


    /* ===============================================
       SESIÓN EXPIRADA
    ================================================ */

    if (
      areasRespuesta.status === 401
      ||
      areasRespuesta.status === 403
      ||
      categoriasRespuesta.status === 401
      ||
      categoriasRespuesta.status === 403
    ) {

      cerrarSesion()

      return
    }


    /* ===============================================
       ERRORES
    ================================================ */

    if (
      !areasRespuesta.ok
    ) {

      throw new Error(
        'No fue posible cargar las áreas.'
      )
    }


    if (
      !categoriasRespuesta.ok
    ) {

      throw new Error(
        'No fue posible cargar las categorías.'
      )
    }


    /* ===============================================
       JSON
    ================================================ */

    const datosAreas =
      await areasRespuesta.json()


    const datosCategorias =
      await categoriasRespuesta.json()


    /* ===============================================
       CONVERTIR
    ================================================ */

    areas.value =
      convertirLista(
        datosAreas
      )


    categorias.value =
      convertirLista(
        datosCategorias
      )

    // La sección ya fue elegida en "Nueva solicitud". La
    // clasificación técnica corresponde a UTIC, no al usuario.
    form.area = areas.value.find(
      area => String(area.codigo || '').toUpperCase() === 'UTIC'
    )?.id || areas.value[0]?.id || ''

    form.categoria = categorias.value.find(
      categoria => String(categoria.codigo || '').toUpperCase() === 'OTRO'
    )?.id || categorias.value[0]?.id || ''


  } catch (error) {

    console.error(
      'Error cargando catálogos:',
      error
    )


    mostrarMensaje(
      error.message
      ||
      'No se pudieron cargar los datos.',
      true
    )
  }
}


/* =========================================================
   CONVERTIR LISTA
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
   SELECCIONAR ARCHIVO
========================================================= */

function seleccionarArchivo(
  evento
) {

  mensaje.value = ''

  esError.value = false


  const archivo =
    evento.target.files?.[0]


  if (
    !archivo
  ) {

    return
  }


  /* ===============================================
     TIPOS PERMITIDOS
  ================================================ */

  const tiposPermitidos = [

    'image/jpeg',

    'image/png',

    'application/pdf',
  ]


  if (
    !tiposPermitidos.includes(
      archivo.type
    )
  ) {

    mostrarMensaje(
      'Solo puede adjuntar archivos JPG, JPEG, PNG o PDF.',
      true
    )


    limpiarInputArchivo()

    return
  }


  /* ===============================================
     TAMAÑO MÁXIMO 5 MB
  ================================================ */

  const cincoMB =
    5 * 1024 * 1024


  if (
    archivo.size > cincoMB
  ) {

    mostrarMensaje(
      'El archivo no puede superar los 5 MB.',
      true
    )


    limpiarInputArchivo()

    return
  }


  /* ===============================================
     GUARDAR
  ================================================ */

  archivoSeleccionado.value =
    archivo


  /* ===============================================
     PREVISUALIZACIÓN SI ES IMAGEN
  ================================================ */

  liberarVistaPrevia()


  if (
    archivo.type.startsWith(
      'image/'
    )
  ) {

    vistaPrevia.value =
      URL.createObjectURL(
        archivo
      )
  }
}


/* =========================================================
   QUITAR ARCHIVO
========================================================= */

function quitarArchivo() {

  archivoSeleccionado.value =
    null


  liberarVistaPrevia()


  limpiarInputArchivo()
}


/* =========================================================
   LIMPIAR INPUT
========================================================= */

function limpiarInputArchivo() {

  if (
    inputArchivo.value
  ) {

    inputArchivo.value.value =
      ''
  }
}


/* =========================================================
   LIBERAR PREVIEW
========================================================= */

function liberarVistaPrevia() {

  if (
    vistaPrevia.value
  ) {

    URL.revokeObjectURL(
      vistaPrevia.value
    )


    vistaPrevia.value =
      null
  }
}


/* =========================================================
   FORMATEAR TAMAÑO
========================================================= */

function formatearTamano(
  bytes
) {

  if (
    !bytes
  ) {

    return '0 KB'
  }


  if (
    bytes < 1024
  ) {

    return `${bytes} bytes`
  }


  if (
    bytes < 1024 * 1024
  ) {

    return `${
      (
        bytes / 1024
      ).toFixed(1)
    } KB`
  }


  return `${
    (
      bytes
      /
      1024
      /
      1024
    ).toFixed(2)
  } MB`
}


/* =========================================================
   REGISTRAR SOLICITUD DE SOPORTE
========================================================= */

async function crearTicket() {

  mensaje.value = ''

  esError.value = false


  /* ===============================================
     VALIDACIÓN
  ================================================ */

  if (
    !form.titulo.trim()
    ||
    !form.descripcion.trim()
    ||
    !form.area
    ||
    !form.categoria
    ||
    !form.ubicacion.trim()
    ||
    !form.equipo_afectado.trim()
  ) {

    mostrarMensaje(
      'Complete todos los campos obligatorios.',
      true
    )

    return
  }


  guardando.value =
    true


  try {

    /* ===============================================
       FORMDATA

       IMPORTANTE:
       Ya NO usamos JSON.stringify porque
       ahora enviamos un archivo.
    ================================================ */

    const datosFormulario =
      new FormData()


    datosFormulario.append(
      'titulo',
      form.titulo.trim()
    )


    datosFormulario.append(
      'descripcion',
      form.descripcion.trim()
    )


    datosFormulario.append(
      'area',
      String(
        form.area
      )
    )


    datosFormulario.append(
      'categoria',
      String(
        form.categoria
      )
    )


    datosFormulario.append(
      'ubicacion',
      form.ubicacion.trim()
    )


    datosFormulario.append(
      'equipo_afectado',
      form.equipo_afectado.trim()
    )


    datosFormulario.append(
      'evidencia',
      form.evidencia.trim()
    )


    /* ===============================================
       ADJUNTO
    ================================================ */

    if (
      archivoSeleccionado.value
    ) {

      datosFormulario.append(
        'evidencia_archivo',
        archivoSeleccionado.value
      )
    }


    /* ===============================================
       PETICIÓN

       NO PONER CONTENT-TYPE.
       El navegador crea multipart/form-data
       automáticamente.
    ================================================ */

    const respuesta =
      await fetch(
        '/api/soporte/tickets/',
        {

          method:
            'POST',

          headers: {

            Authorization:
              `Token ${token()}`,

            Accept:
              'application/json',
          },


          body:
            datosFormulario,
        }
      )


    /* ===============================================
       RESPUESTA
    ================================================ */

    let datos = {}


    try {

      datos =
        await respuesta.json()

    } catch {

      datos = {}
    }


    /* ===============================================
       SESIÓN
    ================================================ */

    if (
      respuesta.status === 401
      ||
      respuesta.status === 403
    ) {

      cerrarSesion()

      return
    }


    /* ===============================================
       ERROR
    ================================================ */

    if (
      !respuesta.ok
    ) {

      console.error(
        'Error creando ticket:',
        datos
      )


      mostrarMensaje(
        obtenerError(
          datos
        ),
        true
      )


      return
    }


    /* ===============================================
       ÉXITO
    ================================================ */

    const codigo =
      datos.ticket?.codigo
      ||
      datos.codigo
      ||
      ''


    mostrarMensaje(

      codigo

        ? `Solicitud de soporte ${codigo} registrada correctamente.`

        : 'Solicitud de soporte registrada correctamente.',

      false
    )


    setTimeout(
      () => {

        router.push(
          '/usuario/mis-solicitudes'
        )

      },
      900
    )


  } catch (error) {

    console.error(
      'Error creando ticket:',
      error
    )


    mostrarMensaje(
      'No fue posible comunicarse con el servidor.',
      true
    )

  } finally {

    guardando.value =
      false
  }
}


/* =========================================================
   ERROR BACKEND
========================================================= */

function obtenerError(
  datos
) {

  if (
    datos.detalle
  ) {

    return datos.detalle
  }


  if (
    datos.detail
  ) {

    return datos.detail
  }


  const errores =
    Object.entries(
      datos
    )
      .map(
        ([campo, valor]) => {

          const texto =
            Array.isArray(valor)
              ? valor.join(', ')
              : String(valor)


          return (
            `${campo}: ${texto}`
          )
        }
      )
      .join(' | ')


  return (
    errores
    ||
    'Revise la información ingresada.'
  )
}


/* =========================================================
   MENSAJE
========================================================= */

function mostrarMensaje(
  texto,
  error = false
) {

  mensaje.value =
    texto


  esError.value =
    error
}


/* =========================================================
   LIMPIAR FORMULARIO
========================================================= */

function limpiarFormulario() {

  form.titulo = ''

  form.descripcion = ''

  form.ubicacion = ''

  form.equipo_afectado = ''

  form.evidencia = ''


  quitarArchivo()


  mensaje.value = ''

  esError.value = false
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

.layout {

  min-height: 100vh;

  display: flex;

  background: #eef3f8;

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}


.main {

  flex: 1;

  min-width: 0;

  padding:
    25px
    30px
    50px;

  overflow-x: hidden;
}


/* =========================================================
   HEADER
========================================================= */

.topbar {

  max-width: 1040px;

  margin:
    0
    auto
    18px;
}




.topbar h1 {

  margin: 0;

  color: #17344f;

  font-size: 31px;
}


.topbar p {

  margin:
    6px
    0
    0;

  color: #718294;

  font-size: 17px;
}


/* =========================================================
   TARJETA FORMULARIO
========================================================= */

.form-card {

  width: 100%;

  max-width: 1040px;

  margin: auto;

  overflow: hidden;

  border-top:
    4px solid #f2c400;

  border-radius: 10px;

  background: #ffffff;

  box-shadow:
    0
    4px
    18px
    rgba(0,0,0,.06);
}


.form-section {

  padding:
    22px
    26px;

  border-bottom:
    1px solid #e7ebef;
}


/* =========================================================
   TÍTULOS SECCIÓN
========================================================= */

.section-heading {

  display: flex;

  align-items: flex-start;

  gap: 10px;

  margin-bottom: 17px;
}


.number {

  width: 30px;

  height: 30px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #153f73;

  color: #ffffff;

  font-size: 15px;

  font-weight: 800;
}


.section-heading h2 {

  margin: 0;

  color: #253f57;

  font-size: 20px;
}


.section-heading p {

  margin:
    4px
    0
    0;

  color: #83919e;

  font-size: 15px;
}


/* =========================================================
   GRID
========================================================= */

.grid {

  display: grid;

  grid-template-columns:
    1fr
    1fr;

  gap: 15px;
}


/* =========================================================
   CAMPOS
========================================================= */

.field {

  min-width: 0;

  display: flex;

  flex-direction: column;

  gap: 6px;
}


.field.full {

  grid-column:
    1 / -1;
}


.field label {

  color: #344d63;

  font-size: 16px;

  font-weight: 700;
}


.field label span {

  color: #c13434;
}


.field label
.optional {

  margin-left: 4px;

  color: #8c99a5;

  font-size: 14px;

  font-weight: 400;
}


.field input,
.field select,
.field textarea {

  width: 100%;

  padding:
    14px
    15px;

  border:
    1px solid #ccd7e1;

  border-radius: 7px;

  background: #ffffff;

  color: #263d50;

  font-family: inherit;

  font-size: 17px;

  outline: none;
}


.field select {

  min-height: 41px;

  cursor: pointer;
}


.field textarea {

  min-height: 145px;

  resize: vertical;

  line-height: 1.5;
}


.field textarea.evidence-text {

  min-height: 80px;
}


.field input:focus,
.field select:focus,
.field textarea:focus {

  border-color: #175b96;

  box-shadow:
    0
    0
    0
    3px
    rgba(23,91,150,.09);
}


.field small {

  color: #8c99a5;

  font-size: 14px;
}


.counter {

  align-self: flex-end;
}


/* =========================================================
   UPLOAD
========================================================= */

.upload-container {

  margin-top: 14px;
}


.file-input {

  position: absolute;

  width: 1px;

  height: 1px;

  opacity: 0;

  pointer-events: none;
}


.upload-box {

  min-height: 145px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  gap: 6px;

  padding: 20px;

  border:
    2px dashed #c9d6e1;

  border-radius: 9px;

  background: #f8fafc;

  cursor: pointer;

  text-align: center;

  transition:
    border-color .2s,
    background .2s;
}


.upload-box:hover {

  border-color: #175b96;

  background: #f2f7fb;
}


.upload-icon {

  width: 38px;

  height: 38px;

  display: flex;

  align-items: center;

  justify-content: center;

  margin-bottom: 4px;

  border-radius: 50%;

  background: #e6eef6;

  color: #153f73;

  font-size: 25px;

  font-weight: 700;
}


.upload-box strong {

  color: #29475f;

  font-size: 17px;
}


.upload-box span {

  color: #728596;

  font-size: 15px;
}


.upload-box small {

  color: #9aa6af;

  font-size: 14px;
}


/* =========================================================
   ARCHIVO SELECCIONADO
========================================================= */

.selected-file-card {

  display: flex;

  align-items: center;

  gap: 13px;

  padding: 13px;

  border:
    1px solid #d5dfe7;

  border-radius: 9px;

  background: #f8fafc;
}


.preview-wrapper {

  width: 86px;

  height: 68px;

  flex-shrink: 0;

  overflow: hidden;

  border-radius: 7px;

  background: #e6edf3;
}


.preview-image {

  width: 100%;

  height: 100%;

  object-fit: cover;
}


.pdf-preview {

  width: 70px;

  height: 68px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 7px;

  background: #f8e9e9;
}


.pdf-icon {

  color: #a53636;

  font-size: 18px;

  font-weight: 900;
}


.file-information {

  flex: 1;

  min-width: 0;
}


.file-information
.file-label {

  display: block;

  margin-bottom: 3px;

  color: #81909d;

  font-size: 14px;
}


.file-information strong {

  display: block;

  overflow: hidden;

  color: #29475f;

  font-size: 16px;

  text-overflow: ellipsis;

  white-space: nowrap;
}


.file-information small {

  display: block;

  margin-top: 4px;

  color: #8b99a4;

  font-size: 14px;
}


.remove-file {

  flex-shrink: 0;

  padding:
    7px
    10px;

  border: none;

  border-radius: 6px;

  background: #fdecec;

  color: #a83232;

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;
}


/* =========================================================
   PRIORIDAD
========================================================= */

.priority-notice {

  margin:
    20px
    26px
    0;

  display: flex;

  gap: 10px;

  padding: 13px;

  border-left:
    4px solid #f2c400;

  border-radius: 7px;

  background: #f5f8fb;
}


.notice-icon {

  width: 25px;

  height: 25px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #153f73;

  color: white;

  font-size: 16px;

  font-weight: 700;
}


.priority-notice strong {

  color: #334e65;

  font-size: 16px;
}


.priority-notice p {

  margin:
    3px
    0
    0;

  color: #758796;

  font-size: 15px;

  line-height: 1.4;
}


/* =========================================================
   MENSAJES
========================================================= */

.message {

  margin:
    16px
    26px
    0;

  padding:
    11px
    13px;

  border-radius: 6px;

  font-size: 16px;
}


.message-error {

  background: #fdecec;

  color: #a83232;
}


.message-success {

  background: #e8f7ee;

  color: #267349;
}


/* =========================================================
   ACCIONES
========================================================= */

.actions {

  display: flex;

  justify-content: flex-end;

  gap: 9px;

  padding:
    19px
    26px;

  background: #fafbfc;
}


.actions button {

  min-height: 48px;

  padding:
    0
    22px;

  border-radius: 7px;

  font-size: 16px;

  font-weight: 700;

  cursor: pointer;
}


.actions button:disabled {

  opacity: .6;

  cursor: not-allowed;
}


.cancel {

  border:
    1px solid #ccd6df;

  background: white;

  color: #536777;
}


.secondary {

  border:
    1px solid #153f73;

  background: white;

  color: #153f73;
}


.primary {

  border: none;

  background: #153f73;

  color: white;
}


.primary:hover:not(:disabled) {

  background: #0e315b;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (
  max-width: 760px
) {

  .layout {

    display: block;
  }


  .main {

    padding: 17px;
  }


  .grid {

    grid-template-columns:
      1fr;
  }


  .field.full {

    grid-column: auto;
  }


  .actions {

    flex-direction:
      column-reverse;
  }


  .actions button {

    width: 100%;
  }


  .selected-file-card {

    align-items:
      flex-start;

    flex-wrap: wrap;
  }


  .file-information {

    min-width:
      calc(100% - 110px);
  }

}

</style>
