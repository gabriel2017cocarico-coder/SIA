<template>
  <div class="layout">

    <SolicitanteMenu />


    <main class="content">

      <header>

        <div>
          <h1>
            Compras
          </h1>

          <p>
            Registre y consulte sus solicitudes de compra.
          </p>
        </div>

        <button
          class="new"
          @click="abrirFormulario"
        >
          + Registrar solicitud de compra
        </button>

      </header>


      <section class="stats">

        <article>
          <span>Solicitudes de compra</span>
          <strong>
            {{ solicitudes.length }}
          </strong>
        </article>

        <article>
          <span>Registradas</span>
          <strong>
            {{ nuevas }}
          </strong>
        </article>

        <article>
          <span>En trámite</span>
          <strong>
            {{ enProceso }}
          </strong>
        </article>

        <article>
          <span>Finalizadas</span>
          <strong>
            {{ cerradas }}
          </strong>
        </article>

      </section>


      <section class="filters">

        <input
          v-model="busqueda"
          placeholder="Buscar código o título..."
        />

        <select v-model="filtroEstado">

          <option value="">
            Todos los estados
          </option>

          <option value="NUEVO">
            Nuevo
          </option>

          <option value="EN_COTIZACION">
            En cotización
          </option>

          <option value="EN_APROBACION">
            En aprobación
          </option>

          <option value="APROBADO">
            Aprobado
          </option>

          <option value="CERRADO">
            Cerrado
          </option>

          <option value="ANULADO">
            Anulado
          </option>

        </select>

      </section>


      <section class="list">

        <div
          v-if="cargando"
          class="empty"
        >
          Cargando solicitudes...
        </div>

        <div
          v-else-if="
            solicitudesFiltradas.length === 0
          "
          class="empty"
        >
          No tiene solicitudes de compra registradas.
        </div>


        <article
          v-for="solicitud in solicitudesFiltradas"
          :key="solicitud.id"
          class="purchase"
        >

          <div>

            <strong class="code">
              {{ solicitud.codigo }}
            </strong>

            <h3>
              {{ solicitud.titulo }}
            </h3>

            <p>
              {{ solicitud.descripcion }}
            </p>

            <div class="meta">

              <span>
                {{ solicitud.tipo_nombre }}
              </span>

              <span>
                Cantidad:
                {{ solicitud.cantidad }}
              </span>

              <span v-if="solicitud.monto_estimado">
                Bs
                {{ solicitud.monto_estimado }}
              </span>

              <span>
                {{ solicitud.via_nombre }}
              </span>

            </div>

          </div>


          <div class="side">

            <span class="status">
              {{ solicitud.estado_nombre }}
            </span>

            <div class="actions">

              <button
                @click="
                  verSolicitud(solicitud)
                "
              >
                Ver
              </button>

              <button
                v-if="
                  ['NUEVO', 'CREADO_PENDIENTE_DAF']
                    .includes(solicitud.estado)
                "
                class="edit"
                @click="
                  editarSolicitud(solicitud)
                "
              >
                Editar
              </button>

              <button
                v-if="
                  ['NUEVO', 'CREADO_PENDIENTE_DAF']
                    .includes(solicitud.estado)
                "
                class="cancel"
                @click="
                  anularSolicitud(solicitud)
                "
              >
                Anular
              </button>

              <button
                v-if="solicitud.estado === 'COMPRADO_Y_ENTREGADO'"
                class="edit"
                @click="presentarDescargo(solicitud)"
              >
                Presentar descargo
              </button>

            </div>

          </div>

        </article>

      </section>

    </main>


    <!-- FORMULARIO -->
    <div
      v-if="mostrarFormulario"
      class="overlay"
    >

      <div class="purchase-page">
        <div class="purchase-page-header">
          <h1>Registrar solicitud de compra</h1>
          <p>Envíe el expediente de adquisición con toda la documentación requerida.</p>
        </div>

      <section class="modal">

        <div class="modal-header">

          <div>
            <h2>Información de la solicitud</h2>

            <p>
              Complete la información de la solicitud de compra.
            </p>
          </div>

          <button
            class="close"
            @click="cerrarFormulario"
          >
            ×
          </button>

        </div>


        <form
          @submit.prevent="guardar"
        >

          <div class="grid">

            <div class="field full">

              <label>
                Título
              </label>

              <input
                v-model="form.titulo"
                required
                placeholder="Ej.: Compra de monitor"
              />

            </div>


            <div class="field full">

              <label>
                Descripción
              </label>

              <textarea
                v-model="form.descripcion"
                required
              ></textarea>

            </div>

            <div class="form-section-title full">
              <span>2</span>
              <div>
                <h3>Clasificación y presupuesto</h3>
                <p>Seleccione el área, el tipo de adquisición, la cantidad y el monto estimado.</p>
              </div>
            </div>


            <div class="field">

              <label>
                Área solicitante
              </label>

              <select
                v-model="form.area"
                required
              >

                <option
                  value=""
                  disabled
                >
                  Seleccione área
                </option>

                <option
                  v-for="area in areas"
                  :key="area.id"
                  :value="area.id"
                >
                  {{ area.nombre }}
                </option>

              </select>

            </div>


            <div class="field">

              <label>
                Tipo
              </label>

              <select
                v-model="form.tipo"
                required
              >

                <option value="BIEN">
                  Bien
                </option>

                <option value="SERVICIO">
                  Servicio
                </option>

                <option value="ACTIVO_FIJO">
                  Activo fijo
                </option>

                <option value="COMPONENTE">
                  Componente
                </option>

              </select>

            </div>


            <div class="field">

              <label>
                Cantidad
              </label>

              <input
                v-model.number="form.cantidad"
                type="number"
                min="1"
                required
              />

            </div>


            <div class="field">

              <label>
                Monto estimado (Bs)
              </label>

              <input
                v-model="form.monto_estimado"
                type="number"
                min="0"
                step="0.01"
                placeholder="Opcional"
              />

            </div>

            <div class="form-section-title full">
              <span>3</span>
              <div>
                <h3>Detalle técnico y justificación</h3>
                <p>Describa las características requeridas y el motivo institucional de la compra.</p>
              </div>
            </div>


            <div class="field full">

              <label>
                Especificaciones
              </label>

              <textarea
                v-model="form.especificaciones"
                required
                placeholder="Características técnicas necesarias..."
              ></textarea>

            </div>


            <div class="field full">

              <label>
                Justificación
              </label>

              <textarea
                v-model="form.justificacion"
                required
                placeholder="Explique por qué se necesita la compra..."
              ></textarea>

            </div>


            <div class="field">

              <label>
                Centro de costo
              </label>

              <input
                v-model="form.centro_costo"
                placeholder="Opcional"
              />

            </div>


            <div class="field">

              <label>
                Solicitud de soporte vinculada
              </label>

              <input
                v-model="
                  form.ticket_soporte_vinculado
                "
                placeholder="Ej.: SOP-2026-0002"
              />

            </div>

            <div v-if="!editando" class="form-section-title full">
              <span>4</span>
              <div>
                <h3>Expediente documental</h3>
                <p>Adjunte los documentos obligatorios para remitir la solicitud a la DAF.</p>
              </div>
            </div>

            <div v-if="!editando" class="field full documents-field">
              <label>Expediente inicial obligatorio</label>
              <p class="file-help">
                Adjunte Informe, POA, Pedido y Proforma en PDF para enviar la solicitud a la DAF.
              </p>
              <div class="document-grid">
                <label class="document-input"><span>Informe</span><input type="file" accept="application/pdf" required @change="seleccionarArchivo('informe', $event)" /></label>
                <label class="document-input"><span>POA</span><input type="file" accept="application/pdf" required @change="seleccionarArchivo('poa', $event)" /></label>
                <label class="document-input"><span>Pedido</span><input type="file" accept="application/pdf" required @change="seleccionarArchivo('pedido', $event)" /></label>
                <label class="document-input"><span>Proforma</span><input type="file" accept="application/pdf" required @change="seleccionarArchivo('proforma', $event)" /></label>
              </div>
            </div>

          </div>


          <div
            v-if="mensajeModal"
            class="error"
          >
            {{ mensajeModal }}
          </div>


          <div class="modal-actions">

            <button
              type="button"
              class="secondary"
              @click="cerrarFormulario"
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
                  : 'Registrar solicitud de compra'
              }}
            </button>

          </div>

        </form>

      </section>

      </div>

    </div>

  </div>
</template>


<script setup>
import {
  computed,
  onMounted,
  reactive,
  ref,
} from 'vue'

import {
  useRouter
} from 'vue-router'

import SolicitanteMenu
  from '../components/SolicitanteMenu.vue'


const router = useRouter()

const solicitudes = ref([])
const areas = ref([])

const busqueda = ref('')
const filtroEstado = ref('')

const cargando = ref(true)
const guardando = ref(false)

const mostrarFormulario = ref(true)
const editando = ref(false)

const solicitudId = ref(null)

const mensajeModal = ref('')


const form = reactive({
  titulo: '',
  descripcion: '',
  area: '',
  tipo: 'BIEN',
  cantidad: 1,
  especificaciones: '',
  justificacion: '',
  centro_costo: '',
  monto_estimado: '',
  ticket_soporte_vinculado: '',
})

const archivos = reactive({
  informe: null,
  poa: null,
  pedido: null,
  proforma: null,
})

function seleccionarArchivo(campo, evento) {
  archivos[campo] = evento.target.files?.[0] || null
}


const token = () =>
  localStorage.getItem(
    'sigta_token'
  )


const authHeaders = () => ({
  'Content-Type':
    'application/json',

  Authorization:
    `Token ${token()}`,
})


const solicitudesFiltradas =
  computed(() => {

    const texto =
      busqueda.value
        .toLowerCase()
        .trim()

    return solicitudes.value.filter(
      (solicitud) => {

        const textoOk =
          !texto
          ||
          String(
            solicitud.codigo
            || ''
          )
            .toLowerCase()
            .includes(texto)
          ||
          String(
            solicitud.titulo
            || ''
          )
            .toLowerCase()
            .includes(texto)

        const estadoOk =
          !filtroEstado.value
          ||
          solicitud.estado
          === filtroEstado.value

        return textoOk && estadoOk
      }
    )
  })


const nuevas = computed(() =>
  solicitudes.value.filter(
    s => s.estado === 'NUEVO'
  ).length
)


const cerradas = computed(() =>
  solicitudes.value.filter(
    s => s.estado === 'CERRADO'
  ).length
)


const enProceso = computed(() =>
  solicitudes.value.filter(
    s =>
      ![
        'NUEVO',
        'CERRADO',
        'ANULADO',
        'RECHAZADO',
      ].includes(s.estado)
  ).length
)


onMounted(async () => {

  if (!token()) {

    router.push(
      '/login'
    )

    return
  }


  await Promise.all([
    cargarSolicitudes(),
    cargarAreas(),
  ])
})


async function cargarSolicitudes() {

  cargando.value = true

  try {

    const respuesta =
      await fetch(
        '/api/compras/solicitudes/',
        {
          headers: {
            Authorization:
              `Token ${token()}`
          }
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

      const detalle =
        await respuesta.text()

      console.error(
        'Error API Compras:',
        respuesta.status,
        detalle
      )

      solicitudes.value = []

      return
    }


    const datos =
      await respuesta.json()


    solicitudes.value =
      Array.isArray(datos)
        ? datos
        : (
            datos.results
            || []
          )

  } catch (e) {

    console.error(e)

  } finally {

    cargando.value = false
  }
}


async function cargarAreas() {

  try {

    const respuesta =
      await fetch(
        '/api/usuarios/areas/',
        {
          headers: {
            Authorization:
              `Token ${token()}`,

            Accept:
              'application/json',
          }
        }
      )


    if (!respuesta.ok) {

      const detalle =
        await respuesta.text()

      console.error(
        'Error API Áreas:',
        respuesta.status,
        detalle
      )

      areas.value = []

      return
    }


    const datos =
      await respuesta.json()


    areas.value =
      Array.isArray(datos)
        ? datos
        : (
            datos.results
            || []
          )


    console.log(
      'Áreas cargadas en Compras:',
      areas.value
    )

  } catch (e) {

    console.error(
      'Error cargando áreas:',
      e
    )

    areas.value = []
  }
}


function abrirFormulario() {

  editando.value = false

  solicitudId.value = null

  limpiar()

  mostrarFormulario.value = true
}


function editarSolicitud(solicitud) {

  editando.value = true

  solicitudId.value =
    solicitud.id

  form.titulo =
    solicitud.titulo

  form.descripcion =
    solicitud.descripcion

  form.area =
    solicitud.area
    ? Number(
        typeof solicitud.area === 'object'
          ? solicitud.area.id
          : solicitud.area
      )
    : ''

  form.tipo =
    solicitud.tipo

  form.cantidad =
    solicitud.cantidad

  form.especificaciones =
    solicitud.especificaciones

  form.justificacion =
    solicitud.justificacion

  form.centro_costo =
    solicitud.centro_costo

  form.monto_estimado =
    solicitud.monto_estimado || ''

  form.ticket_soporte_vinculado =
    solicitud.ticket_soporte_vinculado || ''

  mostrarFormulario.value = true
}


async function guardar() {

  mensajeModal.value = ''

  if (!editando.value) {
    for (const campo of ['informe', 'poa', 'pedido', 'proforma']) {
      const archivo = archivos[campo]
      if (archivo && !archivo.name.toLowerCase().endsWith('.pdf')) {
        mensajeModal.value = 'Informe, POA, Pedido y Proforma deben ser archivos PDF.'
        return
      }
    }
  }

  guardando.value = true

  try {

    const payload = new FormData()

    payload.append('titulo', form.titulo)
    payload.append('descripcion', form.descripcion)
    payload.append('area', String(Number(form.area)))
    payload.append('tipo', form.tipo)
    payload.append('cantidad', String(Number(form.cantidad)))
    payload.append('especificaciones', form.especificaciones)
    payload.append('justificacion', form.justificacion)
    payload.append('centro_costo', form.centro_costo || '')
    if (form.monto_estimado) {
      payload.append('monto_estimado', String(Number(form.monto_estimado)))
    }
    payload.append('ticket_soporte_vinculado', form.ticket_soporte_vinculado || '')

    if (!editando.value) {
      for (const campo of ['informe', 'poa', 'pedido', 'proforma']) {
        if (archivos[campo]) payload.append(campo, archivos[campo])
      }
    }


    let url =
      '/api/compras/solicitudes/'

    let method = 'POST'


    if (editando.value) {

      url =
        `/api/compras/solicitudes/${solicitudId.value}/`

      method = 'PATCH'
    }


    const respuesta =
      await fetch(
        url,
        {
          method,

          headers: {
            Authorization: `Token ${token()}`,
          },

          body: payload,
        }
      )


    const datos =
      await respuesta.json()


    if (!respuesta.ok) {

      console.error(datos)

      mensajeModal.value =
        datos.detalle
        || 'Revise la información ingresada.'

      return
    }


    if (editando.value) {
      cerrarFormulario()
      await cargarSolicitudes()
    } else {
      limpiar()
      router.push('/usuario/mis-solicitudes')
    }

  } catch (e) {

    console.error(e)

    mensajeModal.value =
      'No fue posible guardar la solicitud.'

  } finally {

    guardando.value = false
  }
}


async function anularSolicitud(
  solicitud
) {

  const confirmar =
    window.confirm(
      `¿Desea anular ${solicitud.codigo}?`
    )

  if (!confirmar) {
    return
  }


  const respuesta =
    await fetch(
      `/api/compras/solicitudes/${solicitud.id}/`,
      {
        method: 'DELETE',

        headers:
          authHeaders(),
      }
    )


  if (!respuesta.ok) {

    const datos =
      await respuesta.json()

    alert(
      datos.detalle
      || 'No se pudo anular.'
    )

    return
  }


  await cargarSolicitudes()
}


function verSolicitud(solicitud) {

  alert(
    `${solicitud.codigo}\n\n`
    + `${solicitud.titulo}\n\n`
    + `${solicitud.descripcion}\n\n`
    + `Estado: ${solicitud.estado_nombre}`
  )
}


function cerrarFormulario() {

  mostrarFormulario.value = false

  mensajeModal.value = ''
}


function limpiar() {

  form.titulo = ''
  form.descripcion = ''
  form.area = ''
  form.tipo = 'BIEN'
  form.cantidad = 1
  form.especificaciones = ''
  form.justificacion = ''
  form.centro_costo = ''
  form.monto_estimado = ''
  form.ticket_soporte_vinculado = ''

  archivos.informe = null
  archivos.poa = null
  archivos.pedido = null
  archivos.proforma = null
}

function seleccionarDocumento(accept = '*/*') {
  return new Promise((resolve) => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = accept
    input.onchange = () => resolve(input.files?.[0] || null)
    input.click()
  })
}

async function presentarDescargo(solicitud) {
  try {
    alert('Seleccione la Factura, luego el Acta de Conformidad y finalmente el Fotograma.')
    const factura = await seleccionarDocumento('.pdf,.jpg,.jpeg,.png')
    if (!factura) return
    const acta = await seleccionarDocumento('.pdf,.jpg,.jpeg,.png')
    if (!acta) return
    const fotograma = await seleccionarDocumento('image/*,.pdf')
    if (!fotograma) return
    const datos = new FormData()
    datos.append('factura', factura)
    datos.append('acta_conformidad', acta)
    datos.append('fotograma', fotograma)
    const respuesta = await fetch(`/api/compras/solicitudes/${solicitud.id}/presentar-descargo/`, {
      method: 'POST', headers: { Authorization: `Token ${token()}` }, body: datos,
    })
    const resultado = await respuesta.json()
    if (!respuesta.ok) throw new Error(resultado.detalle || 'No fue posible presentar el descargo.')
    await cargarSolicitudes()
    alert('Descargo enviado correctamente a Tesorería.')
  } catch (error) { alert(error.message) }
}


function cerrarSesion() {

  localStorage.removeItem(
    'sigta_token'
  )

  localStorage.removeItem(
    'sigta_usuario'
  )

  router.push('/login')
}
</script>


<style scoped>
* {
  box-sizing: border-box;
}

.layout {
  min-height: 100vh;
  display: flex;
  background: #f4f6f8;
  font-family: Arial, Helvetica, sans-serif;
}

.content {
  flex: 1;
  min-width: 0;
  padding: 28px;
}

header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

header h1 {
  margin: 0;
  color: #17324a;
}

header p {
  color: #71818f;
  font-size: 19px;
}

.new {
  height: 43px;
  padding: 0 18px;
  border: none;
  border-radius: 8px;
  background: #f2c400;
  color: #17324a;
  font-weight: 800;
  cursor: pointer;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
  margin-bottom: 17px;
}

.stats article {
  padding: 17px;
  background: white;
  border-top: 3px solid #f2c400;
  border-radius: 9px;
}

.stats span {
  color: #71818f;
  font-size: 16px;
  font-weight: 700;
}

.stats strong {
  display: block;
  margin-top: 5px;
  color: #073b6f;
  font-size: 31px;
}

.filters {
  display: grid;
  grid-template-columns: 1fr 230px;
  gap: 12px;
  margin-bottom: 16px;
}

.filters input,
.filters select {
  height: 42px;
  padding: 0 12px;
  border: 1px solid #d0dae2;
  border-radius: 7px;
}

.list {
  background: white;
  border-radius: 10px;
  overflow: hidden;
}

.purchase {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 18px 20px;
  border-bottom: 1px solid #edf0f2;
}

.code {
  color: #07518d;
  font-size: 17px;
}

.purchase h3 {
  margin: 6px 0;
  color: #29475e;
}

.purchase p {
  color: #73818c;
  font-size: 17px;
}

.meta {
  display: flex;
  gap: 7px;
  flex-wrap: wrap;
}

.meta span {
  padding: 4px 7px;
  background: #f3f6f8;
  border-radius: 4px;
  font-size: 15px;
}

.side {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.status {
  padding: 5px 9px;
  border-radius: 20px;
  background: #eaf3fb;
  color: #07518d;
  font-size: 15px;
  font-weight: 800;
}

.actions {
  display: flex;
  gap: 6px;
}

.actions button {
  padding: 6px 9px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.actions .edit {
  background: #eaf3fb;
  color: #07518d;
}

.actions .cancel {
  background: #fdecec;
  color: #a53232;
}

.empty {
  padding: 40px;
  text-align: center;
  color: #71818f;
}

.overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(7,35,60,.6);
}

.modal {
  width: 100%;
  max-width: 650px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
  background: white;
  border-radius: 12px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
}

.modal-header h2 {
  margin: 0;
  color: #17324a;
}

.modal-header p {
  color: #71818f;
  font-size: 17px;
}

.close {
  border: none;
  background: transparent;
  font-size: 33px;
  cursor: pointer;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
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
  font-size: 17px;
  font-weight: 700;
}

.field input,
.field select,
.field textarea {
  padding: 14px 15px;
  border: 1px solid #ccd6de;
  border-radius: 7px;
}

.field textarea {
  min-height: 110px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
  margin-top: 20px;
}

.modal-actions button {
  height: 40px;
  padding: 0 16px;
  border-radius: 7px;
}

.secondary {
  border: 1px solid #ccd6de;
  background: white;
}

.primary {
  border: none;
  background: #073b6f;
  color: white;
}

.error {
  margin-top: 12px;
  padding: 9px;
  border-radius: 6px;
  background: #fdecec;
  color: #a53232;
}

@media (max-width: 760px) {

  .layout {
    display: block;
  }

  .content {
    padding: 16px;
  }

  .stats {
    grid-template-columns: 1fr 1fr;
  }

  .filters,
  .grid {
    grid-template-columns: 1fr;
  }

  .field.full {
    grid-column: auto;
  }

  .purchase {
    flex-direction: column;
  }

  .side {
    align-items: flex-start;
  }
}

.file-help {
  margin: 0 0 10px;
  color: #728393;
  font-size: 16px;
}

.document-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.document-input {
  padding: 11px;
  border: 1px dashed #aebfcd;
  border-radius: 8px;
  background: #f8fafc;
}

.document-input span {
  display: block;
  margin-bottom: 7px;
  color: #174a7d;
  font-size: 16px;
  font-weight: 800;
}

.document-input input {
  width: 100%;
  font-size: 15px;
}

@media (max-width: 560px) {
  .document-grid { grid-template-columns: 1fr; }
}

/* Compras se presenta como formulario directo, igual que Soporte y Mantenimiento. */
.layout > .content {
  display: none;
}

.overlay {
  position: static;
  inset: auto;
  z-index: auto;
  flex: 1;
  min-width: 0;
  display: block;
  padding: 28px;
  background: #f2f5f9;
}

.purchase-page {
  width: 100%;
  max-width: 1040px;
  margin: 0 auto;
}

.purchase-page-header {
  margin-bottom: 20px;
}


.purchase-page-header h1 {
  margin: 0;
  color: #17324a;
  font-size: 34px;
}

.purchase-page-header p {
  margin: 6px 0 0;
  color: #758391;
  font-size: 18px;
}

.modal {
  width: 100%;
  max-width: none;
  max-height: none;
  overflow: visible;
  padding: 0;
  border-top: 4px solid #f2c400;
  border-radius: 10px;
  box-shadow: 0 4px 14px rgba(0,0,0,.05);
}

.modal-header {
  padding: 22px 28px 17px;
  border-bottom: 1px solid #e5ebf0;
}

.modal-header h2 {
  font-size: 24px;
}

.modal-header h2::before {
  content: "1";
  display: inline-grid;
  place-items: center;
  width: 31px;
  height: 31px;
  margin-right: 12px;
  border-radius: 50%;
  background: #174a7d;
  color: #fff;
  font-size: 18px;
}

.modal .close,
.modal-actions .secondary {
  display: none;
}

.modal form {
  padding: 24px 28px 28px;
}

.grid {
  gap: 18px;
}

.form-section-title {
  grid-column: 1 / -1;
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 8px -28px 0;
  padding: 22px 28px 2px;
  border-top: 1px solid #e2e8ed;
}

.form-section-title > span {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #174a7d;
  color: #fff;
  font-size: 15px;
  font-weight: 800;
}

.form-section-title h3 {
  margin: 0;
  color: #17324a;
  font-size: 20px;
}

.form-section-title p {
  margin: 4px 0 0;
  color: #758391;
  font-size: 15px;
}

.documents-field > label,
.documents-field > .file-help {
  display: none;
}

.field label {
  color: #17324a;
  font-size: 17px;
}

.field input,
.field select,
.field textarea {
  padding: 14px 15px;
  background: #fff;
  border: 1px solid #cbd7e1;
  border-radius: 7px;
  font-family: inherit;
}

.field select {
  min-height: 41px;
  cursor: pointer;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: #0a5794;
  box-shadow: 0 0 0 3px rgba(10,87,148,.08);
}

.modal-actions {
  padding-top: 20px;
  border-top: 1px solid #e5ebf0;
}

.modal-actions .primary {
  min-width: 210px;
  min-height: 42px;
  background: #075b9b;
  color: #fff;
}

@media (max-width: 760px) {
  .overlay { padding: 18px; }
  .modal-header, .modal form { padding-inline: 18px; }
  .form-section-title { margin-inline: -18px; padding-inline: 18px; }
}
</style>
