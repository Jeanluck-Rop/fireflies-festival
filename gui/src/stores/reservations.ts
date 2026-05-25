import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Reservacion {
  id: number
  parque: { id: number; nombre: string; imagen_mapa: string | null }
  hospedaje: { id: number; nombre: string }
  fecha_inicio: string   //"YYYY-MM-DD"
  fecha_fin: string      //"YYYY-MM-DD"
  num_personas: number
  tipo_visita: 'CABANA' | 'CAMPING'
  estado: 'ACTIVA' | 'EN_PROCESO' | 'CANCELADA' | 'COMPLETADA'
  created_at: string
  // TODO backend: agregar precio cuando el modelo lo tenga
  // precio?: number
}

export const useReservationsStore = defineStore('reservations', () => {
  const reservaciones  = ref<Reservacion[]>([])
  const loading = ref(false)

  function setReservaciones(data: Reservacion[]) {
    reservaciones.value = data
  }

  function eliminarReservacion(id: number) {
    reservaciones.value = reservaciones.value.filter(r => r.id !== id)
  }

  return { reservaciones, loading, setReservaciones, eliminarReservacion }
})
