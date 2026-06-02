<template>
  <div class="pt-32 lg:px-8 pb-10 relative overflow-hidden">
    <section>
      <div class="mx-auto max-w-330 px-4 relative">
        <nav class="flex items-center gap-2 text-[12.5px] font-mono uppercase tracking-[0.14em] text-bone-soft mb-8 animate-fade-up">
          <RouterLink to="/" class="hover:text-bone transition">Inicio</RouterLink>
          <span class="text-bone-dim">/</span>
          <RouterLink to="/parques" class="hover:text-bone transition">Parques</RouterLink>
          <span class="text-bone-dim">/</span>
          <span class="text-glow">Todos los parques</span>
        </nav>

        <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
          <div class="grid items-end gap-8 sm:grid-cols-2">
            <div class="animate-fade-up">
              <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
                <span class="h-px w-6 bg-(--color-accent)/60"></span>
                Listado completo de parques
                <span class="h-px w-6 bg-(--color-accent)/60"></span>
              </span>
              <h1 class="font-serif font-normal leading-[0.95] tracking-tight text-[clamp(2.6rem,6vw,5rem)] mt-5">
                Descubre todos los<br><em class="italic text-glow text-glow">parques</em> del festival
              </h1>
            </div>
            <div class="animate-fade-up text-[15.5px] leading-relaxed pl-5 text-justify">
              <p class="text-(--color-bone-soft)">
                Explora la lista completa de parques disponibles para hospedarte durante el festival. Cada parque tiene su propio encanto y características únicas. Encuentra el lugar perfecto para tu aventura y disfruta de una experiencia inolvidable rodeado de naturaleza.
              </p>
              <div class="flex items-center gap-6 shrink-0 w-full justify-end pr-3">
                <div class="text-right">
                  <div class="font-serif text-5xl text-(--color-accent)">{{ parksStore.filteredParks.length }}</div>
                  <div class="text-[10px] uppercase tracking-wider text-(--color-bone-mute)">Parque{{ parksStore.filteredParks.length===1?'':'s' }} oficial{{ parksStore.filteredParks.length===1?'':'es' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
      <!-- Search Bar -->
    <section class="flex top-21 z-50 pb-5 mt-10 animate-fade-up">
      <div class="glass-strong rounded-2xl p-3 flex flex-col gap-3 w-full">
        <div class="flex flex-col xl:flex-row xl:items-center gap-3">
          <div class="relative flex-3 min-w-55">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-(--color-bone-soft) pointer-events-none">
              <Search :size="14" />
            </span>
            <input class="w-full h-11 pl-11 pr-4 bg-(--color-bg)/55 border border-white/10 rounded-full text-(--color-bone) text-sm outline-none transition focus:border-(--color-green) focus:ring-3 focus:ring-(--color-green)/15 placeholder:text-[#6d7872]" placeholder="Busca por el nombre del parque" v-model="parksStore.searchQuery" />
          </div>

          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-mono text-[10px] uppercase tracking-[0.14em] text-(--color-bone-soft) pl-1 hidden sm:inline">Hospedaje</span>
            <button  v-for="t in types" :key="t.id" 
              class="inline-flex items-center gap-2 h-9 px-4 rounded-full bg-white/5 border border-white/10 text-sm text-[#a8b3ad] cursor-pointer transition-[background-color,border-color,color] duration-300 ease-out hover:border-white/25 hover:text-(--color-bone)"
              :style="parksStore.filterType === t.id && t.id !== 'all' ? { backgroundColor: `${t.color}1e`, borderColor: `${t.color}66`, color: t.color } : parksStore.filterType === t.id && t.id === 'all' ? {
                backgroundColor: 'rgba(232,255,122,0.1)',
                borderColor: 'rgba(232,255,122,0.4)',
                color: '#E8FF7A'
              } : {}"
              @click="parksStore.filterType=t.id"
            >
              <component :is="t.icon" v-if="t.icon" :size="14" class="transition-all duration-300" :class="{'scale-110': parksStore.filterType === t.id}"/>
              {{ t.label }}
            </button>
          </div>

          <div class="hidden xl:block w-px h-7 bg-white/10"></div>

          <div class="relative flex-1 max-w-xs min-w-35">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-(--color-bone-soft) pointer-events-none">
              <Users :size="14" />
            </span>
            <input type="number" min="1" class="w-full h-11 pl-11 pr-4 bg-(--color-bg)/55 border border-white/10 rounded-full text-(--color-bone) text-sm outline-none transition focus:border-(--color-green) focus:ring-3 focus:ring-(--color-green)/15 placeholder:text-[#6d7872]" placeholder="Visitantes" v-model="parksStore.visitors" />
          </div>
          <span v-if="parksStore.visitorsError" class="text-xs text-red-400 absolute left-0 -bottom-5">
            {{ parksStore.visitorsError }}
          </span>
          <div class="relative">
            <button ref="buttonRef" class="flex items-center gap-2 px-4 h-11 bg-white/5 border border-white/10 hover:border-white/20 rounded-full text-sm text-(--color-bone) transition duration-200 cursor-pointer select-none" 
              :class="{ 'border-(--color-green)/40 bg-(--color-green)/5': sortOpen }"
              @click="sortOpen=!sortOpen">
              <SlidersHorizontal :size="13" class="text-(--color-bone-soft)" />
              <span class="font-medium">{{ sortLabel }}</span>
              <ChevronDown :size="14" class="text-(--color-bone-soft) transition-transform duration-300" :class="{ 'rotate-180 text-(--color-green)': sortOpen }" />
            </button>
            <Teleport to="body">
              <transition name="pop">
                <div v-if="sortOpen" 
                  class="fixed glass-strong border border-white/10 rounded-2xl p-1.5 shadow-2xl z-9999 backdrop-blur-xl animate-in fade-in zoom-in-95 duration-150"
                  :style="getDropdownPosition()">
                  <div class="px-3 py-1.5 text-[10px] font-mono uppercase tracking-wider text-(--color-bone-mute) border-b border-white/5 mb-1">
                    Ordenar por
                  </div>
                  <button v-for="s in sorts" :key="s.id" 
                    class="w-full text-left px-3 py-2.5 rounded-xl text-[13.5px] transition-all duration-200 flex items-center justify-between group cursor-pointer" 
                    :class="parksStore.sortBy === s.id ? 'bg-(--color-green)/10 text-(--color-green) font-medium' : 'text-(--color-bone-soft) hover:bg-white/5 hover:text-(--color-bone)'" 
                    @click="parksStore.sortBy = s.id; sortOpen = false"
                  >
                    {{ s.label }}
                    <Check v-if="parksStore.sortBy === s.id" :size="14" class="text-(--color-green)" />
                  </button>
                </div>
              </transition>
            </Teleport>
          </div>
          <div class="xl:ml-auto flex items-center gap-3 justify-between xl:justify-end border-t border-white/5 pt-2 xl:pt-0 xl:border-0">
            <span class="font-mono text-[11px] uppercase tracking-[0.14em] text-[#9AA39E]">{{ parksStore.filteredParks.length }} resultado{{ parksStore.filteredParks.length===1?'':'s' }}</span>
            <button v-if="parksStore.hasFilters" class="inline-flex items-center gap-1.5 h-8 px-3 rounded-full bg-(--color-danger)/10 border border-(--color-danger)/20 text-xs text-(--color-danger) cursor-pointer transition hover:bg-(--color-danger)/20" @click="parksStore.resetFilters">
              Limpiar ✕
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Search, Users, Home, Tent, SlidersHorizontal, ChevronDown, Check, } from 'lucide-vue-next'
import { useParksStore } from '../../stores/parks'

const parksStore = useParksStore()

const types = ref([
  { id: 'all', label: 'Todos', color: '', icon: '' },
  { id: 'cabin', label: 'Con Cabaña', color: '#f2dc4e', icon: Home },
  { id: 'camping', label: 'Con Camping', color: '#7ad3a4', icon: Tent },
])

const sorts = ref([
  { id: 'name-asc', label: 'Nombre A-Z' },
  { id: 'name-desc', label: 'Nombre Z-A' },
  { id: 'capacity-asc', label: 'Menor capacidad máxima' },
  { id: 'capacity-desc', label: 'Mayor capacidad máxima' },
  { id: 'avail', label: 'Disponibles primero' },
])

const sortOpen = ref(false)
const sortLabel = computed(() => {
  const s = sorts.value.find(s => s.id === parksStore.sortBy);
  return s ? s.label : 'Ordenar';
})

const buttonRef = ref<HTMLElement | null>(null)

const getDropdownPosition = () => {
  if (!buttonRef.value) return {}
  
  const rect = buttonRef.value.getBoundingClientRect()
  return {
    top: `${rect.bottom + 8}px`,
    right: `${window.innerWidth - rect.right}px`,
    width: '224px'
  }
}

const handleClickOutside = (event: MouseEvent) => {
  if (buttonRef.value && !buttonRef.value.contains(event.target as Node)) {
    sortOpen.value = false
  }
}

const handleScroll = () => {
  if (sortOpen.value) {
    sortOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.pop-enter-active,
.pop-leave-active {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(-8px);
}
</style>