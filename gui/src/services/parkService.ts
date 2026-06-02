import { useParksStore } from '../stores/parks'
import type { Parque, HospedajeDetalle } from '../stores/parks'
import cabinnight from '../assets/cabin-night.jpg'
import campingnight from '../assets/camping-night.jpg'
import fireflires1 from '../assets/fireflires_auth_background.jpg'
import fireflires2 from '../assets/fireflires_auth_background2.jpg'
import fireflires3 from '../assets/fireflires_auth_background3.jpg'
import hero from '../assets/hero-forest.jpg'

const API = import.meta.env.VITE_API_URL || null
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

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
    activo: true,
    imagenes: [],
    servicios: [{ id: 1, nombre: 'Senderismo', icono: 'hiking' },
      { id: 2, nombre: 'Recorridos guiados', icono: 'map' },],
    hasCabin: true,
    precio_minimo: 800,
    precio_maximo: 2500,
    capacidad_minima: 2,
    capacidad_maxima: 8,
    cabanas_libres: 4,
    campings_libres: 12
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
    activo: true,
    imagenes: [],
    servicios: [{ id: 3, nombre: 'Camping', icono: 'camping' },
      { id: 4, nombre: 'Observación de luciérnagas', icono: 'bug' },],
    hasCabin: false,
    precio_minimo: 500,
    precio_maximo: 1500,
    capacidad_minima: 2,
    capacidad_maxima: 10,
    cabanas_libres: 0,
    campings_libres: 20
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
    activo: true,
    imagenes: [{id: 1, parque: 3, url: fireflires1}, {id: 2, parque: 3, url: fireflires2}, 
      {id: 3, parque: 3, url: fireflires3}, {id: 4, parque: 3, url: hero}, 
      {id: 5, parque: 3, url: cabinnight}, {id: 6, parque: 3, url: campingnight}],
    servicios: [{ id: 5, nombre: 'Senderismo', icono: 'hiking' },
      { id: 6, nombre: 'Camping', icono: 'camping' },
      { id: 7, nombre: 'Recorridos nocturnos', icono: 'moon' },
      { id: 8, nombre: 'Observación de mariposas', icono: 'butterfly' },],
    hasCabin: true,
    precio_minimo: 1000,
    precio_maximo: 3000,
    capacidad_minima: 2,
    capacidad_maxima: 12,
    cabanas_libres: 6,
    campings_libres: 15
  },
  {
  id: 4,
  nombre: 'Santuario El Rosario',
  direccion: 'Ocampo, Michoacán',
  descripcion: 'Reserva natural famosa por la migración de mariposas monarca y recorridos nocturnos.',
  latitud: 19.6201,
  longitud: -100.2745,
  horario_apertura: '08:00',
  horario_cierre: '22:00',
  activo: false,
  imagenes: [],
  servicios: [{ id: 8, nombre: 'Senderismo', icono: 'hiking' },
    { id: 9, nombre: 'Observación de mariposas', icono: 'butterfly' },],
  hasCabin: true,
  precio_minimo: 1200,
  precio_maximo: 3500,
  capacidad_minima: 2,
  capacidad_maxima: 10,
  cabanas_libres: 0,
  campings_libres: 0
},
{
  id: 5,
  nombre: 'Bosque Esmeralda',
  direccion: 'Amecameca, Estado de México',
  descripcion: 'Zona boscosa ideal para caminatas y observación de luciérnagas.',
  latitud: 19.1234,
  longitud: -98.7654,
  horario_apertura: '10:00',
  horario_cierre: '23:00',
  activo: true,
  imagenes: [],
  servicios: [{ id: 10, nombre: 'Senderismo', icono: 'hiking' },
    { id: 11, nombre: 'Observación de luciérnagas', icono: 'bug' },],
  hasCabin: false,
  precio_minimo: 400,
  precio_maximo: 1200,
  capacidad_minima: 2,
  capacidad_maxima: 8,
  cabanas_libres: 0,
  campings_libres: 10
},
{
  id: 6,
  nombre: 'Rancho Las Luciérnagas',
  direccion: 'Nanacamilpa, Tlaxcala',
  descripcion: 'Experiencia ecoturística con senderos iluminados por luciérnagas.',
  latitud: 19.4720,
  longitud: -98.5340,
  horario_apertura: '18:00',
  horario_cierre: '23:59',
  activo: true,
  imagenes: [],
  servicios: [{ id: 12, nombre: 'Senderismo nocturno', icono: 'hiking' },
    { id: 13, nombre: 'Observación de luciérnagas', icono: 'bug' },],
  hasCabin: false,
  precio_minimo: 300,
  precio_maximo: 1000,
  capacidad_minima: 2,
  capacidad_maxima: 6,
  cabanas_libres: 0,
  campings_libres: 8
},
{
  id: 7,
  nombre: 'Parque Ecoturístico La Soledad',
  direccion: 'Huamantla, Tlaxcala',
  descripcion: 'Área natural protegida con actividades nocturnas y camping.',
  latitud: 19.3150,
  longitud: -97.9230,
  horario_apertura: '09:00',
  horario_cierre: '22:30',
  activo: true,
  imagenes: [],
  servicios: [{ id: 14, nombre: 'Camping', icono: 'camping' },
    { id: 15, nombre: 'Recorridos nocturnos', icono: 'moon' },],
  hasCabin: false,
  precio_minimo: 350,
  precio_maximo: 900,
  capacidad_minima: 2,
  capacidad_maxima: 10,
  cabanas_libres: 0,
  campings_libres: 5
},
{
  id: 8,
  nombre: 'Reserva Santa Elena',
  direccion: 'Tlalpujahua, Michoacán',
  descripcion: 'Bosque de pinos con recorridos guiados y avistamiento de fauna.',
  latitud: 19.8130,
  longitud: -100.1720,
  horario_apertura: '08:30',
  horario_cierre: '21:30',
  activo: true,
  imagenes: [],
  servicios: [{ id: 16, nombre: 'Senderismo', icono: 'hiking' },
    { id: 17, nombre: 'Observación de fauna', icono: 'paw' },],
  hasCabin: true,
  precio_minimo: 600,
  precio_maximo: 2000,
  capacidad_minima: 2,
  capacidad_maxima: 8,
  cabanas_libres: 3,
  campings_libres: 10
},
{
  id: 9,
  nombre: 'Campamento Río Verde',
  direccion: 'Zacatlán, Puebla',
  descripcion: 'Campamento familiar con senderismo y observación nocturna.',
  latitud: 19.9350,
  longitud: -97.9610,
  horario_apertura: '07:00',
  horario_cierre: '23:00',
  activo: true,
  imagenes: [],
  servicios: [{ id: 19, nombre: 'Senderismo', icono: 'hiking' },],
  hasCabin: false,
  precio_minimo: 250,
  precio_maximo: 800,
  capacidad_minima: 2,
  capacidad_maxima: 6,
  cabanas_libres: 0,
  campings_libres: 12
},
{
  id: 10,
  nombre: 'Parque Los Encinos',
  direccion: 'Mineral del Chico, Hidalgo',
  descripcion: 'Parque natural con bosque denso y actividades ecoturísticas.',
  latitud: 20.2160,
  longitud: -98.7310,
  horario_apertura: '09:00',
  horario_cierre: '22:00',
  activo: true,
  imagenes: [],
  servicios: [{ id: 18, nombre: 'Senderismo', icono: 'hiking' },
    { id: 20, nombre: 'Observación de flora', icono: 'leaf' },],
  hasCabin: true,
  precio_minimo: 700,
  precio_maximo: 2200,
  capacidad_minima: 2,
  capacidad_maxima: 10,
  cabanas_libres: 5,
  campings_libres: 8
},
{
  id: 11,
  nombre: 'Bosque de la Esperanza',
  direccion: 'Valle de Bravo, Estado de México',
  descripcion: 'Espacio natural con cabañas y recorridos nocturnos.',
  latitud: 19.1450,
  longitud: -100.0950,
  horario_apertura: '10:00',
  horario_cierre: '23:45',
  activo: true,
  imagenes: [],
  servicios: [{ id: 21, nombre: 'Senderismo', icono: 'hiking' },
    { id: 22, nombre: 'Recorridos nocturnos', icono: 'moon' },],
  hasCabin: true,
  precio_minimo: 900,
  precio_maximo: 2800,
  capacidad_minima: 2,
  capacidad_maxima: 12,
  cabanas_libres: 4,
  campings_libres: 10
},
{
  id: 12,
  nombre: 'Sendero de las Luciérnagas',
  direccion: 'Tetela del Volcán, Morelos',
  descripcion: 'Ruta ecológica rodeada de bosque y fauna nocturna.',
  latitud: 18.8930,
  longitud: -98.7280,
  horario_apertura: '17:00',
  horario_cierre: '23:00',
  activo: true,
  imagenes: [],
  servicios: [],
  hasCabin: false,
  precio_minimo: 200,
  precio_maximo: 700,
  capacidad_minima: 2,
  capacidad_maxima: 6,
  cabanas_libres: 0,
  campings_libres: 15
},
{
  id: 13,
  nombre: 'EcoParque El Cedral',
  direccion: 'Huasca de Ocampo, Hidalgo',
  descripcion: 'Parque recreativo con laguna, bosque y recorridos guiados.',
  latitud: 20.2100,
  longitud: -98.5760,
  horario_apertura: '08:00',
  horario_cierre: '21:00',
  activo: true,
  imagenes: [],
  servicios: [{ id: 23, nombre: 'Senderismo', icono: 'hiking' },
    { id: 24, nombre: 'Observación de aves', icono: 'bird' },],
  hasCabin: true,
  precio_minimo: 500,
  precio_maximo: 1500,
  capacidad_minima: 2,
  capacidad_maxima: 8,
  cabanas_libres: 2,
  campings_libres: 10
}
]

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

export async function fetchHospedajesByPark(parkId: number): Promise<HospedajeDetalle[]> {
    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 500))
      // Retorna datos mock según el parque
      return getMockHospedajes(parkId)
    }

    if (!API) return []

    try {
      const response = await fetch(`${API}/parques/${parkId}/hospedajes/`)
      if (!response.ok) throw new Error('Error fetching hospedajes')
      return await response.json()
    } catch (error) {
      console.error('Error cargando hospedajes:', error)
      return []
    }
}

function getMockHospedajes(parkId: number): HospedajeDetalle[] {
  const mockData: Record<number, HospedajeDetalle[]> = {
    1: [
      {
        id: 1,
        parque: 1,
        tipo: 'CABANA',
        categoria: 'PAREJA',
        capacidad: 2,
        estado: 'DISPONIBLE',
        num_camas: 1,
        num_banos: 1,
        tiene_agua: true,
        tiene_luz: true,
        tiene_regadera: true,
        descripcion: 'Cabaña acogedora con vista al bosque',
        precio: 1200,
        imagenes: [{id: 1, url: fireflires1}, {id: 2, url: fireflires2}, 
        {id: 3, url: fireflires3}, {id: 4, url: hero}, 
        {id: 5, url: cabinnight}, {id: 6, url: campingnight}],
      },
      {
        id: 2,
        parque: 1,
        tipo: 'CABANA',
        categoria: 'FAMILIAR',
        capacidad: 6,
        estado: 'OCUPADO',
        num_camas: 3,
        num_banos: 2,
        tiene_agua: true,
        tiene_luz: true,
        tiene_regadera: true,
        descripcion: 'Cabaña grande perfecta para familias',
        precio: 2000,
        imagenes: []
      },
      {
        id: 3,
        parque: 1,
        tipo: 'CAMPING',
        categoria: 'INDIVIDUAL',
        capacidad: 1,
        estado: 'DISPONIBLE',
        num_camas: 0,
        num_banos: null,
        tiene_agua: true,
        tiene_luz: false,
        tiene_regadera: false,
        descripcion: 'Zona de camping individual',
        precio: 500,
        imagenes: []
      },
      {
        id: 4,
        parque: 1,
        tipo: 'CAMPING',
        categoria: 'PAREJA',
        capacidad: 2,
        estado: 'MANTENIMIENTO',
        num_camas: 0,
        num_banos: null,
        tiene_agua: false,
        tiene_luz: false,
        tiene_regadera: false,
        descripcion: 'Zona de camping para parejas',
        precio: 800,
        imagenes: []
      }
    ],
    2: [
      {
        id: 5,
        parque: 2,
        tipo: 'CAMPING',
        categoria: 'PAREJA',
        capacidad: 2,
        estado: 'DISPONIBLE',
        num_camas: 0,
        num_banos: null,
        tiene_agua: true,
        tiene_luz: true,
        tiene_regadera: false,
        descripcion: 'Camping con electricidad para parejas',
        precio: 800,
        imagenes: []
      }
    ]
  }
  return mockData[parkId] || []
}