<template>
  <div class="park-card">
    <div class="absolute top-3 left-3 flex items-center gap-2 z-600">
      <span class="px-2.5 py-1 rounded-full text-[10.5px] font-mono uppercase tracking-[0.12em]"
            :style="`background:${park.hasCabin ? 'rgba(245,213,122,0.16)' : 'rgba(122,211,164,0.16)'}; color:${park.hasCabin ? '#f5d57a' : '#7ad3a4'}; border:1px solid ${park.hasCabin ? 'rgba(245,213,122,0.4)' : 'rgba(122,211,164,0.4)'};`">
        {{ park.hasCabin ? 'Cabaña + Camping' : 'Solo Camping' }}
      </span>
      <span v-if="park.campings_libres && park.campings_libres > 5" class="px-2.5 py-1 rounded-full text-[10.5px] font-mono uppercase tracking-[0.12em] bg-white/10 border border-white/15 text-(--color--bone-soft)">Disponible</span>
      <span v-else class="px-2.5 py-1 rounded-full text-[10.5px] font-mono uppercase tracking-[0.12em] bg-[rgba(255,138,123,0.14)] border border-[rgba(255,138,123,0.4)] text-[#ff9b8a]">Pocas plazas</span>
    </div>
    <!-- Carrusel de imagenes del parque -->
    <ImageCarousel :images="park.imagenes" :alt="park.nombre" />

    <!-- Contenedor de texto -->
    <div class="card-body">
      <!-- Nombre -->
      <h3 class="card-nombre font-display">{{ park.nombre }}</h3>

      <div class="text-[12px] text-bone-soft mt-1 flex items-center gap-1.5">
        <MapPin :size="14" class="text-(--color-accent)" />
        {{ park.direccion }}
      </div>

      <div v-if="park.servicios.length > 0">
        <div class="text-[10px] uppercase tracking-wider text-(--color-bone-mute) mb-2">Servicios disponibles</div>
        <div class="flex flex-wrap gap-1.5">
          <span v-for="(item, index) in primerosTresElementos" :key="index"
                class="inline-flex items-center gap-1 text-xs px-2.5 py-1 rounded-full bg-[#070b14]/60 border border-(--color-accent)/15 text-(--color-bone-soft)/80">
            {{ item }}
          </span>
        </div>
      </div>

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

      <div class="flex items-center gap-2 border-t border-white/5">
        <AppLink :href="`/all#park-${park.id}`" variant="outline" class="mt-3 w-35">
          Ver detalles
        </AppLink>
        <AppLink v-if="park.activo" :href="auth.token ? `/reservar?park=${park.id}` : '/auth'" variant="yellow" class="mt-3 w-50" :iconRight="ArrowRight">
          Reservar
        </AppLink>
        <AppButton v-else disabled variant="primary" class="mt-3 w-50">
          Reservar
        </AppButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Parque } from "../../stores/parks";
import { is24Hours, getParkStatusText, getParkStatusClass } from "../../utils/parkStatus";
import ImageCarousel from "../ui/ImageCarousel.vue";
import { MapPin, ArrowRight } from "lucide-vue-next";
import AppLink from "../ui/AppLink.vue";
import AppButton from "../ui/AppButton.vue";
import { useAuthStore } from '../../stores/auth';

const auth = useAuthStore();

const props = defineProps<{ park: Parque }>();

const is24hrs = computed(() => is24Hours(props.park));

const primerosTresElementos = computed(() => props.park.servicios.slice(0, 3).map(s => s.nombre));

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
