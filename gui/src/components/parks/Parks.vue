<template>
  <div class="mx-auto max-w-380 mt-5 px-5 lg:px-8 animate-fade-up">
    <div class="parks-container z-0 animate-fade-up">
      <!-- Mapa -->
      <div class="map-wrapper">
        <LMap
          ref="mapRef"
          :zoom="zoom"
          :center="center"
          :use-global-leaflet="false"
          class="park-map"
          @ready="onMapReady"
        >
          <LTileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© Festival Luciérnagas"
          />

          <LMarker
            v-for="park in parks"
            :key="park.id"
            :lat-lng="[park.latitud, park.longitud]"
            :icon="getIcon(park)"
            @click="() => selectPark(park)"
          />
        </LMap>

        <!-- Loading overlay -->
        <div v-if="loading" class="map-loading">
          <FireflyLogo :pulse="true" :drift="false" size="w-12 h-12" />
          <span>Cargando parques...</span>
        </div>
      </div>

      <!-- Popup ParkCard -->
      <transition name="card-pop">
        <div
          v-if="selectedPark"
          ref="cardRef"
          class="card-floating"
          :style="{
            left: popupPosition.x + 'px',
            top: popupPosition.y + 'px',
            visibility: positioned ? 'visible' : 'hidden',
          }"
        >
          <button class="card-close" @click="closeCard" aria-label="Cerrar">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path
                d="M1 1l8 8M9 1l-8 8"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
            </svg>
          </button>
          <ParkCard :park="selectedPark" />
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from "vue";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import FireflyLogo from "../ui/FireflyLogo.vue";
import ParkCard from "./ParkCard.vue";
import { createPinIcon } from "./MapPin.vue";
import { isParkOpen } from "../../utils/parkStatus";
import { useParksStore } from "../../stores/parks";
import type { Parque } from "../../stores/parks";

const store = useParksStore();
const parks = computed(() => store.parks);
const loading = computed(() => store.loading);
const selectedPark = computed(() => store.selectedPark);

const popupPosition = ref({ x: 0, y: 0 });
const positioned = ref(false);

const mapRef = ref<InstanceType<typeof LMap> | null>(null);
const cardRef = ref<HTMLElement | null>(null);
const zoom = ref(6);
const center = ref<[number, number]>([23.6345, -102.5528]);

watch(parks, (newParks) => {
  if (newParks.length) {
    const avgLat = newParks.reduce((s, p) => s + p.latitud, 0) / newParks.length;
    const avgLng = newParks.reduce((s, p) => s + p.longitud, 0) / newParks.length;
    center.value = [avgLat, avgLng];
  }
});

watch(selectedPark, async (park) => {
  if (!park) {
    positioned.value = false;
    return;
  }
  const map = mapRef.value?.leafletObject as L.Map | undefined
  if (map) {
    map.setView([park.latitud, park.longitud], Math.max(map.getZoom(), 12), { animate: true });
  }
  positioned.value = false;
  await nextTick();
  positionCard(park);
  positioned.value = true;
});

function getIcon(park: Parque) {
  const isOpen = isParkOpen(park);
  const isSelected = selectedPark.value?.id === park.id;

  return createPinIcon(isOpen, isSelected);
}

function selectPark(park: Parque) {
  store.selectPark(park);
}

function positionCard(park: Parque) {
  const map = mapRef.value?.leafletObject as L.Map | undefined;
  if (!map) return;

  const point = map.latLngToContainerPoint([park.latitud, park.longitud]);
  const mapSize = map.getSize();
  const cardW = cardRef.value?.offsetWidth ?? 300;
  const cardH = cardRef.value?.offsetHeight ?? 380;
  const M = 12;

  let x = point.x + 20;
  let y = point.y - cardH / 2;

  if (x + cardW + M > mapSize.x) x = point.x - cardW - 20;

  x = Math.max(M, Math.min(x, mapSize.x - cardW - M));
  y = Math.max(M, Math.min(y, mapSize.y - cardH - M));

  popupPosition.value = { x, y };
}

function closeCard() {
  store.selectPark(null);
}

function onMapReady() {
  console.log('Mapa listo');
  const map = mapRef.value?.leafletObject as L.Map | undefined;
  if (!map) return;
  map.on("move zoom", () => {
    if (selectedPark.value) positionCard(selectedPark.value);
  });
}
</script>

<style scoped>
.parks-container {
  position: relative;
  width: 100%;
  height: 70vh;
}

/* Mapa */
.map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.park-map {
  width: 100%;
  height: 100%;
}

/* Tiles oscuros */
.park-map :deep(.leaflet-tile) {
  filter: invert(1) hue-rotate(180deg) brightness(0.85) saturate(0.7);
}

/* Loading */
.map-loading {
  position: absolute;
  inset: 0;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  background: rgba(7, 9, 10, 0.7);
  backdrop-filter: blur(4px);
  color: var(--color-bone-soft);
  font-size: 13px;
}

/* Popup overlay */
.card-floating {
  position: absolute;
  z-index: 1001;
  width: 300px;
  pointer-events: all;
}

.card-close {
  position: absolute;
  top: -10px;
  right: -45px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-bone-soft);
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: color 0.2s;
}
.card-close:hover {
  color: var(--color-bone);
}

.card-pop-enter-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.card-pop-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.card-pop-enter-from {
  opacity: 0;
  transform: translateY(8px) scale(0.97);
}
.card-pop-leave-to {
  opacity: 0;
  transform: translateY(8px) scale(0.97);
}
</style>
