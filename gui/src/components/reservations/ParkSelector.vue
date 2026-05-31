<template>
  <div class="lg:col-span-8">
    <div class="flex flex-col gap-12">
      <fieldset class="flex flex-col gap-2">
        <div class="flex items-baseline justify-between mb-1">
          <legend class="font-display text-[28px] leading-none">
            <span class="text-glow font-serif text-[30px] tracking-[0.14em] mr-3">01</span>
            Selecciona el parque
          </legend>
          <span class="label-mono">Requerido</span>
        </div>
        <p class="text-[13.5px] text-bone-soft mb-3 max-w-[60ch]">
          Solo verás parques oficiales.
        </p>

        <!-- Park selector dropdown -->
        <div class="relative" v-click-outside="() => parkOpen = false">
          <button class="select-trigger" :class="{ 'is-open': parkOpen }" @click="parkOpen = !parkOpen">
            <template v-if="store.parqueSeleccionado">
              <span class="park-thumb w-9! h-9! rounded-lg!"></span>
              <div class="text-left flex-1 min-w-0">
                <div class="text-[14px] leading-tight truncate">{{ store.parqueSeleccionado.nombre }}</div>
                <div class="text-[11.5px] text-bone-soft mt-0.5 truncate">{{ store.parqueSeleccionado.direccion }} · {{ store.parqueSeleccionado.horario_apertura }} · {{ store.parqueSeleccionado.horario_cierre }}</div>
              </div>
            </template>
            <template v-else>
              <MapPin class="text-bone-soft w-4 h-4 shrink-0" />
              <span class="text-bone-soft text-[14px] flex-1 text-left">Elige un parque</span>
            </template>
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" class="ml-auto text-[#9AA39E] shrink-0 transition-transform" :class="{'rotate-180': parkOpen}"><path d="M3 5l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>

          <transition name="pop">
            <div v-if="parkOpen" class="absolute z-50 mt-2 w-full glass-strong rounded-2xl p-2 shadow-2xl max-h-90 overflow-y-auto">
              <div class="px-3 py-2 label-mono"> {{ store.parques.length }} parques disponibles</div>
              <div v-for="p in store.parques" :key="p.id" class="park-option flex items-center gap-3.5 px-4 py-3.5 rounded-[10px] cursor-pointer transition-colors duration-150 ease-out hover:bg-[#e8ff7a]/5" :class="{'is-on': store.parqueSeleccionado?.id === p.id}" @click="onSelectPark(p)">
                <span class="park-thumb"></span>
                <div class="flex-1 min-w-0">
                  <div class="text-[14px] leading-tight truncate">{{ p.nombre }}</div>
                  <div class="text-[11.5px] text-bone-soft mt-0.5">{{ p.direccion }} · {{ p.horario_apertura }} · {{ p.horario_cierre }}</div>
                </div>
                <div class="flex items-center gap-1.5">
                  <span v-if="p.hasCabin" class="text-[10px] font-mono uppercase tracking-[0.14em] text-glow">Cabaña · <span style="color:#7ad3a4;">Camping</span></span>
                  <span v-if="!p.hasCabin" class="text-[10px] font-mono uppercase tracking-[0.14em] text-glow" style="color:#7ad3a4;">Camping</span>
                </div>
              </div>
            </div>
          </transition>
        </div>
      </fieldset>
      <fieldset class="flex flex-col gap-2 animate-fade-up">
        <div class="flex items-baseline justify-between mb-1">
          <legend class="font-display text-[28px] leading-none">
            <span class="text-glow font-serif text-[30px] tracking-[0.14em] mr-3">1.5</span>
            Tipo de hospedaje
          </legend>
          <span class="label-mono">Requerido</span>
        </div>
        <p class="text-[13.5px] text-bone-soft mb-4">
          Selecciona el tipo de hospedaje que deseas. No todos los parques cuentan con ambas opciones, así que elige el que más te guste y se ajuste a tu plan.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <label class="seg-card flex items-start gap-4" :class="{ 'is-on': store.tipoHospedaje==='CABANA', 'is-disabled': !store.parqueSeleccionado?.hasCabin }">
            <input type="radio" v-model="store.tipoHospedaje" value="CABANA" :disabled="!store.parqueSeleccionado?.hasCabin" class="sr-only">
            <span class="w-10 h-10 rounded-xl flex items-center justify-center bg-(--color-accent)/12 text-glow shrink-0 mt-0.5">
              <House class="w-5 h-5" />
            </span>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <span class="font-serif text-[20px] leading-tight">Cabaña</span>
                <span v-if="store.parqueSeleccionado && !store.parqueSeleccionado.hasCabin" class="text-[10px] font-mono uppercase tracking-[0.14em] text-bone-dim">No disponible aquí</span>
              </div>
              <div class="text-[12.5px] text-bone-soft mt-1.5 leading-normal">Privado · cama, baño y chimenea.</div>
            </div>
          </label>

          <label class="seg-card flex items-start gap-4" :class="{ 'is-on': store.tipoHospedaje==='CAMPING' }">
            <input type="radio" v-model="store.tipoHospedaje" value="CAMPING" class="sr-only">
            <span class="w-10 h-10 rounded-xl flex items-center justify-center text-glow shrink-0 mt-0.5" style="color:#7ad3a4;">
              <Tent class="w-5 h-5" />
            </span>
            <div class="flex-1 min-w-0">
              <div class="font-serif text-[20px] leading-tight">Camping</div>
              <div class="text-[12.5px] text-bone-soft mt-1.5 leading-normal">Tienda propia · zona común · sanitarios y fogata demarcada.</div>
            </div>
          </label>
        </div>
      </fieldset>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { MapPin, House, Tent } from 'lucide-vue-next';
import { useReservationStore } from '../../stores/reservationStore.ts';

const store = useReservationStore();
const parkOpen = ref(false);

onMounted(() => {
  if (store.parques.length === 0) {
    store.cargarParques();
  }
});

function onSelectPark(parque: any) {
  store.seleccionarParque(parque);
  if (parque.hasCabin) {
    store.tipoHospedaje = 'CABANA';
  } else {
    store.tipoHospedaje = 'CAMPING';
  }
  parkOpen.value = false;
}
</script>

<style scoped>
.park-thumb { 
  width: 42px; 
  height: 42px; 
  border-radius: 10px; 
  background: #0F1412; 
  background-image: repeating-linear-gradient(135deg, 
  rgba(244,241,232,0.05) 0 1px, 
    transparent 1px 8px); 
  border: 1px solid rgba(244,241,232,0.08); 
  flex-shrink: 0; 
}

.select-trigger {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border-radius: 12px;
  background: rgba(244,241,232,0.025);
  border: 1px solid rgba(244,241,232,0.1);
  color: #F4F1E8;
  font-size: 14px;
  font-family: 'Geist',sans-serif;
  transition: all .15s ease;
  display: flex;
  align-items: center;
  gap: 12px;
}
.select-trigger:focus, .select-trigger.is-open {
  outline: none;
  border-color: rgba(232,255,122,0.5);
  box-shadow: 0 0 0 4px rgba(232,255,122,0.1); 
  background: rgba(232,255,122,0.03);
}

.park-option.is-on { background:rgba(232,255,122,0.08); }

.seg-card {
  padding: 18px;
  border-radius: 16px;
  border: 1px solid rgba(244,241,232,0.08);
  background: rgba(244,241,232,0.025);
  cursor: pointer;
  transition: all .2s ease;
}
.seg-card:hover { border-color:rgba(244,241,232,0.2); }
.seg-card.is-on { 
  border-color: rgba(232,255,122,0.5); 
  background: rgba(232,255,122,0.06);
  box-shadow: 0 0 0 4px rgba(232,255,122,0.08);
}
.seg-card.is-disabled { 
  opacity:.4;
  cursor: not-allowed;
}

.pop-enter-active, .pop-leave-active { transition: opacity .15s ease, transform .15s ease; }
.pop-enter-from, .pop-leave-to {
  opacity:0;
  transform: translateY(-4px) scale(.98);
}
</style>