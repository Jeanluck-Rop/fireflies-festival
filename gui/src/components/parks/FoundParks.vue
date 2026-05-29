<template>
  <div class="mx-auto max-w-380 mt-5 px-5 lg:px-8">
    <div class="flex items-end justify-between gap-4 mb-7">
      <div>
        <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
          <span class="h-px w-6 bg-(--color-accent)/60"></span>
          Resultados de tu búsqueda
          <span class="h-px w-6 bg-(--color-accent)/60"></span>
        </span>
        <h2 class="font-display text-[clamp(1.8rem,3.4vw,2.8rem)]">
          <template v-if="filteredParks.length">{{ filteredParks.length }} parque{{ filteredParks.length===1?'':'s' }} <em class="font-display italic font-normal text-glow">coinciden</em></template>
          <template v-else>Sin coincidencias <em class="font-display italic font-normal text-glow">por ahora</em></template>
        </h2>
      </div>
      <AppLink href="/parques" variant="outline" :icon="Shrub">
        Ver todos los parques
      </AppLink>
    </div>

    <div v-if="filteredParks.length" ref="listRef" class="overflow-x-auto pt-3 pb-4 snap-x snap-mandatory">
      <div class="gap-5" :class="filteredParks.length > 8
          ? 'grid grid-rows-2 grid-flow-col auto-cols-[320px]' : 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'">
        <article
          v-for="p in filteredParks"
          :key="p.id"
          :data-id="p.id"
          class="snap-start park-card glass rounded-3xl overflow-hidden flex flex-col cursor-pointer"
          :class="{ 'is-hover': hoverId === p.id, 'is-selected': selectedId === p.id }"
          @mouseenter="hoverPark(p.id)"
          @mouseleave="hoverPark(null)"
          @click="selectAndScroll(p)"
        >
          <ImageCarousel :images="p.imagenes" :alt="p.nombre" />
          <div class="p-5 flex flex-col gap-3 flex-1">
            <div>
              <div class="flex items-baseline justify-between gap-2">
                <div class="font-serif text-[23px] leading-tight">{{ p.nombre }}</div>
                <span class="font-mono text-[10px] tracking-[0.14em] text-bone-soft shrink-0">#{{ String(p.id).padStart(2,'0') }}</span>
              </div>
              <div class="text-[12px] text-bone-soft mt-1 flex items-center gap-1.5">
                <MapPin :size="14" class="text-(--color-accent)" />
                {{ p.direccion }}
              </div>
            </div>
            <p class="text-[13px] text-bone-mute leading-normal line-clamp-2">{{ p.descripcion || 'Sin descripción' }}</p>
            <div class="mt-auto pt-3 border-t border-white/5 flex items-center justify-between">
              <span class="text-[11px] font-mono uppercase tracking-[0.14em] text-bone-soft">
                <template v-if="is24Hours(p)"> 24 hrs </template>
                <template v-else>{{ p.horario_apertura }} – {{ p.horario_cierre }}</template>
              </span>
              <span class="card-status" :class="getParkStatusClass(p)">
                {{ getParkStatusText(p) }}
              </span>
            </div>
          </div>
        </article>
      </div>
    </div>

    <div v-else class="glass rounded-3xl p-14 text-center flex flex-col items-center gap-4">
      <FireflyLogo :pulse="true" :drift="false" size="w-16 h-16" />
      <div class="font-serif text-[26px]">Ninguna luz por aquí todavía</div>
      <p class="text-[14px] text-bone-mute max-w-[42ch]">No hay parques que coincidan con esos filtros. Prueba ampliar la región o quitar el filtro de disponibilidad.</p>
      <AppButton variant="outline" @click="$emit('reset-filters')">Limpiar filtros</AppButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, nextTick } from "vue";
import { useParksStore } from "../../stores/parks";
import AppLink from "../ui/AppLink.vue";
import AppButton from "../ui/AppButton.vue";
import { Shrub, MapPin } from "lucide-vue-next";
import { is24Hours, getParkStatusText, getParkStatusClass } from "../../utils/parkStatus";
import ImageCarousel from "../ui/ImageCarousel.vue";
import FireflyLogo from "../ui/FireflyLogo.vue";
import type { Parque } from "../../stores/parks";

defineEmits<{ (e: 'reset-filters'): void }>();

const store = useParksStore();

const filteredParks = computed(() => store.parks);

const selectedId = computed(() => store.selectedPark?.id ?? null);

const hoverId = ref<number | null>(null);
function hoverPark(id: number | null) {
  hoverId.value = id;
}

const listRef = ref<HTMLElement | null>(null);

function selectAndScroll(p: Parque) {
  store.selectPark(p);
  document.querySelector('.parks-container')
    ?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

watch(selectedId, async (id) => {
  if (id == null) return;
  await nextTick();
  const container = listRef.value;
  const el = container?.querySelector<HTMLElement>(`[data-id="${id}"]`);

  if (!container || !el) return;

  container.scrollTo({
    left: el.offsetLeft - container.clientWidth / 2 + el.clientWidth / 2,
    behavior: 'smooth',
  });
});
</script>

<style scoped>
.park-card { transition:transform .25s ease, 
  border-color .25s ease, 
  background .25s ease;
}

.park-card:hover, .park-card.is-hover { 
  transform:translateY(-3px); 
  border-color:rgba(245,213,122,.32); 
  background:linear-gradient(180deg, rgba(236,243,238,0.06), 
  rgba(236,243,238,0.02)); 
}

.park-card.is-selected {
  border-color: rgba(245, 213, 122, .55);
  box-shadow: 0 0 0 1px rgba(245, 213, 122, .25);
}

.glass {
  background:linear-gradient(180deg, rgba(236,243,238,0.045), rgba(236,243,238,0.012));
  backdrop-filter:blur(14px) saturate(120%); -webkit-backdrop-filter:blur(14px) saturate(120%);
  border:1px solid rgba(236,243,238,0.08);
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