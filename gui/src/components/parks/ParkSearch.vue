<template>
  <div class="mx-auto max-w-380 mt-5 px-5 lg:px-8 animate-fade-up">
    <section>
      <nav class="flex items-center gap-2 text-[12.5px] font-mono uppercase tracking-[0.14em] text-bone-soft mb-8 animate-fade-up">
        <a href="/" class="hover:text-bone transition">Inicio</a>
        <span class="text-bone-mute">/</span>
        <span class="text-glow">Parques</span>
      </nav>

      <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
        <div class="grid items-end gap-8 sm:grid-cols-2">
          <div class="animate-fade-up">
            <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
              Mapa del festival
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
              {{ useParksStore().filteredParks.length }} parque{{ useParksStore().filteredParks.length===1?'':'s' }} para explorar
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
            </span>
            <h1 class="font-serif font-normal leading-[0.95] tracking-tight text-[clamp(2.6rem,6vw,5rem)] mt-5">
              Encuentra tu lugar<br>para ver <em class="italic text-glow text-glow">la luz.</em>
            </h1>
          </div>
          <div class="animate-fade-up text-[15.5px] leading-relaxed">
            <p class="mb-3 text-(--color-bone-soft)">
              Explora los parques disponibles para acampar durante el festival. Cada parque tiene su propio encanto y características únicas, desde áreas de camping hasta cabañas acogedoras. Utiliza los filtros para encontrar el parque que mejor se adapte a tus necesidades y preferencias, y prepárate para una experiencia inolvidable bajo las estrellas.
            </p>
            <div class="flex items-center gap-6 shrink-0 w-full justify-end pr-8">
              <div class="text-right">
                <div class="font-serif text-4xl text-(--color-accent)">{{ useParksStore().filteredParks.length }}</div>
                <div class="text-[10px] uppercase tracking-wider text-(--color-bone-mute)">Parque{{ useParksStore().filteredParks.length===1?'':'s' }} oficial{{ useParksStore().filteredParks.length===1?'':'es' }}</div>
              </div>
              <div class="w-px h-12 bg-white/20"></div>
              <div class="text-right">
                <div class="font-serif text-4xl" style="color:#7ad3a4;">+12k</div>
                <div class="text-[10px] uppercase tracking-wider text-(--color-bone-mute)">Visitantes 2025</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="sticky top-21 z-50 pb-5 mt-10 animate-fade-up">
      <div class="glass-strong rounded-2xl p-3 flex flex-col gap-3">
        <div class="flex flex-col xl:flex-row xl:items-center gap-3">
          <div class="relative flex-3 min-w-55">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-(--color-bone-soft) pointer-events-none">
              <Search size="14" />
            </span>
            <input class="w-full h-11 pl-11 pr-4 bg-(--color-bg)/55 border border-white/10 rounded-full text-(--color-bone) text-sm outline-none transition focus:border-(--color-green) focus:ring-3 focus:ring-(--color-green)/15 placeholder:text-[#6d7872]" placeholder="Busca por el nombre del parque" v-model="parksStore.searchQuery" />
          </div>

          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-mono text-[10px] uppercase tracking-[0.14em] text-(--color-bone-soft) pl-1 hidden sm:inline">Hospedaje</span>
            <button 
              v-for="t in types" 
              :key="t.id" 
              class="inline-flex items-center gap-2 h-9 px-4 rounded-full bg-white/5 border border-white/10 text-sm text-[#a8b3ad] cursor-pointer transition-[background-color,border-color,color] duration-300 ease-out hover:border-white/25 hover:text-(--color-bone)"
              :style="parksStore.filterType === t.id && t.id !== 'all' ? { backgroundColor: `${t.color}1e`, borderColor: `${t.color}66`, color: t.color } : parksStore.filterType === t.id && t.id === 'all' ? {
                backgroundColor: 'rgba(232,255,122,0.1)',
                borderColor: 'rgba(232,255,122,0.4)',
                color: '#E8FF7A'
              } : {}"
              @click="parksStore.filterType=t.id"
            >
              <component :is="t.icon" v-if="t.icon" size="14" class="transition-all duration-300" :class="{'scale-110': parksStore.filterType === t.id}"/>
              {{ t.label }}
            </button>
          </div>

          <div class="hidden xl:block w-px h-7 bg-white/10"></div>

          <div class="relative flex-1 max-w-xs min-w-35">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-(--color-bone-soft) pointer-events-none">
              <Users size="14" />
            </span>
            <input type="number" min="1" class="w-full h-11 pl-11 pr-4 bg-(--color-bg)/55 border border-white/10 rounded-full text-(--color-bone) text-sm outline-none transition focus:border-(--color-green) focus:ring-3 focus:ring-(--color-green)/15 placeholder:text-[#6d7872]" placeholder="Visitantes" v-model="parksStore.visitors" />
            <span v-if="parksStore.visitorsError" class="text-xs text-red-400 absolute left-0 -bottom-5">
              {{ parksStore.visitorsError }}
            </span>
          </div>

          <button 
            @click="showAdvanced = !showAdvanced"
            class="inline-flex items-center gap-2 h-9 px-4 rounded-full bg-white/5 border border-white/10 text-sm text-[#a8b3ad] cursor-pointer transition-all duration-300 ease-out hover:border-white/25 hover:text-(--color-bone)"
            :class="{'bg-white/10! text-(--color-bone)! border-white/30!': showAdvanced}"
          >
            <svg class="transition-transform duration-400 ease-out" :class="{'rotate-180': showAdvanced}" width="13" height="13" viewBox="0 0 16 16" fill="none">
              <path d="M2 4h12M4 8h8M6 12h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
            </svg>
            {{ showAdvanced ? 'Ocultar filtros' : 'Más filtros' }}
          </button>

          <div class="xl:ml-auto flex items-center gap-3 justify-between xl:justify-end border-t border-white/5 pt-2 xl:pt-0 xl:border-0">
            <span class="font-mono text-[11px] uppercase tracking-[0.14em] text-[#9AA39E]">{{ parksStore.filteredParks.length }} resultado{{ parksStore.filteredParks.length===1?'':'s' }}</span>
            <button v-if="parksStore.hasFilters" class="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-(--color-danger)/10 border border-(--color-danger)/20 text-xs text-(--color-danger) cursor-pointer transition hover:bg-(--color-danger)/20" @click="parksStore.resetFilters">
              Limpiar ✕
            </button>
          </div>
        </div>

        <div v-show="showAdvanced" class="border-t border-white/10 pt-4 mt-1 grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-up">
          <div class="flex flex-col gap-2">
            <span class="label-mono">Rango de Presupuesto ($)</span>
            <div class="flex items-center gap-2">
              <div class="relative flex-1">
                <input type="number" placeholder="Mín" min="0" v-model="parksStore.priceMin" class="w-full h-10 px-4 bg-(--color-bg)/40 border border-white/5 rounded-xl text-(--color-bone) text-xs outline-none focus:border-(--color-green) placeholder:text-[#5c6660]" />
              </div>
              <span class="text-bone-mute text-xs">—</span>
              <div class="relative flex-1">
                <input type="number" placeholder="Máx" min="0" v-model="parksStore.priceMax" class="w-full h-10 px-4 bg-(--color-bg)/40 border border-white/5 rounded-xl text-(--color-bone) text-xs outline-none focus:border-(--color-green) placeholder:text-[#5c6660]" />
              </div>
            </div>
            <span v-if="parksStore.priceError" class="text-xs text-red-400 mt-0.5">{{ parksStore.priceError }}</span>
          </div>

          <div class="flex flex-col gap-2">
            <span class="label-mono">Horario del Parque</span>
            <div class="flex items-center gap-2">

              <div class="relative flex-1 group">
                <Clock3 size="14" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#7ad3a4]/80 group-hover:text-[#7ad3a4] transition-colors z-10 pointer-events-none" />
                <select v-model="parksStore.timeOpen" @change="$event.target.blur()" class="festival-select" :class="{ 'festival-select-active': parksStore.timeOpen }">
                  <option value="" disabled selected hidden>Apertura</option>
                  <option value="">Cualquier hora</option>
                  <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
                </select>
                <ChevronDown size="13" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#9AA39E] group-hover:text-white transition-transform duration-300 pointer-events-none layout-icon" />
              </div>

              <span class="text-bone-mute/50 text-xs font-mono">—</span>

              <div class="relative flex-1 group">
                <Clock3 size="14" class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#7ad3a4]/80 group-hover:text-[#7ad3a4] transition-colors z-10 pointer-events-none" />
                <select v-model="parksStore.timeClose" @change="$event.target.blur()" class="festival-select" :class="{ 'festival-select-active': parksStore.timeClose }">
                  <option value="" disabled selected hidden>Cierre</option>
                  <option value="">Cualquier hora</option>
                  <option v-for="h in hours" :key="h" :value="h">{{ h }}</option>
                </select>
                <ChevronDown size="13" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#9AA39E] group-hover:text-white transition-transform duration-300 pointer-events-none layout-icon" />
              </div>
            </div>
            <span v-if="parksStore.timeError" class="text-xs text-red-400 mt-0.5">{{ parksStore.timeError }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search, Users, Home, Tent, Clock3, ChevronDown } from 'lucide-vue-next'
import { useParksStore } from '../../stores/parks'

const parksStore = useParksStore()
const showAdvanced = ref(false)

const types = ref([
  { id: 'all', label: 'Todos', color: '', icon: '' },
  { id: 'cabin', label: 'Con Cabaña', color: '#f2dc4e', icon: Home },
  { id: 'camping', label: 'Con Camping', color: '#7ad3a4', icon: Tent },
])

const hours = Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00`)
</script>

<style scoped>
.festival-select {
  width: 100%;
  height: 44px;
  padding-left: 2.6rem; 
  padding-right: 2.4rem;
  border-radius: 9999px;
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border: 1px solid rgba(255,255,255,0.1);
  color: var(--color-bone-soft, #a8b3ad);
  font-size: 0.875rem;
  font-weight: 500;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
  transition: all .25s ease;
}

:deep(.group:hover) .festival-select {
  background: rgba(255,255,255,0.08);
  border-color: rgba(255,255,255,0.25);
  color: var(--color-bone);
}

.festival-select:focus {
  outline: none;
  color: var(--color-bone);
  border-color: rgba(122,211,164,.5);
  box-shadow:
    0 0 0 3px rgba(122,211,164,.12),
    0 0 24px rgba(122,211,164,.08);
}

.festival-select-active {
  color: #7ad3a4 !important;
  border-color: rgba(122,211,164,.35);
  background: rgba(122,211,164,.08) !important;
}

.festival-select option {
  background-color: #141715;
  color: #a8b3ad;
  padding: 8px;
}

.festival-select option:disabled {
  color: #4b5550;
}

:deep(.festival-select:focus) ~ .layout-icon {
  transform: translateY(-50%) rotate(180deg);
  color: #7ad3a4;
}

.layout-icon {
  transition: transform 0.3s ease, color 0.3s ease;
}
</style>