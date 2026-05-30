<template>
  <div class="admin-view">
    <div class="admin-view-inner">
      <div class="view-header">
        <h1 class="view-title">Nueva Reservación</h1>
        <p class="view-sub">
          {{ isStaff ? parqueNombre : 'Completa el formulario para registrar una reservación' }}
        </p>
      </div>
      <ReserveUser />
    </div>
  </div>
</template>

<script setup lang="ts">
 import { computed } from 'vue'
 import { useAuthStore } from '../../stores/auth'
 import ReserveUser from '../../components/admin/ReserveUser.vue'

 const auth = useAuthStore()

 const isStaff = computed(() => !!(auth.user?.is_staff && !(auth.user as any)?.is_superuser))
 const parqueNombre = computed(() => {
   const id = (auth.user as any)?.parque_asignado
   const nombres: Record<number, string> = {
     1: 'Parque Sierra Chincua',
     2: 'Parque Piedra Herrada',
     3: 'Parque El Rosario',
   }
   return id ? `Parque asignado: ${nombres[id] ?? `#${id}`}` : ''
 })
</script>


<style scoped>
 .admin-view {
   min-height: calc(100vh - 76px);
   margin-top: 76px;
   display: flex;
   justify-content: center;
   align-items: center;
   padding: 2rem 1.5rem;
 }
 .admin-view-inner {
   width: 100%;
   max-width: 82.5rem;
 }
 .view-header {
   display: flex;
   flex-direction: column;
   gap: 0.45rem; }
 .view-title {
   font-size: 22px; font-weight: 600;
   color: var(--color-bone); letter-spacing: -0.02em;
 }
 .view-sub {
   font-size: 13px;
   color: var(--color-bone-mute);
   margin-bottom: 10px;
 }
</style>
