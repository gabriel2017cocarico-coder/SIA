<template>

  <div class="admin-layout">

    <!-- =====================================================
         MENÚ ÚNICO DEL ADMINISTRADOR
    ====================================================== -->

    <SuperuserMenu />


    <!-- =====================================================
         CONTENIDO
    ====================================================== -->

    <main class="main-content">

      <!-- =================================================
           ENCABEZADO
      ================================================== -->

      <header class="topbar">

        <div>

          <h1>
            Gestión de Usuarios
          </h1>

          <p>
            Alta, consulta, modificación, activación
            e inactivación de usuarios.
          </p>

        </div>


        <button
          class="btn-primary"
          @click="abrirNuevo"
        >
          + Nuevo usuario
        </button>

      </header>


      <!-- =================================================
           RESUMEN
      ================================================== -->

      <section class="stats-grid">

        <article class="stat-card">

          <span>
            Total usuarios
          </span>

          <strong>
            {{ usuarios.length }}
          </strong>

          <small>
            Registrados en SIGTA
          </small>

        </article>


        <article class="stat-card">

          <span>
            Usuarios activos
          </span>

          <strong>
            {{ cantidadActivos }}
          </strong>

          <small>
            Con acceso habilitado
          </small>

        </article>


        <article class="stat-card">

          <span>
            Usuarios inactivos
          </span>

          <strong>
            {{ cantidadInactivos }}
          </strong>

          <small>
            Sin acceso al sistema
          </small>

        </article>


        <article class="stat-card">

          <span>
            Primer ingreso pendiente
          </span>

          <strong>
            {{ cantidadPrimerIngreso }}
          </strong>

          <small>
            Deben cambiar contraseña
          </small>

        </article>

      </section>


      <!-- =================================================
           FILTROS
      ================================================== -->

      <section class="filters-card">

        <div class="search-box">

          <label>
            Buscar usuario
          </label>

          <input
            v-model="busqueda"
            type="text"
            placeholder="Nombre o correo institucional..."
          />

        </div>


        <div class="filter-box">

          <label>
            Estado
          </label>

          <select
            v-model="filtroEstado"
          >

            <option value="">
              Todos los estados
            </option>

            <option value="activo">
              Activos
            </option>

            <option value="inactivo">
              Inactivos
            </option>

          </select>

        </div>

      </section>


      <!-- =================================================
           MENSAJE GENERAL
      ================================================== -->

      <div
        v-if="mensaje"
        :class="[
          'alert',
          error
            ? 'error'
            : 'success'
        ]"
      >
        {{ mensaje }}
      </div>


      <!-- =================================================
           TABLA
      ================================================== -->

      <section class="table-card">

        <div class="table-header">

          <div>

            <h2>
              Usuarios registrados
            </h2>

            <p>
              Administre las cuentas y permisos
              institucionales.
            </p>

          </div>


          <span class="result-count">
            {{ usuariosFiltrados.length }}
            resultado(s)
          </span>

        </div>


        <div
          v-if="cargando"
          class="loading"
        >
          Cargando usuarios...
        </div>


        <div
          v-else-if="
            usuariosFiltrados.length === 0
          "
          class="empty"
        >
          No se encontraron usuarios.
        </div>


        <div
          v-else
          class="table-wrapper"
        >

          <table>

            <thead>

              <tr>

                <th>
                  Usuario
                </th>

                <th>
                  Correo
                </th>

                <th>
                  Rol
                </th>

                <th>
                  Área
                </th>

                <th>
                  Estado
                </th>

                <th>
                  Primer ingreso
                </th>

                <th>
                  Acciones
                </th>

              </tr>

            </thead>


            <tbody>

              <tr
                v-for="usuario in usuariosFiltrados"
                :key="usuario.id"
              >

                <!-- USUARIO -->
                <td>

                  <div class="user-cell">

                    <div class="table-avatar">

                      {{
                        obtenerIniciales(
                          usuario.nombre_completo
                        )
                      }}

                    </div>


                    <div>

                      <strong>
                        {{ usuario.nombre_completo }}
                      </strong>

                      <small>
                        ID {{ usuario.id }}
                      </small>

                    </div>

                  </div>

                </td>


                <!-- CORREO -->
                <td>

                  {{ usuario.email }}

                </td>


                <!-- ROL -->
                <td>

                  <span class="role-badge">

                    {{
                      usuario.roles?.[0]?.rol_nombre
                      || 'Sin rol'
                    }}

                  </span>

                </td>


                <!-- ÁREA -->
                <td>

                  {{
                    usuario.roles?.[0]?.area_nombre
                    || 'Global'
                  }}

                </td>


                <!-- ESTADO -->
                <td>

                  <span
                    :class="[
                      'badge',
                      usuario.is_active
                        ? 'activo'
                        : 'inactivo'
                    ]"
                  >

                    {{
                      usuario.is_active
                        ? 'Activo'
                        : 'Inactivo'
                    }}

                  </span>

                </td>


                <!-- PRIMER INGRESO -->
                <td>

                  <span
                    :class="[
                      'first-login',
                      usuario.must_change_password
                        ? 'pending'
                        : 'completed'
                    ]"
                  >

                    {{
                      usuario.must_change_password
                        ? 'Pendiente'
                        : 'Completado'
                    }}

                  </span>

                </td>


                <!-- ACCIONES -->
                <td>

                  <div class="actions">

                    <button
                      class="btn-edit"
                      @click="
                        editarUsuario(
                          usuario
                        )
                      "
                    >
                      Editar
                    </button>


                    <button
                      v-if="usuario.is_active"
                      class="btn-disable"
                      @click="
                        inactivarUsuario(
                          usuario
                        )
                      "
                    >
                      Inactivar
                    </button>


                    <button
                      v-else
                      class="btn-enable"
                      @click="
                        activarUsuario(
                          usuario
                        )
                      "
                    >
                      Activar
                    </button>

                  </div>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </section>


      <!-- =================================================
           MODAL
      ================================================== -->

      <div
        v-if="mostrarModal"
        class="modal-overlay"
        @click.self="cerrarModal"
      >

        <div class="modal">

          <!-- ENCABEZADO MODAL -->

          <div class="modal-header">

            <div>

              <span class="modal-kicker">
                Administración de identidad
              </span>

              <h2>

                {{
                  editando
                    ? 'Editar usuario'
                    : 'Nuevo usuario'
                }}

              </h2>


              <p>

                {{
                  editando
                    ? 'Modifique los datos permitidos del usuario.'
                    : 'Registre una nueva cuenta institucional en SIGTA.'
                }}

              </p>

            </div>


            <button
              type="button"
              class="close"
              @click="cerrarModal"
            >
              ×
            </button>

          </div>


          <!-- FORMULARIO -->

          <form
            @submit.prevent="guardarUsuario"
          >

            <div class="grid">

              <!-- NOMBRE -->

              <div class="field full">

                <label>
                  Nombre completo
                  <span>*</span>
                </label>

                <input
                  v-model="form.nombre_completo"
                  type="text"
                  placeholder="Ej.: Juan Carlos Pérez"
                  required
                />

              </div>


              <!-- EMAIL -->

              <div class="field full">

                <label>
                  Correo institucional
                  <span>*</span>
                </label>

                <input
                  v-model="form.email"
                  type="email"
                  placeholder="usuario@emi.edu.bo"
                  required
                />

                <small>
                  Se utilizará para iniciar sesión
                  y recibir notificaciones.
                </small>

              </div>


              <!-- ROL -->

              <div class="field">

                <label>
                  Rol
                  <span>*</span>
                </label>

                <select
                  v-model="form.tipo_usuario"
                  required
                  @change="cambioRol"
                >

                  <option
                    value=""
                    disabled
                  >
                    Seleccione tipo
                  </option>


                  <option value="JEFE">Jefe</option>
                  <option value="TECNICO">Técnico</option>
                  <option value="DIRECTOR">Director</option>
                  <option value="USUARIO">Usuario</option>
                  <option value="SUPERUSER">Superuser</option>

                </select>

              </div>


              <!-- ÁREA -->

              <div v-if="requiereArea" class="field">

                <label>
                  Área
                  <span>*</span>
                </label>


                <select
                  v-model="form.area_id"
                  required
                  @change="form.especialidad = ''"
                >

                  <option value="">

                    Seleccione área

                  </option>


                  <option
                    v-for="area in areasFormulario"
                    :key="area.id"
                    :value="area.id"
                  >
                    {{ area.nombre }}
                  </option>

                </select>


              </div>

              <div v-if="form.tipo_usuario === 'TECNICO' && form.area_id" class="field">
                <label>Especialidad <span>*</span></label>
                <select v-model="form.especialidad" required>
                  <option value="" disabled>Seleccione especialidad</option>
                  <option v-for="opcion in especialidadesDisponibles" :key="opcion.valor" :value="opcion.valor">
                    {{ opcion.nombre }}
                  </option>
                </select>
              </div>


              <!-- CONTRASEÑA -->

              <div class="field full">

                <label>

                  {{
                    editando
                      ? 'Nueva contraseña temporal'
                      : 'Contraseña temporal'
                  }}

                  <span
                    v-if="
                      !editando
                    "
                  >
                    *
                  </span>

                </label>


                <input
                  v-model="form.password"
                  type="password"
                  :required="!editando"
                  placeholder="Ej.: Temporal2026*"
                />


                <small>

                  {{
                    editando
                      ? 'Déjelo vacío si no desea cambiar la contraseña.'
                      : 'El usuario deberá cambiarla obligatoriamente en su primer ingreso.'
                  }}

                </small>

              </div>

            </div>


            <!-- ERROR MODAL -->

            <div
              v-if="mensajeModal"
              class="modal-error"
            >
              {{ mensajeModal }}
            </div>


            <!-- ACCIONES MODAL -->

            <div class="modal-actions">

              <button
                type="button"
                class="btn-cancel"
                @click="cerrarModal"
              >
                Cancelar
              </button>


              <button
                type="submit"
                class="btn-save"
                :disabled="guardando"
              >

                {{
                  guardando
                    ? 'Guardando...'
                    : (
                        editando
                          ? 'Guardar cambios'
                          : 'Crear usuario'
                      )
                }}

              </button>

            </div>

          </form>

        </div>

      </div>

    </main>

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


/* =========================================================
   COMPONENTE MENÚ
========================================================= */

import SuperuserMenu
  from '../components/SuperuserMenu.vue'


const router =
  useRouter()


/* =========================================================
   DATOS
========================================================= */

const usuarios =
  ref([])

const roles =
  ref([])

const areas =
  ref([])


/* =========================================================
   ESTADOS
========================================================= */

const cargando =
  ref(true)

const guardando =
  ref(false)

const mostrarModal =
  ref(false)

const editando =
  ref(false)

const usuarioEditandoId =
  ref(null)

const busqueda =
  ref('')

const filtroEstado =
  ref('')

const mensaje =
  ref('')

const mensajeModal =
  ref('')

const error =
  ref(false)


/* =========================================================
   FORMULARIO
========================================================= */

const form =
  reactive({

    nombre_completo: '',

    email: '',

    password: '',

    tipo_usuario: '',

    rol_id: '',

    area_id: '',

    especialidad: '',
  })


/* =========================================================
   TOKEN
========================================================= */

const token = () =>
  localStorage.getItem(
    'sigta_token'
  )


/* =========================================================
   HEADERS
========================================================= */

const headers = () => ({

  'Content-Type':
    'application/json',

  Accept:
    'application/json',

  Authorization:
    `Token ${token()}`,
})


const headersLectura = () => ({

  Accept:
    'application/json',

  Authorization:
    `Token ${token()}`,
})


/* =========================================================
   CONTADORES
========================================================= */

const cantidadActivos =
  computed(() => {

    return usuarios.value.filter(
      usuario =>
        usuario.is_active
    ).length
  })


const cantidadInactivos =
  computed(() => {

    return usuarios.value.filter(
      usuario =>
        !usuario.is_active
    ).length
  })


const cantidadPrimerIngreso =
  computed(() => {

    return usuarios.value.filter(
      usuario =>
        usuario.must_change_password
    ).length
  })


/* =========================================================
   FILTRADO
========================================================= */

const usuariosFiltrados =
  computed(() => {

    const texto =
      busqueda.value
        .toLowerCase()
        .trim()


    return usuarios.value.filter(
      usuario => {

        const coincideTexto =

          !texto

          ||

          usuario.nombre_completo
            ?.toLowerCase()
            .includes(texto)

          ||

          usuario.email
            ?.toLowerCase()
            .includes(texto)


        const coincideEstado =

          !filtroEstado.value

          ||

          (
            filtroEstado.value
            === 'activo'

            &&
            usuario.is_active
          )

          ||

          (
            filtroEstado.value
            === 'inactivo'

            &&
            !usuario.is_active
          )


        return (
          coincideTexto
          &&
          coincideEstado
        )
      }
    )
  })


/* =========================================================
   ROL GLOBAL
========================================================= */

const requiereArea = computed(() => ['JEFE', 'TECNICO'].includes(form.tipo_usuario))

const areasFormulario = computed(() => {
  const oficiales = ['DAF', 'MANTENIMIENTO', 'UTIC']
  return areas.value.filter(area => oficiales.includes(String(area.codigo).toUpperCase()))
})

const areaSeleccionada = computed(() =>
  areas.value.find(area => Number(area.id) === Number(form.area_id))
)

const especialidadesDisponibles = computed(() => {
  const codigo = String(areaSeleccionada.value?.codigo || '').toUpperCase()
  if (codigo === 'UTIC') return [
    { valor: 'REDES', nombre: 'Redes' },
    { valor: 'HARDWARE_COMPUTADORAS', nombre: 'Hardware y computadoras' },
    { valor: 'SISTEMAS_CENTRALIZADOS_DATOS', nombre: 'Sistemas centralizados y datos' },
    { valor: 'EQUIPOS_AUXILIARES', nombre: 'Equipos auxiliares' },
  ]
  if (codigo === 'MANTENIMIENTO') return [
    { valor: 'CHOFER', nombre: 'Chofer' },
    { valor: 'TECNICO_MANTENIMIENTO', nombre: 'Técnico' },
  ]
  if (codigo === 'DAF') return [
    { valor: 'TECNICO_DAF', nombre: 'Técnico de la DAF' },
    { valor: 'ALMACEN_COMPRAS', nombre: 'Técnico de Almacén y Compras' },
    { valor: 'TESORERIA', nombre: 'Técnico de Tesorería' },
  ]
  return []
})

function codigoRolInterno() {
  if (form.tipo_usuario === 'SUPERUSER') return 'SUPERUSER'
  if (form.tipo_usuario === 'DIRECTOR') return 'ADMIN'
  if (form.tipo_usuario === 'USUARIO') return 'SOLICITANTE'
  const area = String(areaSeleccionada.value?.codigo || '').toUpperCase()
  if (form.tipo_usuario === 'JEFE') {
    return { UTIC: 'JEFE_UTIC', MANTENIMIENTO: 'SERVICIOS_GENERALES' }[area]
  }
  if (form.tipo_usuario === 'TECNICO') {
    if (area === 'UTIC') return 'ESPECIALISTA'
    if (area === 'MANTENIMIENTO') return 'AUXILIAR_SERVICIOS_GENERALES'
    return { TECNICO_DAF: 'DAF', ALMACEN_COMPRAS: 'ENCARGADO_COMPRAS_ALMACEN', TESORERIA: 'TESORERIA' }[form.especialidad]
  }
  return ''
}


/* =========================================================
   AL MONTAR
========================================================= */

onMounted(
  async () => {

    if (!token()) {

      router.push(
        '/login'
      )

      return
    }


    await cargarDatos()
  }
)


/* =========================================================
   NORMALIZAR RESPUESTAS
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
   CARGAR USUARIOS, ROLES Y ÁREAS
========================================================= */

async function cargarDatos() {

  cargando.value =
    true


  try {

    const [
      usuariosRespuesta,
      rolesRespuesta,
      areasRespuesta,
    ] = await Promise.all([


      /* USUARIOS */

      fetch(
        '/api/usuarios/usuarios/',
        {
          headers:
            headersLectura(),
        }
      ),


      /* ROLES
         CORREGIDO:
         ahora también manda token
      */

      fetch(
        '/api/usuarios/roles/',
        {
          headers:
            headersLectura(),
        }
      ),


      /* ÁREAS
         CORREGIDO:
         ahora también manda token
      */

      fetch(
        '/api/usuarios/areas/',
        {
          headers:
            headersLectura(),
        }
      ),

    ])


    /* ===============================================
       VALIDAR SESIÓN
    ================================================ */

    const respuestas = [

      usuariosRespuesta,

      rolesRespuesta,

      areasRespuesta,
    ]


    const sinPermiso =
      respuestas.some(
        respuesta =>
          respuesta.status === 401
          ||
          respuesta.status === 403
      )


    if (sinPermiso) {

      cerrarSesion()

      return
    }


    /* ===============================================
       VALIDAR ERRORES
    ================================================ */

    if (!usuariosRespuesta.ok) {

      throw new Error(
        'No se pudieron cargar los usuarios.'
      )
    }


    if (!rolesRespuesta.ok) {

      throw new Error(
        'No se pudieron cargar los roles.'
      )
    }


    if (!areasRespuesta.ok) {

      throw new Error(
        'No se pudieron cargar las áreas.'
      )
    }


    /* ===============================================
       LEER JSON
    ================================================ */

    const datosUsuarios =
      await usuariosRespuesta.json()


    const datosRoles =
      await rolesRespuesta.json()


    const datosAreas =
      await areasRespuesta.json()


    /* ===============================================
       GUARDAR
    ================================================ */

    usuarios.value =
      convertirLista(
        datosUsuarios
      )


    roles.value =
      convertirLista(
        datosRoles
      )


    areas.value =
      convertirLista(
        datosAreas
      )


    console.log(
      'Usuarios:',
      usuarios.value
    )


    console.log(
      'Roles:',
      roles.value
    )


    console.log(
      'Áreas:',
      areas.value
    )


  } catch (e) {

    console.error(
      'Error cargando usuarios:',
      e
    )


    mostrarMensaje(
      e.message
      ||
      'No se pudieron cargar los datos.',
      true
    )

  } finally {

    cargando.value =
      false
  }
}


/* =========================================================
   NUEVO USUARIO
========================================================= */

function abrirNuevo() {

  editando.value =
    false

  usuarioEditandoId.value =
    null

  limpiarFormulario()

  mostrarModal.value =
    true
}


/* =========================================================
   EDITAR USUARIO
========================================================= */

function editarUsuario(
  usuario
) {

  editando.value =
    true


  usuarioEditandoId.value =
    usuario.id


  form.nombre_completo =
    usuario.nombre_completo
    || ''


  form.email =
    usuario.email
    || ''


  form.password = ''


  /*
   * Se convierte a Number para que
   * coincida correctamente con:
   *
   * :value="rol.id"
   */

  form.rol_id =
    usuario.roles?.[0]?.rol_id
      ? Number(
          usuario.roles[0].rol_id
        )
      : ''

  const asignacion = usuario.roles?.[0] || {}
  const codigoRol = asignacion.rol_codigo
  const mapaTipo = {
    SUPERUSER: 'SUPERUSER', ADMIN: 'DIRECTOR', DIRECTOR: 'DIRECTOR', SOLICITANTE: 'USUARIO',
    JEFE_UTIC: 'JEFE', SERVICIOS_GENERALES: 'JEFE',
    ESPECIALISTA: 'TECNICO', AUXILIAR_SERVICIOS_GENERALES: 'TECNICO', DAF: 'TECNICO',
    ENCARGADO_COMPRAS_ALMACEN: 'TECNICO', TESORERIA: 'TECNICO',
  }
  form.tipo_usuario = mapaTipo[codigoRol] || ''


  /*
   * Igual para Área.
   */

  form.area_id =
    usuario.roles?.[0]?.area_id
      ? Number(
          usuario.roles[0].area_id
        )
      : ''

  if (!form.area_id) {
    const codigoArea = {
      JEFE_UTIC: 'UTIC', ESPECIALISTA: 'UTIC',
      DAF: 'DAF', ENCARGADO_COMPRAS_ALMACEN: 'DAF', TESORERIA: 'DAF',
      SERVICIOS_GENERALES: 'MANTENIMIENTO', AUXILIAR_SERVICIOS_GENERALES: 'MANTENIMIENTO',
    }[codigoRol]
    form.area_id = areas.value.find(area => area.codigo === codigoArea)?.id || ''
  }

  form.especialidad = asignacion.especialidad || ({
    DAF: 'TECNICO_DAF', ENCARGADO_COMPRAS_ALMACEN: 'ALMACEN_COMPRAS', TESORERIA: 'TESORERIA',
    AUXILIAR_SERVICIOS_GENERALES: 'TECNICO_MANTENIMIENTO',
  }[codigoRol] || '')


  mensajeModal.value =
    ''


  mostrarModal.value =
    true
}


/* =========================================================
   LIMPIAR
========================================================= */

function limpiarFormulario() {

  form.nombre_completo = ''

  form.email = ''

  form.password = ''

  form.tipo_usuario = ''

  form.rol_id = ''

  form.area_id = ''

  form.especialidad = ''

  mensajeModal.value = ''
}


/* =========================================================
   CERRAR MODAL
========================================================= */

function cerrarModal() {

  mostrarModal.value =
    false

  limpiarFormulario()
}


/* =========================================================
   CAMBIO DE ROL
========================================================= */

function cambioRol() {
  form.rol_id = ''
  form.especialidad = ''
  if (!requiereArea.value) {
    form.area_id = ''
  }
}


/* =========================================================
   GUARDAR USUARIO
========================================================= */

async function guardarUsuario() {

  mensajeModal.value = ''


  /* ===============================================
     CAMPOS OBLIGATORIOS
  ================================================ */

  if (
    !form.nombre_completo.trim()
    ||
    !form.email.trim()
    ||
    !form.tipo_usuario
  ) {

    mensajeModal.value =
      'Complete los campos obligatorios.'

    return
  }

  if (
    form.tipo_usuario === 'JEFE'
    &&
    String(areaSeleccionada.value?.codigo || '').toUpperCase() === 'DAF'
  ) {

    mensajeModal.value =
      'La DAF no tiene jefatura: la solicitud de compra llega directamente a la DAF.'

    return
  }


  /* ===============================================
     CORREO EMI
  ================================================ */

  if (
    !form.email
      .trim()
      .toLowerCase()
      .endsWith(
        '@emi.edu.bo'
      )
  ) {

    mensajeModal.value =
      'Ingrese un correo institucional @emi.edu.bo.'

    return
  }


  /* ===============================================
     ÁREA OBLIGATORIA
  ================================================ */

  if (
    requiereArea.value
    &&
    !form.area_id
  ) {

    mensajeModal.value =
      'Seleccione el área del usuario.'

    return
  }

  if (form.tipo_usuario === 'TECNICO' && !form.especialidad) {
    mensajeModal.value = 'Seleccione la especialidad del técnico.'
    return
  }


  /* ===============================================
     CONTRASEÑA PARA NUEVO USUARIO
  ================================================ */

  if (
    !editando.value
    &&
    !form.password
  ) {

    mensajeModal.value =
      'Ingrese una contraseña temporal.'

    return
  }


  guardando.value =
    true


  try {

    const codigoRol = codigoRolInterno()
    const rolInterno = roles.value.find(rol => rol.codigo === codigoRol)
    if (!rolInterno) {
      mensajeModal.value = 'No se encontró el rol interno para la selección realizada.'
      return
    }

    const payload = {

      nombre_completo:
        form.nombre_completo.trim(),

      email:
        form.email
          .trim()
          .toLowerCase(),

      rol_id: Number(rolInterno.id),

      area_id:
        form.area_id
          ? Number(form.area_id)
          : null,

      especialidad: form.especialidad || '',
    }


    /*
     * La contraseña solamente se manda
     * si se escribió una.
     */

    if (
      form.password
    ) {

      payload.password =
        form.password
    }


    let url =
      '/api/usuarios/usuarios/'


    let method =
      'POST'


    if (
      editando.value
    ) {

      url =
        `/api/usuarios/usuarios/${usuarioEditandoId.value}/`


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
            JSON.stringify(
              payload
            ),
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

      console.error(
        'Error guardando usuario:',
        datos
      )


      mensajeModal.value =
        obtenerError(
          datos
        )


      return
    }


    const eraEdicion =
      editando.value


    cerrarModal()


    mostrarMensaje(

      eraEdicion
        ? 'Usuario actualizado correctamente.'
        : 'Usuario creado correctamente.'
    )


    await cargarDatos()


  } catch (e) {

    console.error(
      'Error guardando usuario:',
      e
    )


    mensajeModal.value =
      'No fue posible guardar el usuario.'

  } finally {

    guardando.value =
      false
  }
}


/* =========================================================
   INACTIVAR
========================================================= */

async function inactivarUsuario(
  usuario
) {

  const confirmar =
    window.confirm(
      `¿Desea inactivar a ${usuario.nombre_completo}?`
    )


  if (!confirmar) {

    return
  }


  try {

    const respuesta =
      await fetch(
        `/api/usuarios/usuarios/${usuario.id}/`,
        {

          method:
            'DELETE',

          headers:
            headers(),
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
        datos.detail
        ||
        'No se pudo inactivar el usuario.',
        true
      )


      return
    }


    mostrarMensaje(
      'Usuario inactivado correctamente.'
    )


    await cargarDatos()


  } catch (e) {

    console.error(
      e
    )


    mostrarMensaje(
      'Error al inactivar el usuario.',
      true
    )
  }
}


/* =========================================================
   ACTIVAR
========================================================= */

async function activarUsuario(
  usuario
) {

  try {

    const respuesta =
      await fetch(
        `/api/usuarios/usuarios/${usuario.id}/activar/`,
        {

          method:
            'POST',

          headers:
            headers(),

          body:
            JSON.stringify({}),
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
        datos.detail
        ||
        'No se pudo activar el usuario.',
        true
      )


      return
    }


    mostrarMensaje(
      'Usuario activado correctamente.'
    )


    await cargarDatos()


  } catch (e) {

    console.error(
      e
    )


    mostrarMensaje(
      'Error al activar el usuario.',
      true
    )
  }
}


/* =========================================================
   ERRORES DEL BACKEND
========================================================= */

function obtenerError(
  datos
) {

  if (
    datos.email
  ) {

    return Array.isArray(
      datos.email
    )
      ? datos.email[0]
      : String(
          datos.email
        )
  }


  if (
    datos.password
  ) {

    return Array.isArray(
      datos.password
    )
      ? datos.password[0]
      : String(
          datos.password
        )
  }


  if (
    datos.area_id
  ) {

    return Array.isArray(
      datos.area_id
    )
      ? datos.area_id[0]
      : String(
          datos.area_id
        )
  }


  if (
    datos.rol_id
  ) {

    return Array.isArray(
      datos.rol_id
    )
      ? datos.rol_id[0]
      : String(
          datos.rol_id
        )
  }


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


  /*
   * Si DRF devuelve otros campos
   * mostramos el primero.
   */

  const errores =
    Object.entries(
      datos
    )


  if (
    errores.length > 0
  ) {

    const [
      campo,
      valor
    ] =
      errores[0]


    const texto =
      Array.isArray(valor)
        ? valor.join(', ')
        : String(valor)


    return (
      `${campo}: ${texto}`
    )
  }


  return (
    'Revise los datos ingresados.'
  )
}


/* =========================================================
   MENSAJE
========================================================= */

function mostrarMensaje(
  texto,
  esError = false
) {

  mensaje.value =
    texto


  error.value =
    esError


  setTimeout(
    () => {

      mensaje.value = ''

    },
    3500
  )
}


/* =========================================================
   INICIALES
========================================================= */

function obtenerIniciales(
  nombre
) {

  if (!nombre) {

    return 'U'
  }


  return nombre
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map(
      palabra =>
        palabra
          .charAt(0)
          .toUpperCase()
    )
    .join('')
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

.admin-layout {

  min-height: 100vh;

  display: flex;

  background: #f2f5f9;

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}


.main-content {

  flex: 1;

  min-width: 0;

  padding: 28px;

  overflow-x: hidden;
}


/* =========================================================
   ENCABEZADO
========================================================= */

.topbar {

  display: flex;

  justify-content:
    space-between;

  align-items: center;

  gap: 20px;

  margin-bottom: 21px;
}


.breadcrumb {

  display: block;

  margin-bottom: 7px;

  color: #8493a0;

  font-size: 15px;
}


.topbar h1 {

  margin: 0;

  color: #17324a;

  font-size: 28px;
}


.topbar p {

  margin:
    5px
    0
    0;

  color: #748391;

  font-size: 18px;
}


.btn-primary {

  min-height: 43px;

  padding:
    0
    18px;

  border: none;

  border-radius: 8px;

  background: #f2c400;

  color: #143250;

  font-size: 17px;

  font-weight: 800;

  cursor: pointer;
}


.btn-primary:hover {

  background: #e2b800;
}


/* =========================================================
   ESTADÍSTICAS
========================================================= */

.stats-grid {

  display: grid;

  grid-template-columns:
    repeat(4,1fr);

  gap: 13px;

  margin-bottom: 18px;
}


.stat-card {

  min-height: 105px;

  padding: 16px;

  border-top:
    3px solid #f2c400;

  border-radius: 9px;

  background: white;

  box-shadow:
    0
    3px
    12px
    rgba(0,0,0,.05);
}


.stat-card span {

  display: block;

  color: #637789;

  font-size: 15px;

  font-weight: 800;

  text-transform: uppercase;
}


.stat-card strong {

  display: block;

  margin:
    7px
    0;

  color: #073b6f;

  font-size: 25px;
}


.stat-card small {

  color: #8996a1;

  font-size: 14px;
}


/* =========================================================
   FILTROS
========================================================= */

.filters-card {

  display: grid;

  grid-template-columns:
    1fr 210px;

  gap: 12px;

  margin-bottom: 16px;

  padding: 14px;

  border-radius: 9px;

  background: #ffffff;

  box-shadow:
    0
    3px
    12px
    rgba(0,0,0,.04);
}


.search-box,
.filter-box {

  display: flex;

  flex-direction: column;

  gap: 6px;
}


.filters-card label {

  color: #52687b;

  font-size: 15px;

  font-weight: 700;
}


.filters-card input,
.filters-card select {

  width: 100%;

  height: 41px;

  padding:
    0
    12px;

  border:
    1px solid #d2dbe3;

  border-radius: 7px;

  background: white;

  color: #30495d;

  font-size: 17px;

  outline: none;
}


.filters-card input:focus,
.filters-card select:focus {

  border-color: #0b5795;

  box-shadow:
    0
    0
    0
    3px
    rgba(11,87,149,.08);
}


/* =========================================================
   ALERTAS
========================================================= */

.alert {

  margin-bottom: 14px;

  padding:
    11px
    14px;

  border-radius: 7px;

  font-size: 17px;
}


.alert.success {

  background: #eaf7ef;

  color: #227442;
}


.alert.error {

  background: #fdecec;

  color: #a83232;
}


/* =========================================================
   TABLA
========================================================= */

.table-card {

  overflow: hidden;

  border-radius: 10px;

  background: white;

  box-shadow:
    0
    4px
    14px
    rgba(0,0,0,.06);
}


.table-header {

  display: flex;

  align-items: center;

  justify-content:
    space-between;

  gap: 12px;

  padding:
    17px
    18px;

  border-bottom:
    1px solid #e8edf1;
}


.table-header h2 {

  margin: 0;

  color: #17324a;

  font-size: 21px;
}


.table-header p {

  margin:
    3px
    0
    0;

  color: #82909c;

  font-size: 15px;
}


.result-count {

  padding:
    5px
    8px;

  border-radius: 15px;

  background: #eef4f8;

  color: #5d7385;

  font-size: 14px;

  font-weight: 700;
}


.table-wrapper {

  width: 100%;

  overflow-x: auto;
}


table {

  width: 100%;

  min-width: 1050px;

  border-collapse:
    collapse;
}


th {

  padding:
    13px
    14px;

  background: #f8fafb;

  color: #586b7b;

  text-align: left;

  font-size: 15px;

  font-weight: 800;

  text-transform:
    uppercase;
}


td {

  padding:
    14px;

  border-top:
    1px solid #edf0f2;

  color: #405464;

  font-size: 16px;

  vertical-align: middle;
}


td strong {

  color: #173a59;
}


/* =========================================================
   USUARIO TABLA
========================================================= */

.user-cell {

  display: flex;

  align-items: center;

  gap: 9px;
}


.table-avatar {

  width: 32px;

  height: 32px;

  flex-shrink: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #e8f1f8;

  color: #07518d;

  font-size: 15px;

  font-weight: 900;
}


.user-cell strong,
.user-cell small {

  display: block;
}


.user-cell small {

  margin-top: 2px;

  color: #9aa5ae;

  font-size: 13px;
}


/* =========================================================
   BADGES
========================================================= */

.badge {

  display: inline-block;

  padding:
    5px
    9px;

  border-radius: 20px;

  font-size: 14px;

  font-weight: 700;
}


.badge.activo {

  background: #e8f7ef;

  color: #1f7845;
}


.badge.inactivo {

  background: #fbeaea;

  color: #a83232;
}


.role-badge {

  display: inline-block;

  padding:
    5px
    7px;

  border-radius: 5px;

  background: #edf3f8;

  color: #405f79;

  font-size: 14px;
}


.first-login {

  font-size: 15px;

  font-weight: 700;
}


.first-login.pending {

  color: #a36d00;
}


.first-login.completed {

  color: #3f6c56;
}


/* =========================================================
   ACCIONES
========================================================= */

.actions {

  display: flex;

  gap: 6px;
}


.actions button {

  padding:
    6px
    9px;

  border: none;

  border-radius: 5px;

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;
}


.btn-edit {

  background: #eaf3fb;

  color: #07518d;
}


.btn-disable {

  background: #fdecec;

  color: #a42828;
}


.btn-enable {

  background: #e8f7ef;

  color: #1e7544;
}


/* =========================================================
   CARGA / VACÍO
========================================================= */

.loading,
.empty {

  padding: 45px;

  text-align: center;

  color: #758391;

  font-size: 17px;
}


/* =========================================================
   MODAL
========================================================= */

.modal-overlay {

  position: fixed;

  inset: 0;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 20px;

  background:
    rgba(7,35,60,.58);

  z-index: 1000;
}


.modal {

  width: 100%;

  max-width: 610px;

  max-height: 90vh;

  overflow-y: auto;

  padding: 24px;

  border-top:
    4px solid #f2c400;

  border-radius: 12px;

  background: white;

  box-shadow:
    0
    20px
    60px
    rgba(0,0,0,.25);
}


.modal-header {

  display: flex;

  justify-content:
    space-between;

  gap: 15px;

  margin-bottom: 20px;
}


.modal-kicker {

  display: block;

  margin-bottom: 5px;

  color: #7e8f9c;

  font-size: 14px;

  text-transform:
    uppercase;

  font-weight: 800;
}


.modal-header h2 {

  margin: 0;

  color: #17324a;

  font-size: 20px;
}


.modal-header p {

  margin:
    4px
    0
    0;

  color: #788794;

  font-size: 16px;
}


.close {

  border: none;

  background: transparent;

  color: #687987;

  font-size: 27px;

  cursor: pointer;
}


/* =========================================================
   FORMULARIO
========================================================= */

.grid {

  display: grid;

  grid-template-columns:
    1fr
    1fr;

  gap: 14px;
}


.field {

  display: flex;

  flex-direction: column;

  gap: 6px;
}


.field.full {

  grid-column:
    1 / -1;
}


.field label {

  color: #34495b;

  font-size: 16px;

  font-weight: 700;
}


.field label span {

  color: #b83232;
}


.field input,
.field select {

  width: 100%;

  height: 42px;

  padding:
    0
    12px;

  border:
    1px solid #ccd6de;

  border-radius: 7px;

  background: white;

  color: #31495c;

  outline: none;

  font-size: 17px;
}


.field input:focus,
.field select:focus {

  border-color: #0b5795;

  box-shadow:
    0
    0
    0
    3px
    rgba(11,87,149,.1);
}


.field select:disabled {

  background: #f1f3f5;

  color: #88949e;

  cursor: not-allowed;
}


.field small {

  color: #7a8995;

  font-size: 14px;

  line-height: 1.4;
}


/* =========================================================
   ERROR MODAL
========================================================= */

.modal-error {

  margin-top: 14px;

  padding: 10px;

  border-radius: 6px;

  background: #fdecec;

  color: #aa2f2f;

  font-size: 16px;
}


/* =========================================================
   ACCIONES MODAL
========================================================= */

.modal-actions {

  display: flex;

  justify-content:
    flex-end;

  gap: 10px;

  margin-top: 22px;
}


.btn-cancel,
.btn-save {

  min-height: 40px;

  padding:
    0
    16px;

  border-radius: 7px;

  font-size: 16px;

  font-weight: 700;

  cursor: pointer;
}


.btn-cancel {

  border:
    1px solid #d0d9e1;

  background: white;

  color: #506273;
}


.btn-save {

  border: none;

  background: #073b6f;

  color: white;
}


.btn-save:disabled {

  opacity: .6;

  cursor: not-allowed;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (
  max-width: 1050px
) {

  .stats-grid {

    grid-template-columns:
      repeat(2,1fr);
  }

}


@media (
  max-width: 760px
) {

  .admin-layout {

    display: block;
  }


  .main-content {

    padding: 18px;
  }


  .topbar {

    align-items:
      flex-start;

    flex-direction:
      column;
  }


  .stats-grid {

    grid-template-columns:
      1fr
      1fr;
  }


  .filters-card {

    grid-template-columns:
      1fr;
  }


  .grid {

    grid-template-columns:
      1fr;
  }


  .field.full {

    grid-column: auto;
  }

}


@media (
  max-width: 480px
) {

  .stats-grid {

    grid-template-columns:
      1fr;
  }


  .modal-actions {

    flex-direction:
      column-reverse;
  }


  .btn-cancel,
  .btn-save {

    width: 100%;
  }

}

</style>
