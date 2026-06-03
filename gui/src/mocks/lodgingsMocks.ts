import type { Hospedaje } from '../stores/reservationStore'

export function getMockHospedajes(parkId: number): Hospedaje[] {
  const mockData: Record<number, Hospedaje[]> = {
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
        imagenes: [
          { id: 1, url: 'https://images.unsplash.com/photo-1542718610-a1d656d1884c?auto=format&fit=crop&w=800&q=80' }, 
          { id: 2, url: 'https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=800&q=80' }, 
          { id: 3, url: 'https://images.unsplash.com/photo-1587061949409-02df41d5e562?auto=format&fit=crop&w=800&q=80' }, 
          { id: 4, url: 'https://images.unsplash.com/photo-1510798831971-661eb04b3739?auto=format&fit=crop&w=800&q=80' }, 
          { id: 5, url: 'https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&w=800&q=80' }, 
          { id: 6, url: 'https://images.unsplash.com/photo-1470240731273-7821a6eeb6bd?auto=format&fit=crop&w=800&q=80' }
        ],
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
        imagenes: [
          { id: 7, url: 'https://images.unsplash.com/photo-1585543805890-6051f7829f98?auto=format&fit=crop&w=800&q=80' }
        ]
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
        imagenes: [
          { id: 8, url: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=800&q=80' }
        ]
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
        imagenes: [
          { id: 9, url: 'https://images.unsplash.com/photo-1533873984035-25970ab07461?auto=format&fit=crop&w=800&q=80' }
        ]
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
        imagenes: [
          { id: 51, url: 'https://images.unsplash.com/photo-1510312305653-8ed496efae75?auto=format&fit=crop&w=800&q=80' }
        ]
      }
    ],
    3: [
      {
        id: 301,
        parque: 3,
        tipo: 'CABANA',
        categoria: 'PREMIUM',
        capacidad: 4,
        estado: 'DISPONIBLE',
        num_camas: 2,
        num_banos: 1,
        tiene_agua: true,
        tiene_luz: true,
        tiene_regadera: true,
        descripcion: 'Cabaña rústica de lujo con terraza privada e ideal para ver las mariposas.',
        precio: 1800,
        imagenes: [
          { id: 31, url: 'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1?auto=format&fit=crop&w=800&q=80' },
          { id: 32, url: 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80' }
        ]
      },
      {
        id: 302,
        parque: 3,
        tipo: 'CAMPING',
        categoria: 'FAMILIAR',
        capacidad: 6,
        estado: 'DISPONIBLE',
        num_camas: 0,
        num_banos: null,
        tiene_agua: true,
        tiene_luz: false,
        tiene_regadera: true,
        descripcion: 'Espacio amplio para casa de campaña familiar cerca de los servicios principales.',
        precio: 950,
        imagenes: [
          { id: 33, url: 'https://images.unsplash.com/photo-1478131143081-80f52842a946?auto=format&fit=crop&w=800&q=80' }
        ]
      }
    ],
    10: [
      {
        id: 1001,
        parque: 10,
        tipo: 'CABANA',
        categoria: 'GRANDE',
        capacidad: 10,
        estado: 'DISPONIBLE',
        num_camas: 5,
        num_banos: 3,
        tiene_agua: true,
        tiene_luz: true,
        tiene_regadera: true,
        descripcion: 'Cabaña de dos pisos en medio del encinar, equipada con cocina y chimenea.',
        precio: 2200,
        imagenes: [
          { id: 101, url: 'https://images.unsplash.com/photo-1508333706533-1ab43ecb1606?auto=format&fit=crop&w=800&q=80' }
        ]
      }
    ],
    101: [
      {
        id: 501,
        parque: 101,
        tipo: "CABANA",
        categoria: "PREMIUM_FAMILIAR",
        capacidad: 6,
        estado: "DISPONIBLE",
        num_camas: 3,
        num_banos: 2,
        tiene_agua: true,
        tiene_luz: true,
        tiene_regadera: true,
        descripcion: "Hermosa cabaña alpina construida con madera sustentable. Cuenta con chimenea interior, balcón con vista panorámica al valle de las luciérnagas y cocina equipada básica.",
        precio: 2200,
        imagenes: [
          {
            id: 10,
            url: "https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&w=1000&q=80"
          },
          {
            id: 11,
            url: "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1000&q=80"
          }
        ]
      },
      {
        id: 502,
        parque: 101,
        tipo: "CAMPING",
        categoria: "ESPACIO_INDIVIDUAL",
        capacidad: 4,
        estado: "DISPONIBLE",
        num_camas: null,
        num_banos: null,
        tiene_agua: false,
        tiene_luz: false,
        tiene_regadera: false,
        descripcion: "Espacio delimitado de 4x4 metros sobre terreno plano y empastado. Incluye acceso a tomacorrientes en palapas comunes y derecho de uso de zonas de fogata asignadas.",
        precio: 450,
        imagenes: [
          {
            id: 20,
            url: "https://images.unsplash.com/photo-1510312305653-8ed496efae75?auto=format&fit=crop&w=1000&q=80"
          }
        ]
      }
    ]
  }
  return mockData[parkId] || []
}