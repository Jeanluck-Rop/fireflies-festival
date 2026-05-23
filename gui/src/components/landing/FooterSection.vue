<template>
  <footer class="border-t border-white/5 bg-black">
    <div class="animate-fade-up mx-auto max-w-6xl px-4 pt-14 pb-8">
      <div class="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">

        <div class="flex flex-col gap-5 lg:col-span-1">
          <AppLink href="/" variant="brand">
            <FireflyLogo :pulse="true" :drift="true" />
            <span class="font-serif text-[22px] tracking-tightest leading-none">
              Luciernagas
            </span>
            <span class="text-[10px] font-mono uppercase tracking-[0.18em] text-bone-soft pl-2 border-l border-white/10 ml-2">
              Festival 2026
            </span>
          </AppLink>

          <p class="text-[13.5px] leading-relaxed text-(--color-bone)/55 max-w-[28ch]">
            Una experiencia coordinada con parques nacionales y reservas certificadas para proteger a las luciérnagas y a quienes las visitan.
          </p>
        </div>

        <div>
          <p class="text-[11px] uppercase tracking-[0.22em] text-(--color-bone)/40 mb-4">
            Experiencias
          </p>
          <ul class="space-y-3">
            <li v-for="l in navExperiencias" :key="l.label">
              <a :href="l.href" class="text-[13.5px] text-(--color-bone)/65 transition hover:text-(--color-accent)">
                {{ l.label }}
              </a>
            </li>
          </ul>
        </div>

        <div>
          <p class="text-[11px] uppercase tracking-[0.22em] text-(--color-bone)/40 mb-4">
            Información
          </p>
          <ul class="space-y-3">
            <li v-for="l in navInfo" :key="l.label">
              <a :href="l.href" class="text-[13.5px] text-(--color-bone)/65 transition hover:text-(--color-accent)">
                {{ l.label }}
              </a>
            </li>
          </ul>
          <div class="mt-4 inline-flex items-center gap-2 rounded-full border border-(--color-accent)/18 bg-(--color-accent)/5 px-3.5 py-1.5">
            <span class="h-1.5 w-1.5 rounded-full bg-(--color-accent) opacity-80 animate-pulse" />
            <span class="text-[11px] font-mono uppercase tracking-[0.16em] text-(--color-accent)/80">
              Temporada Jun–Ago 2026
            </span>
          </div>
        </div>

        <div>
          <p class="text-[11px] uppercase tracking-[0.22em] text-(--color-bone)/40 mb-4">
            Contacto
          </p>
          <ul class="space-y-3">
            <li class="flex items-start gap-2.5 text-[13.5px] text-(--color-bone)/55">
              <MapPin class="mt-0.5 h-3.5 w-3.5 shrink-0 text-(--color-accent)/70" :stroke-width="1.75" />
              México
            </li>
            <li>
              <a href="mailto:festivalluciernagas@gmail.com" class="flex items-center gap-2.5 text-[13.5px] text-(--color-bone)/65 transition hover:text-(--color-accent)">
                <Mail class="h-3.5 w-3.5 shrink-0 text-(--color-accent)/70" :stroke-width="1.75" />
                festivalluciernagas@gmail.com
              </a>
            </li>
          </ul>
          <div class="mt-5 flex items-center gap-3">
            <a v-for="s in socials" :key="s.label" :href="s.href" :aria-label="s.label"
                class="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-white/8 text-(--color-bone)/50
                      transition hover:border-(--color-accent)/30 hover:text-(--color-accent)">
              <component :is="s.icon" class="h-3.5 w-3.5" :stroke-width="1.75" />
            </a>
          </div>
        </div>
      </div>
      <div class="mt-6 border-t border-white/5" />

      <div class="mt-5 flex flex-col items-center justify-between gap-3 sm:flex-row">
        <p class="text-[12px] font-mono text-(--color-bone)/35 tracking-[0.08em]">
          © 2026 Festival Luciernagas · Todos los derechos reservados
        </p>
        <div class="flex items-center gap-5">
          <a v-for="l in navLegal" :key="l.label" :href="l.href" class="text-[12px] text-(--color-bone)/40 transition hover:text-(--color-bone)/70">
            {{ l.label }}
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import AppLink from '../ui/AppLink.vue';
import FireflyLogo from '../ui/FireflyLogo.vue';
import { Instagram, Facebook, Youtube, MapPin, Mail, } from 'lucide-vue-next';

const socials = [
  { label: 'Instagram', href: '#', icon: Instagram },
  { label: 'Facebook',  href: '#', icon: Facebook  },
  { label: 'YouTube',   href: '#', icon: Youtube   },
];

const navExperiencias = [
  { label: 'Inicio',           href: '/'  },
  { label: 'Parques',           href: '/parques' },
];

const navInfo = [
  { label: 'Preguntas frecuentes', href: '#'          },
  { label: 'Guía de viaje',        href: '#'         },
];

const navLegal = [
  { label: 'Términos de Servicio',  href: '/#'   },
  { label: 'Política de Privacidad',href: '/#' },
];
</script>