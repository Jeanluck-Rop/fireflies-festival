<template>
  <div class="mx-auto max-w-330 px-6 lg:px-8 pb-24">
    <ReservationStepper />
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 mt-8">
      <div class="lg:col-span-8 flex flex-col gap-12">
          <ParkSelector />
          <DatePicker />
          <GuestCounter />
          <AvailableUnits v-if="store.disponibilidadConsultada" />
      </div>
      <ReservationSummary />
      <SuccessModal />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useReservationStore } from "../stores/reservationStore.ts";
import ReservationStepper from "../components/reservations/ReservationStepper.vue";
import ParkSelector from "../components/reservations/ParkSelector.vue";
import DatePicker from "../components/reservations/DatePicker.vue";
import GuestCounter from "../components/reservations/GuestCounter.vue";
import AvailableUnits from "../components/reservations/AvailableUnits.vue";
import ReservationSummary from "../components/reservations/ReservationSummary.vue";
import SuccessModal from "../components/reservations/SuccessModal.vue";

const store = useReservationStore();
</script>