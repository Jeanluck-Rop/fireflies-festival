<template>
  <section class="relative py-28 sm:py-36 border-t border-white/5">
    <div class="mx-auto max-w-6xl px-4">
      <div class="mx-auto max-w-2xl text-center animate-fade-up">
        <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
          <span class="h-px w-6 bg-(--color-accent)/60"></span>
          ¿Cabaña o Camping?
          <span class="h-px w-6 bg-(--color-accent)/60"></span>
        </span>
        <h2 class="font-display mt-4 text-balance text-[clamp(2rem,4.5vw,3.4rem)] font-medium leading-[1.05] tracking-tight">
          Dos formas de <em class="italic font-mono" style="color:#7ad3a4;">disfrutar</em> la noche.
        </h2>
        <p class="mt-5 text-[15px] leading-relaxed text-(--color-bone)/65">
          Elige cómo quieres vivir el espectáculo. Dos formas de dormir bajo el cortejo de las luciérnagas. Elige el ritmo que mejor se acomoda a tu noche. 
        </p>
      </div>

      <div class="split mt-13 animate-fade-up delay-2">
        <article class="panel cabin group" style="flex-basis: 50%;">
          <div class="panel-bg">
            <span class="photo-slot__label font-bold">FOTOGRAFÍA · Cabaña ·</span>
          </div>
          <div class="panel-overlay"></div>
          <div class="panel-content">
            <div class="flex items-center justify-between">
              <span class="font-mono font-bold text-[10.5px] tracking-[0.22em] uppercase text-glow">Comodidad total</span>
              <div class="inline-flex items-baseline gap-1 rounded-full bg-background/70 px-3.5 py-1.5 text-[12.5px] backdrop-blur ring-firefly">
                <span class="font-bold text-(--color-accent)">Desde $1,890</span>
                <span class="text-(--color-bone)/55 font-semibold">/ noche</span>
              </div>
            </div>

            <div class="flex flex-col">
              <h3 class="font-serif text-[clamp(3rem,6vw,5.5rem)] leading-[0.9] mb-3">Cabaña</h3>
              <p class="text-[14.5px] mb-4 leading-[1.55] text-(--color-bone)/75 max-w-[36ch]">
                Espacios privados con techo, calefacción y servicios completos. Ideal para
                familias o quienes prefieren la magia del bosque sin renunciar al descanso pleno.
              </p>

              <div class="perks-wrapper">
                <div class="perks-inner">
                  <ul class="panel-perks mt-5 flex flex-col gap-2.5 text-[13.5px] text-(--color-bone)/80">
                    <li v-for="p in cabinPerks" :key="p.description" class="flex items-center gap-3">
                      <span class="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded border border-white/10 bg-(--color-bg)/40 text-(--color-accent)">
                        <component :is="p.icon" class="h-4 w-4" :stroke-width="1.75"/>
                      </span>
                      <span>{{ p.description }}</span>
                    </li>
                  </ul>

                  <AppLink href="/parques" variant="transparent" class="panel-link mt-6 text-glow" :iconRight="MoveUpRight">
                    Ver cabañas disponibles
                  </AppLink>
                </div>
              </div>
            </div>
          </div>
        </article>
        
        <article class="panel camping group" style="flex-basis: 50%;">
          <div class="panel-bg">
            <span class="photo-slot__label font-bold">FOTOGRAFÍA · Camping ·</span>
          </div>
          <div class="panel-overlay"></div>
          <div class="panel-content">
            <div class="flex items-center justify-between">
              <span class="font-mono font-bold text-[10.5px] tracking-[0.22em] uppercase text-glow" style="color:#7ad3a4;">Experiencia única</span>
              <div class="inline-flex items-baseline gap-1 rounded-full bg-background/70 px-3.5 py-1.5 text-[12.5px] backdrop-blur ring-firefly">
                <span class="font-bold" style="color:#7ad3a4;">Desde $1,000</span>
                <span class="text-(--color-bone)/55 font-semibold">/ noche</span>
              </div>
            </div>

            <div class="flex flex-col">
              <h3 class="font-serif text-[clamp(3rem,6vw,5.5rem)] leading-[0.9] mb-3">Camping</h3>
              <p class="text-[14.5px] mb-4 leading-[1.55] text-(--color-bone)/75 max-w-[36ch]">
                A solo una mirada de las estrellas y el parpadeo de las luciérnagas, acampa en zonas designadas dentro de los parques.
                Una experiencia más cercana al ecosistema, pensada para
                aventureros y grupos que viajan ligero.
              </p>

              <div class="perks-wrapper">
                <div class="perks-inner">
                  <ul class="panel-perks mt-5 flex flex-col gap-2.5 text-[13.5px] text-(--color-bone)/80">
                    <li v-for="p in campingPerks" :key="p.description" class="flex items-center gap-3">
                      <span class="inline-flex h-7 w-7 shrink-0 items-center justify-center rounded border border-white/10 bg-(--color-bg)/40" style="color:#7ad3a4;">
                        <component :is="p.icon" class="h-4 w-4" :stroke-width="1.75"/>
                      </span>
                      <span>{{ p.description }}</span>
                    </li>
                  </ul>

                  <AppLink href="/parques" variant="transparent" class="panel-link mt-6 text-glow" :iconRight="MoveUpRight" style="color:#7ad3a4;">
                    Ver campings disponibles
                  </AppLink>
                </div>
              </div>
            </div>
          </div>
        </article>
      </div>

      <p class="mt-6 text-center text-[12px] font-mono uppercase tracking-[0.2em] text-(--color-bone-soft) animate-fade-up delay-3">
        Pasa el cursor sobre cada panel para expandir
      </p>

      <div class="animate-fade-up mt-6 grid gap-3 rounded-3xl border border-white/6 bg-white/2 p-2 sm:grid-cols-3">
        <div v-for="row in [
          { l: 'Mejor para', a: 'Confort y descanso', b: 'Aventura y conexión' },
          { l: 'Equipo incluido', a: 'Todo, listo para llegar', b: 'Tienda básica + linterna' },
          { l: 'Ideal para', a: 'Familias, parejas, grupos grandes', b: 'Amigos, parejas jóvenes, aventureros' },
        ]" :key="row.l" class="rounded-2xl bg-(--color-bg)/40 p-5">
          <p class="text-[11px] uppercase tracking-[0.22em] text-(--color-bone)/45">{{ row.l }}</p>
          <div class="mt-3 flex items-baseline justify-between gap-3 text-[13.5px]">
            <span class="text-(--color-bone)/85">Cabaña</span>
            <span class="text-right text-(--color-bone)/70">{{ row.a }}</span>
          </div>
          <div class="mt-1.5 flex items-baseline justify-between gap-3 text-[13.5px]">
            <span class="text-(--color-bone)/85">Camping</span>
            <span class="text-right text-(--color-bone)/70">{{ row.b }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import AppLink from '../ui/AppLink.vue';
import { MoveUpRight, BedDouble, Flame, Coffee, PlugZap, Tent, MoonStar, FlameKindling, ShowerHead } from 'lucide-vue-next';
const cabinPerks = [
  { icon: BedDouble, description: 'Camas cómodas con sábanas de algodón' },
  { icon: Flame, description: 'Calefacción para noches frías' },
  { icon: Coffee, description: 'Cafetera y desayuno incluido' },
  { icon: PlugZap, description: 'Electricidad, enchufes y baño privado' },
];
const campingPerks = [
  { icon: Tent, description: 'Zonas de acampada designadas' },
  { icon: MoonStar, description: 'Vistas despejadas del cielo nocturno' },
  { icon: FlameKindling, description: 'Fogatas permitidas en zonas autorizadas' },
  { icon: ShowerHead, description: 'Áreas comunes con regaderas y sanitarios' },
];

</script>

<style scoped>
.photo-slot__label {
  position: absolute; left: 14px; bottom: 9px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px; letter-spacing: 0.05em;
  color: rgba(255,255,255,.85);
  text-transform: uppercase;
}

.ring-firefly {
  box-shadow: inset 0 0 0 1px rgba(245, 213, 122, 0.18);
}

.split {
  display: flex;
  gap: 8px;
  min-height: 620px;
}

.panel {
  position: relative;
  flex: 1;
  overflow: hidden;
  border-radius: 28px;
  border: 1px solid rgba(255,255,255,.07);
  cursor: pointer;
  transition:
    flex .9s cubic-bezier(.19,1,.22,1),
    border-color .5s ease;
}
.split:hover .panel         { flex: .88; }
.split .panel:hover         { flex: 1.45; }
.panel.cabin:hover          { border-color: rgba(245,213,122,.28); }
.panel.camping:hover        { border-color: rgba(122,211,164,.28); }

.panel-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transform: scale(1.08);
  will-change: transform, filter;
  transition:
    transform 1.4s cubic-bezier(.19,1,.22,1),
    filter .95s ease;
}
.cabin .panel-bg   { background-image: url('../../assets/cabin-night.jpg'); }
.camping .panel-bg { background-image: url('../../assets/camping-night.jpg'); }

.panel:hover .panel-bg { transform: scale(1); }

.split:hover .panel:not(:hover) .panel-bg {
  filter: brightness(.5) saturate(.55) blur(2px);
}

.panel-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to top,
    rgba(0,0,0,.88) 0%,
    rgba(0,0,0,.3)  55%,
    rgba(0,0,0,.08) 100%
  );
  transition: opacity .7s ease;
}
.split:hover .panel:not(:hover) .panel-overlay { opacity: .6; }

.panel-content {
  position: relative;
  z-index: 2;
  height: 100%;
  padding: 32px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-sizing: border-box;
}

.panel-title {
  transition: letter-spacing .6s cubic-bezier(.19,1,.22,1);
}
.panel:hover .panel-title { letter-spacing: .01em; }

.panel-desc { transition: opacity .5s ease; }
.split:hover .panel:not(:hover) .panel-desc { opacity: .45; }

.panel-perks { list-style: none; padding: 0; margin: 0; }
.panel-perks li {
  opacity: 0;
  transform: translateY(10px);
  transition: opacity .35s ease, transform .35s ease;
}
.panel-perks li:nth-child(1) { transition-delay: .05s; }
.panel-perks li:nth-child(2) { transition-delay: .12s; }
.panel-perks li:nth-child(3) { transition-delay: .19s; }
.panel-perks li:nth-child(4) { transition-delay: .26s; }
.panel:hover .panel-perks li { opacity: 1; transform: translateY(0); }

.perks-wrapper {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows .7s cubic-bezier(.19,1,.22,1);
}
.perks-inner {
  min-height: 0;
  overflow: hidden;
}
.panel:hover .perks-wrapper {
  grid-template-rows: 1fr;
}

.panel-link {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity .35s .32s ease, transform .35s .32s ease;
}
.panel:hover .panel-link { opacity: 1; transform: translateY(0); }
</style>