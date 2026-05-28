<template>
  <div class="park-card">
    <!-- Carrusel de imagenes del parque -->
    <div class="card-images" @mouseenter="stop" @mouseleave="start">
      <transition name="fade-img" mode="out-in">
        <img
          v-if="park.imagenes?.length"
          :key="currentImageIndex"
          :src="park.imagenes[currentImageIndex].url"
          :alt="park.nombre"
          class="card-img"
        />
        <div v-else class="card-img card-img-placeholder">
          <FireflyLogo :pulse="true" :drift="false" size="w-14 h-14" />
        </div>
      </transition>

      <!-- Indicadores del carrusel -->
      <button
        v-if="park.imagenes?.length > 1"
        class="carousel-btn left"
        @click="prev"
      >
        ‹
      </button>

      <button
        v-if="park.imagenes?.length > 1"
        class="carousel-btn right"
        @click="next"
      >
        ›
      </button>

      <div
        v-if="park.imagenes?.length > 1"
        class="carousel-dots"
      >
        <span
          v-for="(_, i) in park.imagenes"
          :key="i"
          class="dot"
          :class="{ 'dot-active': i === currentImageIndex }"
          @click="goTo(i)"
        />
      </div>
    </div>

    <!-- Contenedor de texto -->
    <div class="card-body">
      <!-- Nombre -->
      <h3 class="card-nombre">{{ park.nombre }}</h3>

      <!-- Descripcion con ellipsis -->
      <p class="card-desc">{{ park.descripcion || "Sin descripción" }}</p>

      <!-- Horario y estado -->
      <div class="card-footer">
        <span class="card-horario">
          <template v-if="is24hrs"> 24 hrs </template>
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
import { computed } from "vue";
import FireflyLogo from "../ui/FireflyLogo.vue";
import type { Parque } from "../../stores/parks";
import { is24Hours, getParkStatusText, getParkStatusClass } from "../../utils/parkStatus";
import { useCarousel } from "../../composables/useCarousel";

const props = defineProps<{ park: Parque }>();

//Carrusel de imagenes
const { currentIndex: currentImageIndex, next, prev, goTo, start, stop } = useCarousel(
  props.park.imagenes?.length || 0
);

const is24hrs = computed(() => is24Hours(props.park));

//Texto y clase del estado
const statusText = computed(() => getParkStatusText(props.park));
const statusClass = computed(() => getParkStatusClass(props.park));
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

/* Botones del carrusel */
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.45);
  color: white;
  font-size: 18px;
  transition:
    background 0.2s,
    opacity 0.2s;
  opacity: 0;
}

.card-images:hover .carousel-btn {
  opacity: 1;
}

.carousel-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

.carousel-btn.left {
  left: 8px;
}

.carousel-btn.right {
  right: 8px;
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
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transition: 
    background 0.3s
    transform 0.25s;
}

.dot:hover {
  transform: scale(1.2);
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
