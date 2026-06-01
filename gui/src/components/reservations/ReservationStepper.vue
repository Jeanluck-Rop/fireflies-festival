<template>
  <section class="pt-32 pb-10 relative overflow-hidden">
    <div class="mx-auto max-w-330 px-6 lg:px-8 relative">
      <nav class="flex items-center gap-2 text-[12.5px] font-mono uppercase tracking-[0.14em] text-bone-soft mb-8 animate-fade-up">
        <a href="/" class="hover:text-bone transition">Inicio</a>
        <span class="text-bone-dim">/</span>
        <span class="text-glow">Reservar</span>
      </nav>

      <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6">
        <div class="grid items-end gap-8 sm:grid-cols-2">
          <div class="animate-fade-up">
            <span class="inline-flex items-center gap-2 text-[11px] font-medium uppercase tracking-[0.25em] text-(--color-accent)/90">
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
              Paso a paso
              <span class="h-px w-6 bg-(--color-accent)/60"></span>
            </span>
            <h1 class="font-serif font-normal leading-[0.95] tracking-tight text-[clamp(2.6rem,6vw,5rem)] mt-5">
              Reserva tu noche<br>en el <em class="italic text-glow text-glow">bosque.</em>
            </h1>
          </div>
          <p class="animate-fade-up text-[15.5px] mb-7 leading-relaxed">
            Seis secillos pasos. Selecciona el parque y tipo de hospedaje, ajusta tus fechas, indica el número de personas, busca disponibilidad, 
            selecciona tu opción y confirma. Recibirás la confirmación en tu correo y la podrás consultar en
            <a href="/reservaciones" class="text-(--color-accent) underline decoration-glow/40 underline-offset-4">Mis reservaciones</a>.
          </p>
        </div>
      </div>
      <div class="flex items-center gap-3 shrink-0 mt-10 animate-fade-up">
          <div class="step is-on flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 1, 'is-done': store.currentStep > 1 }">
            <span class="step-dot">01</span>
            <span class="step-label">Parque</span>
          </div>
          <div class="w-8 h-px bg-white/10"></div>
          <div class="step flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 2, 'is-done': store.currentStep > 2 }">
            <span class="step-dot">02</span>
            <span class="step-label">Fechas</span>
          </div>
          <div class="w-8 h-px bg-white/10"></div>
          <div class="step flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 3, 'is-done': store.currentStep > 3 }">
            <span class="step-dot">03</span>
            <span class="step-label">Personas</span>
          </div>
          <div class="w-8 h-px bg-white/10"></div>
          <div class="step flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 4, 'is-done': store.currentStep > 4 }">
            <span class="step-dot">04</span>
            <span class="step-label">Disponibilidad</span>
          </div>
          <div class="w-8 h-px bg-white/10"></div>
          <div class="step flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 5, 'is-done': store.currentStep > 5 }">
            <span class="step-dot">05</span>
            <span class="step-label">Hospedaje</span>
          </div>
          <div class="w-8 h-px bg-white/10"></div>
          <div class="step flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 6, 'is-done': store.currentStep > 6 }">
            <span class="step-dot">06</span>
            <span class="step-label">Confirmar</span>
          </div>
          <div class="w-8 h-px bg-white/10"></div>
          <div class="step flex items-center gap-2.5" :class="{ 'is-on': store.currentStep === 7, 'is-done': store.currentStep > 7 }">
            <span class="step-dot">✓</span>
            <span class="step-label">Listo</span>
          </div>
        </div>
    </div>

    <div class="flex items-start gap-3 p-[16px_18px] rounded-[14px] bg-linear-to-b from-[rgba(255,185,92,0.06)] to-[rgba(255,185,92,0.015)] border border-[rgba(255,185,92,0.22)] mt-10 animate-fade-up">
      <div class="flex items-center justify-center w-8 h-8 rounded-[10px] bg-[rgba(255,185,92,0.12)] text-[#FFB95C] shrink-0">
        <Info class="w-4 h-4"/>
      </div>
      <div>
        <div class="text-[14px] font-medium leading-tight text-white">Antes de continuar</div>
        <p class="text-[13px] text-bone-mute mt-1.5 leading-[1.55] max-w-[68ch]">
          Las reservaciones <strong class="text-(--color-danger) font-semibold">solo aplican entre el 1 de junio y el 31 de agosto de 2026</strong>,
          y los <strong class="text-(--color-danger) font-semibold">martes</strong> el parque cierra por mantenimiento — esos días aparecerán bloqueados en el calendario.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Info } from 'lucide-vue-next';
import { useReservationStore } from '../../stores/reservationStore';

const store = useReservationStore();
</script>

<style scoped>
.step-dot {
  width:28px;
  height:28px;
  border-radius:999px;
  border:1px solid rgba(244,241,232,0.16);
  background:rgba(244,241,232,0.03);
  color:#9AA39E;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
  flex-shrink:0;
  transition:all .25s ease;
}
.step.is-on .step-dot { background:#E8FF7A; color:#07090A; border-color:#E8FF7A; }
.step.is-done .step-dot { background:rgba(232,255,122,0.15); color:#E8FF7A; border-color:rgba(232,255,122,0.4); }
.step-label { font-family:'JetBrains Mono',monospace; font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:#5C645F; transition:color .25s ease; }
.step.is-on .step-label { color:#F4F1E8; }
.step.is-done .step-label { color:#9AA39E; }
</style>