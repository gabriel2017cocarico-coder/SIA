<template>
  <div class="layout">
    <SolicitanteMenu />
    <main class="page">

    <section class="profile">

      <div class="avatar">
        {{
          iniciales
        }}
      </div>

      <h1>
        {{ usuario?.nombre_completo || usuario?.nombre }}
      </h1>

      <p class="email">
        {{ usuario?.email }}
      </p>

      <div class="divider"></div>

      <div class="information">

        <div>
          <span>Rol</span>

          <strong>
            {{
              usuario?.roles?.[0]?.nombre
              || 'Solicitante'
            }}
          </strong>
        </div>

        <div>
          <span>Área</span>

          <strong>
            {{
              usuario?.roles?.[0]?.area
              || 'Sin área'
            }}
          </strong>
        </div>

        <div>
          <span>Estado de cuenta</span>

          <strong class="active">
            Activa
          </strong>
        </div>

      </div>

    </section>

    </main>
  </div>
</template>


<script setup>
import {
  computed,
  ref
} from 'vue'

import SolicitanteMenu from '../components/SolicitanteMenu.vue'

const usuario = ref(
  JSON.parse(
    localStorage.getItem(
      'sigta_usuario'
    )
    || '{}'
  )
)


const iniciales = computed(() => {

  const nombre =
    usuario.value?.nombre_completo
    || usuario.value?.nombre
    || 'Usuario'

  return nombre
    .split(' ')
    .slice(0, 2)
    .map(parte => parte[0])
    .join('')
    .toUpperCase()
})
</script>


<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  background: #f3f6fb;
}

.page {
  min-height: 100vh;
  flex: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 20px;

  background: #f3f6fb;

  font-family:
    Arial,
    Helvetica,
    sans-serif;
}

@media (max-width: 760px) {
  .layout { display: block; }
}

.profile {
  width: 100%;
  max-width: 470px;

  padding: 30px;

  background: white;

  border-top:
    4px solid #f2c400;

  border-radius: 14px;

  box-shadow:
    0 20px 50px
    rgba(0,0,0,.2);

  text-align: center;
}

.avatar {
  width: 75px;
  height: 75px;

  margin: auto;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #073b6f;

  color: white;

  font-size: 25px;
  font-weight: 800;
}

h1 {
  margin-bottom: 4px;

  color: #17324a;
}

.email {
  color: #71818f;
}

.divider {
  height: 3px;

  margin: 22px 0;

  background: #f2c400;

  border-radius: 3px;
}

.information {
  text-align: left;
}

.information div {
  padding: 13px 0;

  border-bottom:
    1px solid #edf0f2;
}

.information span {
  display: block;

  color: #81909b;

  font-size: 10px;
}

.information strong {
  color: #314b60;

  font-size: 13px;
}

.active {
  color: #237344 !important;
}

button {
  width: 100%;
  height: 43px;

  margin-top: 22px;

  border: none;

  border-radius: 7px;

  background: #073b6f;

  color: white;

  font-weight: 700;

  cursor: pointer;
}
</style>
