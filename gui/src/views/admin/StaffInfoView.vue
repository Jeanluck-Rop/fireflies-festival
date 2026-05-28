<template>
  <div class="admin-view">
    <div class="admin-view-inner">
      <div class="admin-placeholder">
        <div class="placeholder-icon">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="1" y="1" width="30" height="30" rx="8" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 3"/>
            <path d="M16 10v12M10 16h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <h1 class="placeholder-title">Equipo Staff</h1>
        <p class="placeholder-sub">Detalles del equipo de staff (próximamente)</p>
      </div>
    </div>
  </div>
</template>
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
 .admin-placeholder {
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   gap: 1rem;
   padding: 4rem 2rem;
   border: 1px dashed rgba(123,167,212,0.2);
   border-radius: 16px;
   background: rgba(123,167,212,0.03);
   text-align: center;
 }
 .placeholder-icon { color: rgba(123,167,212,0.4); }
 .placeholder-title {
   font-size: 22px;
   font-weight: 600;
   color: var(--color-bone);
   letter-spacing: -0.02em;
 }
 .placeholder-sub {
   font-size: 14px;
   color: var(--color-bone-mute);
   max-width: 320px;
 }
</style>
