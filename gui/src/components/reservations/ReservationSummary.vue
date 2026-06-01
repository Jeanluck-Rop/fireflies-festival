<template>
  <aside class="lg:col-span-4 animate-fade-up">
    <div class="sticky top-5 flex flex-col gap-4">
      <div class="glass-strong rounded-3xl overflow-hidden">
        <div class="px-7 pt-7 pb-5">
          <div class="label-mono">Tu reservación</div>
          <div class="font-serif text-[28px] leading-tight mt-1">
            {{ store.parqueSeleccionado ? store.parqueSeleccionado.nombre : 'Resumen pendiente' }}
          </div>
        </div>

        <div class="hairline-flat"></div>

        <div class="px-7 py-6 flex flex-col gap-4">
          <div class="flex items-baseline justify-between gap-3">
            <span class="label-mono">Tipo</span>
            <span class="text-[13.5px]">
              {{ store.tipoHospedaje === 'CABANA' ? 'Cabaña' : (store.tipoHospedaje === 'CAMPING' ? 'Camping' : '—') }}
            </span>
          </div>
          <div class="flex items-baseline justify-between gap-3">
            <span class="label-mono">Llegada</span>
            <span class="text-[13.5px]">{{ formatDate(store.llegada) }}</span>
          </div>
          <div class="flex items-baseline justify-between gap-3">
            <span class="label-mono">Salida</span>
            <span class="text-[13.5px]">{{ formatDate(store.salida) }}</span>
          </div>
          <div class="flex items-baseline justify-between gap-3">
            <span class="label-mono">Noches</span>
            <span class="text-[13.5px]">{{ nights || '—' }}</span>
          </div>
          <div class="flex items-baseline justify-between gap-3">
            <span class="label-mono">Personas</span>
            <span class="text-[13.5px]">{{ store.personas }} {{ store.personas === 1 ? 'persona' : 'personas' }}</span>
          </div>
          <template v-if="store.unidadSeleccionada && store.reservaResumen">
            <div class="hairline-flat" style="background: var(--color-accent);"></div>
            <div class="flex items-baseline justify-between gap-3">
              <span class="label-mono">Tarifa por noche</span>
              <span class="text-[13.5px]">{{ formatCurrency(store.reservaResumen.tarifa_noche) }}</span>
            </div>
            <div class="flex items-baseline justify-between gap-3">
              <span class="label-mono">Subtotal</span>
              <span class="text-[13.5px]">{{ formatCurrency(store.reservaResumen.subtotal) }}</span>
            </div>
            <div class="flex items-baseline justify-between gap-3">
              <span class="label-mono">Servicio (5%)</span>
              <span class="text-[13.5px]">{{ formatCurrency(store.reservaResumen.servicio) }}</span>
            </div>
            <div class="flex items-baseline justify-between gap-3">
              <span class="label-mono font-bold text-white">Total</span>
              <span class="text-[14.5px] font-bold text-white">{{ formatCurrency(store.reservaResumen.total) }}</span>
            </div>
          </template>
        </div>

        <div class="hairline-flat"></div>

        <div class="px-7 py-6 flex flex-col gap-3">
          <template v-if="!store.unidadSeleccionada">
            <AppButton
              variant="primary"
              :loading="store.buscandoDisponibilidad"
              :disabled="!isFormComplete"
              class="w-full h-12"
              @click="handleAvailability">
              Buscar disponibilidad
            </AppButton>
          </template>
          <template v-else>
            <AppButton
              variant="primary"
              :loading="false"
              class="w-full h-12"
              @click="handleReservation">
              Confirmar reservación
            </AppButton>
          </template>

          <p class="text-center text-[11px] font-mono uppercase tracking-[0.14em] text-bone-mute mt-2">
            Cancelación gratis 48h antes
          </p>
        </div>
      </div>

      <div class="glass rounded-2xl p-5 flex items-start gap-3">
        <span class="w-9 h-9 rounded-xl flex items-center justify-center bg-white/5 text-bone-soft shrink-0">
          <Info class="w-5 h-5" />
        </span>
        <div>
          <div class="text-[13.5px] font-medium leading-tight">Confirmación instantánea</div>
          <div class="text-[12px] text-bone-soft mt-1 leading-normal">
            Recibirás un correo con todos los detalles de tu reserva al finalizar.
          </div>
        </div>
      </div>
      <div class="glass rounded-2xl p-5 flex items-start gap-3">
        <span class="w-9 h-9 rounded-xl flex items-center justify-center bg-white/5 text-bone-soft shrink-0">
          <CircleQuestionMark class="w-5 h-5" />
        </span>
        <div>
          <div class="text-[13.5px] font-medium leading-tight">¿Necesitas ayuda?</div>
          <div class="text-[12px] text-bone-soft mt-1 leading-normal">Escríbenos a <a href="mailto:festivalluciernagas2026@gmail.com" class="flex items-center gap-2.5 text-[13.5px] text-(--color-bone)/65 transition hover:text-(--color-accent)">
              <Mail class="h-3.5 w-3.5 shrink-0 text-(--color-accent)/70" :stroke-width="1.75" />
              festivalluciernagas2026@gmail.com
            </a>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { Info, CircleQuestionMark, Mail } from 'lucide-vue-next';
import { useReservationStore } from '../../stores/reservationStore.ts';
import { reservationService } from '../../services/reservationService.ts';
import AppButton from '../ui/AppButton.vue';

const store = useReservationStore();

const formatDate = (isoString: string | null) => {
  if (!isoString) return '—';
  const [year, month, day] = isoString.split('-');
  const d = new Date(Number(year), Number(month) - 1, Number(day));
  const days = ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'];
  const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
  return `${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]}`;
};

const formatCurrency = (amount: number | undefined) => {
  if (amount === undefined) return '—';
  return new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(amount);
};

const nights = computed(() => {
  if (!store.llegada || !store.salida) return 0;
  return store.calcularNoches(store.llegada, store.salida);
});

const isFormComplete = computed(() => {
  return !!(
    store.parqueSeleccionado &&
    store.tipoHospedaje &&
    store.llegada &&
    store.salida
  );
});

const handleAvailability = async () => {
  if (!isFormComplete.value) return;

  await reservationService.buscarUnidadesDisponibles();
};

const handleReservation = async () => {
  if (!isFormComplete.value) return;
  store.calcularResumen();
  store.reservaConfirmada = true;
};
</script>

<style scoped>
.hairline {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(244,241,232,0.16), transparent);
}
.hairline-flat {
  height: 1px;
  background: rgba(244,241,232,0.08);
}
</style>