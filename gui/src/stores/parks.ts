import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ImagenParque {
  id: number
  parque: number
  url: string
}

export interface Parque {
  id: number
  nombre: string
  direccion: string
  descripcion: string | null
  latitud: number
  longitud: number
  horario_apertura: string  //"HH:MM"
  horario_cierre: string  //"HH:MM"
  imagen_mapa: string | null
  activo: boolean
  cabanas_libres: number
  campings_libres: number
  imagenes: ImagenParque[]
}

export const useParksStore = defineStore('parks', () => {
  const parks = ref<Parque[]>([])
  const selectedPark = ref<Parque | null>(null)
  const loading = ref(false)

  function setParks(data: Parque[]) {
    parks.value = data
  }

  function selectPark(park: Parque | null) {
    selectedPark.value = park
  }

  return { parks, selectedPark, loading, setParks, selectPark }
})
