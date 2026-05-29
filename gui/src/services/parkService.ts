import { useParksStore } from '../stores/parks'
import type { Parque } from '../stores/parks'
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
    activo: false,
    imagenes: [{id: 1, parque: 3, url: fireflires1}, {id: 2, parque: 3, url: fireflires2}, 
      {id: 3, parque: 3, url: fireflires3}, {id: 4, parque: 3, url: hero}, 
      {id: 5, parque: 3, url: cabinnight}, {id: 6, parque: 3, url: campingnight}]
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
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
  imagen_mapa: null,
  activo: true,
  imagenes: []
}
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
