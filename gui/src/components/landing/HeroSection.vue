<template>
  <section class="relative isolate min-h-svh overflow-hidden bg-(--color-bg) text-(--color-bone)">
    <div class="absolute inset-0 -z-20">
      <img src="../../assets/hero-forest.jpg" alt="Fondo hero" 
      class="h-full w-full object-cover" loading="eager" fetchpriority="high"/>
      <div class="absolute inset-0 bg-linear-to-b from-(--color-bg)/30 via-(--color-bg)/55 to-(--color-bg)"></div>
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_30%,var(--color-accent-soft),transparent_55%)]"></div>
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_120%,var(--color-green-soft),transparent_60%)]"></div>
    </div>
    <canvas ref="canvasRef" class="absolute inset-0 -z-10 h-full w-full pointer-events-none"></canvas>
    <div class="absolute inset-x-0 top-0 -z-10 h-px bg-linear-to-r from-transparent via-(--color-accent)/40 to-transparent"></div>
    <div class="relative mx-auto flex min-h-svh max-w-6xl flex-col items-center justify-start px-4 pt-20 pb-13 text-center sm:pt-28">
      <div class="animate-fade-up mb-7 inline-flex items-center gap-2.5 rounded-full border border-white/10 bg-white/4 px-4 py-1.5 text-[12.5px] font-medium tracking-wide text-(--color-bone)/85 backdrop-blur">
        <span class="relative inline-flex h-5 w-5">
          <span class="absolute inset-0 animate-ping opacity-50">
            <MoonStar class="h-full w-full text-(--color-accent)" />
          </span>
          <MoonStar class="relative h-5 w-5 text-(--color-accent)" />
        </span>
        Edición 2026
        <span class="text-(--color-bone)/40">·</span>
        <span class="text-(--color-bone)/85">Junio – Agosto</span>
      </div>
      <h1 class="animate-fade-up delay-100 font-serif text-balance text-[clamp(2.6rem,7vw,5.6rem)] font-medium leading-[0.95] tracking-tight">
        Persigue la luz <br class="hidden sm:block"/>
        <span class="relative inline-block text-glow text-(--color-accent)">
          que vive
          <svg class="absolute -bottom-2 left-0 h-3 w-full text-(--color-accent)/60" viewBox="0 0 200 12" preserveAspectRatio="none" fill="none">
            <path d="M2 8 Q 50 1 100 6 T 198 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </span>
        <em class="font-serif italic font-normal"> en el bosque.</em>
      </h1>
      <p class="animate-fade-up delay-200 mt-7 max-w-2xl text-pretty text-[15px] leading-relaxed text-(--color-bone)/70 sm:text-base">
        Cada noche de verano, millones de luciérnagas encienden los bosques protegidos del país.
        Reserva tu cabaña o zona de camping y vive un espectáculo natural que solo ocurre tres meses al año.
      </p>

      <div class="animate-fade-up delay-300 mt-10 flex flex-col items-center gap-3 sm:flex-row">
        <AppLink href="/parques" variant="outline" :icon="MapPinned">
          Explorar Parques
        </AppLink>
        <AppLink href="/auth?mode=signup" variant="yellow" :iconRight="UserPlus">
          Registrarse
        </AppLink>
      </div>

      <ul class="animate-fade-up delay-400 mt-10 flex flex-wrap items-center justify-center gap-2.5">
        <li v-for="b in badges" :key="b.label" class="inline-flex items-center gap-2 rounded-full border border-white/[0.07] bg-white/3 px-3.5 py-1.5 text-[12.5px] text-(--color-bone)/80 backdrop-blur">
          <component :is="b.icon" class="h-3.5 w-3.5 text-(--color-accent)" :stroke-width="2"/>
          {{ b.label }}
        </li>
      </ul>

      <div class="animate-fade-up delay-500 mt-6 flex flex-col items-center gap-2 text-[11px] uppercase tracking-[0.2em] text-(--color-bone)/40">
        <span>Desplaza para descubrir</span>
        <span class="block h-8 w-px animate-pulse bg-linear-to-b from-(--color-bone)/40 to-transparent"></span>
      </div>
    </div>

    <div class="absolute inset-x-0 bottom-0 overflow-hidden border-t border-white/6 bg-(--color-bg)/40 backdrop-blur-md">
      <div class="flex w-max animate-marquee gap-12 py-3 text-[11px] uppercase tracking-[0.25em] text-(--color-bone)/45">
        <template v-for="n in 2" :key="n">
        <template v-for="(lugar, index) in lugares" :key="`${n}-${index}`">
          <span>{{ lugar }}</span>
          <span v-if="index !== lugares.length - 1" class="text-(--color-accent)/60">.</span>
        </template>
      </template>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import AppLink from '../ui/AppLink.vue';
import { MapPinned, UserPlus, MoonStar, MonitorSmartphone, Shrub, CalendarDays } from 'lucide-vue-next';
import { startFireflies } from '../../utils/fireflies';
import { onMounted, onBeforeUnmount, ref } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);
let stop: (() => void) | null = null
onMounted(() => {
  if (!canvasRef.value) return;
  stop = startFireflies(canvasRef.value, {
    count: 50
  });
})
onBeforeUnmount(() => {
  stop?.()
})

const badges = [
  { label: "100% reservas en línea", icon: MonitorSmartphone },
  { label: "8 parques oficiales", icon: Shrub },
  { label: "3 meses de festival", icon: CalendarDays },
]

const lugares = [
  'Bosque Encantado',
  'Valle de las Sombras',
  'Río Susurrante',
  'Colina de los Suspiros',
  'Pradera Estelar',
  'Cueva de los Ecos',
];
</script>

<style scoped>
.glow-firefly {
  box-shadow:
    0 0 0 1px rgba(245, 213, 122, 0.25),
    0 0 24px -4px rgba(245, 213, 122, 0.55),
    0 0 60px -10px rgba(245, 213, 122, 0.4);
}

.text-glow {
  text-shadow: 0 0 24px rgba(245, 213, 122, 0.45), 0 0 60px rgba(245, 213, 122, 0.2);
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 40s linear infinite;
}
</style>