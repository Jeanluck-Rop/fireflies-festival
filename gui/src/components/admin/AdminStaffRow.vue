<template>
  <div class="staff-row">

    <!-- Info principal -->
    <div class="staff-avatar">
      <img
	v-if="staff.avatar"
	:src="staff.avatar"
	:alt="staff.nombre"
	class="avatar-img"
      />
      <span v-else class="avatar-initials">{{ initials }}</span>
    </div>

    <div class="staff-info">
      <div class="staff-top">
        <span class="staff-nombre">{{ staff.nombre }} {{ staff.apellidos }}</span>
        <span class="staff-badge">Staff</span>
      </div>
      <span class="staff-email">{{ staff.email }}</span>
    </div>

    <!-- Parque asignado -->
    <div class="parque-section">
      <label class="parque-label">Parque asignado</label>
      <div class="parque-control">
        <select v-model="parqueLocal" class="parque-select">
          <option :value="null">Sin asignar</option>
          <option v-for="p in PARQUES" :key="p.id" :value="p.id">{{ p.nombre }}</option>
        </select>
        <button
          v-if="parqueChanged"
          class="btn-save-parque"
          :disabled="savingParque"
          @click="saveParque">
          {{ savingParque ? '...' : 'Guardar' }}
        </button>
      </div>
    </div>

    <!-- Acciones superuser -->
    <div v-if="isSuperuser" class="staff-actions">
      <button class="btn-delete" @click="showDeleteDialog = true">
        Eliminar
      </button>
    </div>

    <!-- Dialogo eliminar -->
    <AppConfirmDialog
      v-model="showDeleteDialog"
      title="Eliminar staff"
      confirm-label="Sí, eliminar"
      variant="danger"
      @confirm="$emit('delete', staff.id)">
      ¿Eliminar la cuenta de
      <strong>{{ staff.nombre }} {{ staff.apellidos }}</strong>? Esta acción es irreversible.
    </AppConfirmDialog>

  </div>
</template>

<script setup lang="ts">
 import { ref, computed, watch } from 'vue'
 import { useAuthStore } from '../../stores/auth'
 import { useNotification } from '../../composables/useNotification'
 import AppConfirmDialog from '../ui/AppConfirmDialog.vue'

 const auth = useAuthStore()
 const { show } = useNotification()
 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
 const isSuperuser = computed(() => !!(auth.user as any)?.is_superuser)

 export interface StaffData {
   id: number;
   nombre: string;
   apellidos: string
   email: string;
   parque_asignado: number | null
   avatar?: string | null
 }

 const PARQUES = [
   { id: 1, nombre: 'Parque Sierra Chincua'  },
   { id: 2, nombre: 'Parque Piedra Herrada'  },
   { id: 3, nombre: 'Parque El Rosario'      },
 ]

 const props = defineProps<{ staff: StaffData }>()
 const emit  = defineEmits<{
   delete: [id: number]
   updateParque: [id: number, parqueId: number | null]
 }>()

 const parqueLocal  = ref<number | null>(props.staff.parque_asignado)
 const savingParque = ref(false)
 const showDeleteDialog = ref(false)

 const parqueChanged = computed(() => parqueLocal.value !== props.staff.parque_asignado)

 //Si el prop cambia desde afuera, sincronizar
 watch(() => props.staff.parque_asignado, v => { parqueLocal.value = v })

 async function saveParque() {
   savingParque.value = true
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 400))
     emit('updateParque', props.staff.id, parqueLocal.value)
     const nombre = PARQUES.find(p => p.id === parqueLocal.value)?.nombre ?? 'sin parque'
     show('exito', `Parque de ${props.staff.nombre} actualizado a ${nombre}`)
     // Backend enviaria correo de reasignación
   } else {
     // TODO backend: PATCH /api/staff/{id}/ con parque_asignado
     // El backend envía correo de reasignación al staff
   }
   savingParque.value = false
 }

 const initials = computed(() =>
   ((props.staff.nombre[0] ?? '') + (props.staff.apellidos[0] ?? '')).toUpperCase()
 )
</script>

<style scoped>
 .staff-row {
   display: flex;
   align-items: center;
   gap: 1rem;
   padding: 0.875rem 1rem;
   border-radius: 12px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.02);
   transition: background 0.15s;
   flex-wrap: wrap;
 }
 .staff-row:hover { background: rgba(255,255,255,0.03); }

 .staff-avatar {
   width: 36px; height: 36px; border-radius: 50%; flex-shrink: 0;
   background: linear-gradient(135deg, #7BA7D4, #A8C8F0);
   overflow: hidden;
   display: flex; align-items: center; justify-content: center;
 }
 .avatar-img      { width: 100%; height: 100%; object-fit: cover; display: block; }
 .avatar-initials { color: #0A1525; font-size: 12px; font-weight: 700; }
 
 .staff-info { flex: 1; min-width: 140px; display: flex; flex-direction: column; gap: 0.15rem; }
 .staff-top  { display: flex; align-items: center; gap: 0.5rem; }
 .staff-nombre { font-size: 13.5px; font-weight: 600; color: var(--color-bone); }
 .staff-badge  {
   font-size: 10px; font-weight: 600; padding: 1px 7px; border-radius: 999px;
   background: rgba(123,167,212,0.12); color: var(--color-admin-accent, #7BA7D4);
 }
 .staff-email { font-size: 11.5px; color: var(--color-bone-mute); }

 /* Parque asignado */
 .parque-section { display: flex; flex-direction: column; gap: 0.25rem; min-width: 200px; }
 .parque-label   {
   font-size: 10px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.07em; color: var(--color-bone-mute);
 }
 .parque-control { display: flex; gap: 0.5rem; align-items: center; }
 .parque-select  {
   height: 32px; padding: 0 0.75rem; border-radius: 8px;
   border: 1px solid var(--color-border); background: rgba(255,255,255,0.04);
   color: var(--color-bone); font-size: 12.5px; font-family: var(--font-sans);
   outline: none; appearance: none; cursor: pointer; transition: border-color 0.2s;
   flex: 1;
 }
 .parque-select:focus { border-color: rgba(123,167,212,0.4); }

 .btn-save-parque {
   height: 32px; padding: 0 0.875rem; border-radius: 999px; border: none;
   background: var(--color-admin-accent, #7BA7D4); color: #0A1525;
   font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap;
   transition: all 0.15s;
 }
 .btn-save-parque:disabled { opacity: 0.5; cursor: not-allowed; }

 /* Acciones */
 .staff-actions { flex-shrink: 0; }
 .btn-delete {
   height: 30px; padding: 0 0.75rem; border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.3); background: transparent;
   color: var(--color-danger); font-size: 11.5px; cursor: pointer; transition: all 0.15s;
 }
 .btn-delete:hover { background: rgba(255,138,123,0.08); }
</style>
