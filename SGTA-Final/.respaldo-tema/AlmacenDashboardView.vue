<template>
  <div class="layout">

    <AlmacenMenu />

    <main class="main">

      <!-- =================================================
           ENCABEZADO
      ================================================== -->
      <header class="page-header">

        <div v-if="esRutaRequerimientos">
          <h1>
            Requerimientos
          </h1>

          <p>
            Verificación de existencia en almacén para
            requerimientos de Mantenimiento.
          </p>
        </div>

        <div v-else>
          <h1>
            Compras
          </h1>

          <p>
            Adquisición, ingreso y despacho de compras
            desembolsadas por Tesorería.
          </p>
        </div>

        <div
          v-if="!esRutaRequerimientos"
          class="header-actions"
        >

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

        <button
          v-else
          class="refresh-button"
          type="button"
          :disabled="cargandoRequerimientos"
          @click="cargarRequerimientos"
        >
          {{
            cargandoRequerimientos
              ? 'Actualizando...'
              : 'Actualizar'
          }}
        </button>

      </header>


      <!-- =================================================
           COMPRAS
      ================================================== -->

      <template v-if="!esRutaRequerimientos">

        <div
          v-if="cargando"
          class="loading"
        >
          Cargando solicitudes de compra...
        </div>

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
                    v-if="etapaAccion(compra) === 'comprar'"
                    class="row-aprobar"
                    @click="verDetalle(compra)"
                  >
                    Registrar compra
                  </button>

                  <button
                    v-if="etapaAccion(compra) === 'ingreso'"
                    class="row-aprobar"
                    @click="verDetalle(compra)"
                  >
                    Registrar ingreso
                  </button>

                  <button
                    v-if="etapaAccion(compra) === 'despacho'"
                    class="row-aprobar"
                    @click="verDetalle(compra)"
                  >
                    Registrar despacho
                  </button>

                </div>

              </div>

            </article>

          </div>

        </section>

      </template>


      <!-- =================================================
           REQUERIMIENTOS (MANTENIMIENTO)
      ================================================== -->

      <template v-else>

        <div
          v-if="cargandoRequerimientos"
          class="loading"
        >
          Cargando requerimientos...
        </div>

        <div
          v-else-if="requerimientos.length === 0"
          class="empty"
        >
          No existen requerimientos de mantenimiento registrados.
        </div>

        <section
          v-else
          class="requests-card"
        >

          <div class="request-list">

            <article
              v-for="req in requerimientos"
              :key="req.id"
              class="request"
            >

              <div class="request-main">

                <div class="request-code">
                  <strong>
                    {{ codigoRequerimiento(req) }}
                  </strong>

                  <small>
                    {{ req.area_nombre || 'Área no indicada' }}
                  </small>
                </div>


                <div class="request-info">

                  <h3>
                    {{
                      req.titulo
                      || req.asunto
                      || req.descripcion_corta
                      || 'Requerimiento de mantenimiento'
                    }}
                  </h3>

                  <div class="meta">

                    <span>
                      {{
                        req.solicitante_nombre
                        || req.solicitante_email
                        || 'Sin información'
                      }}
                    </span>

                    <span v-if="req.created_at || req.fecha_solicitud">
                      {{ formatearFecha(req.created_at || req.fecha_solicitud) }}
                    </span>

                  </div>

                </div>

              </div>


              <div class="request-side">

                <span class="status working">
                  {{ estadoRequerimiento(req) }}
                </span>

                <div class="row-actions">

                  <button
                    class="view"
                    @click="verRequerimiento(req)"
                  >
                    Ver detalle
                  </button>

                  <button
                    v-if="req.estado_codigo === 'REVISION_ALMACEN'"
                    class="row-aprobar"
                    @click="verRequerimiento(req)"
                  >
                    Reportar existencia
                  </button>

                </div>

              </div>

            </article>

          </div>

        </section>

      </template>

    </main>


    <!-- =================================================
         DOCUMENTO DE DETALLE (COMPRAS)
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
                <span>
                  {{
                    compraSeleccionada?.solicitante_nombre
                    || compraSeleccionada?.solicitante_email
                    || 'Sin información'
                  }}
                </span>
              </div>

              <div>
                <b>Área</b>
                <span>{{ compraSeleccionada?.area_nombre || 'No indicada' }}</span>
              </div>

              <div>
                <b>Monto desembolsado</b>
                <span>
                  {{
                    compraSeleccionada?.monto_desembolsado
                      ? `Bs ${Number(compraSeleccionada.monto_desembolsado).toFixed(2)}`
                      : 'No indicado'
                  }}
                </span>
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


            <!-- REGISTRAR COMPRA -->

            <template v-if="etapaAccion(compraSeleccionada) === 'comprar'">

              <p class="nota-tramite">
                Registre el monto real cobrado por el
                proveedor y confirme que el componente
                recibido coincide con lo solicitado.
              </p>

              <label>
                Monto real (Bs)
                <span>*</span>
              </label>

              <input
                v-model="montoReal"
                type="number"
                min="0"
                step="0.01"
                placeholder="0.00"
              />

              <label>
                Proveedor
                <span>*</span>
              </label>

              <input
                v-model="proveedor"
                type="text"
                placeholder="Nombre o razón social"
              />

              <div class="acciones-botones">

                <button
                  class="btn-aprobar"
                  :disabled="procesando"
                  @click="confirmarCompra"
                >
                  Confirmar compra
                </button>

              </div>

            </template>


            <!-- INGRESO A ALMACÉN -->

            <template v-else-if="etapaAccion(compraSeleccionada) === 'ingreso'">

              <p class="nota-tramite">
                Confirme el ingreso físico del producto a
                almacén.
              </p>

              <div class="acciones-botones">

                <button
                  class="btn-aprobar"
                  :disabled="procesando"
                  @click="confirmarIngreso"
                >
                  Confirmar ingreso
                </button>

              </div>

            </template>


            <!-- DESPACHO -->

            <template v-else-if="etapaAccion(compraSeleccionada) === 'despacho'">

              <p class="nota-tramite">
                Confirme el despacho y entrega del producto
                al solicitante.
              </p>

              <div class="acciones-botones">

                <button
                  class="btn-aprobar"
                  :disabled="procesando"
                  @click="confirmarDespacho"
                >
                  Confirmar despacho
                </button>

              </div>

            </template>

          </div>

        </div>

      </div>
    </div>


    <!-- =================================================
         DETALLE DE REQUERIMIENTO (MANTENIMIENTO)
    ================================================== -->

    <div
      v-if="mostrarDetalleRequerimiento"
      class="detalle-modal-backdrop"
      @click.self="cerrarRequerimiento"
    >
      <div class="detalle-modal documento-modal">

        <div class="detalle-modal-header">
          <div class="documento-header-titulo">

            <span class="documento-header-icono">🧰</span>

            <div>
              <h3>{{ codigoRequerimiento(requerimientoSeleccionado) }}</h3>
              <small>
                {{
                  requerimientoSeleccionado?.titulo
                  || requerimientoSeleccionado?.asunto
                  || 'Requerimiento de mantenimiento'
                }}
              </small>
            </div>

          </div>

          <button
            class="detalle-modal-close"
            @click="cerrarRequerimiento"
          >✕</button>
        </div>

        <div class="documento-body">

          <div class="documento-seccion">

            <div class="documento-titulo-fila">
              <span class="documento-icono">📝</span>
              <span class="documento-titulo">
                Detalle del requerimiento
              </span>
            </div>

            <p>
              {{
                requerimientoSeleccionado?.descripcion
                || requerimientoSeleccionado?.justificacion
                || 'Sin descripción registrada.'
              }}
            </p>

            <div class="documento-fila">

              <div>
                <b>Solicitante</b>
                <span>
                  {{
                    requerimientoSeleccionado?.solicitante_nombre
                    || requerimientoSeleccionado?.solicitante_email
                    || 'Sin información'
                  }}
                </span>
              </div>

              <div>
                <b>Estado</b>
                <span>{{ estadoRequerimiento(requerimientoSeleccionado) }}</span>
              </div>

              <div>
                <b>Fecha</b>
                <span>
                  {{
                    formatearFecha(
                      requerimientoSeleccionado?.created_at
                      || requerimientoSeleccionado?.fecha_solicitud
                    )
                  }}
                </span>
              </div>

            </div>

          </div>


          <!-- ACCIÓN: REPORTAR EXISTENCIA -->

          <div
            v-if="requerimientoSeleccionado?.estado_codigo === 'REVISION_ALMACEN'"
            class="documento-acciones"
          >

            <p
              v-if="errorAccion"
              class="accion-error"
            >
              {{ errorAccion }}
            </p>

            <p class="nota-tramite">
              Indique si existe stock disponible en almacén
              para atender este requerimiento.
            </p>

            <label>
              Observación de almacén (opcional)
            </label>

            <input
              v-model="observacionAlmacen"
              type="text"
              placeholder="Detalle adicional..."
            />

            <div class="acciones-botones">

              <button
                class="btn-rechazar"
                :disabled="procesando"
                @click="reportarExistencia(false)"
              >
                No hay stock
              </button>

              <button
                class="btn-aprobar"
                :disabled="procesando"
                @click="reportarExistencia(true)"
              >
                Hay stock disponible
              </button>

            </div>

          </div>

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
  useRoute,
  useRouter
} from 'vue-router'

import AlmacenMenu
  from '../components/AlmacenMenu.vue'


const router =
  useRouter()

const route =
  useRoute()

const esRutaRequerimientos =
  computed(() =>
    route.path.endsWith('requerimientos')
  )


// ==========================================================
// COMPRAS
// ==========================================================

const compras =
  ref([])

const cargando =
  ref(true)

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
      },
    ]
  })

const procesando =
  ref(false)

const montoReal =
  ref('')

const proveedor =
  ref('')

const errorAccion =
  ref('')


function resetearFormularios() {

  montoReal.value =
    ''

  proveedor.value =
    ''

  observacionAlmacen.value =
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
    compra.monto_desembolsado
    &&
    !montoReal.value
  ) {

    montoReal.value =
      compra.monto_desembolsado
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
// ETAPA DE ALMACÉN (COMPRAS)
// ==========================================================
//
// El Encargado de Compras y Almacén interviene en 3 pasos del
// BPMN, una vez que Tesorería desembolsó los fondos: comprar
// el pedido, registrar el ingreso físico a almacén y
// registrar el despacho/entrega al solicitante.
// ==========================================================

function etapaAccion(
  compra
) {

  const codigo =
    String(
      compra?.estado
      || ''
    )
      .trim()
      .toUpperCase()

  if (
    codigo === 'FONDOS_DESEMBOLSADOS'
  ) {

    return 'comprar'
  }

  if (
    codigo === 'COMPRA_REGISTRADA'
  ) {

    return compra?.fecha_ingreso_almacen
      ? 'despacho'
      : 'ingreso'
  }

  return null
}


async function confirmarCompra() {

  const monto =
    String(
      montoReal.value
      || ''
    ).trim()

  const nombreProveedor =
    proveedor.value.trim()

  if (
    !monto
    ||
    Number(monto) <= 0
  ) {

    errorAccion.value =
      'Debe indicar el monto real de la compra.'

    return
  }

  if (!nombreProveedor) {

    errorAccion.value =
      'Debe indicar el proveedor.'

    return
  }

  if (
    !window.confirm(
      '¿Confirma que el componente recibido coincide con lo solicitado?'
    )
  ) {

    return
  }

  await ejecutarAccionCompra(
    'registrar-compra',
    {
      monto_real: monto,
      proveedor: nombreProveedor,
      componente_verificado: true,
    }
  )
}


async function confirmarIngreso() {

  if (
    !window.confirm(
      '¿Confirma el ingreso físico del producto a almacén?'
    )
  ) {

    return
  }

  await ejecutarAccionCompra(
    'registrar-ingreso-almacen',
    {}
  )
}


async function confirmarDespacho() {

  if (
    !window.confirm(
      '¿Confirma el despacho y entrega del producto al solicitante?'
    )
  ) {

    return
  }

  await ejecutarAccionCompra(
    'registrar-despacho-almacen',
    {}
  )
}


async function ejecutarAccionCompra(
  endpoint,
  body
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
        || 'No fue posible registrar la acción.'

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
// CARGAR COMPRAS
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


async function cargarCompras() {

  cargando.value =
    true

  try {

    const respuesta =
      await fetch(
        '/api/compras/solicitudes/',
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

    if (!respuesta.ok) {

      compras.value = []

      return
    }

    const datos =
      await respuesta.json()

    compras.value =
      normalizarLista(datos)
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
// ESTADO (AGRUPACIÓN VISUAL SIMPLIFICADA PARA ALMACÉN)
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
    codigo === 'FONDOS_DESEMBOLSADOS'
    ||
    codigo === 'COMPRA_REGISTRADA'
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
      EN_ESPERA: 'La compra se encuentra pendiente de adquisición, ingreso o despacho.',
      APROBADA: 'La compra ya avanzó fuera de la bandeja de Almacén.',
      RECHAZADA: 'La solicitud fue rechazada.',
    }[bucket]
    || ''
  )
}


// ==========================================================
// REQUERIMIENTOS (MANTENIMIENTO)
// ==========================================================

const requerimientos =
  ref([])

const cargandoRequerimientos =
  ref(true)

const mostrarDetalleRequerimiento =
  ref(false)

const requerimientoSeleccionado =
  ref(null)

const observacionAlmacen =
  ref('')


function codigoRequerimiento(
  req
) {

  return (
    req?.codigo
    || req?.numero_solicitud
    || `#${req?.id ?? ''}`
  )
}


function estadoRequerimiento(
  req
) {

  return String(
    req?.estado_nombre
    || req?.estado?.nombre
    || req?.estado
    || 'Pendiente'
  )
}


function verRequerimiento(
  req
) {

  requerimientoSeleccionado.value =
    req

  mostrarDetalleRequerimiento.value =
    true

  observacionAlmacen.value =
    ''

  errorAccion.value =
    ''
}


function cerrarRequerimiento() {

  mostrarDetalleRequerimiento.value =
    false

  requerimientoSeleccionado.value =
    null
}


async function cargarRequerimientos() {

  cargandoRequerimientos.value =
    true

  try {

    const respuesta =
      await fetch(
        '/api/mantenimiento/requerimientos/',
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

    if (!respuesta.ok) {

      requerimientos.value = []

      return
    }

    const datos =
      await respuesta.json()

    requerimientos.value =
      normalizarLista(datos)

  } catch (error) {

    console.error(
      'Error cargando requerimientos:',
      error
    )

    requerimientos.value = []

  } finally {

    cargandoRequerimientos.value =
      false
  }
}


async function reportarExistencia(
  disponible
) {

  if (!requerimientoSeleccionado.value) {
    return
  }

  procesando.value =
    true

  errorAccion.value =
    ''

  try {

    const respuesta =
      await fetch(
        `/api/mantenimiento/requerimientos/${requerimientoSeleccionado.value.id}/reportar-existencia/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token()}`,
            Accept: 'application/json',
          },
          body: JSON.stringify({
            producto_disponible: disponible,
            observacion_almacen: observacionAlmacen.value || '',
          }),
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
        || 'No fue posible registrar la respuesta.'

      return
    }

    cerrarRequerimiento()

    await cargarRequerimientos()

  } catch (error) {

    console.error(
      'Error reportando existencia:',
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
// TOKEN / SESIÓN
// ==========================================================

function token() {

  return localStorage.getItem(
    'sigta_token'
  )
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

    await Promise.all([
      cargarCompras(),
      cargarRequerimientos(),
    ])
  }
)

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


.btn-aprobar:disabled,
.btn-rechazar:disabled {
  opacity: .6;
  cursor: not-allowed;
}


.documento-acciones > label {
  display: block;
  margin-bottom: 6px;
  color: #344a5d;
  font-size: 14px;
  font-weight: 700;
}


.documento-acciones > label span {
  color: #a53232;
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
