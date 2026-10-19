<template>
  <div :class="['portal-layout', { 'con-menu': mostrarMenuUsuario }]">
    <SolicitanteMenu v-if="mostrarMenuUsuario" />
    <main class="password-page">
    <section class="password-card">

      <div class="brand">
        <div class="logo-placeholder"><img src="/img/emi.jpg" alt="EMI" class="logo-img"></div>

        <div class="brand-text">
          <h1>SIGTA</h1>
          <p>Escuela Militar de Ingeniería</p>
          <span>Unidad Académica Santa Cruz</span>
        </div>
      </div>

      <div class="divider"></div>

      <div class="header">
        <h2>{{ mostrarMenuUsuario ? 'Cambiar contraseña' : 'Cambio obligatorio de contraseña' }}</h2>

        <p>
          {{ mostrarMenuUsuario
            ? 'Actualice la contraseña de acceso a su cuenta.'
            : 'Por seguridad, debe cambiar su contraseña temporal antes de continuar al sistema.' }}
        </p>
      </div>

      <form @submit.prevent="cambiarPassword">

        <div class="form-group">
          <label>Contraseña actual</label>

          <div class="password-wrapper">
            <input
              v-model="passwordActual"
              :type="verActual ? 'text' : 'password'"
              placeholder="Ingrese su contraseña actual"
              required
              :disabled="cargando"
            />

            <button
              type="button"
              class="show-password"
              @click="verActual = !verActual"
            >
              {{ verActual ? 'Ocultar' : 'Ver' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Nueva contraseña</label>

          <div class="password-wrapper">
            <input
              v-model="nuevaPassword"
              :type="verNueva ? 'text' : 'password'"
              placeholder="Ingrese su nueva contraseña"
              required
              :disabled="cargando"
            />

            <button
              type="button"
              class="show-password"
              @click="verNueva = !verNueva"
            >
              {{ verNueva ? 'Ocultar' : 'Ver' }}
            </button>
          </div>
        </div>

        <div class="form-group">
          <label>Confirmar nueva contraseña</label>

          <div class="password-wrapper">
            <input
              v-model="confirmarPassword"
              :type="verConfirmacion ? 'text' : 'password'"
              placeholder="Repita la nueva contraseña"
              required
              :disabled="cargando"
            />

            <button
              type="button"
              class="show-password"
              @click="verConfirmacion = !verConfirmacion"
            >
              {{ verConfirmacion ? 'Ocultar' : 'Ver' }}
            </button>
          </div>
        </div>

        <div class="requirements">
          <p>La contraseña debe contener:</p>

          <ul>
            <li>Mínimo 8 caracteres</li>
            <li>Una letra mayúscula</li>
            <li>Una letra minúscula</li>
            <li>Un número</li>
            <li>Un carácter especial</li>
          </ul>
        </div>

        <p
          v-if="mensaje"
          :class="['message', exito ? 'success' : 'error']"
        >
          {{ mensaje }}
        </p>

        <button
          class="primary-button"
          type="submit"
          :disabled="cargando"
        >
          {{ cargando ? 'Actualizando...' : (mostrarMenuUsuario ? 'Guardar contraseña' : 'Guardar y continuar') }}
        </button>
      </form>

      <footer>
        <p>
          Sistema Integral de Gestión de Tickets y Aprobaciones
        </p>

        <span>
          SIGTA · EMI Santa Cruz
        </span>
      </footer>

    </section>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import SolicitanteMenu from '../components/SolicitanteMenu.vue'

const router = useRouter()

const usuarioActual = computed(() => {
  try { return JSON.parse(localStorage.getItem('sigta_usuario') || '{}') }
  catch { return {} }
})

const mostrarMenuUsuario = computed(() => {
  const roles = (usuarioActual.value.roles || []).map(rol => rol.codigo)
  return roles.includes('SOLICITANTE') && !usuarioActual.value.must_change_password
})

const passwordActual = ref('')
const nuevaPassword = ref('')
const confirmarPassword = ref('')

const verActual = ref(false)
const verNueva = ref(false)
const verConfirmacion = ref(false)

const cargando = ref(false)
const mensaje = ref('')
const exito = ref(false)

async function cambiarPassword() {
  mensaje.value = ''
  exito.value = false

  if (
    !passwordActual.value ||
    !nuevaPassword.value ||
    !confirmarPassword.value
  ) {
    mensaje.value = 'Complete todos los campos.'
    return
  }

  if (nuevaPassword.value !== confirmarPassword.value) {
    mensaje.value = 'Las nuevas contraseñas no coinciden.'
    return
  }

  const token = localStorage.getItem('sigta_token')

  if (!token) {
    router.push('/login')
    return
  }

  cargando.value = true

  try {
    const respuesta = await fetch(
      '/api/usuarios/cambiar-password-obligatorio/',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
          password_actual: passwordActual.value,
          nueva_password: nuevaPassword.value,
          confirmar_password: confirmarPassword.value,
        }),
      }
    )

    const datos = await respuesta.json()

    if (!respuesta.ok) {
      mensaje.value =
        datos.mensaje || 'No se pudo cambiar la contraseña.'
      return
    }

    exito.value = true
    mensaje.value = 'Contraseña actualizada correctamente.'

    const usuarioGuardado =
      localStorage.getItem('sigta_usuario')

    if (usuarioGuardado) {
      const usuario = JSON.parse(usuarioGuardado)

      usuario.must_change_password = false

      localStorage.setItem(
        'sigta_usuario',
        JSON.stringify(usuario)
      )
    }

    setTimeout(() => {
      redirigirSegunRol()
    }, 800)

  } catch (error) {
    console.error(error)

    mensaje.value =
      'No fue posible comunicarse con el servidor.'
  } finally {
    cargando.value = false
  }
}

function redirigirSegunRol() {
  const usuarioGuardado =
    localStorage.getItem('sigta_usuario')

  if (!usuarioGuardado) {
    router.push('/login')
    return
  }

  const usuario = JSON.parse(usuarioGuardado)

  const roles =
    usuario.roles.map((rol) => rol.codigo)

  if (roles.includes('ADMIN')) {
    router.push('/admin/dashboard')
    return
  }

  if (roles.includes('JEFE_UTIC')) {
    router.push('/jefe-utic/dashboard')
    return
  }

  if (roles.includes('ESPECIALISTA')) {
    router.push('/especialista/dashboard')
    return
  }

  if (roles.includes('SERVICIOS_GENERALES')) {
    router.push('/servicios-generales/dashboard')
    return
  }

  if (roles.includes('AUXILIAR_SERVICIOS_GENERALES')) {
    router.push('/auxiliar-servicios-generales/dashboard')
    return
  }

  if (roles.includes('TESORERIA')) {
    router.push('/tesoreria/dashboard')
    return
  }

  if (roles.includes('ENCARGADO_COMPRAS_ALMACEN')) {
    router.push('/almacen/dashboard')
    return
  }

  if (roles.includes('DAF')) {
    router.push('/daf/dashboard')
    return
  }

  if (roles.includes('AGENTE')) {
    router.push('/tecnico/dashboard')
    return
  }

  if (
    roles.includes('SUPERVISOR_AREA') ||
    roles.includes('APROBADOR')
  ) {
    router.push('/supervisor/dashboard')
    return
  }

  router.push('/usuario/dashboard')
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.portal-layout {
  min-height: 100vh;
}

.portal-layout.con-menu {
  display: flex;
  background: #f3f6fb;
}

.password-page {
  min-height: 100vh;
  width: 100%;
  flex: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background:
    linear-gradient(
      135deg,
      #0a2f54 0%,
      #124d7c 55%,
      #1f628f 100%
    );

  font-family: Arial, Helvetica, sans-serif;
}

.portal-layout.con-menu .password-page {
  background: #f3f6fb;
}

@media (max-width: 760px) {
  .portal-layout.con-menu { display: block; }
}

.password-card {
  width: 100%;
  max-width: 430px;

  background: white;

  border-radius: 16px;

  padding: 24px 30px 20px;

  border-top: 4px solid #FFFF00;

  box-shadow:
    0 20px 50px rgba(0, 0, 0, 0.24);
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-placeholder {
  width: 56px;
  height: 56px;

  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  background: #6576B4;

  border: 3px solid #FFFF00;

  border-radius: 12px;

  overflow: hidden;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.brand h1 {
  margin: 0;

  color: #073b6f;

  font-size: 27px;
}

.brand p {
  margin: 3px 0 2px;

  color: #1d3348;

  font-size: 13px;
  font-weight: 700;
}

.brand span {
  color: #68798a;

  font-size: 11px;
}

.divider {
  height: 3px;

  margin: 16px 0;

  background: #FFFF00;

  border-radius: 10px;
}

.header h2 {
  margin: 0;

  color: #152b3d;

  font-size: 21px;
}

.header p {
  margin: 7px 0 17px;

  color: #687887;

  font-size: 12.5px;

  line-height: 1.45;
}

.form-group {
  margin-bottom: 12px;
}

.form-group label {
  display: block;

  margin-bottom: 5px;

  color: #273a4b;

  font-size: 13px;
  font-weight: 700;
}

.password-wrapper {
  position: relative;
}

.form-group input {
  width: 100%;
  height: 43px;

  padding: 0 66px 0 13px;

  border: 1px solid #cbd5df;

  border-radius: 8px;

  font-size: 14px;

  outline: none;
}

.form-group input:focus {
  border-color: #0b5795;

  box-shadow:
    0 0 0 3px rgba(11, 87, 149, 0.12);
}

.show-password {
  position: absolute;

  right: 11px;
  top: 50%;

  transform: translateY(-50%);

  border: none;

  background: transparent;

  color: #07518d;

  font-size: 12px;
  font-weight: 700;

  cursor: pointer;
}

.requirements {
  margin: 5px 0 13px;

  padding: 10px 13px;

  background: #f6f8fa;

  border-radius: 8px;

  border-left: 3px solid #FFFF00;
}

.requirements p {
  margin: 0 0 5px;

  color: #34495c;

  font-size: 11.5px;
  font-weight: 700;
}

.requirements ul {
  margin: 0;

  padding-left: 18px;

  color: #667787;

  font-size: 11px;

  line-height: 1.55;
}

.message {
  padding: 9px 11px;

  border-radius: 7px;

  font-size: 12px;
}

.message.error {
  background: #fff1f1;

  color: #a52121;
}

.message.success {
  background: #edf8f0;

  color: #20763b;
}

.primary-button {
  width: 100%;
  height: 45px;

  border: none;

  border-radius: 8px;

  background: #6576B4;

  color: white;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;
}

.primary-button:hover:not(:disabled) {
  background: #073563;
}

.primary-button:disabled {
  opacity: 0.7;

  cursor: not-allowed;
}

footer {
  margin-top: 14px;

  text-align: center;

  color: #75828d;
}

footer p {
  margin: 0 0 2px;

  font-size: 10px;
}

footer span {
  font-size: 10px;

  font-weight: 600;
}

@media (max-width: 520px) {
  .password-page {
    align-items: flex-start;

    padding: 12px;
  }

  .password-card {
    max-width: 100%;

    padding: 20px 18px;

    border-radius: 13px;
  }

  .brand h1 {
    font-size: 24px;
  }

  .brand p {
    font-size: 12px;
  }

  .form-group input {
    font-size: 16px;
  }
}

</style>
