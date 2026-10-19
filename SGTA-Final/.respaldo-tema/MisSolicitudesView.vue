<template>

  <div class="layout">

    <SolicitanteMenu />


    <main class="content">

      <!-- ============================================
           ENCABEZADO
      ============================================= -->

      <header class="topbar">

        <div>

          <h1>
            Mis solicitudes
          </h1>

          <p>
            Consulte y dé seguimiento a sus requerimientos
            de Soporte Técnico y Mantenimiento.
          </p>

        </div>

        <button
          class="btn-new"
          type="button"
          @click="mostrarCrear = !mostrarCrear"
        >
          ＋ Nueva solicitud
        </button>

      </header>

      <section v-if="mostrarCrear" class="create-panel">
        <button type="button" @click="router.push('/usuario/soporte')">
          <span>🖥️</span>
          <div>
            <strong>Soporte Técnico</strong>
            <small>Equipos, redes, sistemas y dispositivos.</small>
          </div>
        </button>

        <button type="button" @click="router.push('/usuario/mantenimiento')">
          <span>🛠️</span>
          <div>
            <strong>Mantenimiento</strong>
            <small>Infraestructura, instalaciones y servicios.</small>
          </div>
        </button>
      </section>


      <!-- ============================================
           RESUMEN
      ============================================= -->

      <section class="summary">

        <article>

          <span>
            Total
          </span>

          <strong>
            {{ solicitudes.length }}
          </strong>

          <small>
            Registros realizados
          </small>

        </article>


        <article>

          <span>
            Soporte Técnico
          </span>

          <strong>
            {{ soporte.length }}
          </strong>

          <small>
            Solicitudes de soporte
          </small>

        </article>


        <article>

          <span>
            Mantenimiento
          </span>

          <strong>
            {{ mantenimiento.length }}
          </strong>

          <small>
            Requerimientos de mantenimiento
          </small>

        </article>

      </section>


      <!-- ============================================
           FILTROS
      ============================================= -->

      <section class="filters-card">

        <div class="search">

          <label>
            Buscar
          </label>

          <input
            v-model="busqueda"
            type="text"
            placeholder="Código, título, ubicación o proceso..."
          />

        </div>


        <div class="filter">

          <label>
            Proceso
          </label>

          <select
            v-model="filtroProceso"
          >

            <option value="">
              Todos
            </option>

            <option value="SOPORTE">
              Soporte Técnico
            </option>

            <option value="MANTENIMIENTO">
              Mantenimiento
            </option>

          </select>

        </div>


        <div class="filter">

          <label>
            Estado
          </label>

          <select
            v-model="filtroEstado"
          >

            <option value="">
              Todos
            </option>

            <option
              v-for="estado in estadosDisponibles"
              :key="estado.valor"
              :value="estado.valor"
            >
              {{ estado.etiqueta }}
            </option>

          </select>

        </div>

      </section>


      <!-- ============================================
           MENSAJES
      ============================================= -->

      <div
        v-if="mensaje"
        :class="[
          'alert',
          esError
            ? 'error'
            : 'success'
        ]"
      >
        {{ mensaje }}
      </div>


      <!-- ============================================
           LISTADO
      ============================================= -->

      <section class="requests-card">

        <div
          v-if="cargando"
          class="empty"
        >
          Cargando sus requerimientos...
        </div>


        <div
          v-else-if="
            solicitudesFiltradas.length === 0
          "
          class="empty"
        >

          <h3>
            No se encontraron solicitudes
          </h3>

          <p>
            Puede registrar una solicitud de soporte
            o un requerimiento de mantenimiento.
          </p>

          <button
            @click="mostrarCrear = true"
          >
            Nueva solicitud
          </button>

        </div>


        <div
          v-else
          class="request-list"
        >

          <article
            v-for="item in solicitudesFiltradas"
            :key="`${item.proceso}-${item.id}`"
            class="request"
          >

            <div class="request-main">

              <div class="request-code">

                <span
                  :class="[
                    'process-indicator',
                    claseProceso(item.proceso)
                  ]"
                ></span>

                <div>

                  <strong>
                    {{ item.codigo }}
                  </strong>

                  <small>
                    {{ item.modulo }}
                  </small>

                </div>

              </div>


              <div class="request-info">

                <h3>
                  {{
                    item.titulo
                    || 'Requerimiento institucional'
                  }}
                </h3>

                <p>
                  {{
                    item.descripcion
                    || 'Sin descripción registrada.'
                  }}
                </p>


                <div class="meta">

                  <span
                    v-if="item.area_nombre"
                  >
                    {{ item.area_nombre }}
                  </span>


                  <span
                    v-if="item.ubicacion"
                  >
                    {{ item.ubicacion }}
                  </span>


                  <span
                    v-if="item.detalle_tipo"
                  >
                    {{ item.detalle_tipo }}
                  </span>


                  <span
                    v-if="item.fecha"
                  >
                    {{ formatearFecha(item.fecha) }}
                  </span>

                </div>

              </div>

            </div>


            <div class="request-side">

              <span
                :class="[
                  'status',
                  claseEstado(item.estado_codigo)
                ]"
              >
                {{
                  item.estado_nombre
                  || item.estado_codigo
                  || 'Registrado'
                }}
              </span>


              <div class="actions">

                <button
                  class="view"
                  @click="verDetalle(item)"
                >
                  Ver
                </button>


                <!--
                  La edición/anulación se conserva únicamente
                  para Soporte Técnico porque ese CRUD ya está
                  implementado en esta misma vista.
                -->

                <button
                  v-if="puedeEditarSoporte(item)"
                  class="edit"
                  @click="abrirEditarSoporte(item)"
                >
                  Editar
                </button>


                <button
                  v-if="puedeCancelar(item)"
                  class="cancel"
                  @click="anularSolicitud(item)"
                >
                  Cancelar
                </button>


                <button
                  v-if="item.proceso === 'SOPORTE' && item.estado_codigo === 'EN_VERIFICACION'"
                  class="edit"
                  @click="verificarFuncionamiento(item, true)"
                >
                  Funciona correctamente
                </button>

                <button
                  v-if="item.proceso === 'SOPORTE' && item.estado_codigo === 'EN_VERIFICACION'"
                  class="cancel"
                  @click="verificarFuncionamiento(item, false)"
                >
                  Sigue con el problema
                </button>


                <button
                  v-if="item.proceso === 'SOPORTE' && item.estado_codigo === 'PENDIENTE_CONFORMIDAD'"
                  class="edit"
                  @click="informarConformidad(item, true)"
                >
                  Estoy conforme
                </button>

                <button
                  v-if="item.proceso === 'SOPORTE' && item.estado_codigo === 'PENDIENTE_CONFORMIDAD'"
                  class="cancel"
                  @click="informarConformidad(item, false)"
                >
                  No conforme
                </button>

              </div>

            </div>

          </article>

        </div>

      </section>

    </main>


    <!-- ============================================
         MODAL DETALLE GENERAL
    ============================================= -->

    <div
      v-if="mostrarDetalle"
      class="overlay"
      @click.self="cerrarDetalle"
    >

      <div class="modal detail-modal">

        <div class="modal-header">

          <div>

            <span class="modal-code">
              {{ solicitudSeleccionada?.codigo }}
            </span>

            <h2>
              {{ solicitudSeleccionada?.titulo }}
            </h2>

            <p>
              {{ solicitudSeleccionada?.modulo }}
            </p>

          </div>


          <button
            class="close"
            @click="cerrarDetalle"
          >
            ×
          </button>

        </div>


        <div class="detail-status">

          <span
            :class="[
              'status',
              claseEstado(
                solicitudSeleccionada?.estado_codigo
              )
            ]"
          >
            {{
              solicitudSeleccionada?.estado_nombre
              ||
              solicitudSeleccionada?.estado_codigo
              ||
              'Registrado'
            }}
          </span>

        </div>

        <div class="timeline">
          <div
            v-for="(paso, indice) in pasosSolicitud(solicitudSeleccionada)"
            :key="paso.nombre"
            :class="['timeline-step', { completado: paso.completado, actual: paso.actual }]"
          >
            <span>{{ paso.completado ? '✓' : indice + 1 }}</span>
            <small>{{ paso.nombre }}</small>
          </div>
        </div>


        <div class="detail-grid">

          <div>

            <label>
              Proceso
            </label>

            <p>
              {{ solicitudSeleccionada?.modulo }}
            </p>

          </div>


          <div>

            <label>
              Área
            </label>

            <p>
              {{
                solicitudSeleccionada?.area_nombre
                || 'No indicada'
              }}
            </p>

          </div>


          <div
            v-if="
              solicitudSeleccionada?.ubicacion
            "
          >

            <label>
              Ubicación
            </label>

            <p>
              {{ solicitudSeleccionada?.ubicacion }}
            </p>

          </div>


          <div
            v-if="
              solicitudSeleccionada?.detalle_tipo
            "
          >

            <label>
              Tipo
            </label>

            <p>
              {{ solicitudSeleccionada?.detalle_tipo }}
            </p>

          </div>


          <div class="full">

            <label>
              Descripción
            </label>

            <p>
              {{
                solicitudSeleccionada?.descripcion
                || 'Sin descripción registrada.'
              }}
            </p>

          </div>


          <!-- SOPORTE -->

          <template
            v-if="
              solicitudSeleccionada?.proceso
              === 'SOPORTE'
            "
          >

            <div>

              <label>
                Categoría
              </label>

              <p>
                {{
                  solicitudSeleccionada?.categoria_nombre
                  || 'Sin categoría'
                }}
              </p>

            </div>


            <div>

              <label>
                Equipo afectado
              </label>

              <p>
                {{
                  solicitudSeleccionada?.equipo_afectado
                  || 'No indicado'
                }}
              </p>

            </div>


            <div class="full">

              <label>
                Evidencia
              </label>

              <p>
                {{
                  solicitudSeleccionada?.evidencia
                  || 'Sin evidencia registrada'
                }}
              </p>

            </div>


            <div class="full">

              <label>
                Revisión del equipo
              </label>

              <p>
                {{
                  solicitudSeleccionada?.diagnostico
                  || 'Pendiente de revisión UTIC'
                }}
              </p>

            </div>


            <div class="full">

              <label>
                Reparación técnica
              </label>

              <p>
                {{
                  solicitudSeleccionada?.solucion
                  || 'Pendiente'
                }}
              </p>

            </div>

          </template>


          <!-- MANTENIMIENTO -->

          <template
            v-if="
              solicitudSeleccionada?.proceso
              === 'MANTENIMIENTO'
            "
          >

            <div>

              <label>
                Tipo de mantenimiento
              </label>

              <p>
                {{
                  solicitudSeleccionada?.tipo_nombre
                  ||
                  solicitudSeleccionada?.tipo
                  ||
                  'No indicado'
                }}
              </p>

            </div>


            <div>

              <label>
                Auxiliar asignado
              </label>

              <p>
                {{
                  solicitudSeleccionada?.auxiliar_asignado_nombre
                  || 'Pendiente de derivación'
                }}
              </p>

            </div>


            <div class="full">

              <label>
                Evidencia
              </label>

              <p>
                {{
                  solicitudSeleccionada?.evidencia
                  || 'Sin evidencia registrada'
                }}
              </p>

            </div>

          </template>

        </div>


        <div class="modal-footer">

          <button
            class="secondary"
            @click="cerrarDetalle"
          >
            Cerrar
          </button>


          <button
            v-if="
              puedeEditarSoporte(
                solicitudSeleccionada
              )
            "
            class="primary"
            @click="editarDesdeDetalle"
          >
            Editar solicitud de soporte
          </button>

        </div>

      </div>

    </div>


    <!-- ============================================
         MODAL EDITAR SOPORTE
    ============================================= -->

    <div
      v-if="mostrarEditar"
      class="overlay"
      @click.self="cerrarEditar"
    >

      <div class="modal">

        <div class="modal-header">

          <div>

            <span class="modal-code">
              {{ solicitudSeleccionada?.codigo }}
            </span>

            <h2>
              Editar solicitud de soporte
            </h2>

            <p>
              Puede modificarla mientras
              se encuentre en estado NUEVO.
            </p>

          </div>


          <button
            class="close"
            @click="cerrarEditar"
          >
            ×
          </button>

        </div>


        <form
          @submit.prevent="guardarEdicionSoporte"
        >

          <div class="form-grid">

            <div class="field full">

              <label>
                Título
              </label>

              <input
                v-model="form.titulo"
                type="text"
                required
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


            <div class="field">

              <label>
                Área
              </label>

              <select
                v-model="form.area"
                required
              >

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
                Categoría
              </label>

              <select
                v-model="form.categoria"
                required
              >

                <option
                  v-for="categoria in categorias"
                  :key="categoria.id"
                  :value="categoria.id"
                >
                  {{ categoria.nombre }}
                </option>

              </select>

            </div>


            <div class="field">

              <label>
                Ubicación
              </label>

              <input
                v-model="form.ubicacion"
                type="text"
                required
              />

            </div>


            <div class="field">

              <label>
                Equipo afectado
              </label>

              <input
                v-model="form.equipo_afectado"
                type="text"
                required
              />

            </div>


            <div class="field full">

              <label>
                Descripción de evidencia
              </label>

              <input
                v-model="form.evidencia"
                type="text"
              />

            </div>

          </div>


          <p
            v-if="mensajeModal"
            class="modal-error"
          >
            {{ mensajeModal }}
          </p>


          <div class="modal-footer">

            <button
              type="button"
              class="secondary"
              @click="cerrarEditar"
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
                  : 'Guardar cambios'
              }}
            </button>

          </div>

        </form>

      </div>

    </div>

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
  useRouter,
  useRoute
} from 'vue-router'

import SolicitanteMenu
  from '../components/SolicitanteMenu.vue'


const router =
  useRouter()

const route =
  useRoute()


// ==========================================================
// DATOS
// ==========================================================

const soporte =
  ref([])

const mantenimiento =
  ref([])

const areas =
  ref([])

const categorias =
  ref([])


// ==========================================================
// ESTADO INTERFAZ
// ==========================================================

const cargando =
  ref(true)

const guardando =
  ref(false)

const mostrarCrear =
  ref(false)

const busqueda =
  ref('')

const filtroProceso =
  ref(
    typeof route.query.proceso === 'string'
      ? route.query.proceso
      : ''
  )

const filtroEstado =
  ref(
    typeof route.query.estado === 'string'
      ? route.query.estado
      : ''
  )

const mensaje =
  ref('')

const mensajeModal =
  ref('')

const esError =
  ref(false)

const mostrarDetalle =
  ref(false)

const mostrarEditar =
  ref(false)

const solicitudSeleccionada =
  ref(null)


// ==========================================================
// FORMULARIO SOPORTE
// ==========================================================

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


// ==========================================================
// TOKEN
// ==========================================================

const token = () =>
  localStorage.getItem(
    'sigta_token'
  )


const authHeaders = () => ({

  'Content-Type':
    'application/json',

  Accept:
    'application/json',

  Authorization:
    `Token ${token()}`,
})


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


    await cargarCatalogos()

    await cargarTodo()

    if (route.query.id && route.query.proceso) {
      const item = solicitudes.value.find(solicitud =>
        solicitud.proceso === route.query.proceso
        && Number(solicitud.id) === Number(route.query.id)
      )
      if (item) verDetalle(item)
    }
  }
)


// ==========================================================
// NORMALIZAR
// ==========================================================

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


// ==========================================================
// FETCH LISTA
// ==========================================================

async function cargarLista(
  url
) {

  const respuesta =
    await fetch(
      url,
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

    throw new Error(
      'Sesión no autorizada.'
    )
  }


  if (!respuesta.ok) {

    throw new Error(
      `Error ${respuesta.status}`
    )
  }


  return convertirLista(
    await respuesta.json()
  )
}


// ==========================================================
// CARGAR TODO
// ==========================================================

async function cargarTodo() {

  cargando.value =
    true


  try {

    const [
      soporteData,
      mantenimientoData
    ] =
      await Promise.all([

        cargarLista(
          '/api/soporte/tickets/'
        ),

        cargarLista(
          '/api/mantenimiento/requerimientos/'
        ),
      ])


    soporte.value =
      soporteData


    mantenimiento.value =
      mantenimientoData


  } catch (error) {

    console.error(
      'Error cargando solicitudes:',
      error
    )


    mostrarMensaje(
      'No fue posible cargar todos sus requerimientos.',
      true
    )


  } finally {

    cargando.value =
      false
  }
}


// ==========================================================
// SOLICITUDES UNIFICADAS
// ==========================================================

const solicitudes =
  computed(() => {

    const st =
      soporte.value.map(
        item => ({

          ...item,

          proceso:
            'SOPORTE',

          modulo:
            'Soporte Técnico',

          detalle_tipo:
            item.categoria_nombre
            || 'Soporte Técnico',

          estado_codigo:
            item.estado_codigo
            || item.estado,

          estado_nombre:
            item.estado_nombre
            || item.estado_codigo
            || item.estado,

          fecha:
            item.creado_en
            || item.fecha_creacion
            || item.created_at
            || null,
        })
      )


    const mt =
      mantenimiento.value.map(
        item => ({

          ...item,

          proceso:
            'MANTENIMIENTO',

          modulo:
            'Mantenimiento',

          detalle_tipo:
            item.tipo_nombre
            || item.tipo
            || 'Mantenimiento',

          estado_codigo:
            item.estado_codigo
            || item.estado,

          estado_nombre:
            item.estado_nombre
            || item.estado_codigo
            || item.estado,

          fecha:
            item.creado_en
            || item.created_at
            || null,
        })
      )


    return [
      ...st,
      ...mt
    ]
      .sort(
        (a, b) => {

          const fechaA =
            new Date(
              a.fecha
              || 0
            ).getTime()

          const fechaB =
            new Date(
              b.fecha
              || 0
            ).getTime()


          if (
            fechaA
            &&
            fechaB
          ) {

            return (
              fechaB
              -
              fechaA
            )
          }


          return (
            Number(b.id || 0)
            -
            Number(a.id || 0)
          )
        }
      )
  })


// ==========================================================
// FILTROS
// ==========================================================

const solicitudesFiltradas =
  computed(() => {

    const texto =
      busqueda.value
        .toLowerCase()
        .trim()


    return solicitudes.value.filter(
      item => {

        const textoGeneral =
          [
            item.codigo,
            item.titulo,
            item.descripcion,
            item.ubicacion,
            item.modulo,
            item.detalle_tipo,
            item.area_nombre,
          ]
            .filter(Boolean)
            .join(' ')
            .toLowerCase()


        const coincideBusqueda =
          !texto
          ||
          textoGeneral.includes(
            texto
          )


        const coincideProceso =
          !filtroProceso.value
          ||
          item.proceso
          === filtroProceso.value


        const coincideEstado =
          !filtroEstado.value
          ||
          bucketEstado(
            item.estado_codigo
          )
          === filtroEstado.value


        return (
          coincideBusqueda
          &&
          coincideProceso
          &&
          coincideEstado
        )
      }
    )
  })


// ==========================================================
// ESTADOS DISPONIBLES (BUCKETS SIMPLIFICADOS)
// ==========================================================
//
// El solicitante no necesita ver los estados internos
// granulares del workflow (Asignado, En verificación,
// Derivado al auxiliar, etc.). Se agrupan en 3 buckets.
// ==========================================================

const estadosDisponibles = [

  { valor: 'PENDIENTES', etiqueta: 'Pendientes' },

  { valor: 'EN_PROCESO', etiqueta: 'En proceso' },

  { valor: 'POR_VALIDAR', etiqueta: 'Por validar' },

  { valor: 'FINALIZADAS', etiqueta: 'Finalizadas' },

  { valor: 'CANCELADAS', etiqueta: 'Canceladas / rechazadas' },
]


function bucketEstado(
  codigo
) {

  const estado =
    String(
      codigo
      || ''
    )
      .toUpperCase()
      .replaceAll(
        ' ',
        '_'
      )


  if (
    estado === 'PENDIENTE_CONFORMIDAD'
    ||
    estado === 'EN_VERIFICACION'
  ) {
    return 'POR_VALIDAR'
  }

  if (
    estado.includes(
      'ANUL'
    )
    ||
    estado.includes(
      'RECHAZ'
    )
  ) {

    return 'CANCELADAS'
  }


  if (
    estado === 'CERRADO'
    ||
    estado === 'RESUELTO'
    ||
    estado === 'FINALIZADO'
  ) {

    return 'FINALIZADAS'
  }

  if (['BORRADOR', 'NUEVO', 'RECIBIDO'].includes(estado)) {
    return 'PENDIENTES'
  }


  return 'EN_PROCESO'
}


// ==========================================================
// CLASE PROCESO
// ==========================================================

function claseProceso(
  proceso
) {

  if (
    proceso ===
    'SOPORTE'
  ) {

    return 'support'
  }


  if (
    proceso ===
    'MANTENIMIENTO'
  ) {

    return 'maintenance'
  }


  return 'generic'
}


// ==========================================================
// VER DETALLE
// ==========================================================

function verDetalle(
  item
) {

  solicitudSeleccionada.value =
    item


  mostrarDetalle.value =
    true
}


function cerrarDetalle() {

  mostrarDetalle.value =
    false


  solicitudSeleccionada.value =
    null
}


// ==========================================================
// CATÁLOGOS SOPORTE
// ==========================================================

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
            headers: {

              Authorization:
                `Token ${token()}`,

              Accept:
                'application/json',
            }
          }
        ),

        fetch(
          '/api/soporte/categorias/',
          {
            headers: {

              Authorization:
                `Token ${token()}`,

              Accept:
                'application/json',
            }
          }
        ),
      ])


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


    if (
      areasRespuesta.ok
    ) {

      areas.value =
        convertirLista(
          await areasRespuesta.json()
        )
    }


    if (
      categoriasRespuesta.ok
    ) {

      categorias.value =
        convertirLista(
          await categoriasRespuesta.json()
        )
    }


  } catch (error) {

    console.error(
      'Error cargando catálogos:',
      error
    )
  }
}


// ==========================================================
// SOPORTE - EDITAR
// ==========================================================

function puedeEditarSoporte(
  item
) {

  if (
    !item
    ||
    item.proceso !==
    'SOPORTE'
  ) {

    return false
  }


  return [
    'BORRADOR',
    'NUEVO'
  ].includes(
    item.estado_codigo
  )
}

function pasosSolicitud(item) {
  const grupo = bucketEstado(item?.estado_codigo)
  const indiceActual = { PENDIENTES: 1, EN_PROCESO: 2, POR_VALIDAR: 3, FINALIZADAS: 4, CANCELADAS: 1 }[grupo] || 1
  const nombres = ['Creada', 'Recibida por jefatura', 'Técnico asignado', 'Validación del usuario', 'Cerrada']
  return nombres.map((nombre, indice) => ({
    nombre,
    completado: grupo === 'FINALIZADAS' || indice < indiceActual,
    actual: grupo !== 'FINALIZADAS' && indice === indiceActual,
  }))
}

function puedeCancelar(item) {
  if (!item) return false
  if (item.proceso === 'SOPORTE') return ['BORRADOR', 'NUEVO'].includes(item.estado_codigo)
  if (item.proceso === 'MANTENIMIENTO') return item.estado_codigo === 'RECIBIDO'
  return false
}


async function abrirEditarSoporte(
  item
) {

  if (
    areas.value.length === 0
    ||
    categorias.value.length === 0
  ) {

    await cargarCatalogos()
  }


  solicitudSeleccionada.value =
    item


  form.titulo =
    item.titulo
    || ''


  form.descripcion =
    item.descripcion
    || ''


  form.area =
    obtenerId(
      item.area
    )


  form.categoria =
    obtenerId(
      item.categoria
    )


  form.ubicacion =
    item.ubicacion
    || ''


  form.equipo_afectado =
    item.equipo_afectado
    || ''


  form.evidencia =
    item.evidencia
    || ''


  mensajeModal.value =
    ''


  mostrarEditar.value =
    true
}


function editarDesdeDetalle() {

  const item =
    solicitudSeleccionada.value


  mostrarDetalle.value =
    false


  abrirEditarSoporte(
    item
  )
}


function obtenerId(
  valor
) {

  if (
    typeof valor ===
    'number'
  ) {

    return valor
  }


  if (
    typeof valor ===
    'string'
    &&
    valor !== ''
  ) {

    const numero =
      Number(
        valor
      )


    return Number.isNaN(
      numero
    )
      ? ''
      : numero
  }


  if (
    valor
    &&
    typeof valor ===
    'object'
    &&
    valor.id
  ) {

    return Number(
      valor.id
    )
  }


  return ''
}


function cerrarEditar() {

  mostrarEditar.value =
    false


  mensajeModal.value =
    ''


  solicitudSeleccionada.value =
    null


  limpiarFormulario()
}


function limpiarFormulario() {

  form.titulo = ''

  form.descripcion = ''

  form.area = ''

  form.categoria = ''

  form.ubicacion = ''

  form.equipo_afectado = ''

  form.evidencia = ''
}


async function guardarEdicionSoporte() {

  mensajeModal.value =
    ''


  if (
    !form.area
  ) {

    mensajeModal.value =
      'Debe seleccionar un área.'

    return
  }


  if (
    !form.categoria
  ) {

    mensajeModal.value =
      'Debe seleccionar una categoría.'

    return
  }


  if (
    !solicitudSeleccionada.value
  ) {

    mensajeModal.value =
      'No existe una solicitud seleccionada.'

    return
  }


  guardando.value =
    true


  try {

    const respuesta =
      await fetch(
        `/api/soporte/tickets/${solicitudSeleccionada.value.id}/`,
        {

          method:
            'PATCH',

          headers:
            authHeaders(),

          body:
            JSON.stringify({

              titulo:
                form.titulo.trim(),

              descripcion:
                form.descripcion.trim(),

              area:
                Number(
                  form.area
                ),

              categoria:
                Number(
                  form.categoria
                ),

              ubicacion:
                form.ubicacion.trim(),

              equipo_afectado:
                form.equipo_afectado.trim(),

              evidencia:
                form.evidencia.trim(),
            })
        }
      )


    let datos = {}


    try {

      datos =
        await respuesta.json()

    } catch {

      datos = {}
    }


    if (!respuesta.ok) {

      mensajeModal.value =
        obtenerMensajeError(
          datos
        )


      return
    }


    cerrarEditar()


    mostrarMensaje(
      'Solicitud de soporte actualizada correctamente.'
    )


    await cargarTodo()


  } catch (error) {

    console.error(
      'Error modificando soporte:',
      error
    )


    mensajeModal.value =
      'No fue posible comunicarse con el servidor.'


  } finally {

    guardando.value =
      false
  }
}


// ==========================================================
// SOPORTE - ANULAR
// ==========================================================

async function anularSolicitud(
  item
) {

  const confirmar =
    window.confirm(
      `¿Confirma la cancelación de ${item.codigo}? Esta acción quedará en el historial.`
    )


  if (!confirmar) {

    return
  }


  try {

    const endpoint = item.proceso === 'MANTENIMIENTO'
      ? `/api/mantenimiento/requerimientos/${item.id}/`
      : `/api/soporte/tickets/${item.id}/`

    const respuesta =
      await fetch(
        endpoint,
        {

          method:
            'DELETE',

          headers:
            authHeaders(),
        }
      )


    let datos = {}


    try {

      datos =
        await respuesta.json()

    } catch {

      datos = {}
    }


    if (!respuesta.ok) {

      mostrarMensaje(
        datos.detalle
        ||
        'No se pudo cancelar la solicitud.',
        true
      )


      return
    }


    mostrarMensaje(
      'Solicitud cancelada correctamente.'
    )


    await cargarTodo()


  } catch (error) {

    console.error(
      'Error cancelando solicitud:',
      error
    )


    mostrarMensaje(
      'No fue posible cancelar la solicitud.',
      true
    )
  }
}


// ==========================================================
// INFORMAR CONFORMIDAD (CIERRE DEL TICKET)
// ==========================================================

/* =========================================================
   VERIFICAR FUNCIONAMIENTO

   BPMN de Soporte Técnico, Fase 6: tras la intervención del
   técnico, es el usuario solicitante quien verifica el equipo
   y decide si el problema quedó resuelto. Si responde que no,
   el ticket vuelve al técnico para una nueva reparación.
========================================================= */

async function verificarFuncionamiento(item, funciona) {

  if (
    !window.confirm(
      funciona
        ? `¿Confirma que ${item.codigo} quedó funcionando correctamente?`
        : `¿Confirma que ${item.codigo} sigue presentando el problema? Volverá al técnico.`
    )
  ) {
    return
  }

  try {

    const respuesta = await fetch(
      `/api/soporte/tickets/${item.id}/verificar-funcionamiento/`,
      {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          funciona_correctamente: funciona,
        }),
      }
    )

    let datos = {}

    try {
      datos = await respuesta.json()
    } catch {
      datos = {}
    }

    if (!respuesta.ok) {

      mostrarMensaje(
        datos.detalle || 'No fue posible registrar la verificación.',
        true
      )

      return
    }

    mostrarMensaje(
      funciona
        ? 'Verificación registrada. Confirme ahora su conformidad para cerrar el ticket.'
        : 'El ticket volvió al técnico para una nueva revisión.'
    )

    await cargarTodo()

  } catch (error) {

    console.error('Error verificando funcionamiento:', error)

    mostrarMensaje(
      'No fue posible registrar la verificación.',
      true
    )
  }
}


async function informarConformidad(
  item,
  conforme
) {

  let observaciones = ''

  if (!conforme) {

    observaciones = window.prompt(
      'Indique por qué no está conforme con la solución:'
    ) || ''

    if (!observaciones.trim()) {
      return
    }

  } else if (
    !window.confirm(
      `¿Confirma que está conforme con la solución de ${item.codigo}? El ticket se cerrará.`
    )
  ) {

    return
  }

  try {

    const respuesta = await fetch(
      `/api/soporte/tickets/${item.id}/informar-conformidad/`,
      {
        method: 'POST',
        headers: authHeaders(),
        body: JSON.stringify({
          conformidad: conforme,
          observaciones: observaciones.trim(),
        }),
      }
    )

    let datos = {}

    try {
      datos = await respuesta.json()
    } catch {
      datos = {}
    }

    if (!respuesta.ok) {
      mostrarMensaje(
        datos.detalle || 'No fue posible registrar la conformidad.',
        true
      )
      return
    }

    mostrarMensaje(
      conforme
        ? 'Conformidad registrada. El ticket fue cerrado.'
        : 'No conformidad registrada. El ticket volvió a ejecución.'
    )

    await cargarTodo()

  } catch (error) {

    console.error('Error informando conformidad:', error)

    mostrarMensaje(
      'No fue posible registrar la conformidad.',
      true
    )
  }
}


// ==========================================================
// MENSAJE BACKEND
// ==========================================================

function obtenerMensajeError(
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
            Array.isArray(
              valor
            )
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
    'No fue posible modificar la solicitud.'
  )
}


// ==========================================================
// MENSAJES
// ==========================================================

function mostrarMensaje(
  texto,
  error = false
) {

  mensaje.value =
    texto


  esError.value =
    error


  setTimeout(
    () => {

      mensaje.value =
        ''

    },
    3500
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
        dateStyle:
          'short',

        timeStyle:
          'short',
      }
    )

  } catch {

    return ''
  }
}


// ==========================================================
// ESTADO
// ==========================================================

function claseEstado(
  codigo
) {

  const estado =
    String(
      codigo
      || ''
    )
      .toUpperCase()
      .replaceAll(
        ' ',
        '_'
      )


  if (
    estado.includes(
      'ANUL'
    )
    ||
    estado.includes(
      'RECHAZ'
    )
  ) {

    return 'cancelled'
  }


  if (
    estado === 'CERRADO'
    ||
    estado === 'RESUELTO'
    ||
    estado === 'FINALIZADO'
  ) {

    return 'closed'
  }


  if (
    estado === 'NUEVO'
    ||
    estado === 'BORRADOR'
    ||
    estado === 'RECIBIDO'
  ) {

    return 'new'
  }


  return 'working'
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


/* ============================================
   LAYOUT
============================================ */

.layout {
  min-height: 100vh;
  display: flex;
  background: #eef3f8;
  font-family: Arial, Helvetica, sans-serif;
}


.content {
  flex: 1;
  min-width: 0;
  padding: 27px 30px 45px;
  overflow-x: hidden;
}


/* ============================================
   TOPBAR
============================================ */

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
  color: #71818f;
  font-size: 17px;
}


.btn-new {
  min-height: 41px;
  padding: 0 15px;
  border: none;
  border-radius: 7px;
  background: #f2c400;
  color: #17324a;
  font-size: 15px;
  font-weight: 900;
  cursor: pointer;
}


/* ============================================
   RESUMEN
============================================ */

.summary {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 13px;
  margin-bottom: 17px;
}


.summary article {
  min-height: 104px;
  padding: 16px;
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
  color: #738391;
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
}


.summary strong {
  display: block;
  margin: 7px 0 4px;
  color: #073b6f;
  font-size: 31px;
}


.summary small {
  color: #8996a1;
  font-size: 14px;
}


/* ============================================
   FILTROS
============================================ */

.filters-card {
  display: grid;
  grid-template-columns: 1fr 200px 220px;
  gap: 12px;
  margin-bottom: 16px;
  padding: 15px;
  border-radius: 9px;
  background: white;
  box-shadow: 0 3px 12px rgba(0,0,0,.04);
}


.search,
.filter {
  display: flex;
  flex-direction: column;
  gap: 5px;
}


.filters-card label {
  color: #536575;
  font-size: 14px;
  font-weight: 800;
}


.filters-card input,
.filters-card select {
  width: 100%;
  height: 40px;
  padding: 0 11px;
  border: 1px solid #d0dae2;
  border-radius: 6px;
  background: white;
  color: #344b5e;
  font-family: inherit;
  font-size: 15px;
  outline: none;
}


/* ============================================
   LISTADO
============================================ */

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
  grid-template-columns: 145px 1fr;
  gap: 15px;
}


.request-code {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}


.process-indicator {
  width: 7px;
  height: 38px;
  flex-shrink: 0;
  border-radius: 10px;
  background: #8193a2;
}


.process-indicator.support {
  background: #07518d;
}


.process-indicator.maintenance {
  background: #d76b12;
}


.request-code strong,
.request-code small {
  display: block;
}


.request-code strong {
  color: #07518d;
  font-size: 15px;
}


.request-code small {
  margin-top: 4px;
  color: #81909c;
  font-size: 13px;
}


.request-info h3 {
  margin: 0 0 5px;
  color: #29475e;
  font-size: 18px;
}


.request-info p {
  max-width: 700px;
  margin: 0 0 8px;
  overflow: hidden;
  color: #73818c;
  font-size: 15px;
  text-overflow: ellipsis;
  white-space: nowrap;
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


/* ============================================
   ESTADO
============================================ */

.status {
  display: inline-block;
  padding: 5px 8px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 800;
}


.status.new {
  background: #eaf3fb;
  color: #07518d;
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


/* ============================================
   ACCIONES
============================================ */

.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 5px;
}


.actions button {
  padding: 6px 8px;
  border: none;
  border-radius: 5px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}


.actions .view {
  background: #edf3f8;
  color: #435a6e;
}


.actions .edit {
  background: #e8f2fa;
  color: #07518d;
}


.actions .cancel {
  background: #fdecec;
  color: #a92d2d;
}


/* ============================================
   VACÍO
============================================ */

.empty {
  padding: 45px 20px;
  text-align: center;
  color: #798793;
  font-size: 15px;
}


.empty h3 {
  color: #314c61;
  font-size: 18px;
}


.empty p {
  max-width: 470px;
  margin: 6px auto 14px;
  line-height: 1.5;
}


.empty button {
  padding: 9px 13px;
  border: none;
  border-radius: 6px;
  background: #073b6f;
  color: white;
  font-size: 14px;
  cursor: pointer;
}


/* ============================================
   ALERTA
============================================ */

.alert {
  margin-bottom: 14px;
  padding: 10px 12px;
  border-radius: 7px;
  font-size: 15px;
}


.alert.success {
  background: #eaf7ef;
  color: #227443;
}


.alert.error {
  background: #fdecec;
  color: #a53232;
}


/* ============================================
   MODAL
============================================ */

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
  border-top: 4px solid #f2c400;
  border-radius: 12px;
  background: white;
  box-shadow: 0 20px 60px rgba(0,0,0,.25);
}


.detail-modal {
  max-width: 740px;
}


.modal-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 15px;
}


.modal-header h2 {
  margin: 3px 0;
  color: #17324a;
  font-size: 25px;
}


.modal-header p {
  margin: 4px 0 0;
  color: #778792;
  font-size: 15px;
}


.modal-code {
  color: #07518d;
  font-size: 14px;
  font-weight: 800;
}


.close {
  border: none;
  background: transparent;
  color: #687988;
  font-size: 33px;
  cursor: pointer;
}


.detail-status {
  margin-bottom: 16px;
}

.create-panel {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin: -4px 0 20px;
}

.create-panel button {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border: 1px solid #dbe4eb;
  border-radius: 12px;
  background: white;
  color: #17324a;
  text-align: left;
  cursor: pointer;
}

.create-panel button:hover {
  border-color: #f2c400;
  box-shadow: 0 7px 18px rgba(23, 50, 74, .1);
  transform: translateY(-1px);
}

.create-panel button > span {
  font-size: 28px;
}

.create-panel strong,
.create-panel small {
  display: block;
}

.create-panel small {
  margin-top: 4px;
  color: #71818f;
}

@media (max-width: 760px) {
  .create-panel { grid-template-columns: 1fr; }
}

.timeline { display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin:4px 0 22px; }
.timeline-step { position:relative;text-align:center;color:#8a98a5; }
.timeline-step::before { content:'';position:absolute;top:14px;left:-50%;width:100%;height:3px;background:#dce4ea; }
.timeline-step:first-child::before { display:none; }
.timeline-step span { position:relative;z-index:1;display:grid;place-items:center;width:30px;height:30px;margin:auto auto 7px;border-radius:50%;background:#e4eaf0;font-weight:800; }
.timeline-step small { font-size:10px; }
.timeline-step.completado span,.timeline-step.actual span { background:#0d5c91;color:white; }
.timeline-step.completado::before,.timeline-step.actual::before { background:#0d5c91; }
.timeline-step.actual small { color:#17324a;font-weight:800; }


.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}


.detail-grid > div {
  padding: 11px;
  border-radius: 7px;
  background: #f7f9fa;
}


.detail-grid .full {
  grid-column: 1 / -1;
}


.detail-grid label {
  color: #72818d;
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
}


.detail-grid p {
  margin: 5px 0 0;
  color: #354d60;
  font-size: 15px;
  line-height: 1.5;
}


.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 13px;
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
  color: #344a5d;
  font-size: 15px;
  font-weight: 700;
}


.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 10px 11px;
  border: 1px solid #ccd6de;
  border-radius: 7px;
  font-family: inherit;
  font-size: 15px;
  outline: none;
}


.field textarea {
  min-height: 105px;
  resize: vertical;
}


.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 18px;
}


.modal-footer button {
  min-height: 38px;
  padding: 0 14px;
  border-radius: 7px;
  font-size: 14px;
  font-weight: 700;
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


.modal-error {
  padding: 9px;
  border-radius: 6px;
  background: #fdecec;
  color: #a53232;
  font-size: 15px;
}


/* ============================================
   RESPONSIVE
============================================ */

@media (max-width: 1000px) {

  .summary {
    grid-template-columns: repeat(2,1fr);
  }


  .filters-card {
    grid-template-columns: 1fr 1fr;
  }


  .search {
    grid-column: 1 / -1;
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


  .filters-card {
    grid-template-columns: 1fr;
  }


  .search {
    grid-column: auto;
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


  .actions {
    justify-content: flex-start;
  }


  .request-info p {
    white-space: normal;
  }


  .detail-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }


  .detail-grid .full,
  .field.full {
    grid-column: auto;
  }

}


@media (max-width: 480px) {

  .summary {
    grid-template-columns: 1fr;
  }


  .modal {
    padding: 18px;
  }

}

</style>
