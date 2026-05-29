<template>
  <div class="park-card">
    <!-- Carrusel de imagenes del parque -->
    <ImageCarousel :images="park.imagenes" :alt="park.nombre" />

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
import type { Parque } from "../../stores/parks";
import { is24Hours, getParkStatusText, getParkStatusClass } from "../../utils/parkStatus";
import ImageCarousel from "../ui/ImageCarousel.vue";

const props = defineProps<{ park: Parque }>();

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
