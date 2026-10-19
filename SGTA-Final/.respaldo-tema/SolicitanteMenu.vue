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

        <div>

          <h2>
            SIGTA
          </h2>

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
         MENÚ
    ====================================================== -->

    <div class="section-title">
      MI PORTAL
    </div>


    <nav @click="menuAbierto = false">

      <!-- INICIO -->

      <router-link
        to="/usuario/dashboard"
        class="menu-item"
      >

        <span class="icon">
          🏠
        </span>

        Inicio

      </router-link>


      <!-- MIS SOLICITUDES -->

      <router-link
        to="/usuario/mis-solicitudes"
        class="menu-item"
      >

        <span class="icon">
          📋
        </span>

        Mis solicitudes

      </router-link>


      <!-- PERFIL -->

      <router-link
        to="/usuario/perfil"
        class="menu-item"
      >

        <span class="icon">
          👤
        </span>

        Mi perfil

      </router-link>

      <router-link
        to="/usuario/configuracion"
        class="menu-item"
      >
        <span class="icon">⚙️</span>
        Configuración
      </router-link>

    </nav>


    <!-- =====================================================
         CERRAR SESIÓN
    ====================================================== -->

    <button
      class="logout"
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


// ==========================================================
// MENÚ MÓVIL (hamburguesa)
// ==========================================================

const menuAbierto =
  ref(false)


// ==========================================================
// USUARIO
// ==========================================================

const usuario =
  ref(null)


const guardado =
  localStorage.getItem(
    'sigta_usuario'
  )


if (guardado) {

  try {

    usuario.value =
      JSON.parse(
        guardado
      )

  } catch (error) {

    console.error(
      'Error leyendo usuario:',
      error
    )
  }
}


// ==========================================================
// CERRAR SESIÓN
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


/* =========================================================
   SIDEBAR
========================================================= */

.sidebar {

  width: 235px;

  min-width: 235px;

  height: 100vh;

  position: sticky;

  top: 0;

  overflow-y: auto;


  display: flex;

  flex-direction: column;


  padding:
    18px
    12px;


  background:
    #6576B4;

  color:
    #ffffff;


  font-family:
    Arial,
    Helvetica,
    sans-serif;
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
    7px
    18px;


  border-bottom:
    1px solid
    rgba(
      255,
      255,
      255,
      .16
    );
}


.brand {

  display: flex;

  align-items: center;


  gap: 10px;
}


.logo {

  width: 43px;

  height: 43px;


  display: flex;

  align-items: center;

  justify-content: center;


  flex-shrink: 0;


  border-radius: 8px;

  overflow: hidden;


  background:
    #FFFF00;
}


.logo-img {

  width: 100%;

  height: 100%;

  object-fit: contain;
}


.brand h2 {

  margin: 0;


  font-size: 19px;
}


.brand span {

  display: block;


  margin-top: 2px;


  color:
    #afc2d4;


  font-size: 10px;
}


/* =========================================================
   TÍTULO DE SECCIÓN
========================================================= */

.section-title {

  margin:
    12px
    8px
    6px;


  color:
    #82a5c6;


  font-size: 10px;

  font-weight: 800;


  letter-spacing: .9px;
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

  min-height: 48px;


  display: flex;

  align-items: center;


  gap: 11px;


  padding:
    0
    10px;


  border-radius: 7px;


  color:
    #e7eef5;


  text-decoration: none;


  font-size: 20px;


  transition:
    background .2s,
    color .2s;
}


.icon {

  width: 28px;


  flex-shrink: 0;


  display: flex;

  align-items: center;

  justify-content: center;


  font-size: 20px;

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
}


/* =========================================================
   OPCIÓN ACTIVA
========================================================= */

.menu-item.router-link-active {

  padding-left: 7px;


  border-left:
    3px solid
    #FFFF00;


  background:
    rgba(
      255,
      255,
      255,
      .12
    );


  color:
    #FFFF00;


  font-weight: 700;
}


.menu-item.router-link-active
.icon {

  color:
    #FFFF00;
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


  background:
    #FFFF00;


  color:
    #17324a;


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


  background:
    #ffffff;


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
   CUERPO DESPLEGABLE (contenido del menú)
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

    width: 100%;

    min-width: 100%;

    height: auto;

    position: static;

    top: auto;


    padding-bottom: 12px;
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

}


</style>
