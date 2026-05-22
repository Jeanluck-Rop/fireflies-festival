<template>
  <section class="relative py-28 sm:py-36">
    <div class="pointer-events-none absolute inset-x-0 top-0 h-px bg-linear-to-r from-transparent via-white/10 to-transparent"></div>
    <div class="mx-auto max-w-6xl px-4">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 mb-20">
        <div class="animate-fade-up lg:col-span-7">
          <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
            <span class="h-px w-6 bg-(--color-accent)/60"></span>
            Cómo funciona
          </span>
          <h2 class="section-title text-[clamp(2.4rem,5.8vw,4.8rem)]">
            Vive una <em class="italic text-glow text-glow">noche inolvidable.</em>
          </h2>
        </div>
        <p class="animate-fade-up pb-6 lg:col-span-5 self-end text-[15.5px] leading-[1.65] text-(--color-bone)/70 delay-1">
          Diseñamos un flujo simple para que pases de la curiosidad
          a la confirmación en menos de tres minutos. <br>
          Sin llamadas, sin papeleo, sin sorpresas. <br>
          Dedica tu tiempo a lo importante: estar presente. 
        </p>
      </div>

      <div class="relative">
        <svg class="absolute inset-0 w-full h-full hidden lg:block pointer-events-none" viewBox="0 0 1200 360" preserveAspectRatio="none" fill="none" aria-hidden="true">
          <defs>
            <linearGradient id="pathGrad" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%"  stop-color="#f5d57a" stop-opacity="0"/>
              <stop offset="20%" stop-color="#f5d57a" stop-opacity=".4"/>
              <stop offset="80%" stop-color="#f5d57a" stop-opacity=".4"/>
              <stop offset="100%" stop-color="#f5d57a" stop-opacity="0"/>
            </linearGradient>
          </defs>
          <path d="M 60 90 C 250 30, 430 180, 600 90 S 940 30, 1140 110" stroke="url(#pathGrad)" stroke-width="1.4" stroke-dasharray="2 6" fill="none" />
        </svg>

        <!-- Flying firefly along path -->
        <div class="absolute inset-0 w-full hidden lg:block pointer-events-none" aria-hidden="true">
          <div class="relative h-90">
            <div class="firefly-traveler absolute" style="width:12px;height:12px;">
              <span class="absolute -inset-3 rounded-full bg-(--color-accent)/30 blur-md"></span>
              <span class="absolute inset-0 rounded-full bg-(--color-accent) shadow-[0_0_18px_4px_rgba(245,213,122,0.7)]"></span>
            </div>
          </div>
        </div>

        <ol class="grid grid-cols-1 md:grid-cols-3 gap-6 relative">
          <li class="animate-fade-up" v-for="(s, i) in steps" :key="i" :class="`delay-${i+1}`">
            <article class="group glass-strong border border-white/10 rounded-3xl p-8 lg:p-9 flex flex-col gap-7 h-full min-h-105 relative overflow-hidden transition-all duration-500 hover:-translate-y-1 hover:border-(--color-accent)/30">
              <div class="pointer-events-none absolute -right-16 -top-16 h-40 w-40 rounded-full bg-(--color-accent)/0 blur-3xl transition-all duration-700 group-hover:bg-(--color-accent)/15"></div>
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10.5px] tracking-[0.22em] text-(--color-bone)/50 uppercase">Paso 0{{ i+1 }}</span>
                <span class="font-serif text-[44px] text-(--color-accent) text-glow leading-none transition-all duration-500 group-hover:scale-110 group-hover:opacity-100 opacity-80">0{{ i+1 }}</span>
              </div>

              <div class="inline-flex w-14 h-14 items-center justify-center rounded-2xl border border-(--color-accent)/30 bg-(--color-accent)/[0.07] transition-all duration-500 group-hover:bg-(--color-accent)/10 group-hover:scale-105">
                <component :is="s.icon" class="h-7 w-7 text-(--color-accent)" :stroke-width="1.5"/>
              </div>

              <div class="mt-auto">
                <h3 class="font-serif text-[30px] leading-tight">{{ s.title }}</h3>
                <p class="mt-3 text-[14.5px] text-(--color-bone)/70 leading-[1.6]">{{ s.body }}</p>
              </div>

              <div class="mt-2 h-px w-full overflow-hidden">
                <div class="h-full w-1/3 bg-linear-to-r from-transparent via-(--color-accent)/50 to-transparent transition-all duration-700 group-hover:w-full"></div>
              </div>

              <div class="pt-3 flex items-center justify-between text-[11px] font-mono uppercase tracking-[0.16em] text-(--color-bone)/50">
                <span>{{ s.note }}</span>
                <span class="text-glow/70">→</span>
              </div>
            </article>
          </li>
        </ol>
      </div>

      <p class="mt-10 text-center text-[12px] font-mono uppercase tracking-[0.2em] text-(--color-bone)/50 animate-fade-up delay-4">
        · El sistema no procesa reservas en martes ·
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { MapPinned, CalendarDays, Shrub } from 'lucide-vue-next';
const steps = [
  {
    title: 'Explora el mapa',
    body: 'Selecciona entre nuestros parques oficiales en el mapa interactivo, cada uno con su propio encanto y espectáculo de luciérnagas.',
    icon: MapPinned,
    note: 'Elige tu destino'
  },
  {
    title: 'Reserva tu espacio',
    body: 'Reserva tu cabaña o zona de camping, las fechas (junio a agosto, excepto martes) y el número de visitantes en pocos clics.',
    icon: CalendarDays,
    note: 'Ver disponibilidad'
  },
  {
    title: 'Vive la magia',
    body: 'Llega a tu parque elegido y déjate envolver por el espectáculo de luz natural más impresionante del año.',
    icon: Shrub,
    note: 'Consejos para el viaje'
  }
]
</script>

<style scoped>
.text-glow {
  color: var(--color-accent);
  text-shadow: 0 0 24px rgba(245, 213, 122, 0.45), 0 0 60px rgba(245, 213, 122, 0.18);
}

.section-title {
  font-family: Georgia, serif;
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.02em;
}

.firefly-traveler {
  offset-path: path('M 60 90 C 250 30, 430 180, 600 90 S 940 30, 1140 110');
  offset-distance: 0;
  animation: travel 14s linear infinite;
}

@keyframes travel {
  0%   { offset-distance: 0%; opacity: 0; }
  8%   { opacity: 1; }
  92%  { opacity: 1; }
  100% { offset-distance: 100%; opacity: 0; }
}

.glass-strong {
  background: linear-gradient(180deg, rgba(236,243,238,0.06), rgba(236,243,238,0.02));
  backdrop-filter: blur(18px) saturate(130%);
  -webkit-backdrop-filter: blur(18px) saturate(130%);
}
</style>