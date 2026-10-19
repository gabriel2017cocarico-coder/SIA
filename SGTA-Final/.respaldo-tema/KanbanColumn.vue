<template>
  <section class="column">

    <header>

      <strong>
        {{ titulo }}
      </strong>

      <span>
        0
      </span>

    </header>


    <div class="body">

      <div class="empty">
        Sin mantenimientos
      </div>

    </div>

  </section>
</template>


<script setup>
defineProps({
  titulo: {
    type: String,
    required: true,
  },
})
</script>


<style scoped>
.column {
  width: 200px;

  border-radius: 8px;

  overflow: hidden;
}

header {
  min-height: 44px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 8px;

  padding: 0 11px;

  background: #dce8f5;

  color: #173a5b;

  font-size: 10px;
}

header span {
  width: 22px;
  height: 22px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 50%;

  background: #073b6f;

  color: #ffffff;

  font-size: 8px;
}

.body {
  min-height: 270px;

  padding: 9px;

  background: #e9eef5;
}

.empty {
  margin-top: 50px;

  color: #98a5b1;

  text-align: center;

  font-size: 9px;
}
</style>