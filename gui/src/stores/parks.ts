import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import * as parksApi from '../services/parkService'

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

  // Filtros de búsqueda
  const searchQuery = ref('')
  const filterType = ref('all') 
  const visitors = ref<number|string>('')
  const priceMin = ref<number|string>('')
  const priceMax = ref<number|string>('')
  const timeOpen = ref('')
  const timeClose = ref('')

  const priceError = ref<string>('')
  watch([priceMin, priceMax], ([min, max]) => {
    if (min !== '' && max !== '' && Number(min) > Number(max)) {
      priceError.value = 'El mínimo no puede exceder el máximo.'
    } else {
      priceError.value = ''
    }
  })

  const visitorsError = ref<string>('')
  watch(visitors, (val) => {
    if (val !== '' && (!/^\d+$/.test(String(val)) || Number(val) < 1)) {
      visitorsError.value = 'El número debe ser mayor que cero.'
    } else {
      visitorsError.value = ''
    }
  })

  const timeError = ref<string>('')
  watch([timeOpen, timeClose], ([open, close]) => {
    if (open && close && open >= close) {
      timeError.value = 'La hora de apertura debe ser menor a la de cierre.'
    } else {
      timeError.value = ''
    }
  })

  function resetFilters() {
    searchQuery.value = ''
    filterType.value = 'all'
    visitors.value = ''
    priceMin.value = ''
    priceMax.value = ''
    timeOpen.value = ''
    timeClose.value = ''
    priceError.value = ''
    visitorsError.value = ''
    timeError.value = ''
  }

  const filteredParks = computed(() => {
    return parks.value.filter(p => {
      const searchStr = searchQuery.value.trim().toLowerCase()
      if ( searchStr && !p.nombre.toLowerCase().includes(searchStr) && !p.direccion.toLowerCase().includes(searchStr)) return false
      if (filterType.value === 'cabin' && !p.hasCabin) return false
      if (filterType.value === 'camping' && p.hasCabin) return false
      if ( visitors.value !== '' && Number(visitors.value) > 0 && 
      (Number(visitors.value) < p.capacidad_minima || Number(visitors.value) > p.capacidad_maxima)) return false
      if (priceMin.value !== '' && p.precio_maximo < Number(priceMin.value)) return false
      if (priceMax.value !== '' && p.precio_minimo > Number(priceMax.value)) return false
      if (timeOpen.value && p.horario_apertura < timeOpen.value) return false
      if (timeClose.value && p.horario_cierre > timeClose.value) return false

      return true
    })
  })

  const hasFilters = computed(() =>
    !!searchQuery.value ||
    filterType.value !== 'all' ||
    visitors.value !== '' ||
    priceMin.value !== '' ||
    priceMax.value !== '' ||
    timeOpen.value !== '' ||
    timeClose.value !== ''
  )

  async function loadParks() {
    loading.value = true
    try {
      const data = await parksApi.fetchParks()
      parks.value = data
    } catch (error) {
      parks.value = []
      console.error('Error cargando parques:', error)
    } finally {
      loading.value = false
    }
  }

  function selectPark(park: Parque | null) {
    selectedPark.value = park
  }

  return { parks, selectedPark, loading, selectPark, loadParks, 
    resetFilters, searchQuery, filterType, visitors, priceMin, priceMax, timeOpen, timeClose,
    filteredParks, hasFilters, priceError, visitorsError, timeError
  }
})
