<template>
  <div class="users-admin">

    <!-- Toolbar -->
    <SearchBar v-model="filters" :filters="filterDefs" />

    <div class="list-header">
      <span class="list-count">{{ filteredUsers.length }} usuarios</span>
    </div>

    <!-- Lista -->
    <div class="users-list">
      <AdminUserRow
        v-for="u in filteredUsers"
        :key="u.id"
        :usuario="u"
        :reservaciones="reservacionesDe(u.email)"
        @delete="handleDelete" />

      <div v-if="filteredUsers.length === 0" class="empty-state">
        No se encontraron usuarios con los filtros aplicados
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
 import { ref, computed, onMounted } from 'vue'
 import { useNotification } from '../../composables/useNotification'
 import SearchBar   from '../ui/SearchBar.vue'
 import AdminUserRow from './AdminUserRow.vue'
 import { useAuthStore } from '../../stores/auth'
 import { userService } from '../../services/userService'
 import type { UsuarioAdmin } from './AdminUserRow.vue'
 import type { Reservacion } from '../../stores/reservations'
 import type { FilterDef, FilterValues } from '../ui/SearchBar.vue'

 const { show } = useNotification()
 const authStore = useAuthStore()
 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
 const listaUsuarios = ref<UsuarioAdmin[]>([])
 const cargando = ref(false)
 const errorMsg = ref('')
 //Mock usuarios
 const mockUsers = ref<UsuarioAdmin[]>([
   { id:1,  nombre:'Fulanito',  apellidos:'Pérez',     email:'fulanito@example.com', rol:'CLIENTE', metodo_pago:'CREDITO',  created_at:'2026-01-15T10:00:00Z'},
   { id:2,  nombre:'Ana',       apellidos:'García',    email:'ana@example.com',      rol:'CLIENTE', metodo_pago:'PAYPAL',   created_at:'2026-02-20T14:00:00Z' },
   { id:3,  nombre:'Carlos',    apellidos:'López',     email:'carlos@example.com',   rol:'CLIENTE', metodo_pago:null,       created_at:'2026-03-01T09:00:00Z' },
   { id:4,  nombre:'Mariana',   apellidos:'Torres',    email:'mariana@example.com',  rol:'CLIENTE', metodo_pago:'DEBITO',   created_at:'2026-03-15T11:00:00Z' },
   { id:5,  nombre:'Roberto',   apellidos:'Sánchez',   email:'roberto@example.com',  rol:'CLIENTE', metodo_pago:'STRIPE',   created_at:'2026-04-02T08:00:00Z' },
 ])

 //Mock reservaciones (por email de usuario)
 const mockReservaciones = ref<(Reservacion & { usuario_email: string })[]>([
   {
     id:1, usuario_email:'fulanito@example.com',
     parque:{ id:1, nombre:'Parque Sierra Chincua', imagen_mapa:null },
     hospedaje:{ id:1, nombre:'Cabaña del Bosque' },
     fecha_inicio:'2026-06-15', fecha_fin:'2026-06-18',
     num_personas:4, tipo_visita:'CABANA', estado:'ACTIVA',
     created_at:'2026-05-01T10:00:00Z', monto:2400,
   },
   {
     id:2, usuario_email:'fulanito@example.com',
     parque:{ id:1, nombre:'Parque Sierra Chincua', imagen_mapa:null },
     hospedaje:{ id:3, nombre:'Zona Camping Sur' },
     fecha_inicio:'2026-03-15', fecha_fin:'2026-03-16',
     num_personas:1, tipo_visita:'CAMPING', estado:'CANCELADA',
     created_at:'2026-03-01T11:00:00Z', monto:350,
   },
   {
     id:3, usuario_email:'ana@example.com',
     parque:{ id:2, nombre:'Parque Piedra Herrada', imagen_mapa:null },
     hospedaje:{ id:5, nombre:'Cabaña a orillas del río' },
     fecha_inicio:'2026-08-10', fecha_fin:'2026-08-15',
     num_personas:2, tipo_visita:'CABANA', estado:'ACTIVA',
     created_at:'2026-05-20T11:00:00Z', monto:5500,
   },
   {
     id:4, usuario_email:'carlos@example.com',
     parque:{ id:3, nombre:'Parque El Rosario', imagen_mapa:null },
     hospedaje:{ id:7, nombre:'Gran Cabaña Familiar' },
     fecha_inicio:'2026-04-01', fecha_fin:'2026-04-03',
     num_personas:6, tipo_visita:'CABANA', estado:'COMPLETADA',
     created_at:'2026-03-01T09:00:00Z', monto:5000,
   },
   {
     id:5, usuario_email:'mariana@example.com',
     parque:{ id:1, nombre:'Parque Sierra Chincua', imagen_mapa:null },
     hospedaje:{ id:2, nombre:'Cabaña Pareja' },
     fecha_inicio:'2026-07-10', fecha_fin:'2026-07-12',
     num_personas:2, tipo_visita:'CABANA', estado:'EN_PROCESO',
     created_at:'2026-05-10T14:00:00Z', monto:1800,
   },
 ])

 const clientes = async () => {
   if (USE_MOCK) {
     listaUsuarios.value = mockUsers.value
     return
   }
   cargando.value = true
   errorMsg.value = ''
   try {
     const data = await userService.obtenerClientes(authStore.token)
     listaUsuarios.value = data
   } catch (error) {
     errorMsg.value = 'Error al cargar usuarios'
     console.error(error)
   } finally {
     cargando.value = false
   }
 }

  onMounted(() => {
    clientes()
  })

 function reservacionesDe(email: string): Reservacion[] {
   return mockReservaciones.value
			   .filter(r => r.usuario_email === email)
			   .map(({ usuario_email: _e, ...r }) => r as Reservacion)
 }

 //Filtros
 const filterDefs: FilterDef[] = [
   { key: 'nombre', type: 'text', placeholder: 'Buscar por nombre o correo...' },
   { key: 'rol', type: 'select', placeholder: 'Rol',
     options: [{ label:'Cliente', value:'CLIENTE' }, { label:'Admin', value:'ADMIN' }] },
   { key: 'estado', type: 'select', placeholder: 'Estado',
     options: [{ label:'Activo', value:'activo' }, { label:'Inactivo', value:'inactivo' }] },
 ]
 const filters = ref<FilterValues>({ nombre: '', rol: '', estado: '' })

 const filteredUsers = computed(() => {
   let r = listaUsuarios.value
   if (filters.value.nombre) {
     const q = filters.value.nombre.toLowerCase()
     r = r.filter(u =>
       `${u.nombre} ${u.apellidos} ${u.email}`.toLowerCase().includes(q)
     )
   }
   if (filters.value.rol)
     r = r.filter(u => u.rol === filters.value.rol)
   if (filters.value.estado === 'activo')
     r = r.filter(u => u.activo)
   if (filters.value.estado === 'inactivo')
     r = r.filter(u => !u.activo)
   return r
 })

 //Acciones
 async function handleDelete(id: number) {
   if (USE_MOCK) {
     mockUsers.value = mockUsers.value.filter(u => u.id !== id)
     show('normal', 'Usuario eliminado')
     return
   }
   // TODO backend: PATCH /api/usuarios/{id}/desactivar/
 }

 async function handleActivate(id: number) {
   if (USE_MOCK) {
     const idx = mockUsers.value.findIndex(u => u.id === id)
     if (idx >= 0) mockUsers.value[idx].activo = true
     show('exito', 'Cuenta activada')
     return
   }
   // TODO backend: PATCH /api/usuarios/{id}/activar/
 }
</script>

<style scoped>
 .users-admin { display: flex; flex-direction: column; gap: 1rem; }

 .list-header { display: flex; align-items: center; justify-content: space-between; }
 .list-count  { font-size: 12px; color: var(--color-bone-mute); font-family: var(--font-mono); }

 .users-list  { display: flex; flex-direction: column; gap: 0.5rem; }

 .empty-state {
   padding: 3rem; text-align: center;
   font-size: 13px; color: var(--color-bone-mute);
   border: 1px dashed rgba(255,255,255,0.07); border-radius: 12px;
 }
</style>
