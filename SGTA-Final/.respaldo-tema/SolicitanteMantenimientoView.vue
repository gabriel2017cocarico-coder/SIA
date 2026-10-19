<template>

  <div class="layout">

    <SolicitanteMenu />

    <main class="main">

      <header class="topbar">

        <div>

          <h1>
            Registrar requerimiento de mantenimiento
          </h1>

          <p>
            Registre el requerimiento de mantenimiento
            preventivo o correctivo para su atención.
          </p>

        </div>

      </header>


      <section class="form-card">

        <!-- =================================================
             1. INFORMACIÓN
        ================================================== -->

        <div class="form-section">

          <div class="section-heading">

            <span class="number">
              1
            </span>

            <div>

              <h2>
                Información del requerimiento
              </h2>

              <p>
                Describa claramente el mantenimiento requerido.
              </p>

            </div>

          </div>


          <div class="grid">

            <div class="field full">

              <label>
                Título
                <span>*</span>
              </label>

              <input
                v-model="form.titulo"
                type="text"
                maxlength="200"
                placeholder="Ej.: Reparación de luminaria del aula"
                required
              />

            </div>


            <div class="field full">

              <label>
                Descripción
                <span>*</span>
              </label>

              <textarea
                v-model="form.descripcion"
                maxlength="1000"
                placeholder="Describa el mantenimiento que necesita..."
                required
              ></textarea>

              <small class="counter">
                {{ form.descripcion.length }} / 1000 caracteres
              </small>

            </div>

          </div>

        </div>


        <!-- =================================================
             2. UBICACIÓN
        ================================================== -->

        <div class="form-section">

          <div class="section-heading">

            <span class="number">
              2
            </span>

            <div>

              <h2>
                Ubicación
              </h2>

              <p>
                Indique dónde debe realizarse
                el mantenimiento.
              </p>

            </div>

          </div>


          <div class="field full">

            <label>
              Ubicación
              <span>*</span>
            </label>

            <input
              v-model="form.ubicacion"
              type="text"
              maxlength="200"
              placeholder="Ej.: Bloque B - Aula B-204"
              required
            />

          </div>

        </div>


        <!-- =================================================
             4. EVIDENCIA
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
                Cargue una fotografía o documento
                que ayude a identificar el requerimiento.
              </p>

            </div>

          </div>


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
              placeholder="Ej.: La luminaria dejó de funcionar..."
            ></textarea>

          </div>


          <div class="upload-container">

            <input
              id="mantenimiento-evidencia"
              ref="inputArchivo"
              class="file-input"
              type="file"
              accept=".jpg,.jpeg,.png,.pdf,image/jpeg,image/png,application/pdf"
              @change="seleccionarArchivo"
            />


            <label
              v-if="!archivoSeleccionado"
              for="mantenimiento-evidencia"
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


            <div
              v-else
              class="selected-file-card"
            >

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


              <div
                v-else
                class="pdf-preview"
              >
                PDF
              </div>


              <div class="file-information">

                <span>
                  Archivo cargado
                </span>

                <strong>
                  {{ archivoSeleccionado.name }}
                </strong>

                <small>
                  {{ formatearTamano(archivoSeleccionado.size) }}
                </small>

              </div>


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
             INFORMACIÓN DEL PROCESO
        ================================================== -->

        <div class="process-notice">

          <div class="notice-icon">
            i
          </div>

          <div>

            <strong>
              Servicios Generales atenderá el requerimiento
            </strong>

            <p>
              Una vez registrado, Servicios Generales podrá
              derivarlo a su auxiliar y continuar el proceso
              de mantenimiento establecido.
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
            @click="router.push('/usuario/dashboard')"
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
            @click="registrarRequerimiento"
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


const router =
  useRouter()


const areas =
  ref([])

const mensaje =
  ref('')

const esError =
  ref(false)

const guardando =
  ref(false)

const archivoSeleccionado =
  ref(null)

const inputArchivo =
  ref(null)

const vistaPrevia =
  ref(null)


const form =
  reactive({

    titulo: '',

    descripcion: '',

    tipo: 'CORRECTIVO',

    area: '',

    ubicacion: '',

    evidencia: '',
  })


const token = () =>
  localStorage.getItem(
    'sigta_token'
  )


function headersAuth() {

  return {

    Authorization:
      `Token ${token()}`,

    Accept:
      'application/json',
  }
}


onMounted(
  async () => {

    if (!token()) {

      router.push(
        '/login'
      )

      return
    }


    await cargarAreas()
  }
)


onBeforeUnmount(
  () => {

    liberarVistaPrevia()
  }
)


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


async function cargarAreas() {

  try {

    const respuesta =
      await fetch(
        '/api/usuarios/areas/',
        {
          headers:
            headersAuth()
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

      throw new Error(
        'No fue posible cargar las áreas.'
      )
    }


    areas.value =
      convertirLista(
        await respuesta.json()
      )

    // La ruta ya identifica esta solicitud como Mantenimiento.
    // La jefatura realizará después la clasificación técnica.
    form.area = areas.value.find(
      area => String(area.codigo || '').toUpperCase() === 'MANTENIMIENTO'
    )?.id || areas.value[0]?.id || ''


  } catch (error) {

    console.error(
      'Error cargando áreas:',
      error
    )


    mostrarMensaje(
      error.message
      ||
      'No fue posible cargar las áreas.',
      true
    )
  }
}


function seleccionarArchivo(
  evento
) {

  mensaje.value = ''

  esError.value = false


  const archivo =
    evento.target.files?.[0]


  if (!archivo) {

    return
  }


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
      'Solo puede cargar archivos JPG, JPEG, PNG o PDF.',
      true
    )


    limpiarInputArchivo()

    return
  }


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


  archivoSeleccionado.value =
    archivo


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


function quitarArchivo() {

  archivoSeleccionado.value =
    null


  liberarVistaPrevia()

  limpiarInputArchivo()
}


function limpiarInputArchivo() {

  if (
    inputArchivo.value
  ) {

    inputArchivo.value.value =
      ''
  }
}


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


function formatearTamano(
  bytes
) {

  if (!bytes) {

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

    return `${(bytes / 1024).toFixed(1)} KB`
  }


  return `${(
    bytes
    /
    1024
    /
    1024
  ).toFixed(2)} MB`
}


async function registrarRequerimiento() {

  mensaje.value = ''

  esError.value = false


  if (
    !form.titulo.trim()
    ||
    !form.descripcion.trim()
    ||
    !form.tipo
    ||
    !form.area
    ||
    !form.ubicacion.trim()
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
      'tipo',
      form.tipo
    )


    datosFormulario.append(
      'area',
      String(
        form.area
      )
    )


    datosFormulario.append(
      'ubicacion',
      form.ubicacion.trim()
    )


    datosFormulario.append(
      'evidencia',
      form.evidencia.trim()
    )


    if (
      archivoSeleccionado.value
    ) {

      datosFormulario.append(
        'evidencia_archivo',
        archivoSeleccionado.value
      )
    }


    const respuesta =
      await fetch(
        '/api/mantenimiento/requerimientos/',
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


    let datos = {}


    try {

      datos =
        await respuesta.json()

    } catch {

      datos = {}
    }


    if (
      respuesta.status === 401
      ||
      respuesta.status === 403
    ) {

      cerrarSesion()

      return
    }


    if (
      !respuesta.ok
    ) {

      console.error(
        'Error creando mantenimiento:',
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


    const codigo =
      datos.requerimiento?.codigo
      ||
      datos.codigo
      ||
      ''


    mostrarMensaje(

      codigo

        ? `Requerimiento ${codigo} registrado correctamente.`

        : 'Requerimiento de mantenimiento registrado correctamente.',

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
      'Error creando mantenimiento:',
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


function obtenerError(
  datos
) {

  if (
    datos?.detalle
  ) {

    return datos.detalle
  }


  if (
    datos?.detail
  ) {

    return datos.detail
  }


  const errores =
    Object.entries(
      datos
      ||
      {}
    )
      .map(
        ([campo, valor]) => {

          const texto =
            Array.isArray(valor)
              ? valor.join(', ')
              : String(valor)


          return `${campo}: ${texto}`
        }
      )
      .join(' | ')


  return (
    errores
    ||
    'Revise la información ingresada.'
  )
}


function mostrarMensaje(
  texto,
  error = false
) {

  mensaje.value =
    texto

  esError.value =
    error
}


function limpiarFormulario() {

  form.titulo = ''

  form.descripcion = ''

  form.tipo = 'CORRECTIVO'

  form.ubicacion = ''

  form.evidencia = ''


  quitarArchivo()


  mensaje.value = ''

  esError.value = false
}


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


.layout {
  min-height: 100vh;
  display: flex;
  background: #eef3f8;
  font-family: Arial, Helvetica, sans-serif;
}


.main {
  flex: 1;
  min-width: 0;
  padding: 25px 30px 50px;
  overflow-x: hidden;
}


.topbar {
  max-width: 1040px;
  margin: 0 auto 18px;
}




.topbar h1 {
  margin: 0;
  color: #17344f;
  font-size: 31px;
}


.topbar p {
  margin: 6px 0 0;
  color: #718294;
  font-size: 17px;
}


.form-card {
  width: 100%;
  max-width: 1040px;
  margin: auto;
  overflow: hidden;
  border-top: 4px solid #f2c400;
  border-radius: 10px;
  background: #ffffff;
  box-shadow: 0 4px 18px rgba(0,0,0,.06);
}


.form-section {
  padding: 22px 26px;
  border-bottom: 1px solid #e7ebef;
}


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
  margin: 4px 0 0;
  color: #83919e;
  font-size: 15px;
}


.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}


.field {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}


.field.full {
  grid-column: 1 / -1;
}


.field label {
  color: #344d63;
  font-size: 16px;
  font-weight: 700;
}


.field label span {
  color: #c13434;
}


.field label .optional {
  margin-left: 4px;
  color: #8c99a5;
  font-size: 14px;
  font-weight: 400;
}


.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 14px 15px;
  border: 1px solid #ccd7e1;
  border-radius: 7px;
  background: #ffffff;
  color: #263d50;
  font-family: inherit;
  font-size: 17px;
  outline: none;
}


.field select {
  min-height: 48px;
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
  box-shadow: 0 0 0 3px rgba(23,91,150,.09);
}


.field small {
  color: #8c99a5;
  font-size: 14px;
}


.counter {
  align-self: flex-end;
}


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
  border: 2px dashed #c9d6e1;
  border-radius: 9px;
  background: #f8fafc;
  cursor: pointer;
  text-align: center;
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


.selected-file-card {
  display: flex;
  align-items: center;
  gap: 13px;
  padding: 13px;
  border: 1px solid #d5dfe7;
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
  color: #a53636;
  font-size: 18px;
  font-weight: 900;
}


.file-information {
  flex: 1;
  min-width: 0;
}


.file-information span,
.file-information strong,
.file-information small {
  display: block;
}


.file-information span {
  margin-bottom: 3px;
  color: #81909d;
  font-size: 14px;
}


.file-information strong {
  overflow: hidden;
  color: #29475f;
  font-size: 16px;
  text-overflow: ellipsis;
  white-space: nowrap;
}


.file-information small {
  margin-top: 4px;
  color: #8b99a4;
  font-size: 14px;
}


.remove-file {
  flex-shrink: 0;
  padding: 7px 10px;
  border: none;
  border-radius: 6px;
  background: #fdecec;
  color: #a83232;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}


.process-notice {
  margin: 20px 26px 0;
  display: flex;
  gap: 10px;
  padding: 13px;
  border-left: 4px solid #f2c400;
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


.process-notice strong {
  color: #334e65;
  font-size: 16px;
}


.process-notice p {
  margin: 3px 0 0;
  color: #758796;
  font-size: 15px;
  line-height: 1.4;
}


.message {
  margin: 16px 26px 0;
  padding: 11px 13px;
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


.actions {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  padding: 19px 26px;
  background: #fafbfc;
}


.actions button {
  min-height: 48px;
  padding: 0 22px;
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
  border: 1px solid #ccd6df;
  background: white;
  color: #536777;
}


.secondary {
  border: 1px solid #153f73;
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


@media (max-width: 760px) {

  .layout {
    display: block;
  }


  .main {
    padding: 17px;
  }


  .grid {
    grid-template-columns: 1fr;
  }


  .field.full {
    grid-column: auto;
  }


  .actions {
    flex-direction: column-reverse;
  }


  .actions button {
    width: 100%;
  }


  .selected-file-card {
    align-items: flex-start;
    flex-wrap: wrap;
  }

}

</style>
