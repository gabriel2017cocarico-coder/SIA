<template>
  <main class="page">

    <section class="card">

      <div class="logo">
        EMI
      </div>

      <h1>
        {{ titulo }}
      </h1>

      <p>
        Este módulo forma parte de SIGTA y
        será habilitado en la siguiente etapa
        de implementación.
      </p>

      <button
        @click="router.push('/usuario/dashboard')"
      >
        Volver al inicio
      </button>

    </section>

  </main>
</template>


<script setup>
import {
  computed
} from 'vue'

import {
  useRoute,
  useRouter
} from 'vue-router'


const route = useRoute()
const router = useRouter()


const titulo = computed(() => {

  if (
    route.path.includes('compras')
  ) {
    return 'Solicitudes de Compras'
  }

  if (
    route.path.includes('notificaciones')
  ) {
    return 'Notificaciones'
  }

  if (
    route.path.includes('perfil')
  ) {
    return 'Mi Perfil'
  }

  return 'SIGTA'
})
</script>


<style scoped>
.page {
  min-height: 100vh;

  display: flex;

  align-items: center;
  justify-content: center;

  padding: 20px;

  background:
    linear-gradient(
      135deg,
      #0a2f54,
      #1f628f
    );

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}

.card {
  width: 100%;
  max-width: 430px;

  padding: 35px;

  text-align: center;

  background: white;

  border-top:
    4px solid #f2c400;

  border-radius: 14px;

  box-shadow:
    0 20px 50px
    rgba(0,0,0,.22);
}

.logo {
  width: 60px;
  height: 60px;

  margin:
    0 auto 18px;

  display: flex;

  align-items: center;
  justify-content: center;

  border:
    3px solid #f2c400;

  border-radius: 12px;

  background: #073b6f;

  color: white;

  font-weight: 800;
}

h1 {
  margin:
    0 0 10px;

  color: #17324a;
}

p {
  color: #71818f;

  font-size: 13px;

  line-height: 1.5;
}

button {
  margin-top: 15px;

  height: 42px;

  padding:
    0 18px;

  border: none;

  border-radius: 7px;

  background: #073b6f;

  color: white;

  font-weight: 700;

  cursor: pointer;
}
</style>