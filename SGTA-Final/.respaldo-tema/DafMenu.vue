<template>
  <aside class="sidebar">

    <!-- =====================================================
         MARCA + BOTÓN DESPLEGABLE (móvil)
    ====================================================== -->

    <div class="brand-row">

      <div class="brand">

        <div class="logo">
          <img src="/img/emi.jpg" alt="EMI" class="logo-img">
        </div>

        <div class="brand-text">
          <h2>SIGTA</h2>

          <span>
            Sistema Integral de Gestión
          </span>
        </div>

      </div>

      <button
        type="button"
        class="menu-toggle"
        :aria-expanded="menuAbierto"
        aria-label="Mostrar opciones del menú"
        @click="menuAbierto = !menuAbierto"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

    </div>


    <!-- =====================================================
         CONTENIDO DESPLEGABLE
    ====================================================== -->

    <div
      class="sidebar-body"
      :class="{ abierto: menuAbierto }"
    >

    <!-- =====================================================
         DAF
    ====================================================== -->

    <div class="section-title">
      DAF
    </div>

    <nav @click="menuAbierto = false">

      <router-link
        to="/daf/dashboard"
        class="menu-item"
      >
        <span class="icon">
          🛒
        </span>

        <span>
          Solicitudes
        </span>
      </router-link>

    </nav>


    <!-- =====================================================
         CERRAR SESIÓN
    ====================================================== -->

    <button
      class="logout"
      type="button"
      @click="cerrarSesion"
    >
      Cerrar sesión
    </button>

    </div>

  </aside>
</template>


<script setup>

import {
  ref
} from 'vue'

import {
  useRouter
} from 'vue-router'


const router =
  useRouter()


/* =========================================================
   MENÚ MÓVIL (desplegable)
========================================================= */

const menuAbierto =
  ref(false)


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
   SIDEBAR
========================================================= */

.sidebar {

  position: sticky;

  top: 0;

  width: 255px;
  min-width: 255px;

  height: 100vh;

  display: flex;
  flex-direction: column;

  padding:
    20px
    14px;

  overflow-y: auto;
  overflow-x: hidden;

  background: #6576B4;

  color: #ffffff;

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}


/* Scroll discreto */

.sidebar::-webkit-scrollbar {
  width: 5px;
}

.sidebar::-webkit-scrollbar-thumb {

  border-radius: 10px;

  background:
    rgba(
      255,
      255,
      255,
      .18
    );
}


/* =========================================================
   MARCA
========================================================= */

.brand-row {

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding:
    0
    8px
    20px;

  border-bottom:
    1px solid
    rgba(
      255,
      255,
      255,
      .17
    );
}


.brand {

  display: flex;
  align-items: center;

  gap: 12px;
}


.logo {

  width: 48px;
  height: 48px;

  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 10px;

  overflow: hidden;

  background: #FFFF00;
}


.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}


.brand-text {
  min-width: 0;
}


.brand h2 {

  margin: 0;

  font-size: 22px;
}


.brand span {

  display: block;

  margin-top: 3px;

  color: #c4d2df;

  font-size: 11px;

  line-height: 1.3;
}


/* =========================================================
   SECCIONES
========================================================= */

.section-title {

  margin:
    17px
    10px
    6px;

  color: #82a5c6;

  font-size: 10px;

  font-weight: 800;

  letter-spacing: 1px;
}


/* =========================================================
   NAVEGACIÓN
========================================================= */

nav {

  display: flex;

  flex-direction: column;

  gap: 3px;
}


.menu-item {

  position: relative;

  min-height: 46px;

  display: flex;

  align-items: center;

  gap: 11px;

  padding:
    0
    11px;

  border-radius: 7px;

  color: #e8eff6;

  text-decoration: none;

  font-size: 13px;

  transition:
    background .2s,
    color .2s,
    padding .2s;
}


.icon {

  width: 27px;

  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 18px;
  line-height: 1;
}


.menu-item:hover {

  background:
    rgba(
      255,
      255,
      255,
      .08
    );

  color: #ffffff;
}


.menu-item.router-link-active {

  padding-left: 8px;

  border-left:
    3px solid #FFFF00;

  background:
    rgba(
      255,
      255,
      255,
      .13
    );

  color: #FFFF00;

  font-weight: 700;
}


.menu-item.router-link-active
.icon {

  color: #FFFF00;
}


/* =========================================================
   CERRAR SESIÓN
========================================================= */

.logout {

  width: 100%;

  min-height: 54px;

  flex-shrink: 0;

  position: sticky;

  bottom: 0;

  margin-top: auto;

  border: none;

  border-radius: 7px;

  background: #FFFF00;

  color: #17324a;

  font-size: 16px;

  font-weight: 800;

  cursor: pointer;

  transition:
    transform .15s ease,
    box-shadow .15s ease;
}


.logout:hover {

  transform: scale(1.05);

  box-shadow:
    0
    4px
    12px
    rgba(0,0,0,.18);
}


/* =========================================================
   BOTÓN DESPLEGABLE (solo móvil)
========================================================= */

.menu-toggle {

  display: none;

  flex-shrink: 0;

  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;

  width: 34px;
  height: 34px;

  border: none;
  border-radius: 7px;

  background:
    rgba(255, 255, 255, .1);

  cursor: pointer;
}


.menu-toggle span {

  width: 16px;
  height: 2px;

  border-radius: 2px;

  background: #ffffff;

  transition:
    transform .2s ease,
    opacity .2s ease;
}


.menu-toggle[aria-expanded="true"] span:nth-child(1) {
  transform: translateY(6px) rotate(45deg);
}

.menu-toggle[aria-expanded="true"] span:nth-child(2) {
  opacity: 0;
}

.menu-toggle[aria-expanded="true"] span:nth-child(3) {
  transform: translateY(-6px) rotate(-45deg);
}


/* =========================================================
   CUERPO DESPLEGABLE
========================================================= */

.sidebar-body {

  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media (
  max-width: 760px
) {

  .sidebar {

    position: relative;

    width: 100%;
    min-width: 100%;

    height: auto;

    min-height: auto;

    overflow-y: visible;
  }


  .menu-toggle {

    display: flex;
  }


  .sidebar-body {

    max-height: 0;

    overflow: hidden;

    transition:
      max-height .25s ease;
  }


  .sidebar-body.abierto {

    max-height: min(65vh, 460px);

    overflow-y: auto;

    -webkit-overflow-scrolling: touch;
  }


  .logout {

    margin-top: 20px;
  }

}

</style>
