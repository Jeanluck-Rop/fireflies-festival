<template>
  <div class="lg:col-span-8">
    <div class="flex flex-col gap-12">
      <fieldset class="flex flex-col gap-2 animate-fade-up">
        <div class="flex items-baseline justify-between mb-1">
          <legend class="font-display text-[28px] leading-none">
            <span class="text-glow font-serif text-[30px] tracking-[0.14em] mr-3">03</span>
            Número de personas
          </legend>
          <span class="label-mono">Requerido</span>
        </div>
        <p class="text-[13.5px] text-bone-soft mb-4 max-w-[60ch]">
          Indica cuántas personas asistirán a esta mágica experiencia.
        </p>

        <div class="glass rounded-2xl p-5 flex items-center justify-between gap-6">
          <div class="flex items-center gap-4">
            <span class="w-11 h-11 rounded-xl flex items-center justify-center bg-glow/12 text-glow">
              <User class="w-5 h-5" />
            </span>
            <div>
              <div class="text-[14.5px] font-medium leading-tight">Visitantes</div>
              <div class="text-[12.5px] text-bone-soft mt-0.5">Adultos y menores · todos los visitantes cuentan</div>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <button class="counter-btn" :disabled="store.personas <= 1" @click="store.setPersonas(Math.max(1, store.personas - 1))">−</button>
            <span class="font-serif text-[28px] w-12 text-center leading-none">{{ store.personas }}</span>
            <button class="counter-btn" :disabled="store.personas >= 12" @click="store.setPersonas(Math.min(12, store.personas + 1))">+</button>
          </div>
        </div>
      </fieldset>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useReservationStore } from '../../stores/reservationStore.ts';
import { User } from 'lucide-vue-next';
const store = useReservationStore();
</script>

<style scoped>
.counter-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(244,241,232,0.04);
  border: 1px solid rgba(244,241,232,0.1);
  color: #F4F1E8;
  cursor: pointer;
  transition: all .2s ease;
  font-size: 16px;
}
.counter-btn:hover:not(:disabled) {
  background: rgba(232,255,122,0.08);
  border-color: rgba(232,255,122,0.4);
  color: #E8FF7A;
}
.counter-btn:disabled {
  opacity: .3;
  cursor: not-allowed;
}
</style>