import { useReservationsStore } from '../stores/reservations'
import type { Reservacion } from '../stores/reservations'

const API = import.meta.env.VITE_API_URL || null
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

//Datos falsos
const MOCK_RESERVACIONES: Reservacion[] = [
  {
    id: 1,
    parque:      { id: 1, nombre: 'Parque Sierra Chincua', imagen_mapa: null },
    hospedaje:   { id: 1, nombre: 'Cabaña del Bosque' },
    fecha_inicio: '2026-06-15',
    fecha_fin:    '2026-06-18',
    num_personas: 4,
    tipo_visita:  'CABANA',
    estado:       'ACTIVA',
    created_at:   '2026-05-01T10:00:00Z',
    monto: 2400
  },
  {
    id: 2,
    parque:      { id: 2, nombre: 'Parque Piedra Herrada', imagen_mapa: null },
    hospedaje:   { id: 2, nombre: 'Zona Camping Norte' },
    fecha_inicio: '2026-07-10',
    fecha_fin:    '2026-07-12',
    num_personas: 2,
    tipo_visita:  'CAMPING',
    estado:       'EN_PROCESO',
    created_at:   '2026-05-10T14:30:00Z',
    monto: 800
  },
  {
    id: 3,
    parque:      { id: 3, nombre: 'Parque El Rosario', imagen_mapa: null },
    hospedaje:   { id: 1, nombre: 'Cabaña Principal' },
    fecha_inicio: '2026-04-01',
    fecha_fin:    '2026-04-03',
    num_personas: 6,
    tipo_visita:  'CABANA',
    estado:       'COMPLETADA',
    created_at:   '2026-03-01T09:00:00Z',
    monto: 3600
  },
  {
    id: 4,
    parque:      { id: 1, nombre: 'Parque Sierra Chincua', imagen_mapa: null },
    hospedaje:   { id: 3, nombre: 'Zona Camping Sur' },
    fecha_inicio: '2026-03-15',
    fecha_fin:    '2026-03-16',
    num_personas: 1,
    tipo_visita:  'CAMPING',
    estado:       'CANCELADA',
    created_at:   '2026-03-01T11:00:00Z',
    monto: 400
  },
]


export const reserveService = {
  async getReservaciones() {
    const store = useReservationsStore()
    store.loading = true

    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 500))
      store.setReservaciones(MOCK_RESERVACIONES)
      store.loading = false
      return
    }

    //Backend:
    const res = await fetch(`${API}/api/reservaciones/`, {
      headers: { Authorization: `Bearer ${useAuthStore().token}` }
     })
    if (!res.ok)
      throw new Error('Error cargando reservaciones')
    const data = await res.json()
    store.setReservaciones(data)
    
    store.loading = false
  }
}
