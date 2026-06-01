import { useReservationStore, type Hospedaje, type Parque } from "../stores/reservationStore";
import { useReservationsStore } from "../stores/reservations";
import { useAuthStore } from "../stores/auth";

const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true";
const API = import.meta.env.VITE_API_URL || null;

const MOCK_PARQUES: Parque[] = [
  {
    id: 1,
    nombre: "Parque de las Fireflies",
    direccion: "Calle Ficticia, 123",
    horario_apertura: "08:00",
    horario_cierre: "20:00",
    hasCabin: true,
    imagen_mapa: null,
  },
  {
    id: 2,
    nombre: "Parque de los Sueños",
    direccion: "Avenida Imaginaria, 456",
    horario_apertura: "09:00",
    horario_cierre: "21:00",
    hasCabin: false,
    imagen_mapa: null,
  },
];

const MOCK_HOSPEDAJES: Hospedaje[] = [
  {
    id: 1,
    parque_id: 1,
    tipo: "CABANA",
    categoria: "PAREJA",
    capacidad: 2,
    estado: "DISPONIBLE",
    num_camas: 1,
    num_banos: 1,
    descripcion: "Cabaña sencilla para parejas",
    tarifa_noche: 1200,
    imagenes: [],
  },
  {
    id: 2,
    parque_id: 1,
    tipo: "CAMPING",
    categoria: "FAMILIAR",
    capacidad: 6,
    estado: "DISPONIBLE",
    num_camas: 0,
    num_banos: 0,
    descripcion: "Zona de camping familiar, hasta 6 personas",
    tarifa_noche: 480,
    imagenes: [],
  },
];

const MOCK_RESERVACIONES = [
  { hospedaje_id: 1, inicio: '2026-06-15', fin: '2026-06-20' }
];

export const reservationService = {
  async obtenerParques(): Promise<Parque[]> {
    if (USE_MOCK) {
      await new Promise((r) => setTimeout(r, 400));
      return MOCK_PARQUES;
    } else {
      const res = await fetch(`${API}/api/parques/`);
      if (!res.ok) throw new Error("Error al obtener parques");
      const data = await res.json();
      return data;
    }
  },

  async buscarUnidadesDisponibles() {
    const store = useReservationStore();
    store.disponibilidadConsultada = true;
    store.buscandoDisponibilidad = true;
    store.errorDisponibilidad = "";

    if (USE_MOCK) {
      // Simula request
      await new Promise((r) => setTimeout(r, 600));
      // Lógica para filtrar/fake según el store...
      let disponibles = MOCK_HOSPEDAJES.filter((unit) =>
          unit.tipo === store.tipoHospedaje && 
          unit.parque_id === store.parqueSeleccionado?.id &&
          unit.capacidad >= store.personas,
      );
      if (store.llegada && store.salida) {
        const llegada = new Date(store.llegada).getTime();
        const salida = new Date(store.salida).getTime();
        disponibles = disponibles.filter((unit) => {
          const tieneEmpalme = MOCK_RESERVACIONES.some(res => {
            if (res.hospedaje_id !== unit.id) return false;
            const resInicio = new Date(res.inicio).getTime();
            const resFin = new Date(res.fin).getTime();
            return (llegada < resFin && salida > resInicio);
          });
          return !tieneEmpalme;
        });
      }
      store.unidadesDisponibles = disponibles;
      if (!disponibles.length) {
        store.errorDisponibilidad = "No hay unidades disponibles para tu selección.";
      }
      store.buscandoDisponibilidad = false;
      return;
    } else {
      try {
        const qs = new URLSearchParams({
          parque_id: store.parqueSeleccionado?.id.toString() || '',
          tipo: store.tipoHospedaje || '',
          personas: store.personas.toString(),
          llegada: store.llegada || '',
          salida: store.salida || ''
        });

        const res = await fetch(`${API}/api/hospedajes/disponibles/?${qs}`);
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.fecha_inicio || err.error || "No hay disponibilidad para esta selección.");
        }
        const disponibles = await res.json();
        
        store.unidadesDisponibles = disponibles;
        if (!disponibles.length) {
          store.errorDisponibilidad = "Lo sentimos, todo está lleno para esas fechas.";
        }
      } catch (e: any) {
        store.errorDisponibilidad = e.message;
      } finally {
        store.buscandoDisponibilidad = false;
      }
    }
  },

  async crearReservacion(reservaData: any) {
    const auth = useAuthStore();

    const payload = {
      parque: reservaData.parque.id,
      hospedaje: reservaData.unidad.id,
      fecha_inicio: reservaData.llegada,
      fecha_fin: reservaData.salida,
      num_personas: reservaData.personas,
      tipo_visita: reservaData.tipo
    };

    const res = await fetch(`${API}/api/reservaciones/`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      console.error("Error devuelto por Django:", err);
      throw err;
    }
    return await res.json();
  },

  async getReservaciones() {
    const store = useReservationsStore()
    store.loading = true

    const res = await fetch(`${API}/api/reservaciones/`, {
      headers: { Authorization: `Bearer ${useAuthStore().token}` }
    })
    if (!res.ok) throw new Error('Error cargando reservaciones')
    const data = await res.json()
    store.setReservaciones(data)
    store.loading = false
  },

  async cancelarReservacion(id: number) {
    const auth = useAuthStore()
    const res = await fetch(`${API}/api/reservaciones/${id}/cancelar/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${auth.token}` }
    })
    if (!res.ok) throw new Error("Error al cancelar la reservación")
    
    await this.getReservaciones() 
  }
};
