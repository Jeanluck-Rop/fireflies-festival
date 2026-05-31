import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface ImagenParque {
  id: number
  parque: number
  url: string
}

export interface ServicioParque {
  id: number
  nombre: string
  icono: string | null
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
  activo: boolean
  imagenes: ImagenParque[]
  servicios: ServicioParque[]
  hasCabin: boolean
  precio_minimo: number
  precio_maximo: number
  capacidad_minima: number
  capacidad_maxima: number
  cabanas_libres?: number
  campings_libres?: number
}

export interface HospedajeDetalle {
  id: number
  tipo: 'CABANA' | 'CAMPING'
  categoria: string
  capacidad: number
  tarifa_noche: number
  tiene_agua: boolean
  tiene_luz: boolean
  tiene_regadera: boolean
  descripcion: string
  imagenes: string[]
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
