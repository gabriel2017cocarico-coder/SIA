<template>
  <div class="layout">
    <SolicitanteMenu />
    <main class="content">
      <header class="topbar">
        <div>
          <h1>Mi perfil</h1>
          <p>Consulte y actualice la información de su cuenta registrada en SIA.</p>
        </div>
      </header>

      <section class="summary">
        <article>
          <span>Usuario</span>
          <strong>{{ iniciales }}</strong>
          <small>{{ form.nombre_completo || 'Usuario' }}</small>
        </article>
        <article>
          <span>Área</span>
          <strong class="summary-text">{{ form.area_nombre || 'Sin área' }}</strong>
          <small>Dependencia registrada</small>
        </article>
        <article>
          <span>Cuenta</span>
          <strong class="summary-text">Activa</strong>
          <small>{{ form.rol_nombre || 'Solicitante' }}</small>
        </article>
      </section>

      <section class="profile-sheet requests-card">
        <div class="identity">
          <div class="avatar">{{ iniciales }}</div>
          <div><strong>{{ form.nombre_completo || 'Usuario' }}</strong><span>{{ form.email }}</span></div>
        </div>

        <form @submit.prevent="guardar">
          <div class="field">
            <label for="nombre">Nombre completo</label>
            <input id="nombre" v-model="form.nombre_completo" maxlength="150" required :disabled="guardando" />
          </div>
          <div class="field">
            <label for="correo">Correo institucional</label>
            <input id="correo" v-model="form.email" disabled />
            <small>El correo identifica su cuenta y no se modifica desde el perfil.</small>
          </div>
          <div class="field">
            <label for="area">Área</label>
            <select id="area" v-model="form.area_id" required :disabled="guardando">
              <option value="">Seleccione un área</option>
              <option v-for="area in areas" :key="area.id" :value="area.id">{{ area.nombre }}</option>
            </select>
          </div>
          <div class="field">
            <label>Rol</label>
            <input :value="form.rol_nombre || 'Solicitante'" disabled />
          </div>

          <SistemaNotificacion
            v-if="mensaje"
            :key="mensaje"
            :tipo="esError ? 'error' : 'exito'"
            :titulo="esError ? 'No se pudo actualizar el perfil' : 'Perfil actualizado'"
            :descripcion="mensaje"
            :duracion="esError ? 0 : 5000"
            @close="mensaje = ''"
          />

          <div class="actions"><button type="submit" :disabled="guardando">{{ guardando ? 'Guardando...' : 'Guardar cambios' }}</button></div>
        </form>
      </section>


      <!-- ==============================
           SECCIÓN 2FA FACIAL
      ============================== -->

      <section class="face-section requests-card">
        <header class="face-header">
          <div class="face-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="8" r="4"/>
              <path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>
            </svg>
          </div>
          <div>
            <h3>Autenticación facial (2FA)</h3>
            <p v-if="!face2faEnabled">
              Agregue verificación facial para mayor seguridad en su cuenta.
            </p>
            <p v-else>
              Rostro registrado el {{ formatearFecha(faceRegisteredAt) }}.
            </p>
          </div>
        </header>

        <div class="face-status-badge" :class="face2faEnabled ? 'enabled' : 'disabled'">
          {{ face2faEnabled ? 'Activo' : 'Inactivo' }}
        </div>

        <div class="face-actions">
          <button
            v-if="!face2faEnabled"
            type="button"
            class="btn-face-register"
            :disabled="procesandoFace"
            @click="mostrarRegistroFacial = true"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"/>
              <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
            </svg>
            Registrar rostro
          </button>

          <template v-else>
            <button
              type="button"
              class="btn-face-update"
              :disabled="procesandoFace"
              @click="mostrarRegistroFacial = true"
            >
              Actualizar rostro
            </button>
            <button
              type="button"
              class="btn-face-disable"
              :disabled="procesandoFace"
              @click="deshabilitarFacial"
            >
              Deshabilitar
            </button>
          </template>
        </div>
      </section>


      <!-- MODAL DE CAPTURA -->
      <FaceCaptureModal
        v-if="mostrarRegistroFacial"
        titulo="Registrar rostro"
        modo="register"
        @cerrar="mostrarRegistroFacial = false"
        @capturas="registrarRostro"
      />

    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import SolicitanteMenu from '../components/SolicitanteMenu.vue'
import SistemaNotificacion from '../components/SistemaNotificacion.vue'
import FaceCaptureModal from '../components/FaceCaptureModal.vue'

const areas = ref([]), guardando = ref(false), mensaje = ref(''), esError = ref(false)
const form = reactive({ nombre_completo: '', email: '', area_id: '', rol_nombre: '' })

// Estado 2FA facial
const mostrarRegistroFacial = ref(false)
const face2faEnabled = ref(false)
const faceRegisteredAt = ref(null)
const procesandoFace = ref(false)
const token = () => localStorage.getItem('sigta_token')
const headers = () => ({ Authorization: `Token ${token()}`, Accept: 'application/json' })
const iniciales = computed(() => (form.nombre_completo || 'Usuario').split(' ').filter(Boolean).slice(0, 2).map(x => x[0]).join('').toUpperCase())

async function cargar() {
  try {
    const [perfilRespuesta, areasRespuesta, faceRespuesta] = await Promise.all([
      fetch('/api/usuarios/mi-perfil/', { headers: headers() }),
      fetch('/api/usuarios/areas/', { headers: headers() }),
      fetch('/api/usuarios/face-status/', { headers: headers() }),
    ])
    if (!perfilRespuesta.ok || !areasRespuesta.ok) throw new Error('No fue posible cargar el perfil.')
    Object.assign(form, await perfilRespuesta.json())
    const datosAreas = await areasRespuesta.json()
    areas.value = Array.isArray(datosAreas) ? datosAreas : (datosAreas.results || [])

    // Cargar estado facial
    if (faceRespuesta.ok) {
      const datosFace = await faceRespuesta.json()
      face2faEnabled.value = datosFace.face_2fa_enabled || false
      faceRegisteredAt.value = datosFace.face_registered_at || null
    }
  } catch (error) {
    console.error('Error cargando perfil:', error)
    esError.value = true; mensaje.value = error.message
  }
}

// Registrar rostro para 2FA
async function registrarRostro(capturas) {
  procesandoFace.value = true
  mensaje.value = ''; esError.value = false
  try {
    const respuesta = await fetch('/api/usuarios/face-register/', {
      method: 'POST',
      headers: { ...headers(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ frames: capturas }),
    })
    const datos = await respuesta.json()
    if (!respuesta.ok) throw new Error(datos.mensaje || 'No se pudo registrar el rostro.')
    face2faEnabled.value = true
    faceRegisteredAt.value = new Date().toISOString()
    mensaje.value = 'Rostro registrado correctamente. 2FA facial activado.'
  } catch (error) {
    console.error('Error registrando rostro:', error)
    esError.value = true; mensaje.value = error.message
  } finally {
    procesandoFace.value = false
    mostrarRegistroFacial.value = false
  }
}

// Deshabilitar 2FA facial
async function deshabilitarFacial() {
  if (!confirm('¿Deshabilitar autenticación facial?\n\nTendrá que registrar su rostro de nuevo si desea reactivarla.')) return
  procesandoFace.value = true
  mensaje.value = ''; esError.value = false
  try {
    const respuesta = await fetch('/api/usuarios/face-disable/', {
      method: 'DELETE',
      headers: headers(),
    })
    const datos = await respuesta.json()
    if (!respuesta.ok) throw new Error(datos.mensaje || 'No se pudo deshabilitar 2FA.')
    face2faEnabled.value = false
    faceRegisteredAt.value = null
    mensaje.value = '2FA facial deshabilitado.'
  } catch (error) {
    console.error('Error deshabilitando 2FA:', error)
    esError.value = true; mensaje.value = error.message
  } finally { procesandoFace.value = false }
}

// Formatear fecha
function formatearFecha(fecha) {
  if (!fecha) return ''
  return new Date(fecha).toLocaleDateString('es-BO', { year: 'numeric', month: 'long', day: 'numeric' })
}

async function guardar() {
  guardando.value = true; mensaje.value = ''; esError.value = false
  try {
    const respuesta = await fetch('/api/usuarios/mi-perfil/', {
      method: 'PATCH',
      headers: { ...headers(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre_completo: form.nombre_completo.trim(), area_id: form.area_id }),
    })
    const datos = await respuesta.json()
    if (!respuesta.ok) throw new Error(datos.nombre_completo || datos.area_id || datos.detalle || 'No se pudo actualizar el perfil.')
    Object.assign(form, datos)
    const usuario = JSON.parse(localStorage.getItem('sigta_usuario') || '{}')
    usuario.nombre = datos.nombre_completo; usuario.nombre_completo = datos.nombre_completo
    if (usuario.roles?.[0]) { usuario.roles[0].area_id = datos.area_id; usuario.roles[0].area_nombre = datos.area_nombre; usuario.roles[0].area = datos.area_nombre }
    localStorage.setItem('sigta_usuario', JSON.stringify(usuario))
    mensaje.value = 'Su nombre y área se guardaron correctamente.'
  } catch (error) {
    console.error('Error actualizando perfil:', error)
    esError.value = true; mensaje.value = error.message
  } finally { guardando.value = false }
}

onMounted(cargar)
</script>

<style scoped>
* { box-sizing: border-box; }
.layout { min-height: 100vh; display: flex; background: var(--sigta-azul-tenue); font-family: var(--sigta-fuente); }
.content { flex: 1; min-width: 0; padding: 27px 30px 45px; overflow-x: hidden; }
.topbar { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-bottom: 20px; }
.topbar h1 { margin: 0; color: var(--sigta-texto); font-size: 33px; }
.topbar p { margin: 5px 0 0; color: var(--sigta-texto-suave); font-size: 17px; }
.summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 13px; margin-bottom: 17px; }
.summary article { min-height: 104px; padding: 16px; border-top: 4px solid var(--sigta-mostaza); border-radius: 9px; background: white; box-shadow: 0 3px 12px rgba(0,0,0,.05); }
.summary span, .summary small { display: block; }
.summary span { color: var(--sigta-texto-suave); font-size: 14px; font-weight: 800; text-transform: uppercase; }
.summary strong { display: block; margin: 7px 0 4px; color: var(--sigta-azul); font-size: 31px; }
.summary strong.summary-text { overflow: hidden; font-size: 21px; line-height: 37px; text-overflow: ellipsis; white-space: nowrap; }
.summary small { color: var(--sigta-texto-suave); font-size: 14px; }
.requests-card { overflow: hidden; border-radius: 10px; background: white; box-shadow: 0 4px 14px rgba(0,0,0,.05); }
.identity { display: flex; align-items: center; gap: 14px; padding: 20px; border-bottom: 1px solid var(--sigta-azul-tenue); }
.avatar { width: 56px; height: 56px; display: grid; place-items: center; flex-shrink: 0; border-radius: 50%; background: var(--sigta-azul); color: white; font-size: 20px; font-weight: 800; }
.identity strong, .identity span { display: block; }
.identity strong { color: var(--sigta-azul); font-size: 18px; }
.identity span { margin-top: 4px; color: var(--sigta-texto-suave); font-size: 14px; }
form { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding: 20px; }
.field { display: flex; flex-direction: column; gap: 5px; }
.field label { color: var(--sigta-texto-suave); font-size: 14px; font-weight: 800; }
.field input, .field select { width: 100%; height: 40px; padding: 0 11px; border: 1px solid var(--sigta-borde); border-radius: 6px; background: white; color: var(--sigta-azul); font-family: inherit; font-size: 15px; outline: none; }
.field input:disabled { background: var(--sigta-azul-tenue); color: var(--sigta-texto-suave); }
.field small { color: var(--sigta-texto-suave); font-size: 12px; }
form :deep(.notificacion) { grid-column: 1 / -1; margin: 0; }
.actions { grid-column: 1 / -1; display: flex; justify-content: flex-end; padding-top: 4px; }
.actions button { min-height: 41px; padding: 0 18px; border: 0; border-radius: 7px; background: var(--sigta-azul); color: white; font-size: 15px; font-weight: 800; cursor: pointer; }
@media (max-width: 760px) { .layout { display: block; } .content { padding: 18px 15px 35px; } .summary, form { grid-template-columns: 1fr; } .actions { grid-column: auto; } .actions button { width: 100%; } }

/* 2FA Facial */
.face-section { margin-top: 17px; padding: 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 16px; }
.face-header { display: flex; align-items: center; gap: 14px; flex: 1; min-width: 280px; }
.face-icon { width: 48px; height: 48px; display: grid; place-items: center; border-radius: 12px; background: var(--sigta-azul-tenue); color: var(--sigta-azul); }
.face-icon svg { width: 24px; height: 24px; }
.face-header h3 { margin: 0 0 4px; color: var(--sigta-azul); font-size: 17px; }
.face-header p { margin: 0; color: var(--sigta-texto-suave); font-size: 13px; }
.face-status-badge { padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; text-transform: uppercase; }
.face-status-badge.enabled { background: var(--sigta-exito-fondo, #e6f7ed); color: var(--sigta-exito, #276749); }
.face-status-badge.disabled { background: var(--sigta-superficie, #f5f7fa); color: var(--sigta-texto-suave); }
.face-actions { display: flex; gap: 10px; flex-wrap: wrap; }
.btn-face-register { display: flex; align-items: center; gap: 8px; min-height: 40px; padding: 0 18px; border: 0; border-radius: 8px; background: var(--sigta-azul); color: white; font-size: 14px; font-weight: 700; cursor: pointer; }
.btn-face-register svg { width: 18px; height: 18px; }
.btn-face-register:hover:not(:disabled) { background: var(--sigta-azul-oscuro, #073563); }
.btn-face-update { min-height: 40px; padding: 0 16px; border: 1px solid var(--sigta-borde); border-radius: 8px; background: white; color: var(--sigta-texto); font-size: 14px; font-weight: 600; cursor: pointer; }
.btn-face-disable { min-height: 40px; padding: 0 16px; border: 1px solid var(--sigta-error, #c53030); border-radius: 8px; background: white; color: var(--sigta-error, #c53030); font-size: 14px; font-weight: 600; cursor: pointer; }
.btn-face-disable:hover:not(:disabled) { background: var(--sigta-error-fondo, #fde8e8); }
@media (max-width: 600px) { .face-section { flex-direction: column; align-items: stretch; } .face-actions { justify-content: stretch; } .face-actions button { flex: 1; } }
</style>
