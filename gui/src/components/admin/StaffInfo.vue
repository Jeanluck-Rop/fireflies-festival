<template>
  <div class="staff-admin">

    <!-- Toolbar -->
    <div class="toolbar">
      <SearchBar v-model="filters" :filters="filterDefs" class="toolbar-search" />
      <button class="btn-nuevo" @click="showAddDialog = true">
        <IconPlus size="12px" /> Agregar staff
      </button>
    </div>

    <div class="list-header">
      <span class="list-count">{{ filteredStaff.length }} miembros de staff</span>
    </div>

    <!-- Lista -->
    <div class="staff-list">
      <AdminStaffRow
        v-for="s in filteredStaff"
        :key="s.id"
        :staff="s"
        @delete="handleDelete"
        @update-parque="handleUpdateParque" />

      <div v-if="filteredStaff.length === 0" class="empty-state">
        No se encontraron miembros de staff
      </div>
    </div>

    <!-- Dialogo agregar staff -->
    <transition name="dialog-fade">
      <div v-if="showAddDialog" class="dialog-backdrop" @click.self="closeAddDialog">
        <div class="dialog-box">
          <div class="dialog-header">
            <h3 class="dialog-title">Agregar staff</h3>
            <button class="dialog-close" @click="closeAddDialog">
              <svg width="11" height="11" viewBox="0 0 10 10" fill="none">
                <path d="M1 1l8 8M9 1l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="add-form">
            <div class="form-row-2">
              <div class="field-group">
                <label class="field-label">Nombre</label>
                <input v-model="newStaff.nombre" class="form-input" placeholder="Nombre" />
              </div>
              <div class="field-group">
                <label class="field-label">Apellidos</label>
                <input v-model="newStaff.apellidos" class="form-input" placeholder="Apellidos" />
              </div>
            </div>
            <div class="field-group">
              <label class="field-label">Correo electrónico</label>
              <input
                v-model="newStaff.email"
                type="email"
                class="form-input"
                :class="{ 'input-error': addError }"
                placeholder="correo@ejemplo.com"
                @input="addError = ''" />
              <span v-if="addError" class="error-text">{{ addError }}</span>
            </div>
            <div class="field-group">
              <label class="field-label">Parque asignado</label>
              <select v-model="newStaff.parque_asignado" class="form-input form-select">
                <option :value="null">Sin asignar por ahora</option>
                <option v-for="p in PARQUES" :key="p.id" :value="p.id">{{ p.nombre }}</option>
              </select>
            </div>
            <p class="add-hint">
              Se generará una contraseña automáticamente y se enviará al correo del nuevo staff junto con un mensaje de bienvenida.
            </p>
          </div>

          <div class="dialog-actions">
            <button class="btn-cancel" @click="closeAddDialog">Cancelar</button>
            <button class="btn-save" :disabled="creating" @click="handleCreate">
              {{ creating ? 'Creando...' : 'Crear staff' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup lang="ts">
 import { ref, reactive, computed } from 'vue'
 import { useNotification } from '../../composables/useNotification'
 import SearchBar from '../ui/SearchBar.vue'
 import AdminStaffRow from './AdminStaffRow.vue'
 import IconPlus from '../svg/IconPlus.vue'
 import type { StaffData } from './AdminStaffRow.vue'
 import type { FilterDef, FilterValues } from '../ui/SearchBar.vue'

 const { show } = useNotification()
 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'

 const PARQUES = [
   { id: 1, nombre: 'Parque Sierra Chincua' },
   { id: 2, nombre: 'Parque Piedra Herrada' },
   { id: 3, nombre: 'Parque El Rosario'     },
 ]

 //Mock data
 const mockStaff = ref<StaffData[]>([
   { id:10, nombre:'Lucía',   apellidos:'Ramírez',   email:'lucia@admin.com',   parque_asignado:1 },
   { id:11, nombre:'Miguel',  apellidos:'Herrera',   email:'miguel@admin.com',  parque_asignado:2 },
   { id:12, nombre:'Sofía',   apellidos:'Mendoza',   email:'sofia@admin.com',   parque_asignado:3 },
   { id:13, nombre:'Diego',   apellidos:'Castro',    email:'diego@admin.com',   parque_asignado:1 },
   { id:14, nombre:'Valeria', apellidos:'Flores',    email:'valeria@admin.com', parque_asignado:null },
 ])

 //Filtros
 const filterDefs: FilterDef[] = [
   { key: 'nombre', type: 'text', placeholder: 'Buscar por nombre o correo...' },
   { key: 'parque', type: 'select', placeholder: 'Parque',
     options: PARQUES.map(p => ({ label: p.nombre, value: String(p.id) }))
   },
 ]
 const filters = ref<FilterValues>({ nombre: '', parque: '' })

 const filteredStaff = computed(() => {
   let r = mockStaff.value
   if (filters.value.nombre) {
     const q = filters.value.nombre.toLowerCase()
     r = r.filter(s => `${s.nombre} ${s.apellidos} ${s.email}`.toLowerCase().includes(q))
   }
   if (filters.value.parque)
     r = r.filter(s => s.parque_asignado === Number(filters.value.parque))
   return r
 })

 //Agregar staff
 const showAddDialog = ref(false)
 const creating = ref(false)
 const addError = ref('')

 const newStaff = reactive({
   nombre: '', apellidos: '', email: '',
   parque_asignado: null as number | null,
 })

 function closeAddDialog() {
   showAddDialog.value = false
   addError.value = ''
   Object.assign(newStaff, { nombre:'', apellidos:'', email:'', parque_asignado:null })
 }

 async function handleCreate() {
   addError.value = ''
   if (!newStaff.nombre || !newStaff.apellidos || !newStaff.email) {
     addError.value = 'Completa todos los campos obligatorios'
     return
   }
   const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
   if (!EMAIL_RE.test(newStaff.email)) {
     addError.value = 'Correo inválido'
     return
   }

   creating.value = true

   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 600))

     // Verificar que el correo no esté en uso
     const exists = mockStaff.value.some(
       s => s.email.toLowerCase() === newStaff.email.toLowerCase()
     )
     if (exists) {
       addError.value = 'Ya existe un staff con este correo'
       creating.value = false
       return
     }

     const newId = Math.max(...mockStaff.value.map(s => s.id)) + 1
     mockStaff.value.push({
       id: newId,
       nombre:         newStaff.nombre,
       apellidos:      newStaff.apellidos,
       email:          newStaff.email,
       parque_asignado: newStaff.parque_asignado,
     })
     show('exito', `Staff ${newStaff.nombre} creado. Se envió correo de bienvenida con contraseña.`)
     closeAddDialog()
   } else {
     // TODO backend: POST /api/staff/
     // {nombre, apellidos, email, parque_asignado}
     // El backend:
     //   - Verifica que el correo no exista
     //   - Crea el usuario con rol ADMIN, is_staff=true
     //   - Genera contraseña aleatoria
     //   - Envía correo de bienvenida con contraseña
     // Si el correo ya existe → 400 con mensaje de error
   }

   creating.value = false
 }

 //Acciones
 async function handleDelete(id: number) {
   if (USE_MOCK) {
     mockStaff.value = mockStaff.value.filter(s => s.id !== id)
     show('normal', 'Cuenta de staff eliminada')
     return
   }
   // TODO backend: DELETE /api/staff/{id}/
 }

 function handleUpdateParque(id: number, parqueId: number | null) {
   const idx = mockStaff.value.findIndex(s => s.id === id)
   if (idx >= 0) mockStaff.value[idx].parque_asignado = parqueId
   // El correo de reasignación lo envía el backend en PATCH /api/staff/{id}/
 }
</script>

<style scoped>
 .staff-admin { display: flex; flex-direction: column; gap: 1rem; }

 .toolbar { display: flex; align-items: flex-end; gap: 0.75rem; flex-wrap: wrap; }
 .toolbar-search { flex: 1; }

 .btn-nuevo {
   height: 40px; padding: 0 1rem; border-radius: 8px;
   border: 1px solid rgba(123,167,212,0.3); background: transparent;
   color: var(--color-admin-accent, #7BA7D4); font-size: 13px;
   cursor: pointer; display: flex; align-items: center; gap: 0.4rem;
   transition: all 0.15s; white-space: nowrap; flex-shrink: 0;
 }
 .btn-nuevo:hover { background: rgba(123,167,212,0.1); }

 .list-header { display: flex; align-items: center; }
 .list-count  { font-size: 12px; color: var(--color-bone-mute); font-family: var(--font-mono); }

 .staff-list { display: flex; flex-direction: column; gap: 0.5rem; }

 .empty-state {
   padding: 3rem; text-align: center; font-size: 13px; color: var(--color-bone-mute);
   border: 1px dashed rgba(255,255,255,0.07); border-radius: 12px;
 }

 /* Dialogo */
 .dialog-backdrop {
   position: fixed; inset: 0; z-index: 9999;
   background: rgba(0,0,0,0.65); backdrop-filter: blur(4px);
   display: flex; align-items: center; justify-content: center; padding: 1rem;
 }
 .dialog-box {
   background: #0d1a10; border: 1px solid rgba(123,167,212,0.18);
   border-radius: 16px; padding: 1.75rem; width: min(480px, 100%);
   box-shadow: 0 24px 48px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 1.25rem;
 }
 .dialog-header { display: flex; align-items: center; justify-content: space-between; }
 .dialog-title  { font-size: 18px; font-weight: 600; color: var(--color-bone); }
 .dialog-close  {
   width: 28px; height: 28px; border-radius: 8px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); cursor: pointer;
   display: flex; align-items: center; justify-content: center; transition: background 0.15s;
 }
 .dialog-close:hover { background: rgba(255,255,255,0.06); }

 /* Formulario */
 .add-form   { display: flex; flex-direction: column; gap: 0.875rem; }
 .form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
 .field-group { display: flex; flex-direction: column; gap: 0.3rem; }
 .field-label {
   font-size: 10.5px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-bone-mute);
 }
 .form-input {
   height: 38px; padding: 0 0.75rem; border-radius: 8px;
   border: 1px solid var(--color-border); background: rgba(255,255,255,0.04);
   color: var(--color-bone); font-size: 13px; font-family: var(--font-sans);
   outline: none; width: 100%; transition: border-color 0.2s;
 }
 .form-input:focus { border-color: rgba(123,167,212,0.4); }
 .form-input.input-error { border-color: rgba(255,138,123,0.4); }
 .form-select { appearance: none; cursor: pointer; }
 .error-text  { font-size: 11px; color: var(--color-danger); }

 .add-hint {
   font-size: 11.5px; color: var(--color-bone-mute);
   font-style: italic; line-height: 1.5; margin: 0;
 }

 .dialog-actions { display: flex; gap: 0.75rem; justify-content: flex-end; }
 .btn-cancel {
   height: 36px; padding: 0 1rem; border-radius: 999px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); font-size: 13px; cursor: pointer;
 }
 .btn-save {
   height: 36px; padding: 0 1.25rem; border-radius: 999px; border: none;
   background: var(--color-admin-accent, #7BA7D4); color: #0A1525;
   font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s;
 }
 .btn-save:disabled { opacity: 0.5; cursor: not-allowed; }

 /* Animacion */
 .dialog-fade-enter-active, .dialog-fade-leave-active { transition: opacity 0.2s ease; }
 .dialog-fade-enter-from, .dialog-fade-leave-to { opacity: 0; }
</style>
