<template>
  <section class="relative isolate min-h-svh overflow-hidden bg-(--color-bg) text-(--color-bone)">
    <div class="absolute inset-0 -z-20">
      <img src="../../assets/hero-forest.jpg" alt="Fondo hero" 
      class="h-full w-full object-cover opacity-65" loading="eager" fetchpriority="high"/>
      <div class="absolute inset-0 bg-linear-to-b from-(--color-bg)/45 via-(--color-bg)/70 to-(--color-bg)"></div>
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_30%,var(--color-accent-soft),transparent_70%)] opacity-40"></div>
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_120%,var(--color-green-soft),transparent_75%)] opacity-30"></div>
    </div>
    <canvas ref="canvasRef" class="absolute inset-0 -z-10 h-full w-full pointer-events-none"></canvas>
    <div class="absolute inset-x-0 top-0 -z-10 h-px bg-linear-to-r from-transparent via-(--color-accent)/40 to-transparent"></div>
    <div class="relative mx-auto flex min-h-svh max-w-6xl flex-col items-center justify-start px-4 pt-20 pb-13 text-center sm:pt-28">
      <span class="animate-fade-up delay-100 inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
        <span class="h-px w-6 bg-(--color-accent)/60"></span>
        La temporada está cerca
        <span class="h-px w-6 bg-(--color-accent)/60"></span>
      </span>
      <h2 class="animate-fade-up delay-100 font-serif text-balance text-[clamp(2.6rem,7vw,5.6rem)] font-medium leading-[0.95] tracking-tight">
        La luz no espera. <br class="hidden sm:block"/>
        <em class="font-display italic font-normal text-glow">Tú tampoco deberías.</em>
      </h2>
      <p class="animate-fade-up delay-200 mt-7 max-w-2xl text-pretty text-[15px] leading-relaxed text-(--color-bone)/70 sm:text-base">
        Explora los parques oficiales y asegura tu lugar para el Festival 2026.
        Los lugares son limitados y se llenan rápido. No pierdas la oportunidad de vivir esta experiencia única.
      </p>

      <div class="animate-fade-up delay-300 mt-10 flex flex-col items-center gap-3 sm:flex-row">
        <AppLink href="/parques" variant="outline" :icon="MapPinned">
          Explorar Parques
        </AppLink>
        <AppLink :href="auth.isLoggedIn ? '/reservar' : '/auth'" variant="yellow" :iconRight="CalendarSearch">
          Reservar Ahora
        </AppLink>
      </div>

      <ul class="animate-fade-up delay-400 mt-10 flex flex-wrap items-center justify-center gap-2.5">
        <li v-for="b in badges" :key="b.label" class="inline-flex items-center gap-2 rounded-full border border-white/[0.07] bg-white/3 px-3.5 py-1.5 text-[12.5px] text-(--color-bone)/80 backdrop-blur">
          <component :is="b.icon" class="h-3.5 w-3.5 text-(--color-accent)" :stroke-width="2"/>
          {{ b.label }}
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import AppLink from '../ui/AppLink.vue';
import { MapPinned, CalendarSearch, ShieldCheck, MailCheck, TicketX } from 'lucide-vue-next';
import { startFireflies } from '../../utils/fireflies';
import { onMounted, onBeforeUnmount, ref } from 'vue';
import { useAuthStore } from '../../stores/auth';

const auth = useAuthStore();

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
  { label: "Pago seguro", icon: ShieldCheck },
  { label: "Confirmación inmediata", icon: MailCheck },
  { label: "Cancelación flexible", icon: TicketX },
]
</script>

<style scoped>
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee {
  animation: marquee 40s linear infinite;
}
</style>