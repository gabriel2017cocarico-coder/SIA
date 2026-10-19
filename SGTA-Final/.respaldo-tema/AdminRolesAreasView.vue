<template>

  <div class="layout">

    <!-- =====================================================
         MENÚ ADMIN ÚNICO
    ====================================================== -->

    <SuperuserMenu />


    <!-- =====================================================
         CONTENIDO
    ====================================================== -->

    <main class="content">

      <!-- =================================================
           ENCABEZADO
      ================================================== -->

      <header class="page-header">

        <div>

          <h1>
            Roles, permisos y áreas
          </h1>

          <p>
            Administre la estructura organizacional
            y determine qué puede visualizar y ejecutar
            cada rol dentro de SIGTA.
          </p>

        </div>

      </header>


      <!-- =================================================
           MENSAJES
      ================================================== -->

      <div
        v-if="mensaje"
        :class="[
          'message',
          mensajeError
            ? 'error'
            : 'success'
        ]"
      >
        {{ mensaje }}
      </div>


      <!-- =================================================
           RESUMEN
      ================================================== -->

      <section class="summary-grid">

        <article class="summary-card">

          <span>
            Roles
          </span>

          <strong>
            {{ roles.length }}
          </strong>

          <small>
            Registrados en SIGTA
          </small>

        </article>


        <article class="summary-card">

          <span>
            Permisos
          </span>

          <strong>
            {{ permisos.length }}
          </strong>

          <small>
            Acciones controladas
          </small>

        </article>


        <article class="summary-card">

          <span>
            Áreas
          </span>

          <strong>
            {{ areas.length }}
          </strong>

          <small>
            Áreas institucionales
          </small>

        </article>


        <article class="summary-card">

          <span>
            Roles activos
          </span>

          <strong>
            {{ rolesActivos }}
          </strong>

          <small>
            Disponibles para usuarios
          </small>

        </article>

      </section>


      <!-- =================================================
           PESTAÑAS
      ================================================== -->

      <section class="tabs">

        <button
          :class="{
            active: pestaña === 'roles'
          }"
          @click="pestaña = 'roles'"
        >
          Roles
        </button>


        <button
          :class="{
            active: pestaña === 'permisos'
          }"
          @click="pestaña = 'permisos'"
        >
          Permisos
        </button>


        <button
          :class="{
            active: pestaña === 'areas'
          }"
          @click="pestaña = 'areas'"
        >
          Áreas
        </button>

      </section>


      <!-- =================================================
           CARGANDO
      ================================================== -->

      <div
        v-if="cargando"
        class="loading"
      >
        Cargando configuración...
      </div>


      <!-- =================================================
           PESTAÑA ROLES
      ================================================== -->

      <section
        v-else-if="pestaña === 'roles'"
        class="panel"
      >

        <div class="panel-header">

          <div>

            <span class="section-label">
              CONTROL DE ACCESO
            </span>

            <h2>
              Roles del sistema
            </h2>

            <p>
              Cada usuario recibe uno o más roles.
              Los permisos se asignan al rol,
              no directamente a cada usuario.
            </p>

          </div>


          <button
            class="yellow-button"
            @click="nuevoRol"
          >
            + Nuevo rol
          </button>

        </div>


        <div class="role-grid">

          <article
            v-for="rol in roles"
            :key="rol.id"
            class="role-card"
          >

            <div class="role-card-header">

              <div>

                <span class="role-code">
                  {{ rol.codigo }}
                </span>

                <h3>
                  {{ rol.nombre }}
                </h3>

              </div>


              <span
                :class="[
                  'status-badge',
                  rol.activo
                    ? 'active'
                    : 'inactive'
                ]"
              >
                {{
                  rol.activo
                    ? 'Activo'
                    : 'Inactivo'
                }}
              </span>

            </div>


            <p class="role-description">
              {{
                rol.descripcion
                ||
                'Sin descripción registrada.'
              }}
            </p>


            <div class="role-info">

              <div>

                <span>
                  Tipo
                </span>

                <strong>
                  {{
                    rol.es_global
                      ? 'Global'
                      : 'Por área'
                  }}
                </strong>

              </div>


              <div>

                <span>
                  Permisos
                </span>

                <strong>
                  {{
                    rol.cantidad_permisos
                    ??
                    cantidadPermisosRol(
                      rol.id
                    )
                  }}
                </strong>

              </div>

            </div>


            <div class="role-actions">

              <button
                class="secondary-button"
                @click="editarRol(rol)"
              >
                Editar
              </button>


              <button
                class="blue-button"
                @click="
                  abrirPermisosRol(
                    rol
                  )
                "
              >
                Administrar permisos
              </button>

            </div>

          </article>


          <div
            v-if="roles.length === 0"
            class="empty"
          >
            No existen roles registrados.
          </div>

        </div>

      </section>


      <!-- =================================================
           PESTAÑA PERMISOS
      ================================================== -->

      <section
        v-else-if="pestaña === 'permisos'"
        class="panel"
      >

        <div class="panel-header">

          <div>

            <span class="section-label">
              MATRIZ DE PERMISOS
            </span>

            <h2>
              Permisos de SIGTA
            </h2>

            <p>
              Los nombres de las acciones están alineados
              con las actividades de los procesos.
            </p>

          </div>

        </div>


        <!-- BUSCADOR -->

        <div class="permission-filters">

          <input
            v-model="buscarPermiso"
            placeholder="Buscar permiso por nombre o código..."
          />


          <select
            v-model="filtroModulo"
          >

            <option value="">
              Todos los módulos
            </option>

            <option value="GENERAL">
              General
            </option>

            <option value="AUTOSERVICIO">
              Portal Solicitante
            </option>

            <option value="SOPORTE">
              Soporte Técnico
            </option>

            <option value="MANTENIMIENTO">
              Mantenimiento
            </option>

            <option value="COMPRAS">
              Compras
            </option>

            <option value="ADMINISTRACION">
              Administración
            </option>

            <option value="AUDITORIA">
              Auditoría
            </option>

            <option value="CONFIGURACION">
              Configuración
            </option>

          </select>

        </div>


        <!-- PERMISOS AGRUPADOS -->

        <div
          v-for="grupo in permisosAgrupados"
          :key="grupo.modulo"
          class="permission-group"
        >

          <div class="permission-group-header">

            <div>

              <span>
                MÓDULO
              </span>

              <h3>
                {{ grupo.nombre }}
              </h3>

            </div>


            <strong>
              {{ grupo.permisos.length }}
            </strong>

          </div>


          <div class="permission-list">

            <article
              v-for="permiso in grupo.permisos"
              :key="permiso.id"
              class="permission-row"
            >

              <div>

                <strong>
                  {{ permiso.nombre }}
                </strong>

                <span class="permission-code">
                  {{ permiso.codigo }}
                </span>

                <p>
                  {{
                    permiso.descripcion
                    ||
                    'Sin descripción.'
                  }}
                </p>

              </div>


              <span
                :class="[
                  'status-badge',
                  permiso.activo
                    ? 'active'
                    : 'inactive'
                ]"
              >
                {{
                  permiso.activo
                    ? 'Activo'
                    : 'Inactivo'
                }}
              </span>

            </article>

          </div>

        </div>


        <div
          v-if="permisosFiltrados.length === 0"
          class="empty"
        >
          No se encontraron permisos.
        </div>

      </section>


      <!-- =================================================
           PESTAÑA ÁREAS
      ================================================== -->

      <section
        v-else
        class="panel"
      >

        <div class="panel-header">

          <div>

            <span class="section-label">
              ESTRUCTURA ORGANIZACIONAL
            </span>

            <h2>
              Áreas institucionales
            </h2>

            <p>
              Las áreas permiten identificar la unidad
              organizacional a la que pertenece cada usuario.
            </p>

          </div>


          <button
            class="yellow-button"
            @click="nuevaArea"
          >
            + Nueva área
          </button>

        </div>


        <div class="area-table">

          <div class="area-header">

            <span>
              Código
            </span>

            <span>
              Área
            </span>

            <span>
              Descripción
            </span>

            <span>
              Estado
            </span>

            <span>
              Acción
            </span>

          </div>


          <div
            v-for="area in areas"
            :key="area.id"
            class="area-row"
          >

            <strong>
              {{ area.codigo }}
            </strong>


            <span>
              {{ area.nombre }}
            </span>


            <span>
              {{
                area.descripcion
                ||
                '-'
              }}
            </span>


            <span>

              <span
                :class="[
                  'status-badge',
                  area.activo
                    ? 'active'
                    : 'inactive'
                ]"
              >
                {{
                  area.activo
                    ? 'Activa'
                    : 'Inactiva'
                }}
              </span>

            </span>


            <span>

              <button
                class="secondary-button"
                @click="editarArea(area)"
              >
                Editar
              </button>

            </span>

          </div>


          <div
            v-if="areas.length === 0"
            class="empty"
          >
            No existen áreas registradas.
          </div>

        </div>

      </section>

    </main>


    <!-- =====================================================
         MODAL ROL
    ====================================================== -->

    <div
      v-if="modalRol"
      class="overlay"
      @click.self="cerrarModalRol"
    >

      <section class="modal">

        <div class="modal-header">

          <div>

            <span>
              CONFIGURACIÓN DEL ROL
            </span>

            <h2>
              {{
                rolId
                  ? 'Editar rol'
                  : 'Nuevo rol'
              }}
            </h2>

          </div>


          <button
            type="button"
            class="close-button"
            @click="cerrarModalRol"
          >
            ×
          </button>

        </div>


        <form
          @submit.prevent="guardarRol"
        >

          <div class="field">

            <label>
              Código
            </label>

            <input
              v-model="formRol.codigo"
              maxlength="50"
              placeholder="Ej.: JEFE_UTIC"
              required
            />

            <small>
              Utilice un código claro relacionado
              con el rol institucional.
            </small>

          </div>


          <div class="field">

            <label>
              Nombre
            </label>

            <input
              v-model="formRol.nombre"
              maxlength="100"
              placeholder="Ej.: Jefe de UTIC"
              required
            />

          </div>


          <div class="field">

            <label>
              Descripción
            </label>

            <textarea
              v-model="formRol.descripcion"
              placeholder="Describa la responsabilidad del rol..."
            ></textarea>

          </div>


          <label class="check-card">

            <input
              v-model="formRol.es_global"
              type="checkbox"
            />

            <div>

              <strong>
                Rol global
              </strong>

              <span>
                No necesita estar asociado
                a un área específica.
              </span>

            </div>

          </label>


          <label class="check-card">

            <input
              v-model="formRol.activo"
              type="checkbox"
            />

            <div>

              <strong>
                Rol activo
              </strong>

              <span>
                Podrá asignarse a usuarios.
              </span>

            </div>

          </label>


          <div class="modal-actions">

            <button
              type="button"
              class="secondary-button"
              @click="cerrarModalRol"
            >
              Cancelar
            </button>


            <button
              type="submit"
              class="primary-button"
              :disabled="guardando"
            >
              {{
                guardando
                  ? 'Guardando...'
                  : 'Guardar rol'
              }}
            </button>

          </div>

        </form>

      </section>

    </div>


    <!-- =====================================================
         MODAL ÁREA
    ====================================================== -->

    <div
      v-if="modalArea"
      class="overlay"
      @click.self="cerrarModalArea"
    >

      <section class="modal">

        <div class="modal-header">

          <div>

            <span>
              ESTRUCTURA ORGANIZACIONAL
            </span>

            <h2>
              {{
                areaId
                  ? 'Editar área'
                  : 'Nueva área'
              }}
            </h2>

          </div>


          <button
            type="button"
            class="close-button"
            @click="cerrarModalArea"
          >
            ×
          </button>

        </div>


        <form
          @submit.prevent="guardarArea"
        >

          <div class="field">

            <label>
              Código
            </label>

            <input
              v-model="formArea.codigo"
              maxlength="30"
              placeholder="Ej.: UTIC"
              required
            />

          </div>


          <div class="field">

            <label>
              Nombre
            </label>

            <input
              v-model="formArea.nombre"
              maxlength="100"
              placeholder="Ej.: Unidad de Tecnologías de Información"
              required
            />

          </div>


          <div class="field">

            <label>
              Descripción
            </label>

            <textarea
              v-model="formArea.descripcion"
              placeholder="Descripción del área..."
            ></textarea>

          </div>


          <label class="check-card">

            <input
              v-model="formArea.activo"
              type="checkbox"
            />

            <div>

              <strong>
                Área activa
              </strong>

              <span>
                Disponible para asignación
                de usuarios y requerimientos.
              </span>

            </div>

          </label>


          <div class="modal-actions">

            <button
              type="button"
              class="secondary-button"
              @click="cerrarModalArea"
            >
              Cancelar
            </button>


            <button
              type="submit"
              class="primary-button"
              :disabled="guardando"
            >
              {{
                guardando
                  ? 'Guardando...'
                  : 'Guardar área'
              }}
            </button>

          </div>

        </form>

      </section>

    </div>


    <!-- =====================================================
         MODAL PERMISOS DEL ROL
    ====================================================== -->

    <div
      v-if="modalPermisos"
      class="overlay"
      @click.self="cerrarModalPermisos"
    >

      <section class="modal permissions-modal">

        <div class="modal-header">

          <div>

            <span>
              MATRIZ DE PERMISOS
            </span>

            <h2>
              {{ rolSeleccionado?.nombre }}
            </h2>

            <p>
              {{ rolSeleccionado?.codigo }}
            </p>

          </div>


          <button
            type="button"
            class="close-button"
            @click="cerrarModalPermisos"
          >
            ×
          </button>

        </div>


        <div class="permission-warning">

          Los permisos determinan qué puede visualizar
          y ejecutar este rol dentro del sistema.

        </div>


        <div class="role-permissions-scroll">

          <section
            v-for="grupo in permisosPorModuloTodos"
            :key="grupo.modulo"
            class="role-permission-group"
          >

            <div class="role-permission-title">

              <h3>
                {{ grupo.nombre }}
              </h3>

              <span>
                {{ grupo.permisos.length }}
              </span>

            </div>


            <label
              v-for="permiso in grupo.permisos"
              :key="permiso.id"
              class="permission-checkbox"
            >

              <input
                type="checkbox"
                :checked="
                  permisoAsignado(
                    permiso.id
                  )
                "
                :disabled="
                  modificandoPermiso === permiso.id
                "
                @change="
                  cambiarPermisoRol(
                    permiso,
                    $event.target.checked
                  )
                "
              />


              <div>

                <strong>
                  {{ permiso.nombre }}
                </strong>

                <span>
                  {{ permiso.codigo }}
                </span>

                <p>
                  {{ permiso.descripcion }}
                </p>

              </div>

            </label>

          </section>

        </div>


        <div class="modal-actions">

          <button
            type="button"
            class="primary-button"
            @click="cerrarModalPermisos"
          >
            Finalizar
          </button>

        </div>

      </section>

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
  useRouter
} from 'vue-router'

import SuperuserMenu
  from '../components/SuperuserMenu.vue'


const router =
  useRouter()


/* =========================================================
   DATOS
========================================================= */

const roles =
  ref([])

const areas =
  ref([])

const permisos =
  ref([])

const rolPermisos =
  ref([])


/* =========================================================
   INTERFAZ
========================================================= */

const pestaña =
  ref('roles')

const cargando =
  ref(true)

const guardando =
  ref(false)

const mensaje =
  ref('')

const mensajeError =
  ref(false)


/* =========================================================
   MODALES
========================================================= */

const modalRol =
  ref(false)

const modalArea =
  ref(false)

const modalPermisos =
  ref(false)


const rolId =
  ref(null)

const areaId =
  ref(null)

const rolSeleccionado =
  ref(null)


/* =========================================================
   PERMISOS
========================================================= */

const buscarPermiso =
  ref('')

const filtroModulo =
  ref('')

const modificandoPermiso =
  ref(null)


/* =========================================================
   FORMULARIOS
========================================================= */

const formRol =
  reactive({

    codigo: '',

    nombre: '',

    descripcion: '',

    es_global: false,

    activo: true,
  })


const formArea =
  reactive({

    codigo: '',

    nombre: '',

    descripcion: '',

    activo: true,
  })


/* =========================================================
   TOKEN
========================================================= */

const obtenerToken = () =>
  localStorage.getItem(
    'sigta_token'
  )


function headers() {

  return {

    'Content-Type':
      'application/json',

    Accept:
      'application/json',

    Authorization:
      `Token ${obtenerToken()}`,
  }
}


/* =========================================================
   INICIO
========================================================= */

onMounted(
  async () => {

    if (
      !obtenerToken()
    ) {

      router.push(
        '/login'
      )

      return
    }


    await cargarTodo()
  }
)


/* =========================================================
   NORMALIZAR LISTAS
========================================================= */

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


/* =========================================================
   CARGAR TODO
========================================================= */

async function cargarTodo() {

  cargando.value = true


  try {

    const [
      rolesRes,
      areasRes,
      permisosRes,
      rolPermisosRes
    ] =
      await Promise.all([

        fetch(
          '/api/usuarios/roles/',
          {
            headers:
              headers()
          }
        ),

        fetch(
          '/api/usuarios/areas/',
          {
            headers:
              headers()
          }
        ),

        fetch(
          '/api/usuarios/permisos/',
          {
            headers:
              headers()
          }
        ),

        fetch(
          '/api/usuarios/rol-permisos/',
          {
            headers:
              headers()
          }
        ),

      ])


    const respuestas = [
      rolesRes,
      areasRes,
      permisosRes,
      rolPermisosRes
    ]


    if (
      respuestas.some(
        r =>
          r.status === 401
          ||
          r.status === 403
      )
    ) {

      cerrarSesion()

      return
    }


    if (
      !rolesRes.ok
      ||
      !areasRes.ok
      ||
      !permisosRes.ok
      ||
      !rolPermisosRes.ok
    ) {

      throw new Error(
        'No fue posible cargar la configuración.'
      )
    }


    roles.value =
      normalizarLista(
        await rolesRes.json()
      )


    areas.value =
      normalizarLista(
        await areasRes.json()
      )


    permisos.value =
      normalizarLista(
        await permisosRes.json()
      )


    rolPermisos.value =
      normalizarLista(
        await rolPermisosRes.json()
      )


  } catch (error) {

    console.error(
      error
    )


    mostrarMensaje(
      'No fue posible cargar roles, permisos y áreas.',
      true
    )

  } finally {

    cargando.value = false
  }
}


/* =========================================================
   CONTADORES
========================================================= */

const rolesActivos =
  computed(() => {

    return roles.value.filter(
      rol =>
        rol.activo
    ).length
  })


function cantidadPermisosRol(
  rolIdValor
) {

  return rolPermisos.value.filter(
    rp =>
      Number(
        rp.rol
      )
      ===
      Number(
        rolIdValor
      )
      &&
      rp.activo !== false
  ).length
}


/* =========================================================
   PERMISOS FILTRADOS
========================================================= */

const permisosFiltrados =
  computed(() => {

    const buscar =
      buscarPermiso.value
        .trim()
        .toLowerCase()


    return permisos.value.filter(
      permiso => {

        const coincideModulo =
          !filtroModulo.value
          ||
          permiso.modulo
          ===
          filtroModulo.value


        const coincideTexto =
          !buscar
          ||
          permiso.nombre
            ?.toLowerCase()
            .includes(
              buscar
            )
          ||
          permiso.codigo
            ?.toLowerCase()
            .includes(
              buscar
            )
          ||
          permiso.descripcion
            ?.toLowerCase()
            .includes(
              buscar
            )


        return (
          coincideModulo
          &&
          coincideTexto
        )
      }
    )
  })


/* =========================================================
   AGRUPAR PERMISOS
========================================================= */

const nombresModulo = {

  GENERAL:
    'General',

  AUTOSERVICIO:
    'Portal Solicitante',

  SOPORTE:
    'Soporte Técnico',

  MANTENIMIENTO:
    'Mantenimiento',

  COMPRAS:
    'Compras',

  ADMINISTRACION:
    'Administración',

  AUDITORIA:
    'Auditoría',

  CONFIGURACION:
    'Configuración',
}


function agruparPermisos(
  lista
) {

  const grupos = {}


  for (
    const permiso
    of lista
  ) {

    const modulo =
      permiso.modulo
      ||
      'GENERAL'


    if (
      !grupos[modulo]
    ) {

      grupos[modulo] = {
        modulo,

        nombre:
          permiso.modulo_nombre
          ||
          nombresModulo[modulo]
          ||
          modulo,

        permisos: [],
      }
    }


    grupos[modulo]
      .permisos
      .push(
        permiso
      )
  }


  return Object.values(
    grupos
  )
}


const permisosAgrupados =
  computed(() => {

    return agruparPermisos(
      permisosFiltrados.value
    )
  })


const permisosPorModuloTodos =
  computed(() => {

    return agruparPermisos(
      permisos.value.filter(
        permiso =>
          permiso.activo !== false
      )
    )
  })


/* =========================================================
   ROL
========================================================= */

function nuevoRol() {

  rolId.value = null


  Object.assign(
    formRol,
    {
      codigo: '',

      nombre: '',

      descripcion: '',

      es_global: false,

      activo: true,
    }
  )


  modalRol.value = true
}


function editarRol(
  rol
) {

  rolId.value =
    rol.id


  Object.assign(
    formRol,
    {
      codigo:
        rol.codigo
        ||
        '',

      nombre:
        rol.nombre
        ||
        '',

      descripcion:
        rol.descripcion
        ||
        '',

      es_global:
        Boolean(
          rol.es_global
        ),

      activo:
        Boolean(
          rol.activo
        ),
    }
  )


  modalRol.value = true
}


function cerrarModalRol() {

  modalRol.value = false

  rolId.value = null
}


async function guardarRol() {

  guardando.value = true


  try {

    let url =
      '/api/usuarios/roles/'


    let method =
      'POST'


    const editando =
      Boolean(
        rolId.value
      )


    if (
      editando
    ) {

      url +=
        `${rolId.value}/`

      method =
        'PATCH'
    }


    const respuesta =
      await fetch(
        url,
        {
          method,

          headers:
            headers(),

          body:
            JSON.stringify({
              codigo:
                formRol.codigo
                  .trim()
                  .toUpperCase()
                  .replace(
                    /\s+/g,
                    '_'
                  ),

              nombre:
                formRol.nombre
                  .trim(),

              descripcion:
                formRol.descripcion
                  .trim(),

              es_global:
                formRol.es_global,

              activo:
                formRol.activo,
            })
        }
      )


    const datos =
      await leerJson(
        respuesta
      )


    if (
      !respuesta.ok
    ) {

      mostrarMensaje(
        obtenerError(
          datos
        ),
        true
      )

      return
    }


    modalRol.value =
      false


    mostrarMensaje(
      editando
        ? 'Rol actualizado correctamente.'
        : 'Rol creado correctamente.'
    )


    await cargarTodo()


  } catch (error) {

    console.error(
      error
    )


    mostrarMensaje(
      'No fue posible guardar el rol.',
      true
    )

  } finally {

    guardando.value = false
  }
}


/* =========================================================
   ÁREA
========================================================= */

function nuevaArea() {

  areaId.value = null


  Object.assign(
    formArea,
    {
      codigo: '',

      nombre: '',

      descripcion: '',

      activo: true,
    }
  )


  modalArea.value = true
}


function editarArea(
  area
) {

  areaId.value =
    area.id


  Object.assign(
    formArea,
    {
      codigo:
        area.codigo
        ||
        '',

      nombre:
        area.nombre
        ||
        '',

      descripcion:
        area.descripcion
        ||
        '',

      activo:
        Boolean(
          area.activo
        ),
    }
  )


  modalArea.value = true
}


function cerrarModalArea() {

  modalArea.value = false

  areaId.value = null
}


async function guardarArea() {

  guardando.value = true


  try {

    let url =
      '/api/usuarios/areas/'


    let method =
      'POST'


    const editando =
      Boolean(
        areaId.value
      )


    if (
      editando
    ) {

      url +=
        `${areaId.value}/`

      method =
        'PATCH'
    }


    const respuesta =
      await fetch(
        url,
        {
          method,

          headers:
            headers(),

          body:
            JSON.stringify({
              codigo:
                formArea.codigo
                  .trim()
                  .toUpperCase()
                  .replace(
                    /\s+/g,
                    '_'
                  ),

              nombre:
                formArea.nombre
                  .trim(),

              descripcion:
                formArea.descripcion
                  .trim(),

              activo:
                formArea.activo,
            })
        }
      )


    const datos =
      await leerJson(
        respuesta
      )


    if (
      !respuesta.ok
    ) {

      mostrarMensaje(
        obtenerError(
          datos
        ),
        true
      )

      return
    }


    modalArea.value =
      false


    mostrarMensaje(
      editando
        ? 'Área actualizada correctamente.'
        : 'Área creada correctamente.'
    )


    await cargarTodo()


  } catch (error) {

    console.error(
      error
    )


    mostrarMensaje(
      'No fue posible guardar el área.',
      true
    )

  } finally {

    guardando.value = false
  }
}


/* =========================================================
   PERMISOS DEL ROL
========================================================= */

function abrirPermisosRol(
  rol
) {

  rolSeleccionado.value =
    rol


  modalPermisos.value =
    true
}


function cerrarModalPermisos() {

  modalPermisos.value =
    false


  rolSeleccionado.value =
    null
}


function permisoAsignado(
  permisoId
) {

  if (
    !rolSeleccionado.value
  ) {

    return false
  }


  return rolPermisos.value.some(
    rp =>

      Number(
        rp.rol
      )
      ===
      Number(
        rolSeleccionado.value.id
      )

      &&

      Number(
        rp.permiso
      )
      ===
      Number(
        permisoId
      )

      &&

      rp.activo !== false
  )
}


function encontrarAsignacion(
  permisoId
) {

  if (
    !rolSeleccionado.value
  ) {

    return null
  }


  return rolPermisos.value.find(
    rp =>

      Number(
        rp.rol
      )
      ===
      Number(
        rolSeleccionado.value.id
      )

      &&

      Number(
        rp.permiso
      )
      ===
      Number(
        permisoId
      )
  )
}


/* =========================================================
   ASIGNAR / QUITAR PERMISO
========================================================= */

async function cambiarPermisoRol(
  permiso,
  asignar
) {

  if (
    !rolSeleccionado.value
  ) {

    return
  }


  modificandoPermiso.value =
    permiso.id


  try {

    if (
      asignar
    ) {

      const respuesta =
        await fetch(
          '/api/usuarios/rol-permisos/',
          {
            method:
              'POST',

            headers:
              headers(),

            body:
              JSON.stringify({
                rol:
                  rolSeleccionado.value.id,

                permiso:
                  permiso.id,

                activo:
                  true,
              })
          }
        )


      const datos =
        await leerJson(
          respuesta
        )


      if (
        !respuesta.ok
      ) {

        throw new Error(
          obtenerError(
            datos
          )
        )
      }


      mostrarMensaje(
        `Permiso "${permiso.nombre}" asignado al rol.`
      )

    } else {

      const asignacion =
        encontrarAsignacion(
          permiso.id
        )


      if (
        !asignacion
      ) {

        return
      }


      const respuesta =
        await fetch(
          `/api/usuarios/rol-permisos/${asignacion.id}/`,
          {
            method:
              'DELETE',

            headers:
              headers(),
          }
        )


      const datos =
        await leerJson(
          respuesta
        )


      if (
        !respuesta.ok
      ) {

        throw new Error(
          obtenerError(
            datos
          )
        )
      }


      mostrarMensaje(
        `Permiso "${permiso.nombre}" retirado del rol.`
      )
    }


    await cargarTodo()


    /* Mantener actualizado rol seleccionado */

    rolSeleccionado.value =
      roles.value.find(
        rol =>
          rol.id
          ===
          rolSeleccionado.value?.id
      )
      ||
      rolSeleccionado.value


  } catch (error) {

    console.error(
      error
    )


    mostrarMensaje(
      error.message
      ||
      'No fue posible modificar el permiso.',
      true
    )


    await cargarTodo()

  } finally {

    modificandoPermiso.value =
      null
  }
}


/* =========================================================
   UTILIDADES
========================================================= */

async function leerJson(
  respuesta
) {

  try {

    return await respuesta.json()

  } catch {

    return {}
  }
}


function obtenerError(
  datos
) {

  if (
    datos.detail
  ) {

    return datos.detail
  }


  if (
    datos.detalle
  ) {

    return datos.detalle
  }


  if (
    datos.mensaje
  ) {

    return datos.mensaje
  }


  const entrada =
    Object.entries(
      datos
      ||
      {}
    )[0]


  if (
    entrada
  ) {

    const [
      campo,
      valor
    ] =
      entrada


    return (
      `${campo}: ${
        Array.isArray(
          valor
        )
          ? valor.join(', ')
          : String(valor)
      }`
    )
  }


  return (
    'Revise la información ingresada.'
  )
}


function mostrarMensaje(
  texto,
  esError = false
) {

  mensaje.value =
    texto


  mensajeError.value =
    esError


  setTimeout(
    () => {

      mensaje.value =
        ''

    },
    4000
  )
}


/* =========================================================
   SESIÓN
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

  background: #f2f5f9;

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}


.content {

  flex: 1;

  min-width: 0;

  padding: 28px;

  overflow-x: hidden;
}


/* =========================================================
   ENCABEZADO
========================================================= */

.page-header {

  margin-bottom: 22px;
}


.breadcrumb {

  display: block;

  margin-bottom: 7px;

  color: #8493a0;

  font-size: 15px;
}


.page-header h1 {

  margin: 0;

  color: #17324a;

  font-size: 28px;
}


.page-header p {

  max-width: 780px;

  margin:
    6px
    0
    0;

  color: #71818f;

  font-size: 17px;

  line-height: 1.5;
}


/* =========================================================
   MENSAJE
========================================================= */

.message {

  margin-bottom: 17px;

  padding:
    11px
    13px;

  border-radius: 7px;

  font-size: 15px;
}


.message.success {

  background: #e8f7ef;

  color: #237345;
}


.message.error {

  background: #fdecec;

  color: #a83232;
}


/* =========================================================
   RESUMEN
========================================================= */

.summary-grid {

  display: grid;

  grid-template-columns:
    repeat(4,1fr);

  gap: 14px;

  margin-bottom: 20px;
}


.summary-card {

  min-height: 110px;

  padding: 17px;

  background: white;

  border-top:
    4px solid #f2c400;

  border-radius: 9px;

  box-shadow:
    0
    3px
    12px
    rgba(0,0,0,.04);
}


.summary-card span {

  display: block;

  color: #647484;

  font-size: 14px;

  font-weight: 800;

  text-transform: uppercase;
}


.summary-card strong {

  display: block;

  margin:
    7px
    0
    5px;

  color: #073b6f;

  font-size: 25px;
}


.summary-card small {

  color: #8995a0;

  font-size: 14px;
}


/* =========================================================
   TABS
========================================================= */

.tabs {

  display: flex;

  gap: 4px;

  margin-bottom: 15px;

  padding: 5px;

  border-radius: 9px;

  background: #e8edf2;
}


.tabs button {

  min-width: 140px;

  min-height: 38px;

  padding:
    0
    15px;

  border: none;

  border-radius: 7px;

  background: transparent;

  color: #617586;

  font-size: 15px;

  font-weight: 700;

  cursor: pointer;
}


.tabs button.active {

  background: white;

  color: #073b6f;

  box-shadow:
    0
    2px
    7px
    rgba(0,0,0,.07);
}


/* =========================================================
   PANEL
========================================================= */

.panel {

  padding: 21px;

  border-top:
    4px solid #f2c400;

  border-radius: 10px;

  background: white;

  box-shadow:
    0
    4px
    14px
    rgba(0,0,0,.05);
}


.panel-header {

  display: flex;

  align-items: flex-start;

  justify-content:
    space-between;

  gap: 15px;

  margin-bottom: 20px;
}


.section-label {

  display: block;

  margin-bottom: 5px;

  color: #0b5795;

  font-size: 13px;

  font-weight: 900;

  letter-spacing: .8px;
}


.panel-header h2 {

  margin: 0;

  color: #17324a;

  font-size: 17px;
}


.panel-header p {

  margin:
    5px
    0
    0;

  color: #71818f;

  font-size: 15px;
}


/* =========================================================
   BOTONES
========================================================= */

.yellow-button,
.primary-button,
.blue-button,
.secondary-button {

  min-height: 36px;

  padding:
    0
    12px;

  border-radius: 6px;

  font-size: 14px;

  font-weight: 800;

  cursor: pointer;
}


.yellow-button {

  border: none;

  background: #f2c400;

  color: #183750;
}


.primary-button {

  border: none;

  background: #073b6f;

  color: white;
}


.blue-button {

  border: none;

  background: #e7f1f9;

  color: #07518d;
}


.secondary-button {

  border:
    1px solid #ccd6de;

  background: white;

  color: #526677;
}


.primary-button:disabled {

  opacity: .55;

  cursor: not-allowed;
}


/* =========================================================
   ROLES
========================================================= */

.role-grid {

  display: grid;

  grid-template-columns:
    repeat(3,1fr);

  gap: 13px;
}


.role-card {

  min-width: 0;

  padding: 15px;

  border:
    1px solid #dce3e9;

  border-radius: 9px;

  background: #fbfcfd;
}


.role-card-header {

  display: flex;

  align-items: flex-start;

  justify-content:
    space-between;

  gap: 10px;
}


.role-code {

  display: block;

  margin-bottom: 4px;

  color: #07518d;

  font-size: 13px;

  font-weight: 900;
}


.role-card h3 {

  margin: 0;

  color: #17324a;

  font-size: 18px;
}


.role-description {

  min-height: 42px;

  margin:
    9px
    0;

  color: #71818f;

  font-size: 14px;

  line-height: 1.45;
}


.role-info {

  display: grid;

  grid-template-columns:
    1fr
    1fr;

  gap: 8px;

  margin-bottom: 12px;

  padding:
    10px
    0;

  border-top:
    1px solid #e8edf1;

  border-bottom:
    1px solid #e8edf1;
}


.role-info span,
.role-info strong {

  display: block;
}


.role-info span {

  color: #8a97a2;

  font-size: 13px;
}


.role-info strong {

  margin-top: 3px;

  color: #29475e;

  font-size: 15px;
}


.role-actions {

  display: flex;

  justify-content:
    flex-end;

  gap: 7px;
}


/* =========================================================
   ESTADOS
========================================================= */

.status-badge {

  display: inline-block;

  padding:
    4px
    7px;

  border-radius: 14px;

  font-size: 13px;

  font-weight: 800;
}


.status-badge.active {

  background: #e8f7ef;

  color: #237345;
}


.status-badge.inactive {

  background: #fdecec;

  color: #a83232;
}


/* =========================================================
   FILTROS PERMISOS
========================================================= */

.permission-filters {

  display: grid;

  grid-template-columns:
    1fr
    250px;

  gap: 10px;

  margin-bottom: 17px;
}


.permission-filters input,
.permission-filters select {

  height: 40px;

  padding:
    0
    11px;

  border:
    1px solid #ccd6de;

  border-radius: 7px;

  background: white;

  color: #344b5e;

  font-size: 15px;

  outline: none;
}


/* =========================================================
   GRUPOS DE PERMISOS
========================================================= */

.permission-group {

  margin-bottom: 16px;

  overflow: hidden;

  border:
    1px solid #dce3e9;

  border-radius: 8px;
}


.permission-group-header {

  display: flex;

  align-items: center;

  justify-content:
    space-between;

  padding:
    12px
    14px;

  background: #eef3f7;
}


.permission-group-header span {

  display: block;

  color: #84919c;

  font-size: 13px;
}


.permission-group-header h3 {

  margin:
    3px
    0
    0;

  color: #17324a;

  font-size: 17px;
}


.permission-group-header > strong {

  width: 27px;

  height: 27px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #073b6f;

  color: white;

  font-size: 14px;
}


.permission-row {

  display: flex;

  align-items: flex-start;

  justify-content:
    space-between;

  gap: 15px;

  padding:
    13px
    14px;

  border-top:
    1px solid #edf0f2;
}


.permission-row strong {

  color: #29475e;

  font-size: 15px;
}


.permission-code {

  display: block;

  margin-top: 4px;

  color: #07518d;

  font-size: 13px;

  font-weight: 700;
}


.permission-row p {

  margin:
    5px
    0
    0;

  color: #7c8a95;

  font-size: 14px;
}


/* =========================================================
   ÁREAS
========================================================= */

.area-table {

  overflow-x: auto;
}


.area-header,
.area-row {

  display: grid;

  grid-template-columns:
    150px
    220px
    minmax(280px,1fr)
    120px
    110px;

  gap: 10px;

  align-items: center;

  min-width: 880px;
}


.area-header {

  padding:
    11px
    13px;

  background: #f4f7f9;

  color: #617586;

  font-size: 14px;

  font-weight: 800;

  text-transform: uppercase;
}


.area-row {

  padding:
    13px;

  border-top:
    1px solid #edf0f2;

  color: #526777;

  font-size: 15px;
}


.area-row > strong {

  color: #07518d;
}


/* =========================================================
   MODALES
========================================================= */

.overlay {

  position: fixed;

  inset: 0;

  z-index: 1000;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 20px;

  background:
    rgba(
      7,
      35,
      60,
      .65
    );
}


.modal {

  width: 520px;

  max-width: 100%;

  max-height: 92vh;

  overflow-y: auto;

  padding: 23px;

  border-top:
    4px solid #f2c400;

  border-radius: 11px;

  background: white;

  box-shadow:
    0
    20px
    60px
    rgba(0,0,0,.25);
}


.permissions-modal {

  width: 820px;
}


.modal-header {

  display: flex;

  align-items: flex-start;

  justify-content:
    space-between;

  gap: 12px;

  margin-bottom: 17px;
}


.modal-header > div > span {

  display: block;

  color: #0b5795;

  font-size: 13px;

  font-weight: 900;
}


.modal-header h2 {

  margin:
    4px
    0
    0;

  color: #17324a;

  font-size: 18px;
}


.modal-header p {

  margin:
    4px
    0
    0;

  color: #7c8a95;

  font-size: 14px;
}


.close-button {

  border: none;

  background: transparent;

  color: #697b89;

  font-size: 25px;

  cursor: pointer;
}


/* =========================================================
   CAMPOS
========================================================= */

.field {

  display: flex;

  flex-direction: column;

  gap: 5px;

  margin-top: 12px;
}


.field label {

  color: #344b5e;

  font-size: 15px;

  font-weight: 800;
}


.field input,
.field textarea {

  width: 100%;

  padding:
    10px
    11px;

  border:
    1px solid #ccd6de;

  border-radius: 7px;

  color: #344b5e;

  font-family: inherit;

  font-size: 15px;

  outline: none;
}


.field textarea {

  min-height: 90px;

  resize: vertical;
}


.field small {

  color: #87939d;

  font-size: 13px;
}


.check-card {

  display: flex;

  align-items:
    flex-start;

  gap: 9px;

  margin-top: 13px;

  padding: 11px;

  border:
    1px solid #e0e6eb;

  border-radius: 7px;

  cursor: pointer;
}


.check-card strong,
.check-card span {

  display: block;
}


.check-card strong {

  color: #344b5e;

  font-size: 15px;
}


.check-card span {

  margin-top: 3px;

  color: #84919b;

  font-size: 13px;
}


.modal-actions {

  display: flex;

  justify-content:
    flex-end;

  gap: 8px;

  margin-top: 20px;
}


/* =========================================================
   MATRIZ DE ROL
========================================================= */

.permission-warning {

  margin-bottom: 14px;

  padding:
    10px
    12px;

  border-radius: 7px;

  background: #edf4fa;

  color: #07518d;

  font-size: 14px;

  line-height: 1.45;
}


.role-permissions-scroll {

  max-height: 580px;

  overflow-y: auto;

  padding-right: 4px;
}


.role-permission-group {

  margin-bottom: 14px;

  border:
    1px solid #dce3e9;

  border-radius: 8px;

  overflow: hidden;
}


.role-permission-title {

  display: flex;

  justify-content:
    space-between;

  align-items: center;

  padding:
    10px
    12px;

  background: #eef3f7;
}


.role-permission-title h3 {

  margin: 0;

  color: #17324a;

  font-size: 16px;
}


.role-permission-title span {

  color: #07518d;

  font-size: 14px;

  font-weight: 800;
}


.permission-checkbox {

  display: flex;

  align-items:
    flex-start;

  gap: 10px;

  padding:
    11px
    12px;

  border-top:
    1px solid #edf0f2;

  cursor: pointer;
}


.permission-checkbox input {

  margin-top: 3px;
}


.permission-checkbox strong,
.permission-checkbox span {

  display: block;
}


.permission-checkbox strong {

  color: #29475e;

  font-size: 15px;
}


.permission-checkbox span {

  margin-top: 3px;

  color: #07518d;

  font-size: 13px;
}


.permission-checkbox p {

  margin:
    4px
    0
    0;

  color: #7d8a95;

  font-size: 13px;
}


/* =========================================================
   VACÍO / LOADING
========================================================= */

.loading,
.empty {

  padding: 35px;

  text-align: center;

  color: #788794;

  font-size: 15px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (
  max-width: 1100px
) {

  .summary-grid {

    grid-template-columns:
      repeat(2,1fr);
  }


  .role-grid {

    grid-template-columns:
      repeat(2,1fr);
  }

}


@media (
  max-width: 760px
) {

  .layout {

    display: block;
  }


  .content {

    padding: 16px;
  }


  .summary-grid,
  .role-grid {

    grid-template-columns:
      1fr;
  }


  .tabs {

    overflow-x: auto;
  }


  .permission-filters {

    grid-template-columns:
      1fr;
  }

}

</style>