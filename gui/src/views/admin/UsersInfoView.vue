<template>
  <div class="admin-view">
    <div class="admin-view-inner">
      <div class="view-header">
        <h1 class="view-title">Usuarios</h1>
        <p class="view-sub">Gestiona las cuentas y reservaciones de usuarios</p>
      </div>
      <UsersInfo />
    </div>
  </div>
</template>

<script setup lang="ts">
 import UsersInfo from '../../components/admin/UsersInfo.vue'
</script>

<style scoped>
 .admin-view {
   min-height: calc(100vh - 76px);
   margin-top: 76px;
   display: flex;
   justify-content: center;
   padding: 2rem 1.5rem;
   box-sizing: border-box;
 }
 .admin-view-inner {
   width: 100%;
   max-width: 900px;
   display: flex;
   flex-direction: column;
   gap: 1.5rem;
 }
 .view-header { display: flex; flex-direction: column; gap: 0.25rem; }
 .view-title  { font-size: 22px; font-weight: 600; color: var(--color-bone); letter-spacing: -0.02em; }
 .view-sub    { font-size: 13px; color: var(--color-bone-mute); }
</style>
