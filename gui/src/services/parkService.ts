import { useParksStore } from '../stores/parks'
import type { Parque } from '../stores/parks'

const API = import.meta.env.VITE_API_URL || null
const IS_DEV = import.meta.env.DEV

//Datos Falsos
const MOCK_PARQUES: Parque[] = [
  {
    id: 1,
    nombre: 'Parque Sierra Chincua',
    direccion: 'Angangueo, Michoacán',
    descripcion: 'Santuario de mariposas monarca y luciérnagas en temporada.',
    latitud: 19.6731,
    longitud: -100.2800,
    horario_apertura: '01:00',
    horario_cierre: '23:00',
    imagen_mapa: null,
    activo: true,
    imagenes: []
  },
  {
    id: 2,
    nombre: 'Parque Piedra Herrada',
    direccion: 'Valle de Bravo, Estado de México',
    descripcion: 'Bosque de oyamel con avistamiento nocturno de luciérnagas.',
    latitud: 19.1800,
    longitud: -100.1300,
    horario_apertura: '09:00',
    horario_cierre: '23:30',
    imagen_mapa: null,
    activo: true,
    imagenes: []
  },
  {
    id: 3,
    nombre: 'Parque El Rosario',
    direccion: 'Ocampo, Michoacán',
    descripcion: 'El santuario más grande del festival, senderos iluminados.',
    latitud: 19.5620,
    longitud: -100.2710,
    horario_apertura: '10:30',
    horario_cierre: '23:00',
    imagen_mapa: null,
    activo: true,
    imagenes: []
  },
]

export const parkService = {
  async getParks() {
    const store = useParksStore()
    store.loading = true
    try {
      /*
      if (IS_DEV) {
        await new Promise(r => setTimeout(r, 700))
        store.setParks(MOCK_PARQUES)
        store.loading = false
        return
      }
      */
      const res = await fetch(`${API}/api/parques/`)
      if (!res.ok) {
        const errorData = await res.json()
        console.error(errorData)
        throw new Error('Error al obtener información de los parques.')
      }
      const parques = await res.json().catch(() => ({}))
      store.setParks(parques)
      store.loading = false
    }
    catch (error) {
      console.error('Error de red o de servidor:', error)
      throw error
    } finally {
      store.loading = false
    }
  }
}
