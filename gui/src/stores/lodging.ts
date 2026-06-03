import { defineStore } from "pinia";
import { ref } from "vue";
import * as parkService from "../services/parkService";
import type { Hospedaje } from "./reservationStore";

export const useLodgingStore = defineStore("lodging", () => {
  const hospedajes = ref<Hospedaje[]>([]);
  const loading = ref(false);
  const currentParkId = ref<number | null>(null);

  async function loadHospedajesByPark(parkId: number) {
    // Si ya están cargados, no recargues
    if (currentParkId.value === parkId && hospedajes.value.length > 0) {
      return;
    }

    loading.value = true;
    currentParkId.value = parkId;

    try {
      const data = await parkService.fetchHospedajesByPark(parkId)
      hospedajes.value = data
    } catch (error) {
      console.error("Error cargando hospedajes:", error);
      hospedajes.value = [];
    } finally {
      loading.value = false;
    }
  }

  function clearHospedajes() {
    hospedajes.value = [];
    currentParkId.value = null;
  }

  return {
    hospedajes,
    loading,
    currentParkId,
    loadHospedajesByPark,
    clearHospedajes,
  };
});
