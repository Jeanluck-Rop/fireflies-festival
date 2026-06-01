<template>
  <div class="admin-view">
    <div class="admin-view-inner">
      <div class="view-header">
        <h1 class="view-title">{{ isSuperuser ? 'Parques' : 'Hospedajes' }}</h1>
        <p class="view-sub">
          {{ isSuperuser
          ? 'Gestiona los parques, hospedajes y reservaciones'
          : 'Gestiona los hospedajes y reservaciones de tu parque' }}
        </p>
      </div>
      <ParksInfo />
    </div>
  </div>
</template>

<script setup lang="ts">
 import { computed } from 'vue'
 import { useAuthStore } from '../../stores/auth'
 import ParksInfo from '../../components/admin/ParksInfo.vue'

 const auth = useAuthStore()
 const isSuperuser = computed(() => !!(auth.user as any)?.is_superuser)
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
   max-width: 1100px;
   display: flex;
   flex-direction: column;
   gap: 1.5rem;
 }
 .view-header { display: flex; flex-direction: column; gap: 0.25rem; }
 .view-title { font-size: 22px; font-weight: 600; color: var(--color-bone); letter-spacing: -0.02em; }
 .view-sub { font-size: 13px; color: var(--color-bone-mute); }
</style>
