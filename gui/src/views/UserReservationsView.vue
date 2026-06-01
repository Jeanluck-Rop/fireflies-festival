<template>
  <div>
    <section class="pt-32 pb-12 relative overflow-hidden">
      <div class="mx-auto max-w-330 px-6 lg:px-8 relative">

        <!-- Breadcrumb -->
        <nav class="flex items-center gap-2 text-[12.5px] font-mono uppercase tracking-[0.14em] text-bone-soft mb-8 animate-fade-up">
          <a href="/" class="hover:text-bone transition">Inicio</a>
          <span class="opacity-40">/</span>
          <span class="text-glow">Mis Reservaciones</span>
        </nav>

        <!-- Contenido en dos columnas -->
        <div class="grid lg:grid-cols-2 gap-8 lg:gap-16 items-end">

          <!-- Columna izquierda: etiqueta + titulo -->
          <div class="animate-fade-up">
            <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90 mb-5">
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
              Festival 2026
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
            </span>
            <h1 class="font-serif font-normal leading-[0.95] tracking-tight text-[clamp(2.6rem,6vw,4.5rem)]">
              Tus noches<br>en la <em class="italic text-glow">naturaleza</em>
            </h1>
          </div>

          <!-- Columna derecha: descripcion + stats + boton -->
          <div class="animate-fade-up delay-100 flex flex-col gap-6 pb-2">
            <p class="text-[15.5px] leading-relaxed text-bone-soft">
              Consulta y gestiona todas tus reservaciones en los parques del festival.
              Puedes cancelar las activas o en proceso antes de tu fecha de entrada.
            </p>

            <!-- Stats -->
            <div class="flex items-center gap-8" v-if="!loading">
              <div>
                <div class="text-[2rem] font-bold leading-none tracking-tight text-bone">
                  {{ reservaciones.length }}
                </div>
                <div class="text-[11px] font-mono uppercase tracking-[0.14em] text-bone-mute mt-1">
                  Reservaciones
                </div>
              </div>
              <div class="w-px h-10 bg-white/10" />
              <div>
                <div class="text-[2rem] font-bold leading-none tracking-tight"
                     :style="{ color: 'var(--color-green)' }">
                  {{ stats.activas }}
                </div>
                <div class="text-[11px] font-mono uppercase tracking-[0.14em] text-bone-mute mt-1">
                  Activas
                </div>
              </div>
              <div class="w-px h-10 bg-white/10" />
              <div>
                <div class="text-[2rem] font-bold leading-none tracking-tight"
                     :style="{ color: 'var(--color-accent)' }">
                  {{ stats.en_proceso }}
                </div>
                <div class="text-[11px] font-mono uppercase tracking-[0.14em] text-bone-mute mt-1">
                  En proceso
                </div>
              </div>
            </div>

            <!-- Boton -->
            <div>
              <AppButton variant="primary" @click="router.push('/reservar')">
                <IconPlus size="12px" style="margin-right: 6px" />
                Nueva reservación
              </AppButton>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- Contenido: busqueda + lista -->
    <div class="reservations-content">
      <div class="reservations-inner">

        <!-- SearchBar -->
        <SearchBar v-model="filters" :filters="filterDefs" />

        <!-- Contador de resultados -->
        <div class="results-row">
          <span v-if="!loading" class="results-count">
            {{ filteredReservaciones.length }}
            {{ filteredReservaciones.length === 1 ? 'reservación' : 'reservaciones' }}
          </span>
        </div>

        <!-- Lista -->
        <div class="reservations-list">

          <!-- Loading -->
          <div v-if="loading" class="list-loading">
            <FireflyLogo :pulse="true" :drift="false" size="w-10 h-10" />
            <span>Cargando reservaciones...</span>
          </div>

          <!-- Sin resultados de busqueda -->
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
              @cancelar="handleCancelar" />
          </template>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
 import { ref, computed, onMounted } from 'vue'
 import { useRouter } from 'vue-router'
 import FireflyLogo    from '../components/ui/FireflyLogo.vue'
 import AppButton      from '../components/ui/AppButton.vue'
 import SearchBar      from '../components/ui/SearchBar.vue'
 import ReservationRow from '../components/reservations/ReservationRow.vue'
 import IconPlus       from '../components/svg/IconPlus.vue'
 import { reserveService }      from '../services/reserveService'
 import { useReservationsStore } from '../stores/reservations'
 import type { Reservacion }    from '../stores/reservations'
 import type { FilterDef, FilterValues } from '../components/ui/SearchBar.vue'

 const router = useRouter()
 const store  = useReservationsStore()

 const reservaciones = computed(() => store.reservaciones)
 const loading       = computed(() => store.loading)

 //Stats
 const stats = computed(() => {
   const all = reservaciones.value
   return {
     activas:    all.filter(r => r.estado === 'ACTIVA').length,
     en_proceso: all.filter(r => r.estado === 'EN_PROCESO').length,
   }
 })

 //Filtros
 const filterDefs: FilterDef[] = [
   { key: 'parque', type: 'text', placeholder: 'Buscar por parque...' },
   {
     key: 'estado', type: 'select', placeholder: 'Estado',
     options: [
       { label: 'Activa',     value: 'ACTIVA'     },
       { label: 'En proceso', value: 'EN_PROCESO'  },
       { label: 'Completada', value: 'COMPLETADA'  },
       { label: 'Cancelada',  value: 'CANCELADA'   },
     ],
   },
   { key: 'fechas', type: 'daterange' },
   { key: 'precio', type: 'number', placeholder: 'Total máx.' },
 ]

 const filters = ref<FilterValues>({
   parque: '', estado: '', fechas_desde: '', fechas_hasta: '', precio: '',
 })

 const filteredReservaciones = computed(() => {
   let result = reservaciones.value

   if (filters.value.parque) {
     const q = filters.value.parque.toLowerCase()
     result = result.filter(r => r.parque.nombre.toLowerCase().includes(q))
   }
   if (filters.value.estado)
     result = result.filter(r => r.estado === filters.value.estado)
   if (filters.value.fechas_desde)
     result = result.filter(r => r.fecha_inicio >= filters.value.fechas_desde)
   if (filters.value.fechas_hasta)
     result = result.filter(r => r.fecha_fin <= filters.value.fechas_hasta)
   if (filters.value.precio) {
     const max = parseFloat(filters.value.precio)
     result = result.filter(r => r.monto == null || r.monto <= max)
   }

   return result
 })

 //Carga inicial
 onMounted(async () => {
   await reserveService.getReservaciones()
 })

 //Handlers
 function handleCancelar(reservacion: Reservacion) {
   // TODO backend: POST /api/reservaciones/:id/cancelar/
   store.eliminarReservacion(reservacion.id)
 }
</script>

<style scoped>
 /* Seccion de contenido */
 .reservations-content {
   display: flex;
   justify-content: center;
   padding: 0 1.5rem 3rem;
   box-sizing: border-box;
 }

 .reservations-inner {
   width: 100%;
   max-width: 82.5rem;
   display: flex;
   flex-direction: column;
   gap: 1rem;
 }

 /* Contador de resultados */
 .results-row  { display: flex; align-items: center; }
 .results-count {
   font-size: 11.5px;
   color: var(--color-bone-mute);
   font-family: var(--font-mono);
   text-transform: uppercase;
   letter-spacing: 0.1em;
 }

 /* Lista */
 .reservations-list { display: flex; flex-direction: column; gap: 0.5rem; }

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

 /* Vacio */
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
