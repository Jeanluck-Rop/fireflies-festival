<template>
  <div class="reservations-view">
    <div class="reservations-inner">

      <!-- Header de la seccion -->
      <div class="section-header">
        <div class="section-title-group">
          <h1 class="section-title">Mis Reservaciones</h1>
          <span v-if="!loading" class="section-count">
            {{ filteredReservaciones.length }}
            {{ filteredReservaciones.length === 1 ? 'reservación' : 'reservaciones' }}
          </span>
        </div>

        <!-- Boton nueva reservacion -->
	<AppButton variant="primary" @click="router.push('/reservar')">
	  <IconPlus size="12px" style="margin-right: 6px" />
	  Nueva reservación
	</AppButton>
      </div>

      <!-- SearchBar -->
      <SearchBar
        v-model="filters"
        :filters="filterDefs"
      />

      <!-- Lista -->
      <div class="reservations-list">

        <!-- Loading -->
        <div v-if="loading" class="list-loading">
          <FireflyLogo :pulse="true" :drift="false" size="w-10 h-10" />
          <span>Cargando reservaciones...</span>
        </div>

        <!-- Sin resultados de búsqueda -->
        <div v-else-if="filteredReservaciones.length === 0 && reservaciones.length > 0" class="list-empty">
          <p class="empty-title">Sin resultados</p>
          <p class="empty-sub">Intenta ajustar los filtros de búsqueda</p>
        </div>

        <!-- Sin reservaciones -->
        <div v-else-if="reservaciones.length === 0" class="list-empty">
          <FireflyLogo :pulse="true" :drift="false" size="w-12 h-12" />
          <p class="empty-title">Aún no tienes reservaciones</p>
          <p class="empty-sub">Explora los parques y reserva tu lugar en el festival</p>
          <AppButton variant="outline" @click="router.push('/parques')">
            Explorar parques
          </AppButton>
        </div>

        <!-- Filas -->
        <template v-else>
          <ReservationRow
            v-for="reservacion in filteredReservaciones"
            :key="reservacion.id"
            :reservacion="reservacion"
            @cancelar="handleCancelar"/>
        </template>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
 import { ref, computed, onMounted, reactive } from 'vue'
 import { useRouter } from 'vue-router'
 import FireflyLogo from '../components/ui/FireflyLogo.vue'
 import AppButton from '../components/ui/AppButton.vue'
 import SearchBar from '../components/ui/SearchBar.vue'
 import ReservationRow from '../components/reservations/ReservationRow.vue'
 import IconPlus from '../components/svg/IconPlus.vue'
 import { reserveService } from '../services/reserveService'
 import { useReservationsStore } from '../stores/reservations'
 import type { Reservacion } from '../stores/reservations'
 import type { FilterDef, FilterValues } from '../components/ui/SearchBar.vue'

 const router = useRouter()
 const store = useReservationsStore()

 const reservaciones = computed(() => store.reservaciones)
 const loading = computed(() => store.loading)

 //Filtros
 const filterDefs: FilterDef[] = [
   {
     key: 'parque',
     type: 'text',
     placeholder: 'Buscar por parque...',
   },
   {
     key: 'estado',
     type: 'select',
     placeholder: 'Estado',
     options: [
       { label: 'Activa',      value: 'ACTIVA' },
       { label: 'En proceso',  value: 'EN_PROCESO' },
       { label: 'Completada',  value: 'COMPLETADA' },
       { label: 'Cancelada',   value: 'CANCELADA' },
     ],
   },
   {
     key:  'fechas',
     type: 'daterange',
   },
   {
     key:         'precio',
     type:        'number',
     placeholder: 'Precio máx.',
   },
 ]

 const filters = ref<FilterValues>({
   parque: '',
   estado: '',
   fechas_desde: '',
   fechas_hasta: '',
   // precio: '',  // TODO backend
 })

 //Lógica de filtrado
 const filteredReservaciones = computed(() => {
   let result = reservaciones.value

   // Filtro por nombre de parque
   if (filters.value.parque) {
     const q = filters.value.parque.toLowerCase()
     result = result.filter(r =>
       r.parque.nombre.toLowerCase().includes(q)
     )
   }

   // Filtro por estado
   if (filters.value.estado) {
     result = result.filter(r => r.estado === filters.value.estado)
   }

   // Filtro por rango de fechas
   if (filters.value.fechas_desde) {
     result = result.filter(r =>
       r.fecha_inicio >= filters.value.fechas_desde
     )
   }
   if (filters.value.fechas_hasta) {
     result = result.filter(r =>
       r.fecha_fin <= filters.value.fechas_hasta
     )
   }
   //Fltro por total
   if (filters.value.precio) {
     const max = parseFloat(filters.value.precio)
     result = result.filter(r =>
       r.monto == null || r.monto <= max
     )
   }

   return result
 })

 //Carga inicial
 onMounted(async () => {
   await reserveService.getReservaciones()
 })

 //Handlers
 function handleVer(reservacion: Reservacion) {
   // TODO: abrir modal de detalle o navegar a /reservaciones/:id
   console.log('Ver reservación', reservacion.id)
 }

 function handleCancelar(reservacion: Reservacion) {
   // TODO backend: POST /api/reservaciones/:id/cancelar/
   // Confirmar con modal antes de cancelar
   store.eliminarReservacion(reservacion.id)
 }
</script>

<style scoped>
 .reservations-view {
   min-height: calc(100vh - 80px);
   margin-top: 80px;
   display: flex;
   justify-content: center;
   padding: 2rem 1.5rem;
   box-sizing: border-box;
 }

 .reservations-inner {
   width: 100%;
   max-width: 82.5rem;
   display: flex;
   flex-direction: column;
   gap: 1.25rem;
 }

 /* Header */
 .section-header {
   display: flex;
   align-items: center;
   justify-content: space-between;
   gap: 1rem;
 }

 .section-title-group {
   display: flex;
   align-items: baseline;
   gap: 0.75rem;
 }

 .section-title {
   font-size: 22px;
   font-weight: 600;
   color: var(--color-bone);
   letter-spacing: -0.02em;
 }

 .section-count {
   font-size: 12px;
   color: var(--color-bone-mute);
   font-family: var(--font-mono);
 }

 /* Lista */
 .reservations-list {
   display: flex;
   flex-direction: column;
   gap: 0.5rem;
 }

 /* Loading */
 .list-loading {
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   gap: 0.75rem;
   padding: 4rem 0;
   color: var(--color-bone-soft);
   font-size: 13px;
 }

 /* Vacío */
 .list-empty {
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   gap: 0.75rem;
   padding: 4rem 0;
   text-align: center;
 }

 .empty-title {
   font-size: 16px;
   font-weight: 500;
   color: var(--color-bone-soft);
 }

 .empty-sub {
   font-size: 13px;
   color: var(--color-bone-mute);
   max-width: 280px;
 }
</style>
