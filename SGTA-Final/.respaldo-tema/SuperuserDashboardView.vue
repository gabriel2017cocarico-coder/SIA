<template>

  <div class="layout">

    <SuperuserMenu />

    <main class="main">

      <header class="page-header">

        <div>
          <h1>
            Panel de Superusuario
          </h1>

          <p>
            Administración técnica del sistema: usuarios, roles y
            permisos, auditoría y configuración de SIGTA.
          </p>
        </div>

      </header>


      <section class="quick-grid">

        <button
          class="quick-card"
          type="button"
          @click="router.push('/superuser/usuarios')"
        >
          <div class="quick-icon">
            👥
          </div>

          <div>
            <strong>
              Usuarios
            </strong>

            <span>
              Crear, modificar, activar e inactivar
              cuentas institucionales.
            </span>
          </div>
        </button>


        <button
          class="quick-card"
          type="button"
          @click="router.push('/superuser/roles-permisos')"
        >
          <div class="quick-icon">
            🔐
          </div>

          <div>
            <strong>
              Roles y permisos
            </strong>

            <span>
              Definir qué puede visualizar y ejecutar
              cada rol dentro de SIGTA.
            </span>
          </div>
        </button>


        <button
          class="quick-card"
          type="button"
          @click="router.push('/superuser/auditoria')"
        >
          <div class="quick-icon">
            📜
          </div>

          <div>
            <strong>
              Auditoría
            </strong>

            <span>
              Consultar accesos, acciones y trazabilidad
              de los procesos del sistema.
            </span>
          </div>
        </button>


        <button
          class="quick-card"
          type="button"
          @click="router.push('/superuser/smtp')"
        >
          <div class="quick-icon">
            📧
          </div>

          <div>
            <strong>
              Correo SMTP
            </strong>

            <span>
              Configurar el canal de correo para
              recuperación y notificaciones.
            </span>
          </div>
        </button>


        <button
          class="quick-card"
          type="button"
          @click="router.push('/superuser/preferencias')"
        >
          <div class="quick-icon">
            ⚙️
          </div>

          <div>
            <strong>
              Preferencias
            </strong>

            <span>
              Configurar parámetros generales del
              funcionamiento de SIGTA.
            </span>
          </div>
        </button>

      </section>

    </main>

  </div>

</template>


<script setup>

import {
  useRouter
} from 'vue-router'

import SuperuserMenu
  from '../components/SuperuserMenu.vue'


const router =
  useRouter()

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
  margin-bottom: 22px;
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


/* =========================================================
   ACCESOS RÁPIDOS
========================================================= */

.quick-grid {
  display: grid;
  grid-template-columns: repeat(2,1fr);
  gap: 15px;
}


.quick-card {
  min-height: 105px;
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 19px;
  border: 1px solid #dae2e8;
  border-radius: 9px;
  background: #fbfcfd;
  text-align: left;
  cursor: pointer;
  transition:
    border-color .2s,
    box-shadow .2s,
    transform .1s;
}


.quick-card:hover {
  border-color: #6576B4;
  box-shadow: 0 5px 14px rgba(0,0,0,.07);
}


.quick-card:active {
  transform: scale(.995);
}


.quick-icon {
  width: 46px;
  height: 46px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #6576B4;
  font-size: 22px;
}


.quick-card strong {
  display: block;
  color: #17324a;
  font-size: 18px;
}


.quick-card span {
  display: block;
  margin-top: 4px;
  color: #6f7e8b;
  font-size: 15px;
  line-height: 1.5;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (max-width: 900px) {

  .quick-grid {
    grid-template-columns: 1fr;
  }
}


@media (max-width: 760px) {

  .layout {
    display: block;
  }

  .main {
    padding: 16px;
  }
}

</style>
