<template>
  <div class="park-card">

    <!-- Carrusel de imagenes del parque -->
    <div class="card-images">
      <transition name="fade-img" mode="out-in">
        <img
          v-if="park.imagenes && park.imagenes.length"
          :key="currentImageIndex"
          :src="park.imagenes[currentImageIndex].url"
          :alt="park.nombre"
          class="card-img"/>
        <div v-else class="card-img card-img-placeholder">
          <FireflyLogo :pulse="true" :drift="false" size="w-14 h-14" />
        </div>
      </transition>

      <!-- Indicadores del carrusel -->
      <div v-if="park.imagenes && park.imagenes.length > 1" class="carousel-dots">
        <span
          v-for="(_, i) in park.imagenes"
          :key="i"
          class="dot"
          :class="{ 'dot-active': i === currentImageIndex }"
        />
      </div>
    </div>

    <!-- Contenedor de texto -->
    <div class="card-body">

      <!-- Nombre -->
      <h3 class="card-nombre">{{ park.nombre }}</h3>

      <!-- Descripcion con ellipsis -->
      <p class="card-desc">{{ park.descripcion || 'Sin descripción' }}</p>

      <!-- Horario y estado -->
      <div class="card-footer">
        <span class="card-horario">
          <template v-if="is24hrs">
            24 hrs
          </template>
          <template v-else>
            {{ park.horario_apertura }} – {{ park.horario_cierre }}
          </template>
        </span>

        <span class="card-status" :class="statusClass">
          {{ statusText }}
        </span>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
 import { ref, computed, onMounted, onUnmounted } from 'vue'
 import FireflyLogo from '../ui/FireflyLogo.vue'
 import type { Parque } from '../../stores/parks'

 const props = defineProps<{ park: Parque }>()

 //Carrusel de imagenes
 const currentImageIndex = ref(0)
 let carouselTimer: ReturnType<typeof setInterval> | null = null

 onMounted(() => {
   if (props.park.imagenes && props.park.imagenes.length > 1) {
     carouselTimer = setInterval(() => {
       currentImageIndex.value =
         (currentImageIndex.value + 1) % props.park.imagenes.length
     }, 2500)
   }
 })

 onUnmounted(() => {
   if (carouselTimer) clearInterval(carouselTimer)
 })

 //Logica de horario
 const apertura = props.park.horario_apertura
 const cierre = props.park.horario_cierre

 const is24hrs = computed(() =>
   apertura === cierre || (apertura === '00:00' && cierre === '00:00')
 )

 const isOpen = computed(() => {
   if (!props.park.activo)
     return false
   if (is24hrs.value)
     return true

   // Hora aproximada en zona del parque por longitud
   const offsetHours  = Math.round(props.park.longitud / 15)
   const nowUtc = new Date()
   const parkTime = new Date(nowUtc.getTime() + offsetHours * 60 * 60 * 1000)
   const parkMinutes = parkTime.getUTCHours() * 60 + parkTime.getUTCMinutes()

   const [aH, aM] = apertura.split(':').map(Number)
   const [cH, cM] = cierre.split(':').map(Number)
   const openMinutes  = aH * 60 + aM
   const closeMinutes = cH * 60 + cM

   //Turno nocturno
   if (openMinutes > closeMinutes) {
     return parkMinutes >= openMinutes || parkMinutes < closeMinutes
   }

   return parkMinutes >= openMinutes && parkMinutes < closeMinutes
 })

 //Texto y clase del estado
 const statusText = computed(() => {
   if (!props.park.activo)
     return 'No disponible'
   return isOpen.value ? 'Abierto' : 'Cerrado'
 })

 const statusClass = computed(() => {
   if (!props.park.activo)
     return 'status-unavailable'
   return isOpen.value ? 'status-open' : 'status-closed'
 })
</script>

<style scoped>
.park-card {
  width: 340px;
  border-radius: 14px;
  overflow: hidden;
  background: rgba(13, 20, 14, 0.92);
  border: 1px solid rgba(123, 216, 176, 0.15);
  box-shadow:
    0 8px 24px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.04);
}

.card-images {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #0d1a10;
}

 .card-img {
   width: 100%;
   height: 200px;
   object-fit: cover;
   display: block;
 }

 .card-img-placeholder {
   display: flex;
   align-items: center;
   justify-content: center;
   background: #0d1a10;
 }

 /* Dots del carrusel */
 .carousel-dots {
   position: absolute;
   bottom: 6px;
   left: 50%;
   transform: translateX(-50%);
   display: flex;
   gap: 4px;
 }

 .dot {
   width: 4px;
   height: 4px;
   border-radius: 50%;
   background: rgba(255, 255, 255, 0.3);
   transition: background 0.3s;
 }

 .dot-active {
   background: var(--color-accent);
 }

 /* Transicion entre imagenes */
 .fade-img-enter-active,
 .fade-img-leave-active {
   transition: opacity 0.5s ease;
 }
 .fade-img-enter-from,
 .fade-img-leave-to {
   opacity: 0;
 }

 /* Texto */
.card-body {
  padding: 0.9rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.card-nombre {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-bone);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

 .card-desc {
   font-size: 13px;
   color: var(--color-bone-soft);
   white-space: nowrap;
   overflow: hidden;
   text-overflow: ellipsis;
   max-width: 100%;
 }

 .card-footer {
   display: flex;
   align-items: center;
   justify-content: space-between;
   margin-top: 0.25rem;
 }

.card-horario {
  font-size: 12.5px;
  color: var(--color-bone-mute);
}

 .card-status {
   font-size: 12px;
   font-weight: 600;
   padding: 0.25rem 0.6rem;
   border-radius: 999px;
   letter-spacing: 0.04em;
 }

 .status-open {
   background: rgba(123, 216, 176, 0.15);
   color: var(--color-green);
 }

 .status-closed {
   background: rgba(255, 138, 123, 0.12);
   color: var(--color-danger);
 }

 .status-unavailable {
   background: rgba(255, 255, 255, 0.06);
   color: var(--color-bone-mute);
 }
</style>
