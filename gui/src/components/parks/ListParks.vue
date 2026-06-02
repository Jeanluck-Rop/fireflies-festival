<template>
  <div class="lg:px-8 pb-10 relative z-1"> 
    <div v-if="filteredParks.length === 0" class="glass rounded-3xl p-12 lg:p-20 text-center flex flex-col items-center gap-5 animate-fade-up">
      <FireflyLogo :pulse="true" :drift="false" size="w-20 h-20" />
      <div class="font-serif text-3xl lg:text-4xl text-(--color-bone)">Ninguna luz por aquí todavía</div>
      <p class="text-[15px] text-(--color-bone-mute) max-w-[46ch] leading-relaxed">
        No hay parques que coincidan con esos filtros. Prueba ampliar la región o quitar el filtro de disponibilidad.
      </p>
      <AppButton variant="outline" class="mt-2" @click="parksStore.resetFilters()">Limpiar filtros</AppButton>
    </div>
    <div class="flex flex-col gap-8 lg:gap-10">
      <article v-for="(p,idx) in filteredParks" :key="p.id" :id="`park-${p.id}`"
                class="transition-[border-color,transform] duration-300 ease-out hover:border-[rgba(245,213,122,0.22)] glass-strong rounded-[28px] grid grid-cols-1 lg:grid-cols-[1.1fr_1fr]"
                :class="{'lg:[direction:rtl]': idx%2===1}">
        <div class="relative [direction:ltr] p-3 w-full shrink-0">
          <div class="absolute top-7 left-4 z-10">
            <span class="ml-3 px-3 py-1.5 rounded-full text-[10px] font-mono uppercase tracking-[0.15em] font-semibold backdrop-blur-md"
                  :style="`background:${p.hasCabin ? 'rgba(245,213,122,0.16)' : 'rgba(122,211,164,0.16)'}; color:${p.hasCabin ? '#f5d57a' : '#7ad3a4'}; border:1px solid ${p.hasCabin ? 'rgba(245,213,122,0.4)' : 'rgba(122,211,164,0.4)'};`">
              {{ p.hasCabin ? 'Cabaña + Camping' : 'Solo Camping' }}
            </span>
          </div>
          <ImageCarousel :images="p.imagenes" :alt="p.nombre" aspect="aspect-[4/3] lg:aspect-auto lg:h-full w-full rounded-[20px]"/>
        </div>

        <div class="[direction:ltr] p-6 flex flex-col gap-4">
          <div>
            <div class="flex items-start justify-between gap-4">
              <h2 class="font-serif text-3xl lg:text-4xl text-(--color-bone) leading-tight tracking-tight">
                {{ p.nombre }}
              </h2>
              <span class="font-mono text-xs tracking-widest text-(--color-bone-mute) bg-white/5 px-2.5 py-1 mt-3 rounded-lg shrink-0">
                #{{ String(p.id).padStart(2,'0') }}
              </span>
            </div>
            
            <div class="mt-2.5 flex flex-wrap items-center justify-between gap-2 border-b border-white/5 pb-4">
              <div class="text-[14px] text-(--color-bone-soft) flex items-center gap-1.5">
                <MapPin :size="14" class="text-(--color-accent)" />
                {{ p.direccion }}
              </div>
              <span class="font-mono text-[10px] mt-1 tracking-wider text-(--color-bone-mute) bg-white/5 px-2 py-0.5 rounded">
                {{ p.latitud.toFixed(3) }}°{{ p.latitud < 0 ? 'S' : 'N' }}, {{ p.longitud.toFixed(3) }}°{{ p.longitud < 0 ? 'O' : 'E' }}
              </span>
            </div>
          </div>
          <p class="text-[13px] text-(--color-bone-soft) leading-normal line-clamp-2">{{ p.descripcion || 'Sin descripción' }}</p>

          <div class="grid grid-cols-3 gap-3">
            <div class="rounded-xl glass border border-white/5 flex py-2 flex-col justify-center items-center text-center">
              <div class="font-mono text-[10.5px] uppercase tracking-widest text-(--color-bone-soft)/80">Horario</div>
              <div class="font-serif text-[28px] leading-none">{{ horario(p) }}</div>
            </div>
            <div v-if="p.hasCabin" class="rounded-xl glass border border-white/5 flex py-2 flex-col justify-center items-center text-center">
              <div class="font-mono text-[10.5px] uppercase tracking-widest text-(--color-bone-soft)/80">Cabañas disponibles</div>
              <div class="font-serif text-[28px] leading-none text-glow">{{ p.cabanas_libres }}</div>
            </div>
            <div v-else class="rounded-xl glass border border-white/5 flex py-2 flex-col justify-center items-center text-center">
              <div class="font-mono text-[13px] uppercase tracking-widest text-(--color-bone-soft)/80">Cabañas no disponibles</div>
            </div>
            <div class="rounded-xl glass border border-white/5 flex py-2 flex-col justify-center items-center text-center">
              <div class="font-mono text-[10.5px] uppercase tracking-widest text-(--color-bone-soft)/80">Campings disponibles</div>
              <div class="font-serif text-[28px] leading-none" style="color:#7ad3a4">{{ p.campings_libres }}</div>
            </div>
          </div>

          <div class="glass-strong rounded-xl p-5 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div class="flex-1 flex flex-col items-center text-center gap-1">
              <span class="text-[11px] font-mono uppercase tracking-widest text-(--color-bone-soft)/60">Tarifa por noche</span>
              <span class="font-serif text-xl lg:text-2xl text-[#CAD2C5]">
                ${{ p.precio_minimo }} <span class="text-[#848E7E] mx-1">—</span> ${{ p.precio_maximo }}
              </span>
            </div>
            <div class="hidden sm:block w-0.5 h-15 bg-white/5"></div> 
            <div class="flex-1 flex flex-col items-center text-center gap-1">
              <span class="text-[11px] font-mono uppercase tracking-widest text-(--color-bone-soft)/60">Capacidad de personas</span>
              <span class="font-serif text-xl lg:text-2xl text-[#A3B19B]">
                {{ p.capacidad_minima }} <span class="text-[#525E4E] mx-1">—</span> {{ p.capacidad_maxima }}
              </span>
            </div>
          </div>

          <div class="flex flex-wrap gap-2">
            <span v-for="s in p.servicios" :key="s.id" class="glass inline-flex items-center gap-1.75 px-2.75 py-1.5 rounded-[9px] text-[12px] text-(--color-bone-soft) hover:text-(--color-green) hover:border-(--color-green)/50 transition-colors duration-300">
              {{ s.nombre }}
            </span>
          </div>

          <div class="mt-auto pt-2 border-t border-white/5 flex flex-wrap items-center justify-between gap-3">
            <span class="text-[13px] font-semibold px-3.5 py-2 rounded-full tracking-wider uppercase h-fit" :class="getParkStatusClass(p)">
              {{ getParkStatusText(p) }}
            </span>
            <div class="ml-auto flex items-center gap-2">
              <AppButton variant="outline" class="w-50" @click="openLodgingModal(p)">
                Ver hospedajes
              </AppButton>
              <AppLink v-if="getParkStatusClass(p) !== 'status-unavailable'" :href="auth.isLoggedIn ? `/reservar?park=${p.id}` : '/auth'" variant="yellow" class="w-50" :iconRight="ArrowRight">
                Reservar
              </AppLink>
              <AppButton v-else :disabled=true variant="primary" class="w-50">
                Reservar
              </AppButton>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div v-if="selectedParkForModal" class="lb-overlay fixed inset-0 z-2000 flex items-center justify-center p-4 sm:p-8 animate-fade-in" @click.self="closeModal">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-md"></div>
      <div class="lb-panel relative glass-strong-modal rounded-[26px] w-full max-w-270 max-h-[90vh] overflow-hidden flex flex-col animate-scale-up">
        <div class="flex items-center justify-between gap-4 px-6 py-5 border-b border-white/8 shrink-0">
          <div>
            <div class="font-serif text-[26px] leading-tight text-(--color-bone)">{{ selectedParkForModal.nombre }}</div>
            <div class="text-[12px] text-(--color-bone-mute) mt-0.5 flex items-center gap-1">
              <MapPin :size="12" class="text-(--color-accent)" />
              {{ selectedParkForModal.direccion }}
            </div>
          </div>
          <div class="flex items-center gap-3">
            <div class="hidden sm:flex items-center gap-1 glass rounded-full p-1">
              <button v-for="tab in modalTabs" :key="tab.id" class="px-4 py-2 rounded-full text-[13px] transition-all duration-200" 
                      :class="activeTab === tab.id ? 'bg-(--color-accent) text-black font-medium' : 'text-(--color-bone-mute) hover:text-(--color-bone)'" 
                      @click="activeTab = tab.id">
                {{ tab.label }} 
                <span class="opacity-60 ml-1">
                  ({{ tab.id === 'cabanas' ? countByType('CABANA') : countByType('CAMPING') }})
                </span>
              </button>
            </div>
            
            <button class="w-9 h-9 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center transition-colors text-(--color-bone)" @click="closeModal">
              <svg width="14" height="14" viewBox="0 0 12 12" fill="none"><path d="M2 2l8 8M10 2l-8 8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto min-h-0">
          <div v-if="lodgingStore.loading" class="flex items-center justify-center py-20">
            <div class="text-(--color-bone-mute)">Cargando hospedajes...</div>
          </div>
          <div v-else-if="filteredHospedajes.length" class="overflow-x-auto px-6 pt-5 pb-6 snap-x snap-mandatory">
            <div class="grid grid-flow-col auto-cols-[320px] gap-5">
              <article v-for="h in filteredHospedajes" :key="h.id"
                  class="snap-start park-card glass rounded-3xl overflow-hidden flex flex-col cursor-pointer relative" >
                  <div class="absolute top-3 left-3 flex items-center gap-2 z-50">
                    <span class="px-2.5 py-1 rounded-full text-[10.5px] font-mono uppercase tracking-[0.12em]"
                      :style="CATEGORIA_STYLES[h.categoria] || 'background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); color: #a8b3ad;'">
                      {{ h.categoria }}
                    </span>
                    <span class="px-2.5 py-1 rounded-full text-[10.5px] font-mono uppercase tracking-[0.12em]" :style="ESTADO_STYLES[h.estado] || ''">
                      {{ h.estado.toLowerCase() }}
                    </span>
                  </div>
                  <ImageCarousel :images="h.imagenes" :alt="`${h.tipo} #${h.id}`" aspect="aspect-[16/10]" />

                  <div class="p-5 flex flex-col gap-3 flex-1">
                    <div>
                      <div class="flex items-baseline justify-between gap-2">
                        <div class="font-serif text-[21px] leading-tight capitalize text-white">
                          {{ h.tipo.toLowerCase() }} #{{ String(h.id).padStart(2, '0') }}
                        </div>
                      </div>
                    </div>

                    <p class="text-[13px] text-(--color-bone-mute) leading-normal line-clamp-2">
                      {{ h.descripcion || 'Sin descripción disponible.' }}
                    </p>

                    <div class="glass-strong rounded-xl p-5 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div class="flex-1 flex flex-col items-center text-center gap-1">
                        <span class="text-[11px] font-mono uppercase tracking-widest text-(--color-bone-soft)/60">Precio por noche</span>
                        <span class="font-serif text-xl lg:text-2xl text-[#CAD2C5]">
                          ${{ h.precio }} 
                        </span>
                      </div>
                      <div class="hidden sm:block w-0.5 h-15 bg-white/5"></div> 
                      <div class="flex-1 flex flex-col items-center text-center gap-1">
                        <span class="text-[11px] font-mono uppercase tracking-widest text-(--color-bone-soft)/60">Capacidad</span>
                        <span class="font-serif text-xl lg:text-2xl text-[#A3B19B]">
                          {{ h.capacidad }}
                        </span>
                      </div>
                    </div>

                    <div class="grid grid-cols-2 gap-3">
                      <div class="rounded-xl glass border border-white/5 flex py-2 flex-col justify-center items-center text-center">
                        <div class="font-mono text-[10.5px] uppercase tracking-widest text-(--color-bone-soft)/80">Camas</div>
                        <div class="font-serif text-[28px] leading-none text-glow">{{ h.num_camas ?? 0 }}</div>
                      </div>
                      <div class="rounded-xl glass border border-white/5 flex py-2 flex-col justify-center items-center text-center">
                        <div class="font-mono text-[10.5px] uppercase tracking-widest text-(--color-bone-soft)/80">Baños</div>
                        <div class="font-serif text-[28px] leading-none" style="color:#7ad3a4">{{ h.num_banos ?? 0 }}</div>
                      </div>
                    </div>

                    <div v-if="h.tiene_agua || h.tiene_luz || h.tiene_regadera" class="flex flex-wrap gap-2 pt-1">
                      <div class="w-full text-[10px] uppercase tracking-wider text-(--color-bone-mute) mb-1">Servicios disponibles</div>
                      <span v-if="h.tiene_agua" class="glass inline-flex items-center gap-1.75 px-2.75 py-1.5 rounded-[9px] text-[12px] text-(--color-bone-soft) hover:text-(--color-green) hover:border-(--color-green)/50 transition-colors duration-300">
                        <Droplet :size="12"/> Agua
                      </span>
                      <span v-if="h.tiene_luz" class="glass inline-flex items-center gap-1.75 px-2.75 py-1.5 rounded-[9px] text-[12px] text-(--color-bone-soft) hover:text-(--color-green) hover:border-(--color-green)/50 transition-colors duration-300">
                        <Lightbulb :size="12"/> Luz
                      </span>
                      <span v-if="h.tiene_regadera" class="glass inline-flex items-center gap-1.75 px-2.75 py-1.5 rounded-[9px] text-[12px] text-(--color-bone-soft) hover:text-(--color-green) hover:border-(--color-green)/50 transition-colors duration-300">
                        <ShowerHead :size="12"/> Regadera
                      </span>
                    </div>
                  </div>
              </article>
            </div>
          </div>
          <div v-else class="flex flex-col items-center justify-center py-20 text-center px-6">
            <p class="text-(--color-bone-mute) text-[15px]">No hay opciones de {{ activeTab }} disponibles en este momento.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { MapPin, ArrowRight, Droplet, Lightbulb, ShowerHead } from "lucide-vue-next";
import ImageCarousel from "../ui/ImageCarousel.vue";
import { is24Hours, getParkStatusText, getParkStatusClass } from "../../utils/parkStatus";
import { useParksStore } from "../../stores/parks";
import { useLodgingStore } from "../../stores/lodging";
import type { Parque } from "../../stores/parks";
import AppLink from "../ui/AppLink.vue";
import AppButton from "../ui/AppButton.vue";
import FireflyLogo from "../ui/FireflyLogo.vue";
import { useAuthStore } from '../../stores/auth';
const auth = useAuthStore();

const parksStore = useParksStore();
const lodgingStore = useLodgingStore();
const filteredParks = computed(() => parksStore.filteredParks);

const selectedParkForModal = ref<Parque | null>(null);
const activeTab = ref<'cabanas' | 'campings'>('campings');

watch(selectedParkForModal, (newPark) => {
  if (newPark) {
    lodgingStore.loadHospedajesByPark(newPark.id)
  }
})

const filteredHospedajes = computed(() => {
  return lodgingStore.hospedajes.filter(h => {
    if (activeTab.value === 'cabanas') {
      return h.tipo === 'CABANA'
    } else {
      return h.tipo === 'CAMPING'
    }
  })
})

const countByType = (tipo: 'CABANA' | 'CAMPING') => {
  return lodgingStore.hospedajes.filter(h => h.tipo === tipo).length
}

const modalTabs = computed(() => {
  const tabs = []
  if (lodgingStore.hospedajes.some(h => h.tipo === 'CABANA')) {
    tabs.push({ id: 'cabanas', label: 'Cabañas' })
  }
  if (lodgingStore.hospedajes.some(h => h.tipo === 'CAMPING')) {
    tabs.push({ id: 'campings', label: 'Camping' })
  }
  return tabs
})

function horario(p: Parque) {
  return is24Hours(p) ? '24 hrs' : `${p.horario_apertura} – ${p.horario_cierre}`
}

function openLodgingModal(p: Parque) {
  selectedParkForModal.value = p;
  activeTab.value = p.hasCabin ? 'cabanas' : 'campings';
}

function closeModal() {
  selectedParkForModal.value = null;
}

const ESTADO_STYLES: Record<string, string> = {
  DISPONIBLE: 'background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); color: #cbd5e1;',
  OCUPADO: 'background: rgba(255,138,123,0.14); border: 1px solid rgba(255,138,123,0.4); color: #ff9b8a;',
  MANTENIMIENTO: 'background: rgba(245,158,11,0.14); border: 1px solid rgba(245,158,11,0.4); color: #fbbf24;',
}
const CATEGORIA_STYLES: Record<string, string> = {
  FAMILIAR: 'background: rgba(168, 85, 247, 0.12); border: 1px solid rgba(168, 85, 247, 0.35); color: #a855f7;',
  PAREJA: 'background: rgba(236, 72, 153, 0.12); border: 1px solid rgba(236, 72, 153, 0.35); color: #ec4899;',
  INDIVIDUAL: 'background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.35); color: #38bdf8;',
}
</script>

<style scoped>
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

.glass-strong-modal {
  background: linear-gradient(180deg, rgba(12,23,20,0.92), rgba(7,16,13,0.92));
  backdrop-filter: blur(22px) saturate(135%); 
  -webkit-backdrop-filter: blur(22px) saturate(135%);
  border:1px solid rgba(236,243,238,0.1);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes scaleUp {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}
.animate-scale-up {
  animation: scaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.park-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.park-card:hover, .park-card.is-hover {
  transform: translateY(-4px);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 12px 30px -10px rgba(0,0,0,0.5);
}
.park-card.is-selected {
  border-color: #7ad3a4;
  box-shadow: 0 0 20px rgba(122, 211, 164, 0.2);
}
</style>