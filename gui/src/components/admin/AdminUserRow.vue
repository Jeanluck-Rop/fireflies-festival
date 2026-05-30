<template>
  <div class="user-row" :class="{ expanded: isExpanded }">

    <!-- Header clickable -->
    <div class="user-header" @click="toggle">
      <div class="user-avatar">
	<img
	  v-if="usuario.avatar"
	  :src="usuario.avatar"
	  :alt="usuario.nombre"
	  class="avatar-img"/>
	<span v-else class="avatar-initials">{{ initials }}</span>
      </div>

      <div class="user-info">
        <div class="user-top">
          <span class="user-nombre">{{ usuario.nombre }} {{ usuario.apellidos }}</span>
          <span :class="['rol-badge', usuario.rol === 'ADMIN' ? 'badge-admin' : 'badge-cliente']">
            {{ usuario.rol === 'ADMIN' ? 'Admin' : 'Cliente' }}
          </span>
        </div>
        <div class="user-meta">
          <span>{{ usuario.email }}</span>
          <IconDot size="4px" class="sep" />
          <span>{{ metodoPagoLabel }}</span>
          <IconDot size="4px" class="sep" />
          <span>Desde {{ formatDate(usuario.created_at) }}</span>
        </div>
      </div>

      <!-- Acciones (detener propagacion para no togglear el row) -->
      <div class="user-actions" @click.stop>
        <button
	  v-if="isSuperuser"
	  class="btn-deactivate"
	  @click="showDeactivateDialog = true">
	  Eliminar
	</button>
      </div>

      <IconChevronUp   v-if="isExpanded" size="10px" class="chevron" />
      <IconChevronDown v-else             size="10px" class="chevron" />
    </div>

    <!-- Reservaciones expandidas -->
    <div v-if="isExpanded" class="user-reservaciones">

      <div class="reserv-header">
        <span class="reserv-title">
          Reservaciones de {{ usuario.nombre }} {{ usuario.apellidos }}
        </span>
        <span class="reserv-count font-mono">{{ filteredReserv.length }}</span>
      </div>

      <!-- Filtros -->
      <div class="reserv-filters">
        <select v-model="filterEstado" class="filter-select">
          <option value="">Todos los estados</option>
          <option value="ACTIVA">Activa</option>
          <option value="EN_PROCESO">En proceso</option>
          <option value="COMPLETADA">Completada</option>
          <option value="CANCELADA">Cancelada</option>
        </select>
      </div>

      <!-- Lista de reservaciones, reutilizamos ReservationRow -->
      <div class="reserv-list">
        <ReservationRow
          v-for="r in filteredReserv"
          :key="r.id"
          :reservacion="r"
          @cancelar="handleCancelReserv" />
        <div v-if="filteredReserv.length === 0" class="empty-reserv">
          Sin reservaciones
        </div>
      </div>
    </div>

    <!-- Dialogo desactivar -->
    <AppConfirmDialog
      v-model="showDeactivateDialog"
      title="Eliminar usuario"
      confirm-label="Sí, eliminar usuario"
      variant="danger"
      @confirm="$emit('delete', usuario.id)">
      ¿Eliminar la cuenta de
      <strong>{{ usuario.nombre }} {{ usuario.apellidos }}</strong>?
      Esta acción es permanente e irreversible.
    </AppConfirmDialog>

  </div>
</template>

<script setup lang="ts">
 import { ref, computed } from 'vue'
 import { useAuthStore } from '../../stores/auth'
 import { useNotification } from '../../composables/useNotification'
 import type { Reservacion } from '../../stores/reservations'
 import AppConfirmDialog from '../ui/AppConfirmDialog.vue'
 import ReservationRow   from '../reservations/ReservationRow.vue'
 import IconDot          from '../svg/IconDot.vue'
 import IconChevronUp    from '../svg/IconChevronUp.vue'
 import IconChevronDown  from '../svg/IconChevronDown.vue'

 const auth = useAuthStore()
 const { show } = useNotification()
 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
 const isSuperuser = computed(() => !!(auth.user as any)?.is_superuser)

 export interface UsuarioAdmin {
   id: number;
   nombre: string;
   apellidos: string; email: string
   rol: 'CLIENTE' | 'ADMIN';
   metodo_pago: string | null
   created_at: string;
   avatar?: string | null
 }

 const props = defineProps<{
   usuario: UsuarioAdmin
   reservaciones: Reservacion[]   // ya filtradas por este usuario
 }>()

 defineEmits<{ delete: [id: number] }>()

 //Expand
 const isExpanded         = ref(false)
 const showDeactivateDialog = ref(false)
 const filterEstado       = ref('')

 function toggle() { isExpanded.value = !isExpanded.value }

 const filteredReserv = computed(() => {
   if (!filterEstado.value) return props.reservaciones
   return props.reservaciones.filter(r => r.estado === filterEstado.value)
 })

 //Cancelar reservacion (perspectiva admin)
 function handleCancelReserv(r: Reservacion) {
   if (USE_MOCK) {
     show('normal', `Reservación #${r.id} cancelada`)
     return
   }
   // TODO backend: PATCH /api/reservaciones/{id}/cancelar/
 }

 //Helpers
 const initials = computed(() =>
   ((props.usuario.nombre[0] ?? '') + (props.usuario.apellidos[0] ?? '')).toUpperCase()
 )

 const metodoPagoMap: Record<string, string> = {
   PAYPAL:'PayPal', STRIPE:'Stripe', DEBITO:'Débito', CREDITO:'Crédito',
 }
 const metodoPagoLabel = computed(() =>
   metodoPagoMap[props.usuario.metodo_pago ?? ''] ?? 'Sin método de pago'
 )

 function formatDate(s: string): string {
   const d = new Date(s)
   const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
   return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`
 }
</script>

<style scoped>
 .user-row {
   border: 1px solid var(--color-border);
   border-radius: 12px; overflow: hidden;
   background: rgba(255,255,255,0.02); transition: border-color 0.15s;
 }
 .user-row.expanded { border-color: rgba(123,167,212,0.2); }

 .user-header {
   display: flex; align-items: center; gap: 0.875rem;
   padding: 0.875rem 1rem; cursor: pointer; transition: background 0.15s;
 }
 .user-header:hover { background: rgba(255,255,255,0.03); }

 .user-avatar {
   width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
   background: linear-gradient(135deg, #7BA7D4, #A8C8F0);
   overflow: hidden;
   display: flex; align-items: center; justify-content: center;
 }
 .avatar-img {
   width: 100%; height: 100%; object-fit: cover; display: block;
 }
 .avatar-initials {
   color: #0A1525; font-size: 12px; font-weight: 700;
 }
 .user-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 0.2rem; }

 .user-top { display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; }
 .user-nombre { font-size: 13.5px; font-weight: 600; color: var(--color-bone); }

 .user-meta {
   display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;
   font-size: 11.5px; color: var(--color-bone-mute);
 }
 .sep { display: flex; align-items: center; }

 .rol-badge {
   font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 999px;
 }
 .badge-cliente  { background: rgba(123,216,176,0.1);  color: var(--color-green); }
 .badge-admin    { background: rgba(123,167,212,0.12); color: var(--color-admin-accent,#7BA7D4); }
 .badge-inactivo { background: rgba(255,138,123,0.1);  color: var(--color-danger); }

 .user-actions { display: flex; gap: 0.5rem; flex-shrink: 0; }
 .btn-deactivate {
   height: 28px; padding: 0 0.75rem; border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.3); background: transparent;
   color: var(--color-danger); font-size: 11.5px; cursor: pointer; transition: all 0.15s;
 }
 .btn-deactivate:hover { background: rgba(255,138,123,0.08); }

 .chevron { color: var(--color-bone-mute); flex-shrink: 0; }

 /* Reservaciones expandidas */
 .user-reservaciones {
   border-top: 1px solid var(--color-border); padding: 1rem;
   background: rgba(123,167,212,0.02); display: flex; flex-direction: column; gap: 0.875rem;
 }

 .reserv-header { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
 .reserv-title  { font-size: 12px; font-weight: 600; color: var(--color-bone-soft); }
 .reserv-count  { font-size: 11px; color: var(--color-bone-mute); font-family: var(--font-mono); }

 .reserv-filters { display: flex; gap: 0.5rem; }
 .filter-select {
   height: 30px; padding: 0 1.5rem 0 0.75rem; border-radius: 999px;
   border: 1px solid var(--color-border); background: rgba(255,255,255,0.04);
   color: var(--color-bone); font-size: 11.5px; outline: none; appearance: none; cursor: pointer;
 }

 .reserv-list { display: flex; flex-direction: column; gap: 0.5rem; }

 .empty-reserv {
   padding: 1.5rem; text-align: center; font-size: 12px; color: var(--color-bone-mute);
   border: 1px dashed rgba(255,255,255,0.07); border-radius: 8px;
 }
</style>
