import { defineStore } from 'pinia';
import { reservationService } from '../services/reservationService';

export type TipoHospedaje = 'CABANA' | 'CAMPING';
export interface Parque {
  id: number;
  nombre: string;
  direccion: string;
  horario_apertura: string;
  horario_cierre: string;
  hasCabin: boolean;
  imagen_mapa: string | null;
}

export interface ImagenHospedaje {
  id: number
  id_Parque: number
  id_hospedaje: number
  url: string
}

export interface Hospedaje {
  id: number;
  parque_id: number;
  tipo: TipoHospedaje;
  categoria: string;
  capacidad: number;
  estado: string;
  num_camas: number | null;
  num_banos: number | null;
  descripcion: string;
  tarifa_noche: number;
  imagenes : ImagenHospedaje[];
}

export interface ReservaBusquedaParams {
  parque_id: number;
  tipo: TipoHospedaje;
  fecha_inicio: string; // ISO format: '2026-06-17'
  fecha_fin: string;    // ISO format
  personas: number;
}

export interface ReservaResumen {
  parque: Parque | null;
  llegada: string | null;
  salida: string | null;
  noches: number;
  tipo: TipoHospedaje | null;
  personas: number;
  unidad: Hospedaje | null; // selección final
  tarifa_noche?: number; // del hospedaje seleccionado
  subtotal?: number;
  servicio?: number;
  total?: number;
}

export const useReservationStore = defineStore('reservation', {
  state: () => ({
    disponibilidadConsultada: false,
    reservaConfirmada: false,
    // Selecciones usuario
    parques: [] as Parque[],
    cargandoParques: false,

    parqueSeleccionado: null as Parque | null,
    tipoHospedaje: null as TipoHospedaje | null,
    llegada: null as string | null, // formato ISO string
    salida: null as string | null,
    personas: 1,
    // Resultado consulta
    unidadesDisponibles: [] as Hospedaje[],
    // Selección final antes de reservar
    unidadSeleccionada: null as Hospedaje | null,

    buscandoDisponibilidad: false,
    errorDisponibilidad: '',

    reservaResumen: null as ReservaResumen | null,
  }),
  
  getters: {
    currentStep: (state) => {
      if (state.reservaConfirmada) {
        return 7;
      }
      if (!state.parqueSeleccionado || !state.tipoHospedaje) {
        return 1;
      }
      if (!state.llegada || !state.salida) {
        return 2;
      }
      if (!state.personas || state.personas < 1) {
        return 3;
      }
      if (!state.disponibilidadConsultada) {
        return 4;
      }
      if (!state.unidadSeleccionada) {
        return 5;
      }
      return 6;
    }
  },

  actions: {
    async cargarParques() {
      this.cargandoParques = true;
      try {
        this.parques = await reservationService.obtenerParques();
      } catch (error) {
        console.error("Error al cargar parques:", error);
      } finally {
        this.cargandoParques = false;
      }
    },

    seleccionarParque(parque: Parque) {
      this.parqueSeleccionado = parque;
      this.unidadSeleccionada = null;
      this.unidadesDisponibles = [];
      this.errorDisponibilidad = '';
      this.disponibilidadConsultada = false;
    },

    seleccionarTipoHospedaje(tipo: TipoHospedaje) {
      this.tipoHospedaje = tipo;
      this.unidadSeleccionada = null;
      this.unidadesDisponibles = [];
      this.errorDisponibilidad = '';
      this.disponibilidadConsultada = false;
    },

    setFechas(llegada: string | null, salida: string | null) {
      this.llegada = llegada;
      this.salida = salida;
      this.disponibilidadConsultada = false;
    },

    setPersonas(n: number) {
      this.personas = n;
      this.disponibilidadConsultada = false;
    },

    seleccionarUnidad(hospedaje: Hospedaje) {
      this.unidadSeleccionada = hospedaje;
      this.calcularResumen();
    },

    resetearReserva() {
      this.disponibilidadConsultada = false;
      this.reservaConfirmada = false;
      this.parqueSeleccionado = null;
      this.tipoHospedaje = null;
      this.llegada = null;
      this.salida = null;
      this.personas = 1;
      this.unidadSeleccionada = null;
      this.unidadesDisponibles = [];
      this.errorDisponibilidad = '';
      this.reservaResumen = null;
    },

    calcularResumen() {
      if (
        this.parqueSeleccionado &&
        this.llegada &&
        this.salida &&
        this.tipoHospedaje &&
        this.unidadSeleccionada
      ) {
        const nights = this.calcularNoches(this.llegada, this.salida);
        const tarifa = (this.unidadSeleccionada.tarifa_noche || 0);
        const subtotal = tarifa * nights;
        const servicio = subtotal * 0.05; 
        const total = subtotal + servicio;

        this.reservaResumen = {
          parque: this.parqueSeleccionado,
          llegada: this.llegada,
          salida: this.salida,
          noches: nights,
          tipo: this.tipoHospedaje,
          personas: this.personas,
          unidad: this.unidadSeleccionada,
          tarifa_noche: tarifa,
          subtotal,
          servicio,
          total,
        };
      }
    },

    calcularNoches(inicio: string, fin: string): number {
      const d1 = new Date(inicio);
      const d2 = new Date(fin);
      const ms = d2.getTime() - d1.getTime();
      return Math.max(0, Math.round(ms / 86400000));
    },
  },
});