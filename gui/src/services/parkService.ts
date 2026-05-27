import { useParksStore } from '../stores/parks'
import type { Parque } from '../stores/parks'

const API = import.meta.env.VITE_API_URL || null
const USE_MOCK = import.meta.env.VITE_USE_MOCK

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

    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 700))
      store.setParks(MOCK_PARQUES)
      store.loading = false
      return
    }

    // TODO: conexion con back
    // const res = await fetch(`${API}/api/parques/`)
    // if (!res.ok)
    //   throw new Error('Error cargando parques')
    // const data = await res.json()
    // store.setParks(data)
    store.loading = false
  }
}
