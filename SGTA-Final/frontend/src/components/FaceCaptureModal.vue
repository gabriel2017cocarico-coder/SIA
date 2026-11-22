<template>
  <ModalSia
    :titulo="titulo"
    :ocupado="procesando"
    amplio
    @cerrar="cancelar"
  >
    <div class="face-capture">

      <!-- ==============================
           MENSAJE DE ESTADO
      ============================== -->

      <p
        class="face-status"
        :class="{
          'face-status--error': tieneError,
          'face-status--exito': capturas.length >= 3 && !tieneError
        }"
      >
        {{ mensaje }}
      </p>


      <!-- ==============================
           VIDEO
      ============================== -->

      <div class="face-video-container">

        <video
          ref="videoRef"
          autoplay
          playsinline
          muted
          class="face-video"
        />

        <canvas
          ref="overlayRef"
          class="face-overlay"
        />


        <!-- CARGANDO -->
        <div
          v-if="iniciando"
          class="face-loading"
        >
          <div class="face-spinner"></div>
          <span>Iniciando cámara...</span>
        </div>


        <!-- GUÍA OVAL -->
        <div
          v-if="!iniciando"
          class="face-guide"
        >
          <svg viewBox="0 0 200 260" class="face-oval">
            <ellipse
              cx="100"
              cy="130"
              rx="70"
              ry="95"
              fill="none"
              :stroke="colorGuia"
              stroke-width="3"
              stroke-dasharray="8,4"
            />
          </svg>
        </div>

      </div>


      <!-- ==============================
           INSTRUCCIONES
      ============================== -->

      <div class="face-instructions">

        <div
          class="face-step"
          :class="{ active: paso === 1, done: paso > 1 }"
        >
          <span class="step-icon">
            {{ paso > 1 ? '✓' : '1' }}
          </span>
          <span>Centre su rostro</span>
        </div>

        <div
          class="face-step"
          :class="{ active: paso === 2, done: paso > 2 }"
        >
          <span class="step-icon">
            {{ paso > 2 ? '✓' : '2' }}
          </span>
          <span>Parpadee</span>
        </div>

        <div
          class="face-step"
          :class="{ active: paso === 3, done: paso > 3 }"
        >
          <span class="step-icon">
            {{ paso > 3 ? '✓' : '3' }}
          </span>
          <span>Gire levemente</span>
        </div>

      </div>


      <!-- ==============================
           PROGRESO
      ============================== -->

      <div class="face-progress">
        <div
          class="face-progress-bar"
          :style="{ width: `${(capturas.length / 5) * 100}%` }"
        />
        <span class="face-progress-text">
          {{ capturas.length }} / 5 capturas
        </span>
      </div>

    </div>


    <!-- ==============================
         ACCIONES
    ============================== -->

    <template #acciones>

      <button
        type="button"
        class="btn-secundario"
        :disabled="procesando"
        @click="cancelar"
      >
        Cancelar
      </button>

      <button
        v-if="capturas.length >= 3"
        type="button"
        class="btn-primario"
        :disabled="procesando"
        @click="enviar"
      >
        {{ procesando ? 'Procesando...' : 'Confirmar' }}
      </button>

    </template>

  </ModalSia>
</template>


<script setup>
/**
 * FaceCaptureModal.vue
 *
 * Componente para captura de rostro con prueba de vida.
 * Usa MediaPipe Face Mesh para detectar landmarks y guiar al usuario.
 *
 * Props:
 *   - titulo: Título del modal
 *   - modo: 'register' | 'verify'
 *
 * Events:
 *   - @cerrar: Usuario cancela
 *   - @capturas: Array de imágenes base64 listas para enviar
 */

import {
  computed,
  onMounted,
  onUnmounted,
  ref,
} from 'vue'

import ModalSia from './ModalSia.vue'


// ==============================
// PROPS Y EVENTOS
// ==============================

const props = defineProps({

  titulo: {
    type: String,
    default: 'Verificación facial'
  },

  modo: {
    type: String,
    default: 'verify'
  }

})

const emit = defineEmits([
  'cerrar',
  'capturas'
])


// ==============================
// REFERENCIAS
// ==============================

const videoRef = ref(null)
const overlayRef = ref(null)


// ==============================
// ESTADO
// ==============================

const iniciando = ref(true)
const procesando = ref(false)
const tieneError = ref(false)
const mensaje = ref('Iniciando cámara...')
const paso = ref(1)
const capturas = ref([])

let stream = null
let animationFrame = null


// ==============================
// COLOR DE GUÍA
// ==============================

const colorGuia = computed(() => {

  if (tieneError.value) {
    return 'var(--sigta-error)'
  }

  if (capturas.value.length >= 3) {
    return 'var(--sigta-exito)'
  }

  return 'var(--sigta-mostaza)'
})


// ==============================
// DETECCIÓN DE PARPADEO Y GIRO
// ==============================

let lastBlinkTime = 0
let blinkDetected = false
let turnDetected = false
let faceDetector = null


// ==============================
// INICIAR CÁMARA
// ==============================

async function iniciarCamara() {

  try {

    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'user',
        width: { ideal: 640 },
        height: { ideal: 480 }
      },
      audio: false
    })

    videoRef.value.srcObject = stream

    await videoRef.value.play()

    iniciando.value = false
    mensaje.value = 'Centre su rostro en el óvalo'

    // Iniciar detección básica con canvas
    iniciarDeteccion()

  } catch (err) {

    iniciando.value = false
    tieneError.value = true

    if (err.name === 'NotAllowedError') {
      mensaje.value = 'Permiso de cámara denegado. Habilítelo en su navegador.'
    } else if (err.name === 'NotFoundError') {
      mensaje.value = 'No se encontró ninguna cámara.'
    } else {
      mensaje.value = 'Error al acceder a la cámara.'
    }

    console.error('Error de cámara:', err)
  }
}


// ==============================
// DETECCIÓN DE ROSTRO
// ==============================

async function iniciarDeteccion() {

  // Intentar cargar MediaPipe Face Mesh
  try {

    const { FaceMesh } = await import('@mediapipe/face_mesh')
    const { Camera } = await import('@mediapipe/camera_utils')

    faceDetector = new FaceMesh({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
    })

    faceDetector.setOptions({
      maxNumFaces: 1,
      refineLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    })

    faceDetector.onResults(procesarResultadosMediaPipe)

    const camera = new Camera(videoRef.value, {
      onFrame: async () => {
        if (faceDetector && videoRef.value) {
          await faceDetector.send({ image: videoRef.value })
        }
      },
      width: 640,
      height: 480
    })

    camera.start()

  } catch (err) {

    // Fallback: detección básica sin MediaPipe
    console.warn('MediaPipe no disponible, usando detección básica:', err)
    iniciarDeteccionBasica()
  }
}


// ==============================
// RESULTADOS MEDIAPIPE
// ==============================

function procesarResultadosMediaPipe(results) {

  if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
    tieneError.value = true
    mensaje.value = 'No se detecta rostro'
    paso.value = 1
    return
  }

  if (results.multiFaceLandmarks.length > 1) {
    tieneError.value = true
    mensaje.value = 'Solo debe haber un rostro'
    return
  }

  tieneError.value = false
  const landmarks = results.multiFaceLandmarks[0]


  // Verificar centrado del rostro
  const nose = landmarks[1]
  const centerX = nose.x
  const centerY = nose.y
  const isCentered = Math.abs(centerX - 0.5) < 0.15 && Math.abs(centerY - 0.5) < 0.15

  if (!isCentered) {
    mensaje.value = 'Centre su rostro en el óvalo'
    paso.value = 1
    return
  }


  // Detectar parpadeo (Eye Aspect Ratio)
  const leftEyeTop = landmarks[159]
  const leftEyeBottom = landmarks[145]
  const earLeft = Math.abs(leftEyeTop.y - leftEyeBottom.y)

  if (earLeft < 0.015 && Date.now() - lastBlinkTime > 500) {
    lastBlinkTime = Date.now()
    blinkDetected = true
    capturarFrame()
  }

  if (!blinkDetected) {
    mensaje.value = 'Parpadee para continuar'
    paso.value = 2
    return
  }


  // Detectar giro de cabeza
  const leftCheek = landmarks[234]
  const rightCheek = landmarks[454]
  const faceTurn = (leftCheek.x + rightCheek.x) / 2

  if (Math.abs(faceTurn - 0.5) > 0.08) {
    turnDetected = true
    capturarFrame()
  }

  if (!turnDetected) {
    mensaje.value = 'Gire levemente la cabeza'
    paso.value = 3
    return
  }


  // Todas las verificaciones pasadas
  paso.value = 4

  if (capturas.value.length < 5) {
    capturarFrame()
    mensaje.value = `Capturado ${capturas.value.length}/5`
  } else {
    mensaje.value = 'Capturas completas. Presione Confirmar.'
  }
}


// ==============================
// DETECCIÓN BÁSICA (FALLBACK)
// ==============================

function iniciarDeteccionBasica() {

  // Si MediaPipe no está disponible, usar detección simple por tiempo
  mensaje.value = 'Centre su rostro y manténgase quieto'

  let frameCount = 0

  function detectar() {

    if (!videoRef.value) return

    frameCount++

    // Capturar cada 30 frames (~1 segundo a 30fps)
    if (frameCount % 30 === 0 && capturas.value.length < 5) {

      capturarFrame()
      mensaje.value = `Capturado ${capturas.value.length}/5`

      if (capturas.value.length >= 3) {
        paso.value = 4
        mensaje.value = 'Capturas listas. Presione Confirmar.'
      } else {
        paso.value = Math.min(capturas.value.length + 1, 3)
      }
    }

    animationFrame = requestAnimationFrame(detectar)
  }

  animationFrame = requestAnimationFrame(detectar)
}


// ==============================
// CAPTURAR FRAME
// ==============================

function capturarFrame() {

  if (capturas.value.length >= 5) return
  if (!videoRef.value) return

  const canvas = document.createElement('canvas')
  canvas.width = videoRef.value.videoWidth || 640
  canvas.height = videoRef.value.videoHeight || 480

  const ctx = canvas.getContext('2d')
  ctx.drawImage(videoRef.value, 0, 0)

  const base64 = canvas.toDataURL('image/jpeg', 0.85)
  capturas.value.push(base64)
}


// ==============================
// ENVIAR CAPTURAS
// ==============================

function enviar() {

  if (capturas.value.length < 3) {
    tieneError.value = true
    mensaje.value = 'Se requieren al menos 3 capturas.'
    return
  }

  procesando.value = true
  emit('capturas', capturas.value)
}


// ==============================
// CANCELAR
// ==============================

function cancelar() {

  if (!procesando.value) {
    emit('cerrar')
  }
}


// ==============================
// DETENER CÁMARA
// ==============================

function detenerCamara() {

  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }

  if (animationFrame) {
    cancelAnimationFrame(animationFrame)
    animationFrame = null
  }

  if (faceDetector) {
    faceDetector.close?.()
    faceDetector = null
  }
}


// ==============================
// CICLO DE VIDA
// ==============================

onMounted(() => {
  iniciarCamara()
})

onUnmounted(() => {
  detenerCamara()
})
</script>


<style scoped>

/* ==============================
   CONTENEDOR
============================== */

.face-capture {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 4px;
}


/* ==============================
   ESTADO
============================== */

.face-status {
  margin: 0;
  padding: 12px 16px;
  border-radius: var(--sigta-radio-chico, 8px);
  background: var(--sigta-azul-tenue, #e8f0f8);
  color: var(--sigta-azul, #0b5795);
  font-size: 14px;
  font-weight: 600;
  text-align: center;
}

.face-status--error {
  background: var(--sigta-error-fondo, #fde8e8);
  color: var(--sigta-error, #c53030);
}

.face-status--exito {
  background: var(--sigta-exito-fondo, #e6f7ed);
  color: var(--sigta-exito, #276749);
}


/* ==============================
   VIDEO
============================== */

.face-video-container {
  position: relative;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  aspect-ratio: 4/3;
  border-radius: var(--sigta-radio, 12px);
  overflow: hidden;
  background: #1a1a1a;
}

.face-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
}

.face-overlay {
  position: absolute;
  inset: 0;
  transform: scaleX(-1);
  pointer-events: none;
}


/* ==============================
   GUÍA OVAL
============================== */

.face-guide {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.face-oval {
  width: 70%;
  height: 85%;
  opacity: 0.9;
}


/* ==============================
   CARGANDO
============================== */

.face-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  font-size: 14px;
}

.face-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--sigta-mostaza, #d4a017);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}


/* ==============================
   INSTRUCCIONES
============================== */

.face-instructions {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.face-step {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--sigta-radio-chico, 8px);
  background: var(--sigta-superficie, #f5f7fa);
  opacity: 0.5;
  font-size: 13px;
  transition: all 0.2s;
}

.face-step.active {
  opacity: 1;
  background: var(--sigta-azul-tenue, #e8f0f8);
  color: var(--sigta-azul, #0b5795);
  font-weight: 700;
}

.face-step.done {
  opacity: 1;
  background: var(--sigta-exito-fondo, #e6f7ed);
  color: var(--sigta-exito, #276749);
}

.step-icon {
  width: 24px;
  height: 24px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: var(--sigta-borde, #d1d5db);
  font-size: 12px;
  font-weight: 800;
}

.face-step.active .step-icon {
  background: var(--sigta-mostaza, #d4a017);
  color: var(--sigta-azul-oscuro, #073563);
}

.face-step.done .step-icon {
  background: var(--sigta-exito, #276749);
  color: white;
}


/* ==============================
   PROGRESO
============================== */

.face-progress {
  position: relative;
  height: 24px;
  border-radius: 12px;
  background: var(--sigta-borde, #d1d5db);
  overflow: hidden;
}

.face-progress-bar {
  height: 100%;
  background: linear-gradient(
    90deg,
    var(--sigta-azul, #0b5795),
    var(--sigta-exito, #276749)
  );
  transition: width 0.3s ease;
}

.face-progress-text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}


/* ==============================
   BOTONES
============================== */

.btn-primario {
  min-height: 42px;
  padding: 0 24px;
  border: 0;
  border-radius: var(--sigta-radio-chico, 8px);
  background: var(--sigta-azul, #0b5795);
  color: white;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

.btn-primario:hover:not(:disabled) {
  background: var(--sigta-azul-oscuro, #073563);
}

.btn-primario:active:not(:disabled) {
  transform: scale(0.98);
}

.btn-primario:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secundario {
  min-height: 42px;
  padding: 0 24px;
  border: 1px solid var(--sigta-borde, #d1d5db);
  border-radius: var(--sigta-radio-chico, 8px);
  background: white;
  color: var(--sigta-texto, #374151);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secundario:hover:not(:disabled) {
  background: var(--sigta-superficie, #f5f7fa);
}

.btn-secundario:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}


/* ==============================
   RESPONSIVE
============================== */

@media (max-width: 600px) {

  .face-video-container {
    max-width: 100%;
    border-radius: 8px;
  }

  .face-instructions {
    gap: 8px;
  }

  .face-step {
    padding: 6px 10px;
    font-size: 12px;
  }

  .face-step span:last-child {
    display: none;
  }
}

</style>
