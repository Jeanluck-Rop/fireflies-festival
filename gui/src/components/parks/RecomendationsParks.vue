<template>
  <section class="relative mx-auto max-w-380 px-6 lg:px-10 mt-20 mb-32">
    <header class="animate-fade-up">
      <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
        <span class="h-px w-6 bg-(--color-accent)/60"></span>
        Recomendaciones para tu visita
        <span class="h-px w-6 bg-(--color-accent)/60"></span>
      </span>
      <div class="grid items-end gap-x-8 gap-y-2 sm:grid-cols-2 mt-4">
        <h2 class="font-display text-balance text-[clamp(2rem,4.5vw,3.4rem)] font-medium leading-[1.05] tracking-tight">
          Haz que tu noche <br />se <em class="font-display italic text-glow">encienda</em>
        </h2>
        <p class="mb-7 text-[15px] leading-relaxed text-(--color-bone)/65">
          Tres parques elegidos al azar de la temporada. Cada noche el comité destaca un favorito distinto.
        </p>
      </div>
    </header>

    <div v-if="picked.length" class="animate-fade-up mt-8 mb-16 grid grid-cols-1 gap-4 lg:h-155 lg:grid-cols-3 lg:grid-rows-2 lg:gap-5">
      <!-- Parque Grande -->
      <article v-if="hero"
        class="group relative cursor-pointer overflow-hidden rounded-[28px] ring-1 ring-white/10 transition-[box-shadow,transform] duration-500 hover:shadow-[0_24px_60px_-24px_rgba(0,0,0,0.7)] min-h-155 lg:col-span-2 lg:row-span-2 lg:min-h-0"
        :class="{ 'ring-2 ring-(--color-accent)/60': selectedId === hero.id }" @click="selectPark(hero)" >
        <template v-if="hasPhoto(hero)">
          <img
            :src="firstImage(hero)" :alt="hero.nombre"
            class="absolute inset-0 h-full w-full scale-[1.001] object-cover transition-transform duration-1600 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:scale-110 motion-reduce:transition-none motion-reduce:group-hover:scale-100"
          />
          <div class="absolute inset-0 bg-[linear-gradient(90deg,var(--color-bg)_0%,rgba(7,16,13,0.78)_45%,rgba(7,16,13,0.25)_75%,transparent_100%)]"></div>
        </template>
        <div v-else class="photo-slot absolute inset-0">
          <FireflyLogo :pulse="true" :drift="false" size="w-16 h-16" />
          <span class="px-6 text-center font-mono text-[12px] uppercase tracking-[0.14em] text-(--color-bone-mute)">{{ hero.nombre }}</span>
        </div>

        <div class="relative flex h-full items-end lg:items-center">
          <div class="max-w-140 p-7 lg:p-12">
            <div class="flex flex-wrap items-center gap-2.5">
              <span class="inline-flex items-center gap-2 rounded-full border border-(--color-accent)/30 bg-(--color-accent)/10 px-3.5 py-1.5 font-mono text-[11px] uppercase tracking-[0.16em] text-(--color-accent)">
                <span class="relative inline-flex h-4 w-4">
                  <Sparkles class="absolute inset-0 h-full w-full animate-ping opacity-50" />
                  <Sparkles class="relative h-4 w-4" />
                </span>
                Destacado de la temporada
              </span>
              <span class="card-status" :class="getParkStatusClass(hero)">{{ getParkStatusText(hero) }}</span>
            </div>

            <h3 class="mb-3 mt-5 font-serif text-[clamp(2.1rem,4.4vw,3.6rem)] leading-[0.96] [text-shadow:0_0_36px_rgba(123,216,176,0.28)]">
              {{ hero.nombre }}
            </h3>

            <div class="mb-4 flex items-center gap-1.5 text-sm text-(--color-bone-soft)">
              <MapPin class="h-4 w-4 text-(--color-accent)" /><span>{{ hero.direccion }}</span>
            </div>

            <p class="mb-7 max-w-[46ch] text-[15px] leading-[1.65] text-(--color-bone-soft) line-clamp-3">
              {{ hero.descripcion || 'Sin descripción disponible.' }}
            </p>

            <div class="mb-8 flex flex-wrap items-center gap-6">
              <div>
                <div class="font-serif text-[26px] leading-none text-glow">{{ horario(hero) }}</div>
                <div class="mt-1.5 font-mono text-[10px] uppercase tracking-[0.14em] text-(--color-bone-mute)">horario</div>
              </div>
              <div class="h-9 w-px bg-white/10"></div>
              <div>
                <div class="font-serif text-[26px] leading-none text-(--color-green)">Jun–Ago</div>
                <div class="mt-1.5 font-mono text-[10px] uppercase tracking-[0.14em] text-(--color-bone-mute)">pico de cortejo</div>
              </div>
            </div>

            <div class="flex flex-wrap gap-2.5">
              <AppButton variant="primary" @click.stop="selectPark(hero)">
                Conocer este parque
                <ArrowUpRight class="h-4 w-4 ml-2" :stroke-width="2" />
              </AppButton>
              <AppButton variant="outline" @click.stop="viewOnMap(hero)">
                Ver en el mapa
                <MapPin class="h-4 w-4 ml-2" />
              </AppButton>
            </div>
          </div>
        </div>
      </article>

      <!-- Parques pequeños -->
      <article v-for="p in sides" :key="p.id"
        class="group relative cursor-pointer overflow-hidden rounded-3xl ring-1 ring-white/10 transition-[box-shadow,transform] duration-500 hover:shadow-[0_24px_60px_-24px_rgba(0,0,0,0.7)] min-h-57.5 lg:min-h-0"
        :class="{ 'ring-2 ring-(--color-accent)/60': selectedId === p.id }" @click="hero && viewOnMap(p)" >
        <template v-if="hasPhoto(p)">
          <img :src="firstImage(p)" :alt="p.nombre"
            class="absolute inset-0 h-full w-full scale-[1.001] object-cover transition-transform duration-1500 ease-[cubic-bezier(0.16,1,0.3,1)] group-hover:scale-110 motion-reduce:transition-none motion-reduce:group-hover:scale-100" />
          <div class="absolute inset-0 bg-[linear-gradient(0deg,var(--color-bg)_0%,rgba(7,16,13,0.55)_45%,transparent_80%)]"></div>
        </template>
        <div v-else class="photo-slot absolute inset-0">
          <FireflyLogo :pulse="true" :drift="false" size="w-12 h-12" />
          <span class="px-5 text-center font-mono text-[10px] uppercase tracking-[0.14em] text-(--color-bone-mute)">{{ p.nombre }}</span>
        </div>

        <span class="absolute left-4 top-4 z-10 inline-flex items-center gap-1.5 rounded-full border border-(--color-accent)/30 bg-(--color-bg)/70 px-2.5 py-1 font-mono text-[9px] uppercase tracking-[0.14em] text-(--color-accent) backdrop-blur">
          <Sparkles class="h-3 w-3" /> Destacado
        </span>

        <div class="relative flex h-full flex-col justify-end p-6">
          <h3 class="font-serif text-[22px] leading-tight">{{ p.nombre }}</h3>
          <div class="mt-1 flex items-center gap-1.5 text-[13px] text-(--color-bone-mute)">
            <MapPin class="h-3.5 w-3.5" />{{ p.direccion }}
          </div>
          <div class="mt-3 flex items-center justify-between border-t border-white/10 pt-3">
            <span class="font-mono text-[11px] uppercase tracking-[0.14em] text-(--color-bone-soft)">{{ horario(p) }}</span>
            <span class="card-status" :class="getParkStatusClass(p)">{{ getParkStatusText(p) }}</span>
          </div>
        </div>
      </article>
    </div>

    <!-- ===== Colecciones ===== -->
    <div class="mb-6 animate-fade-up">
      <div class="mb-2 font-mono text-[11px] uppercase tracking-[0.22em] text-(--color-accent)">Explora por momento</div>
      <p class="max-w-[52ch] text-[14.5px] leading-[1.6] text-(--color-bone-soft)">
        Colecciones curadas para distintos tipos de visita. Toca una y el mapa mostrara el parque.
      </p>
    </div>

    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 animate-fade-up">
      <button v-for="c in collections" :key="c.id"
        class="glass relative flex min-h-55 flex-col gap-4 overflow-hidden rounded-3xl p-7 text-left transition-all duration-300 hover:-translate-y-1 hover:border-white/15"
        @click="hero && viewOnMap(hero)" >
        <div class="pointer-events-none absolute -right-8 -top-8 h-32 w-32 rounded-full opacity-[0.12] blur-2xl" :style="{ background: c.accent }"></div>
        <div class="inline-flex h-12 w-12 items-center justify-center rounded-2xl border" :style="{ borderColor: c.accent + '55', background: c.accent + '14' }">
          <component :is="c.icon" class="h-5 w-5" :style="{ color: c.accent }" :stroke-width="1.8" />
        </div>
        <div class="mt-auto">
          <div class="font-serif text-[24px] leading-tight">{{ c.title }}</div>
          <p class="mt-2 text-[13px] leading-normal text-(--color-bone-soft)">{{ c.desc }}</p>
        </div>
        <div class="flex items-center justify-between border-t border-white/5 pt-3">
          <span class="font-mono text-[10.5px] uppercase tracking-[0.14em] text-(--color-bone-mute)">{{ totalParks }} parques</span>
          <span class="text-[12.5px] font-medium" :style="{ color: c.accent }">Ver en el mapa →</span>
        </div>
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { Sparkles, MapPin, ArrowUpRight, Heart, Users, Camera, Compass } from 'lucide-vue-next'
import AppButton from '../ui/AppButton.vue'
import FireflyLogo from '../ui/FireflyLogo.vue'
import { is24Hours, getParkStatusText, getParkStatusClass } from '../../utils/parkStatus'
import { useParksStore } from '../../stores/parks'
import type { Parque } from '../../stores/parks'

const store = useParksStore()
const selectedId = computed(() => store.selectedPark?.id ?? null)

/* --- 3 recomendaciones al azar, estables (se eligen al cargar los parques) --- */
function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

const picked = ref<Parque[]>([])
watch(() => store.parks, (parks) => {
  if (!parks.length) { picked.value = []; return }
  const activos = parks.filter(p => p.activo)
  const pool = activos.length >= 3 ? activos : parks
  picked.value = shuffle(pool).slice(0, 3)
}, { immediate: true })

const hero = computed<Parque | undefined>(() => picked.value[0])
const sides = computed<Parque[]>(() => picked.value.slice(1, 3))

const totalParks = computed(() => store.parks.length)

function firstImage(p?: Parque): string | undefined {
  const img = p?.imagenes?.[0] as any
  if (!img) return undefined
  return typeof img === 'string' ? img : (img.url ?? img.src ?? img.ruta ?? img.imagen)
}
const hasPhoto = (p?: Parque) => !!firstImage(p)

function horario(p: Parque) {
  return is24Hours(p) ? '24 hrs' : `${p.horario_apertura} – ${p.horario_cierre}`
}

/* --- Selección compartida con mapa y lista --- */
function selectPark(p: Parque) {
  store.selectPark(p)
}
function viewOnMap(p: Parque) {
  store.selectPark(p)
  document.querySelector('.parks-container')
    ?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

/* --- Tarjetas de consejo --- */
const collections = [
  { id: 'cita',     title: 'Primera cita',        desc: 'Senderos íntimos y miradores tranquilos para dos.',          accent: '#F5D57A', icon: Heart },
  { id: 'familia',  title: 'En familia',          desc: 'Recorridos accesibles y seguros para todas las edades.',     accent: '#7BD8B0', icon: Users },
  { id: 'foto',     title: 'Fotografía nocturna', desc: 'Picos de luz y cielos despejados para capturar el cortejo.', accent: '#7BA7D4', icon: Camera },
  { id: 'aventura', title: 'Aventura',            desc: 'Caminatas largas y desniveles para los más intrépidos.',     accent: '#C9A7E8', icon: Compass },
]
</script>


<style scoped>
.photo-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  border: 1px dashed rgba(123, 216, 176, 0.28);
  background:
    radial-gradient(120% 100% at 30% 0%, rgba(123, 216, 176, 0.1), transparent 60%),
    repeating-linear-gradient(45deg, rgba(255, 255, 255, 0.025) 0 12px, transparent 12px 24px),
    var(--color-bg-soft);
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