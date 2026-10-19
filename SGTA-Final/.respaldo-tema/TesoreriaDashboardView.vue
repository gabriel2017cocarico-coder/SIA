<template>
  <div class="layout">

    <TesoreriaMenu />

    <main class="main">

      <!-- =================================================
           ENCABEZADO
      ================================================== -->
      <header class="page-header">

        <div>
          <h1>
            Desembolso de Caja Chica
          </h1>

          <p>
            Expedientes autorizados por el Director que esperan
            la entrega del efectivo.
          </p>
        </div>

        <div class="header-actions">

          <select
            v-model="filtroEstado"
            class="filtro-estado"
          >
            <option value="">Todas las solicitudes</option>
            <option value="APROBADA">Solicitudes aprobadas</option>
            <option value="RECHAZADA">Solicitudes rechazadas</option>
          </select>

          <button
            class="refresh-button"
            type="button"
            :disabled="cargando"
            @click="cargarCompras"
          >
            {{
              cargando
                ? 'Actualizando...'
                : 'Actualizar'
            }}
          </button>

        </div>

      </header>


      <!-- =================================================
           CARGANDO
      ================================================== -->
      <div
        v-if="cargando"
        class="loading"
      >
        Cargando solicitudes de compra...
      </div>


      <!-- =================================================
           SIN REGISTROS
      ================================================== -->
      <div
        v-else-if="compras.length === 0"
        class="empty"
      >
        No existen solicitudes de compra registradas.
      </div>


      <div
        v-else-if="comprasFiltradas.length === 0"
        class="empty"
      >
        No hay {{ etiquetaFiltroVacio(filtroEstado) }}.
      </div>


      <!-- =================================================
           LISTADO
      ================================================== -->
      <section
        v-else
        class="requests-card"
      >

        <div class="request-list">

          <article
            v-for="compra in comprasFiltradas"
            :key="compra.id"
            class="request"
          >

            <div class="request-main">

              <div class="request-code">
                <strong>
                  {{ compra.codigo }}
                </strong>

                <small>
                  {{ compra.area_nombre || 'Área no indicada' }}
                </small>
              </div>


              <div class="request-info">

                <h3>
                  {{
                    compra.titulo
                    || compra.descripcion
                    || 'Solicitud de compra'
                  }}
                </h3>

                <div class="meta">

                  <span>
                    {{
                      compra.solicitante_nombre
                      || compra.solicitante_email
                      || 'Sin información'
                    }}
                  </span>

                  <span>
                    {{
                      compra.via_nombre
                      || 'Vía no indicada'
                    }}
                  </span>

                  <span v-if="compra.creado_en">
                    {{ formatearFecha(compra.creado_en) }}
                  </span>

                </div>

              </div>

            </div>


            <div class="request-side">

              <span
                :class="['status', claseBucket(bucketEstado(compra.estado))]"
              >
                {{ etiquetaBucket(bucketEstado(compra.estado)) }}
              </span>

              <div class="row-actions">

                <button
                  class="view"
                  @click="verDetalle(compra)"
                >
                  Ver detalle
                </button>

                <button
                  v-if="etapaAccion(compra) === 'desembolso'"
                  class="row-aprobar"
                  @click="verDetalle(compra)"
                >
                  Desembolsar
                </button>

              </div>

            </div>

          </article>

        </div>

      </section>

    </main>


    <!-- =================================================
         DOCUMENTO DE DETALLE
    ================================================== -->

    <div
      v-if="mostrarDetalle"
      class="detalle-modal-backdrop"
      @click.self="cerrarDetalle"
    >
      <div class="detalle-modal documento-modal">

        <div class="detalle-modal-header">
          <div class="documento-header-titulo">

            <span class="documento-header-icono">📄</span>

            <div>
              <h3>{{ compraSeleccionada?.codigo }}</h3>
              <small>{{ compraSeleccionada?.titulo }}</small>
            </div>

          </div>

          <button
            class="detalle-modal-close"
            @click="cerrarDetalle"
          >✕</button>
        </div>

        <div class="documento-body">

          <div
            :class="['estado-banner', claseBucket(bucketEstado(compraSeleccionada?.estado))]"
          >
            <span class="estado-banner-icono">
              {{ iconoBucket(bucketEstado(compraSeleccionada?.estado)) }}
            </span>

            <div>
              <strong>{{ etiquetaBucket(bucketEstado(compraSeleccionada?.estado)) }}</strong>
              <span class="estado-banner-descripcion">
                {{ descripcionBucket(bucketEstado(compraSeleccionada?.estado)) }}
              </span>
            </div>
          </div>


          <div class="documento-seccion">

            <div class="documento-titulo-fila">
              <span class="documento-icono">📦</span>
              <span class="documento-titulo">
                Producto o servicio a comprar
              </span>
            </div>

            <h4>{{ compraSeleccionada?.titulo || 'Sin título' }}</h4>

            <p>{{ compraSeleccionada?.descripcion || 'Sin descripción registrada.' }}</p>


            <div class="documento-fila documento-fila-5">

              <div>
                <b>Tipo</b>
                <span>{{ compraSeleccionada?.tipo_nombre || compraSeleccionada?.tipo || 'No indicado' }}</span>
              </div>

              <div>
                <b>Cantidad</b>
                <span>{{ compraSeleccionada?.cantidad || 1 }}</span>
              </div>

              <div>
                <b>Monto estimado</b>
                <span>
                  {{
                    compraSeleccionada?.monto_estimado
                      ? `Bs ${Number(compraSeleccionada.monto_estimado).toFixed(2)}`
                      : 'No indicado'
                  }}
                </span>
              </div>

              <div>
                <b>Especificaciones</b>
                <span>{{ compraSeleccionada?.especificaciones || 'No registradas.' }}</span>
              </div>

              <div>
                <b>Justificación</b>
                <span>{{ compraSeleccionada?.justificacion || 'No registrada.' }}</span>
              </div>

            </div>

          </div>


          <div class="documento-seccion">

            <div class="documento-titulo-fila">
              <span class="documento-icono">📁</span>
              <span class="documento-titulo">
                Datos del expediente
              </span>
            </div>

            <div class="documento-fila">

              <div>
                <b>Solicitante</b>
                <button
                  v-if="compraSeleccionada?.solicitante"
                  type="button"
                  class="solicitante-link"
                  @click="abrirSolicitante(compraSeleccionada.solicitante)"
                >
                  <span>
                    {{
                      compraSeleccionada?.solicitante_nombre
                      || 'Sin información'
                    }}
                  </span>
                  <small v-if="compraSeleccionada?.solicitante_email">
                    {{ compraSeleccionada.solicitante_email }}
                  </small>
                </button>
                <span v-else>Sin información</span>
              </div>

              <div>
                <b>Área</b>
                <span>{{ compraSeleccionada?.area_nombre || 'No indicada' }}</span>
              </div>

              <div>
                <b>Vía de adquisición</b>
                <span>{{ compraSeleccionada?.via_nombre || 'No indicada' }}</span>
              </div>

            </div>

            <div class="documento-fila">

              <div>
                <b>Fecha de registro</b>
                <span>{{ formatearFecha(compraSeleccionada?.creado_en) }}</span>
              </div>

              <div v-if="compraSeleccionada?.monto_desembolsado">
                <b>Monto desembolsado</b>
                <span>Bs {{ Number(compraSeleccionada.monto_desembolsado).toFixed(2) }}</span>
              </div>

            </div>

          </div>


          <div class="documento-seccion">

            <div class="documento-titulo-fila">
              <span class="documento-icono">📄</span>
              <span class="documento-titulo">
                Documentos del expediente
              </span>
            </div>

            <div class="documento-lista">

              <template
                v-for="doc in documentosExpediente"
                :key="doc.label"
              >

                <a
                  v-if="doc.url"
                  :href="doc.url"
                  target="_blank"
                  class="documento-item ok"
                >
                  <span class="documento-item-icono">📄</span>
                  <span class="documento-item-label">{{ doc.label }}</span>
                  <span class="documento-item-accion">
                    Ver archivo
                    <span class="documento-item-ojo">👁</span>
                  </span>
                </a>

                <div
                  v-else
                  class="documento-item falta"
                >
                  <span class="documento-item-icono">📄</span>
                  <span class="documento-item-label">{{ doc.label }}</span>
                  <small>{{ doc.pendienteTexto || 'No adjuntado' }}</small>
                </div>

              </template>

            </div>

          </div>


          <div
            class="documento-seccion motivo-rechazo"
            v-if="compraSeleccionada?.motivo_rechazo"
          >
            <span class="documento-titulo">
              Motivo de rechazo
            </span>

            <p>{{ compraSeleccionada.motivo_rechazo }}</p>
          </div>


          <!-- ACCIONES -->

          <div
            v-if="etapaAccion(compraSeleccionada)"
            class="documento-acciones"
          >

            <p
              v-if="errorAccion"
              class="accion-error"
            >
              {{ errorAccion }}
            </p>


            <!-- DESEMBOLSO -->

            <template v-if="etapaAccion(compraSeleccionada) === 'desembolso'">

              <p class="nota-tramite">
                Registre el monto efectivo entregado y el
                responsable que recibe el efectivo para la
                adquisición.
              </p>

              <label>
                Monto desembolsado (Bs)
                <span>*</span>
              </label>

              <input
                v-model="montoDesembolso"
                type="number"
                min="0"
                step="0.01"
                placeholder="0.00"
              />

              <label>
                Responsable que recibe el efectivo
                <span>*</span>
              </label>

              <input
                v-model="responsableDesembolso"
                type="text"
                placeholder="Nombre del responsable"
              />

              <div class="acciones-botones">

                <button
                  class="btn-aprobar"
                  :disabled="procesando"
                  @click="confirmarDesembolso"
                >
                  Registrar desembolso
                </button>

              </div>

            </template>


          </div>

        </div>

      </div>
    </div>


    <!-- =================================================
         DATOS DEL SOLICITANTE
    ================================================== -->

    <div
      v-if="mostrarSolicitante"
      class="solicitante-modal-backdrop"
      @click.self="cerrarSolicitante"
    >
      <div class="detalle-modal">

        <div class="detalle-modal-header">
          <div>
            <h3>Datos del solicitante</h3>
          </div>

          <button
            class="detalle-modal-close"
            @click="cerrarSolicitante"
          >✕</button>
        </div>

        <div class="detalle-modal-body">

          <p
            v-if="cargandoSolicitante"
            class="detalle-vacio"
          >
            Cargando...
          </p>

          <template v-else-if="solicitanteDetalle">

            <div class="documento-fila">

              <div>
                <b>Nombre completo</b>
                <span>{{ solicitanteDetalle.nombre_completo || '—' }}</span>
              </div>

              <div>
                <b>Correo</b>
                <span>{{ solicitanteDetalle.email || '—' }}</span>
              </div>

            </div>

            <div class="documento-fila">

              <div>
                <b>Usuario</b>
                <span>{{ solicitanteDetalle.username || '—' }}</span>
              </div>

              <div>
                <b>Estado de la cuenta</b>
                <span>{{ solicitanteDetalle.is_active ? 'Activa' : 'Inactiva' }}</span>
              </div>

            </div>

            <div class="detalle-campo">
              <b>Roles</b>
              <span>
                {{
                  (solicitanteDetalle.roles || [])
                    .map(rol => rol.rol_nombre || rol.nombre)
                    .join(', ')
                  || 'Sin rol asignado'
                }}
              </span>
            </div>

          </template>

          <p
            v-else
            class="detalle-vacio"
          >
            No fue posible cargar los datos del solicitante.
          </p>

        </div>

      </div>
    </div>

  </div>
</template>


<script setup>

import {
  computed,
  onMounted,
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'

import TesoreriaMenu
  from '../components/TesoreriaMenu.vue'


const router =
  useRouter()


// ==========================================================
// DATOS
// ==========================================================

const compras =
  ref([])

const cargando =
  ref(true)


// ==========================================================
// FILTRO
// ==========================================================

const filtroEstado =
  ref('')

const comprasFiltradas =
  computed(() => {

    if (!filtroEstado.value) {
      return compras.value
    }

    return compras.value.filter(
      compra =>
        bucketEstado(compra.estado)
        === filtroEstado.value
    )
  })


// ==========================================================
// DETALLE (DOCUMENTO)
// ==========================================================

const mostrarDetalle =
  ref(false)

const compraSeleccionada =
  ref(null)

const documentosExpediente =
  computed(() => {

    const c =
      compraSeleccionada.value

    if (!c) {
      return []
    }

    return [
      { label: 'Informe', url: c.informe },
      { label: 'POA', url: c.poa },
      { label: 'Pedido', url: c.pedido },
      { label: 'Proforma', url: c.proforma },
      {
        label: 'Certificación presupuestaria',
        url: c.certificacion_presupuestaria,
        pendienteTexto: 'Pendiente (la genera la DAF)',
      },
      {
        label: 'Factura',
        url: c.factura,
        pendienteTexto: 'Pendiente (descargo del solicitante)',
      },
      {
        label: 'Acta de conformidad',
        url: c.acta_conformidad,
        pendienteTexto: 'Pendiente (descargo del solicitante)',
      },
      {
        label: 'Fotograma',
        url: c.fotograma,
        pendienteTexto: 'Pendiente (descargo del solicitante)',
      },
    ]
  })

const procesando =
  ref(false)

const montoDesembolso =
  ref('')

const responsableDesembolso =
  ref('')

const errorAccion =
  ref('')


function resetearFormularios() {

  montoDesembolso.value =
    ''

  responsableDesembolso.value =
    ''

  errorAccion.value =
    ''
}


function verDetalle(
  compra
) {

  compraSeleccionada.value =
    compra

  mostrarDetalle.value =
    true

  resetearFormularios()

  if (
    compra.monto_estimado
    &&
    !montoDesembolso.value
  ) {

    montoDesembolso.value =
      compra.monto_estimado
  }
}


function cerrarDetalle() {

  mostrarDetalle.value =
    false

  compraSeleccionada.value =
    null

  resetearFormularios()
}


// ==========================================================
// DATOS DEL SOLICITANTE
// ==========================================================

const mostrarSolicitante =
  ref(false)

const solicitanteDetalle =
  ref(null)

const cargandoSolicitante =
  ref(false)


async function abrirSolicitante(
  usuarioId
) {

  mostrarSolicitante.value =
    true

  cargandoSolicitante.value =
    true

  solicitanteDetalle.value =
    null

  try {

    const respuesta =
      await fetch(
        `/api/usuarios/usuarios/${usuarioId}/`,
        {
          headers: {
            Authorization: `Token ${token()}`,
            Accept: 'application/json',
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

    if (respuesta.ok) {

      solicitanteDetalle.value =
        await respuesta.json()
    }

  } catch (error) {

    console.error(
      'Error cargando datos del solicitante:',
      error
    )

  } finally {

    cargandoSolicitante.value =
      false
  }
}


function cerrarSolicitante() {

  mostrarSolicitante.value =
    false

  solicitanteDetalle.value =
    null
}


// ==========================================================
// ETAPA DE TESORERÍA
// ==========================================================
//
// Tesorería interviene en 3 compuertas del BPMN de Compra
// Caja Chica: verificar el expediente certificado por la DAF
// (o rechazarlo), registrar el desembolso una vez que el
// Director dio el visto bueno, y cerrar/archivar el
// expediente tras revisar el descargo final. Cada etapa usa
// su propio formulario.
// ==========================================================

function etapaAccion(
  compra
) {

  // En el BPMN de Caja Chica, Tesorería ejecuta una única tarea:
  // "DESEMBOLZAR DINERO", una vez que el Director autoriza la compra.
  const codigo =
    String(
      compra?.estado
      || ''
    )
      .trim()
      .toUpperCase()

  if (
    codigo === 'APROBADO_PARA_DESEMBOLSO'
  ) {

    return 'desembolso'
  }

  return null
}


async function confirmarDesembolso() {

  const monto =
    String(
      montoDesembolso.value
      || ''
    ).trim()

  const responsable =
    responsableDesembolso.value.trim()

  if (
    !monto
    ||
    Number(monto) <= 0
  ) {

    errorAccion.value =
      'Debe indicar el monto desembolsado.'

    return
  }

  if (!responsable) {

    errorAccion.value =
      'Debe indicar el responsable que recibe el efectivo.'

    return
  }

  await ejecutarAccion(
    'desembolsar',
    {
      monto_desembolsado: monto,
      responsable_adquisicion: responsable,
    },
    'aprobar'
  )
}


async function ejecutarAccion(
  endpoint,
  body,
  tipo
) {

  procesando.value =
    true

  errorAccion.value =
    ''

  try {

    const respuesta =
      await fetch(
        `/api/compras/solicitudes/${compraSeleccionada.value.id}/${endpoint}/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token()}`,
            Accept: 'application/json',
          },
          body: JSON.stringify(body),
        }
      )

    let datos = {}

    try {
      datos = await respuesta.json()
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

    if (!respuesta.ok) {

      errorAccion.value =
        datos.detalle
        || `No fue posible ${tipo === 'aprobar' ? 'registrar' : 'rechazar'} la solicitud.`

      return
    }

    cerrarDetalle()

    await cargarCompras()

  } catch (error) {

    console.error(
      'Error ejecutando la acción:',
      error
    )

    errorAccion.value =
      'No fue posible comunicarse con el servidor.'

  } finally {

    procesando.value =
      false
  }
}


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


    await cargarCompras()
  }
)


// ==========================================================
// NORMALIZAR
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
// CARGAR COMPRAS
// ==========================================================

async function cargarCompras() {

  cargando.value =
    true


  try {

    const respuesta =
      await fetch(
        '/api/compras/solicitudes/',
        {
          headers: {

            Authorization:
              `Token ${token()}`,

            Accept:
              'application/json',
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

      console.error(
        'Compras:',
        respuesta.status
      )

      compras.value = []

      return
    }


    const datos =
      await respuesta.json()


    compras.value =
      normalizarLista(
        datos
      )
      .sort(
        (a, b) => {

          const fechaA =
            new Date(a.creado_en || 0).getTime()

          const fechaB =
            new Date(b.creado_en || 0).getTime()

          return fechaB - fechaA
        }
      )


  } catch (error) {

    console.error(
      'Error cargando compras:',
      error
    )

    compras.value = []


  } finally {

    cargando.value =
      false
  }
}


// ==========================================================
// ESTADO (AGRUPACIÓN VISUAL SIMPLIFICADA PARA TESORERÍA)
// ==========================================================
//
// Para Tesorería, "en espera" es el único estado que le
// corresponde resolver: APROBADO_PARA_DESEMBOLSO.
// ==========================================================

function bucketEstado(
  estado
) {

  const codigo =
    String(
      estado
      || ''
    )
      .trim()
      .toUpperCase()


  if (
    codigo === 'RECHAZADO'
    ||
    codigo === 'ANULADO'
  ) {

    return 'RECHAZADA'
  }


  if (
    codigo === 'APROBADO_PARA_DESEMBOLSO'
  ) {

    return 'EN_ESPERA'
  }


  return 'APROBADA'
}


function etiquetaBucket(
  bucket
) {

  return (
    {
      EN_ESPERA: 'Aprobación en espera',
      APROBADA: 'Aprobada',
      RECHAZADA: 'Rechazada',
    }[bucket]
    || bucket
  )
}


function etiquetaFiltroVacio(
  bucket
) {

  return (
    {
      APROBADA: 'solicitudes aprobadas',
      RECHAZADA: 'solicitudes rechazadas',
    }[bucket]
    || 'solicitudes'
  )
}


function claseBucket(
  bucket
) {

  return (
    {
      EN_ESPERA: 'working',
      APROBADA: 'closed',
      RECHAZADA: 'cancelled',
    }[bucket]
    || 'working'
  )
}


function iconoBucket(
  bucket
) {

  return (
    {
      EN_ESPERA: '⏳',
      APROBADA: '✅',
      RECHAZADA: '❌',
    }[bucket]
    || '⏳'
  )
}


function descripcionBucket(
  bucket
) {

  return (
    {
      EN_ESPERA: 'El expediente se encuentra pendiente de verificación, desembolso o cierre.',
      APROBADA: 'El expediente ya avanzó fuera de la bandeja de Tesorería.',
      RECHAZADA: 'El expediente fue rechazado.',
    }[bucket]
    || ''
  )
}


// ==========================================================
// FECHA
// ==========================================================

function formatearFecha(
  fecha
) {

  if (!fecha) {

    return ''
  }


  try {

    return new Date(
      fecha
    ).toLocaleString(
      'es-BO',
      {
        dateStyle: 'short',
        timeStyle: 'short',
      }
    )

  } catch {

    return ''
  }
}


// ==========================================================
// SESIÓN
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


.main {
  flex: 1;
  min-width: 0;
  padding: 27px;
  overflow-x: hidden;
}


/* =========================================================
   HEADER
========================================================= */

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 18px;
  margin-bottom: 20px;
}


.page-header h1 {
  margin: 0;
  color: #17324a;
  font-size: 33px;
}


.page-header p {
  margin: 5px 0 0;
  color: #718294;
  font-size: 17px;
}


.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}


.filtro-estado {
  min-height: 41px;
  padding: 0 12px;
  border: 1px solid #d0dae2;
  border-radius: 7px;
  background: white;
  color: #17324a;
  font-family: inherit;
  font-size: 15px;
  outline: none;
}


.refresh-button {
  min-height: 41px;
  padding: 0 15px;
  border: 1px solid #073b6f;
  border-radius: 7px;
  background: white;
  color: #073b6f;
  font-size: 15px;
  font-weight: 800;
  cursor: pointer;
}


.refresh-button:disabled {
  opacity: .6;
  cursor: not-allowed;
}


/* =========================================================
   LISTADO
========================================================= */

.requests-card {
  overflow: hidden;
  border-radius: 10px;
  background: white;
  box-shadow: 0 4px 14px rgba(0,0,0,.05);
}


.request-list {
  display: flex;
  flex-direction: column;
}


.request {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  padding: 17px 20px;
  border-bottom: 1px solid #edf0f2;
}


.request:last-child {
  border-bottom: none;
}


.request-main {
  flex: 1;
  min-width: 0;
  display: grid;
  grid-template-columns: 155px 1fr;
  gap: 15px;
}


.request-code strong {
  display: block;
  color: #07518d;
  font-size: 15px;
}


.request-code small {
  display: block;
  margin-top: 4px;
  color: #81909c;
  font-size: 13px;
}


.request-info h3 {
  margin: 0 0 5px;
  color: #29475e;
  font-size: 18px;
}


.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}


.meta span {
  padding: 4px 6px;
  border-radius: 4px;
  background: #f3f6f8;
  color: #687986;
  font-size: 13px;
}


.request-side {
  flex-shrink: 0;
  display: flex;
  align-items: flex-end;
  flex-direction: column;
  gap: 9px;
}


/* =========================================================
   ESTADO
========================================================= */

.status {
  display: inline-block;
  padding: 5px 8px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 800;
}


.status.working {
  background: #fff6d9;
  color: #866400;
}


.status.closed {
  background: #e8f6ee;
  color: #237345;
}


.status.cancelled {
  background: #fdeaea;
  color: #a53232;
}


.row-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
}


.view,
.row-aprobar,
.row-rechazar {
  padding: 6px 8px;
  border: none;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}


.view {
  background: #edf3f8;
  color: #435a6e;
}


.row-aprobar {
  background: #e5f3ea;
  color: #237345;
}


.row-rechazar {
  background: #fdecec;
  color: #a53232;
}


/* =========================================================
   VACÍOS
========================================================= */

.loading,
.empty {
  padding: 45px 20px;
  text-align: center;
  color: #798793;
  font-size: 16px;
}


.empty {
  border-radius: 10px;
  background: white;
}


/* =========================================================
   DOCUMENTO DE DETALLE
========================================================= */

.documento-modal {
  max-width: 700px;
}


.documento-modal .detalle-modal-header h3 {
  font-size: 20px;
}


.documento-modal .detalle-modal-header small {
  font-size: 13px;
}


.documento-body {
  padding: 18px 22px 22px;
}


.estado-banner {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
  padding: 14px 16px;
  border-radius: 8px;
}


.estado-banner-icono {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255,255,255,.6);
  font-size: 19px;
}


.estado-banner strong {
  display: block;
  font-size: 18px;
  font-weight: 800;
}


.estado-banner-descripcion {
  display: block;
  margin-top: 2px;
  font-size: 15px;
  font-weight: 500;
  opacity: .85;
}


.estado-banner.working {
  background: #fff6d9;
  color: #866400;
}


.estado-banner.closed {
  background: #e8f6ee;
  color: #237345;
}


.estado-banner.cancelled {
  background: #fdeaea;
  color: #a53232;
}


.documento-seccion {
  padding: 16px 0;
  border-top: 1px solid #edf0f2;
}


.documento-seccion:first-of-type {
  border-top: none;
  padding-top: 0;
}


.documento-header-titulo {
  display: flex;
  align-items: center;
  gap: 12px;
}


.documento-header-icono {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #fdf3d9;
  font-size: 17px;
}


.documento-titulo-fila {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}


.documento-icono {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  background: #eef1f8;
  font-size: 13px;
}


.documento-titulo {
  display: block;
  margin-bottom: 8px;
  color: #8592a0;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .6px;
  text-transform: uppercase;
}


.documento-titulo-fila .documento-titulo {
  margin-bottom: 0;
}


.documento-seccion h4 {
  margin: 0 0 6px;
  color: #17324a;
  font-size: 20px;
}


.documento-seccion > p {
  margin: 0 0 10px;
  color: #354d60;
  font-size: 16px;
  line-height: 1.5;
  white-space: pre-wrap;
}


.documento-seccion b {
  display: block;
  margin-bottom: 4px;
  color: #8592a0;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: .5px;
  text-transform: uppercase;
}


.documento-fila {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 12px;
  margin-bottom: 12px;
}


.documento-fila-5 {
  grid-template-columns: repeat(auto-fit, minmax(105px, 1fr));
}


.documento-fila > div span {
  display: block;
  color: #26333f;
  font-size: 16px;
}


.solicitante-link {
  display: block;
  width: 100%;
  padding: 0;
  border: none;
  background: transparent;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
}


.solicitante-link span {
  display: block;
  color: #07518d;
  font-size: 14px;
  font-weight: 700;
  text-decoration: underline;
}


.solicitante-link:hover span {
  color: #073b6f;
}


.solicitante-link small {
  display: block;
  margin-top: 2px;
  color: #26333f;
  font-size: 13px;
}


.solicitante-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(10, 20, 35, .55);
}


.documento-lista {
  display: flex;
  flex-direction: column;
  gap: 8px;
}


.documento-item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 12px;
  border: none;
  border-radius: 7px;
  font-family: inherit;
  text-align: left;
  text-decoration: none;
}


.documento-item-icono {
  flex-shrink: 0;
  font-size: 16px;
}


.documento-item-label {
  flex: 1;
  color: #26333f;
  font-size: 14px;
  font-weight: 700;
}


.documento-item small {
  font-size: 13px;
}


.documento-item-accion {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}


.documento-item-ojo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255,255,255,.6);
  font-size: 11px;
}


.documento-item.ok {
  background: #e8f6ee;
}


.documento-item.ok .documento-item-accion {
  color: #237345;
  font-weight: 700;
}


.documento-item.falta {
  background: #f3f6f8;
}


.documento-item.falta small {
  color: #8a97a2;
}


.motivo-rechazo {
  padding: 14px;
  border: none;
  border-radius: 8px;
  background: #fdecec;
}


.motivo-rechazo .documento-titulo {
  color: #a53232;
}


.motivo-rechazo p {
  margin: 0;
  color: #7a2828;
  font-size: 14px;
  line-height: 1.5;
}


/* =========================================================
   ACCIONES DE DECISIÓN
========================================================= */

.documento-acciones {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #edf0f2;
}


.nota-tramite {
  margin: 0 0 12px;
  padding: 12px 14px;
  border-radius: 7px;
  background: #eef3f8;
  color: #536575;
  font-size: 14px;
  line-height: 1.5;
}


.accion-error {
  margin: 0 0 10px;
  padding: 10px 12px;
  border-radius: 7px;
  background: #fdecec;
  color: #a53232;
  font-size: 14px;
}


.acciones-botones {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}


.btn-aprobar,
.btn-rechazar,
.btn-cancelar {
  min-height: 40px;
  padding: 0 16px;
  border: none;
  border-radius: 7px;
  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
}


.btn-aprobar {
  background: #237345;
  color: white;
}


.btn-rechazar {
  background: #a53232;
  color: white;
}


.btn-cancelar {
  background: #edf0f2;
  color: #435a6e;
}


.btn-aprobar:disabled,
.btn-rechazar:disabled,
.btn-cancelar:disabled {
  opacity: .6;
  cursor: not-allowed;
}


.form-rechazo label,
.documento-acciones > label {
  display: block;
  margin-bottom: 6px;
  color: #344a5d;
  font-size: 14px;
  font-weight: 700;
}


.form-rechazo label span,
.documento-acciones > label span {
  color: #a53232;
}


.form-rechazo textarea {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px 12px;
  border: 1px solid #d0dae2;
  border-radius: 7px;
  background: white;
  color: #26333f;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  outline: none;
}


.documento-acciones > input {
  width: 100%;
  min-height: 40px;
  margin-bottom: 12px;
  padding: 0 12px;
  border: 1px solid #d0dae2;
  border-radius: 7px;
  background: white;
  color: #26333f;
  font-family: inherit;
  font-size: 14px;
  outline: none;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 760px) {

  .layout {
    display: block;
  }


  .main {
    padding: 16px;
  }


  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }


  .header-actions {
    width: 100%;
  }


  .filtro-estado {
    flex: 1;
  }


  .request {
    align-items: flex-start;
    flex-direction: column;
  }


  .request-main {
    grid-template-columns: 1fr;
  }


  .request-side {
    width: 100%;
    align-items: flex-start;
  }


  .documento-fila {
    grid-template-columns: 1fr;
  }

}

</style>
