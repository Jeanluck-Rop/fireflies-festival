<template>
  <section class="relative py-28 sm:py-36 border-t border-white/5">
    <div class="mx-auto max-w-6xl px-4">
      <div class="grid items-end gap-8 sm:grid-cols-2">
        <div class="animate-fade-up">
          <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
            <span class="h-px w-6 bg-(--color-accent)/60"></span>
            ¿Sabías qué?
          </span>
          <h2 class="font-display mt-4 text-balance text-[clamp(2rem,4.5vw,3.4rem)] font-medium leading-[1.05] tracking-tight">
            La ciencia detrás <br/>
            de la <em class="italic font-serif text-glow">luz viva.</em>
          </h2>
        </div>
        <p class="animate-fade-up text-[15px] mb-5 leading-relaxed text-(--color-bone)/65">
          Cada destello en el bosque es una conversación química. Conoce algunas razones por las que estos pequeños faros merecen toda nuestra atención y cuidado.
        </p>
      </div>

      <ol class="group/reveal mt-12 flex h-125 w-full max-w-300 mx-auto gap-1.25 overflow-hidden rounded-[20px]">
        <li v-for="(s, i) in steps" :key="i" class="group/card animate-fade-up relative flex-1 overflow-hidden cursor-pointer
                                                    card-flex hover:flex-4 group-hover/reveal:flex-[0.75]">
          <img :src="s.image" :alt="s.title" class="card-img absolute inset-0 h-full w-full object-cover 
                scale-[1.07] will-change-[transform,filter] group-hover/card:scale-100
                group-hover/reveal:brightness-[.45] group-hover/reveal:saturate-50 group-hover/reveal:blur-[1.5px]
                group-hover/card:brightness-110! group-hover/card:saturate-100! group-hover/card:blur-none!">
          <div class="absolute inset-0 bg-linear-to-t from-black/90 via-black/30 to-black/5
                      transition-opacity duration-600 group-hover/reveal:opacity-70 group-hover/card:opacity-100!" />
          <span class="absolute left-5.5 top-5 z-3 font-mono text-[10px] uppercase tracking-[.2em] text-white/45 [writing-mode:vertical-rl] 
                      rotate-180 transition-opacity duration-500 group-hover/reveal:opacity-0 group-hover/card:opacity-100!">
            0{{ i + 1 }} / 0{{ steps.length }}
          </span>
          <div class="absolute inset-x-0 bottom-0 z-3 px-6 pb-7">
            <p class="mb-2.5 inline-flex items-center gap-1.5 font-mono text-[10.7px] uppercase tracking-[.2em] text-white/55 before:block before:h-px before:w-4.5 
                      before:bg-white/40 opacity-0 translate-y-3.5 transition-[opacity,transform] duration-350 ease-out group-hover/card:opacity-100 group-hover/card:translate-y-0">
              {{ s.chip }}
            </p>
            <h2 class="mb-2 text-[clamp(1.1rem,2vw,1.5rem)] font-display text-glow font-semibold leading-[1.2] text-white opacity-0 translate-y-3.5
                      transition-[opacity,transform] duration-380 delay-60 ease-out group-hover/card:opacity-100 group-hover/card:translate-y-0">
              {{ s.title }}
            </h2>
            <p class="text-[13px] leading-[1.55] text-white/70 opacity-0 translate-y-2.5 transition-[opacity,transform] 
                      duration-380 delay-140 ease-out group-hover/card:opacity-100 group-hover/card:translate-y-0">
              {{ s.detail }}
            </p>
          </div>
        </li>
      </ol>

      <p class="mt-6 text-center text-[12px] font-mono uppercase tracking-[0.2em] text-(--color-bone-soft) animate-fade-up delay-3">
        Pasa el cursor sobre cada panel para descubrir algunas curiosidades fascinantes sobre las luciérnagas.
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
import fireflyMacro from '../../assets/firefly-macro.jpg'
import firefly from '../../assets/firefly.png'
import luciernagas from '../../assets/luciernagas.jpg'
import personWithFireflies from '../../assets/personwithFireflies.jpg'
import ffly from '../../assets/ffly.jpg'
import muchasluc from '../../assets/muchasluc.jpg'

const steps = [
  {
    image: fireflyMacro,
    chip: '¿Sabías que?',
    title: 'Bioluminiscencia única',
    detail: 'Las luciérnagas producen su propia luz mediante una reacción química en su abdomen entre la enzima luciferasa y el compuesto luciferina. Lo más asombroso es que es una "luz fría", ya que casi el 100% de la energía se convierte en luz y no en calor.'
  },
  {
    image: firefly,
    chip: 'Dato curioso',
    title: 'Defensa brillante',
    detail: 'Además de para el romance, su luz sirve como advertencia. Para los depredadores, el brillo de una luciérnaga es un aviso de que tienen un sabor horrible y contienen químicos tóxicos que las protegen de ser devoradas.'
  },
  {
    image: muchasluc,
    chip: 'Increíble',
    title: 'Sincronización mágica',
    detail: 'En algunas regiones del mundo, miles de luciérnagas sincronizan sus destellos al mismo tiempo, creando espectáculos naturales impresionantes que iluminan bosques y campos durante la noche.'
  },
  {
    image: luciernagas,
    chip: 'Curiosidad',
    title: 'Distribución global',
    detail: 'Existen más de 2,000 especies de luciérnagas. Habitan en diversos ecosistemas alrededor del mundo, desde selvas tropicales hasta praderas, y aunque prefieren la humedad, están presentes en casi todos los continentes excepto la Antártida. Cada región alberga especies únicas.'
  },
  {
    image: ffly,
    chip: 'Interesante',
    title: 'Un lenguaje de luces',
    detail: 'Utilizan sus destellos para comunicarse. Los machos emiten señales luminosas específicas mientras vuelan para atraer a las hembras, y cada especie tiene su propio "código" secreto de parpadeo para no confundirse entre sí.'
  },
  {
    image: personWithFireflies,
    chip: 'Asombroso',
    title: 'La temporada perfecta',
    detail: 'Su temporada de reproducción coincide con la época de lluvias, entre junio y agosto. Es en estos meses cuando las noches húmedas y oscuras se convierten en el escenario ideal para presenciar su avistamiento.'
  }
];
</script>

<style scoped>
.card-flex {
  transition: flex .85s cubic-bezier(.19, 1, .22, 1);
}

.card-img {
  transition:
    transform 1.3s cubic-bezier(.19, 1, .22, 1),
    filter .9s ease;
}
</style>