<template>
  <div class="animate-fade-up">
    <div class="flex items-end justify-between gap-4 mb-7">
      <div>
        <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
          <span class="h-px w-6 bg-(--color-accent)/60"></span>
          Resultados de tu búsqueda
          <span class="h-px w-6 bg-(--color-accent)/60"></span>
        </span>
        <h2 class="font-display text-[clamp(1.8rem,3.4vw,2.8rem)] mt-1">
          <template v-if="unidades.length">
            {{ unidades.length }} opci{{ unidades.length === 1 ? 'ón' : 'ones' }} 
            <em class="font-display italic font-normal text-glow">disponible{{ unidades.length === 1 ? 's' : 's' }}</em>
          </template>
          <template v-else>Sin disponibilidad <em class="font-display italic font-normal text-glow">por ahora</em></template>
        </h2>
      </div>
    </div>

    <div v-if="unidades.length" class="grid grid-cols-1 md:grid-cols-2 gap-5 pb-4">
      <article
        v-for="u in unidades"
        :key="u.id"
        :data-id="u.id"
        class="unit-card glass rounded-3xl overflow-hidden flex flex-col cursor-pointer transition-all duration-250 ease-out"
        :class="{ 'is-selected': store.unidadSeleccionada?.id === u.id }"
        @click="seleccionar(u)"
      >
        <ImageCarousel :images="u.imagenes" :alt="u.descripcion" class="h-48" />

        <div class="p-5 flex flex-col gap-3 flex-1">
          <div>
            <div class="flex items-baseline justify-between gap-2">
              <div class="font-serif text-[23px] leading-tight capitalize">
                {{ u.tipo === 'CABANA' ? 'Cabaña' : 'Camping' }} {{ u.id }} - {{ u.categoria.toLowerCase() }}
              </div>
            </div>
            
            <div class="flex items-center gap-3 mt-3">
              <div class="flex items-center gap-1.5 text-[12px] text-bone-soft" title="Capacidad máxima">
                <Users :size="14" class="text-(--color-accent)" />
                <span>{{ u.capacidad }}</span>
              </div>
              <div v-if="u.num_camas !== null" class="flex items-center gap-1.5 text-[12px] text-bone-soft" title="Camas">
                <Bed :size="14" class="text-(--color-accent)" />
                <span>{{ u.num_camas }}</span>
              </div>
              <div v-if="u.num_banos !== null" class="flex items-center gap-1.5 text-[12px] text-bone-soft" title="Baños">
                <Bath :size="14" class="text-(--color-accent)" />
                <span>{{ u.num_banos }}</span>
              </div>
            </div>
          </div>
          
          <p class="text-[13px] text-bone-mute leading-normal line-clamp-2 mt-1">
            {{ u.descripcion || 'Sin descripción disponible.' }}
          </p>

          <div class="mt-auto pt-4 border-t border-white/5 flex items-center justify-between">
            <span class="text-[15px] font-medium text-white">
              {{ formatCurrency(u.tarifa_noche) }} <span class="text-[11px] font-mono text-bone-soft uppercase tracking-widest font-normal">/ noche</span>
            </span>
            
            <div class="w-6 h-6 rounded-full border flex items-center justify-center transition-colors duration-200"
                 :class="store.unidadSeleccionada?.id === u.id ? 'bg-(--color-accent) border-(--color-accent) text-black' : 'border-white/20 text-transparent'">
              <Check :size="14" :stroke-width="3" />
            </div>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="glass rounded-3xl p-14 text-center flex flex-col items-center gap-4">
      <FireflyLogo :pulse="true" :drift="false" size="w-16 h-16" />
      <div class="font-serif text-[26px]">Ninguna luz por aquí todavía</div>
      <p class="text-[14px] text-bone-mute max-w-[42ch]">
        No hay unidades que coincidan con estos filtros para las fechas seleccionadas o exceden la capacidad permitida.
      </p>
      <AppButton variant="outline" @click="store.currentStep = 1">Modificar búsqueda</AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useReservationStore, type Hospedaje } from "../../stores/reservationStore";
import { Users, Bed, Bath, Check } from "lucide-vue-next";
import AppButton from "../ui/AppButton.vue";
import ImageCarousel from "../ui/ImageCarousel.vue";
import FireflyLogo from "../ui/FireflyLogo.vue";

const store = useReservationStore();

const unidades = computed(() => store.unidadesDisponibles);

function seleccionar(u: Hospedaje) {
  store.seleccionarUnidad(u);
}

const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount);
};
</script>

<style scoped>
.unit-card { 
  transform: translateY(0);
}

.unit-card:hover { 
  transform: translateY(-3px); 
  border-color: rgba(232, 255, 122, 0.32); 
  background: linear-gradient(180deg, rgba(236,243,238,0.06), rgba(236,243,238,0.02)); 
}

.unit-card.is-selected {
  border-color: var(--color-accent, #E8FF7A);
  box-shadow: 0 0 0 1px rgba(232, 255, 122, 0.25), 0 8px 24px -8px rgba(232, 255, 122, 0.15);
  background: linear-gradient(180deg, rgba(232,255,122,0.06), rgba(232,255,122,0.01)); 
}

.glass {
  background: linear-gradient(180deg, rgba(236,243,238,0.045), rgba(236,243,238,0.012));
  backdrop-filter: blur(14px) saturate(120%); 
  -webkit-backdrop-filter: blur(14px) saturate(120%);
  border: 1px solid rgba(236,243,238,0.08);
}
</style>