<template>
  <transition name="modal">
    <div v-if="showModal" class="modal-overlay" @click.self="cerrarModal">
      <div class="modal-card glass-strong rounded-3xl w-full max-w-125 p-10 text-center relative overflow-hidden">

        <div class="relative">
          <div class="w-22 h-22 rounded-full mx-auto mb-7 flex items-center justify-center bg-(--color-accent)/12 border border-(--color-accent)/40 relative">
            <span class="absolute inset-0 rounded-full" style="background:radial-gradient(closest-side, rgba(232,255,122,.4), transparent); animation:pulse 2.4s ease-in-out infinite;"></span>
            <FireflyLogo :pulse="true" :drift="true" size="w-10 h-10" />
          </div>

          <div class="font-mono font-[11px] tracking-[0.18em] uppercase text-[#C7E25E] mb-3">Edición 2026</div>
          <h2 class="font-serif font-normal leading-[0.95] tracking-tight text-[44px] mb-4">¡Reservación <em class="italic text-glow text-glow" style="color:#C7E25E;">confirmada</em>!</h2>
          <p class="text-[14px] text-bone-mute leading-[1.6] max-w-[42ch] mx-auto">
            Te enviamos los detalles a <span class="text-white font-medium">tu correo registrado</span>.
            También puedes consultarla en <strong class="text-bone">Mis reservaciones</strong>.
          </p>

          <!-- Summary chips -->
          <div class="grid grid-cols-3 gap-2 mt-7 mb-7">
            <div class="px-3 py-3 rounded-xl bg-white/3 border border-white/5">
              <div class="label-mono">Total</div>
              <div class="text-[17px] font-mono mt-1.5 text-glow text-bold" style="color:#7ad3a4;">{{ totalFormateado }}</div>
            </div>
            <div class="px-3 py-3 rounded-xl bg-white/3 border border-white/5">
              <div class="label-mono">Noches</div>
              <div class="text-[17px] font-mono mt-1.5 text-glow text-bold" style="color:#7ad3a4;">{{ nights }}</div>
            </div>
            <div class="px-3 py-3 rounded-xl bg-white/3 border border-white/5">
              <div class="label-mono">Personas</div>
              <div class="text-[17px] font-mono mt-1.5 text-glow text-bold" style="color:#7ad3a4;">{{ guests }}</div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <AppLink href="/reservaciones" variant="yellow" :iconRight="CalendarSearch" class="w-70">
              Mis Reservaciones
            </AppLink>
            <AppButton variant="outline" @click="cerrarModal" class="w-30">
              Cerrar
            </AppButton>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { CalendarSearch } from 'lucide-vue-next';
import { useReservationStore } from '../../stores/reservationStore.ts';
import AppButton from '../ui/AppButton.vue';
import AppLink from '../ui/AppLink.vue';
import FireflyLogo from '../ui/FireflyLogo.vue';

const store = useReservationStore();

const showModal = computed(() => store.reservaConfirmada);

const totalFormateado = computed(() => {
  const amount = store.reservaResumen?.total || 0;
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount);
});

const nights = computed(() => store.reservaResumen?.noches || 0);
const guests = computed(() => store.reservaResumen?.personas || 0);


const cerrarModal = () => {
  store.resetearReserva();
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(7,9,10,0.85);
  backdrop-filter: blur(10px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.modal-enter-active, .modal-leave-active {transition: opacity .25s ease; }
.modal-enter-active .modal-card, .modal-leave-active .modal-card { transition: transform .35s cubic-bezier(0.34, 1.56, 0.64, 1), opacity .25s ease; }
.modal-enter-from { opacity:0; }
.modal-enter-from .modal-card { transform:scale(.92) translateY(20px); opacity:0; }
.modal-leave-to { opacity:0; }
.modal-leave-to .modal-card { transform:scale(.96) translateY(10px); opacity:0; }
</style>