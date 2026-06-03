import { useParksStore } from '../stores/parks'
import type { Parque } from '../stores/parks'
import type { Hospedaje } from '../stores/reservationStore'
import { createMockListaParques } from '../mocks/parksMocks'
import { getMockHospedajes } from '../mocks/lodgingsMocks'

const API = import.meta.env.VITE_API_URL || null
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

//Datos Falsos
const MOCK_PARQUES: Parque[] = createMockListaParques()

export async function fetchParks(): Promise<Parque[]> {
    const store = useParksStore()
    store.loading = true

    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 700))
      return MOCK_PARQUES
    }

    try {
      const res = await fetch(`${API}/api/parques/`)
      
      if (!res.ok) {
        throw new Error('Error cargando parques desde el servidor')
      }
      
      const data = await res.json()
      return data
      
    } catch (error) {
      console.error('Fetch Parks Error:', error)
      return []
    } finally {
      store.loading = false
    }
}

export async function fetchHospedajesByPark(parkId: number): Promise<Hospedaje[]> {
    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 500))
      // Retorna datos mock según el parque
      return getMockHospedajes(parkId)
    }

    if (!API) return []

    try {
      const response = await fetch(`${API}/api/hospedajes/?parque_id=${parkId}`)
      if (!response.ok) throw new Error('Error fetching hospedajes')
      return await response.json()
    } catch (error) {
      console.error('Error cargando hospedajes:', error)
      return []
    }
}