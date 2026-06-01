<template>
  <div class="parks-admin">

    <!-- Toolbar: selector + nuevo parque -->
    <div class="toolbar">
      <div class="park-selector-wrap">
        <label class="form-label">{{ isSuperuser ? 'Parque' : 'Tu parque asignado' }}</label>
        <select
          v-model="selectedParkId"
          :disabled="isStaff"
          class="park-select"
          @change="onParkChange">
          <option value="">Selecciona un parque</option>
          <option v-for="p in parquesDisponibles" :key="p.id" :value="p.id">
            {{ p.nombre }}{{ !p.activo ? ' (Inactivo)' : '' }}
          </option>
        </select>
      </div>
      <button v-if="isSuperuser" class="btn-nuevo" @click="openNewPark">
        <IconPlus size="12px" /> Nuevo parque
      </button>
    </div>

    <!-- Sin parque -->
    <div v-if="!selectedPark" class="empty-park">
      <p>Selecciona un parque para gestionar su información</p>
    </div>

    <!-- Parque seleccionado -->
    <template v-else>

      <!-- Tabs -->
      <div class="tabs-bar">
        <button
          v-for="t in tabs" :key="t.key"
          :class="['tab-btn', activeTab === t.key && 'active']"
          @click="activeTab = t.key">
          {{ t.label }}
        </button>
      </div>

      <!-- TAB: Informacion -->
      <div v-show="activeTab === 'info'" class="tab-content">

        <!-- Estado -->
        <div class="status-row">
          <span :class="['status-badge', parkForm.activo ? 'badge-activo' : 'badge-inactivo']">
	    <IconDot v-if="parkForm.activo" size="16px" />
	    <IconDotOutline v-else size="8px" />
	    {{ parkForm.activo ? 'Activo' : 'Inactivo' }}
          </span>
          <button class="btn-toggle" @click="parkForm.activo = !parkForm.activo">
            {{ parkForm.activo ? 'Desactivar parque' : 'Activar parque' }}
          </button>
        </div>

        <div class="form-section">
          <h3 class="section-label">Datos generales</h3>

          <!-- Nombre -->
          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Nombre</span>
              <input
                v-model="parkForm.nombre"
                :disabled="!parkEditing.nombre"
                :class="['field-input', parkEditing.nombre && 'active']"
                placeholder="Nombre del parque"/>
            </div>
            <button :class="['edit-btn', parkEditing.nombre && 'active']" @click="toggleParkEdit('nombre')">
              <IconEdit />
            </button>
          </div>

          <!-- Direccion -->
          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Dirección</span>
              <input
                v-model="parkForm.direccion"
                :disabled="!parkEditing.direccion"
                :class="['field-input', parkEditing.direccion && 'active']"
                placeholder="Dirección completa"/>
            </div>
            <button :class="['edit-btn', parkEditing.direccion && 'active']" @click="toggleParkEdit('direccion')">
              <IconEdit />
            </button>
          </div>

          <!-- Descripcion -->
          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Descripción</span>
              <textarea
                v-model="parkForm.descripcion"
                :disabled="!parkEditing.descripcion"
                :class="['field-input field-textarea', parkEditing.descripcion && 'active']"
                placeholder="Descripción del parque"
                rows="3"/>
            </div>
            <button :class="['edit-btn', parkEditing.descripcion && 'active']" @click="toggleParkEdit('descripcion')">
              <IconEdit />
            </button>
          </div>

          <!-- Horarios -->
          <div class="field-row-2">
            <div class="field-content">
              <span class="field-label">Horario apertura</span>
              <input
                v-model="parkForm.horario_apertura"
                :disabled="!parkEditing.horario_apertura"
                :class="['field-input', parkEditing.horario_apertura && 'active']"
                type="time"/>
            </div>
            <button :class="['edit-btn', parkEditing.horario_apertura && 'active']" @click="toggleParkEdit('horario_apertura')">
              <IconEdit />
            </button>
            <div class="field-content">
              <span class="field-label">Horario cierre</span>
              <input
                v-model="parkForm.horario_cierre"
                :disabled="!parkEditing.horario_cierre"
                :class="['field-input', parkEditing.horario_cierre && 'active']"
                type="time"/>
            </div>
            <button :class="['edit-btn', parkEditing.horario_cierre && 'active']" @click="toggleParkEdit('horario_cierre')">
              <IconEdit />
            </button>
          </div>

          <!-- Coordenadas (solo superuser) -->
          <div v-if="isSuperuser" class="field-row-2">
            <div class="field-content">
              <span class="field-label">Latitud</span>
              <input
                v-model.number="parkForm.latitud"
                :disabled="!parkEditing.latitud"
                :class="['field-input', parkEditing.latitud && 'active']"
                type="number" step="0.000001"/>
            </div>
            <button :class="['edit-btn', parkEditing.latitud && 'active']" @click="toggleParkEdit('latitud')">
              <IconEdit />
            </button>
            <div class="field-content">
              <span class="field-label">Longitud</span>
              <input
                v-model.number="parkForm.longitud"
                :disabled="!parkEditing.longitud"
                :class="['field-input', parkEditing.longitud && 'active']"
                type="number" step="0.000001"/>
            </div>
            <button :class="['edit-btn', parkEditing.longitud && 'active']" @click="toggleParkEdit('longitud')">
              <IconEdit />
            </button>
          </div>
        </div>

        <!-- Imagenes -->
        <div class="form-section">
          <h3 class="section-label">Imágenes del parque</h3>
          <div class="images-gallery">
            <div
              v-for="(img, idx) in parkImages"
              :key="img.id ?? idx"
              class="img-thumb">
              <img :src="img.url" alt="imagen" />
              <button class="img-remove" @click="removeParkImage(idx)">
		<IconCross size="8px" />
	      </button>
            </div>
            <label class="img-add">
              <input
                ref="parkImageInput"
                type="file"
                accept="image/*"
                multiple
                style="display:none"
                @change="addParkImages"/>
              <span>+</span>
              <span class="img-add-label">Agregar</span>
            </label>
          </div>
        </div>

        <!-- Acciones -->
        <div class="park-actions">
          <button class="btn-save" :disabled="savingPark" @click="savePark">
            {{ savingPark ? 'Guardando...' : 'Guardar cambios' }}
          </button>
          <button v-if="isSuperuser" class="btn-danger-outline" @click="showDeletePark = true">
            Eliminar parque
          </button>
        </div>
      </div>

      <!-- TAB: Hospedajes -->
      <div v-show="activeTab === 'hospedajes'" class="tab-content">
	<SearchBar
	  v-model="hospFilters"
	  :filters="hospFilterDefs"
	/>

        <div class="section-toolbar">
          <p class="results-count">{{ parkHospedajes.length }} hospedajes</p>
          <button class="btn-nuevo" @click="showNewHospedaje = !showNewHospedaje">
	    <template v-if="showNewHospedaje">
	      <IconMinus size="12px" /> Cerrar
	    </template>
	    <template v-else>
	      <IconPlus size="12px" /> Nuevo hospedaje
	    </template>
	  </button>
        </div>

        <!-- Formulario nuevo hospedaje -->
        <div v-if="showNewHospedaje" class="form-section hospedaje-form">
          <h3 class="section-label">Crear hospedaje</h3>
          <HospedajeForm
            :form="newHospedajeForm"
            :saving="creatingHospedaje"
            @save="createHospedaje"
            @cancel="showNewHospedaje = false" />
        </div>

        <!-- Lista de hospedajes -->
        <div class="hospedajes-list">
          <div
            v-for="h in parkHospedajes"
            :key="h.id"
            class="hospedaje-row">

            <!-- Row compacta -->
            <div class="hosp-row-header" @click="toggleHospedajeEdit(h.id)">
              <div class="hosp-row-left">
                <span :class="['hosp-estado-dot', estadoHospDot(h.estado)]" />
                <span class="hosp-tipo">
		  {{ h.tipo === 'CABANA' ? 'Cabaña' : 'Camping' }} #{{ h.id }}
		  · {{ categoriaLabel[h.categoria] }}
		</span>
		<span class="hosp-cap">
		  <IconPeople size="11px" />
		  {{ h.capacidad }}
		</span>
                <span class="hosp-precio">${{ h.precio.toLocaleString('es-MX') }}/noche</span>
              </div>
              <div class="hosp-row-right">
                <span :class="['hosp-estado-badge', `hosp-${h.estado.toLowerCase()}`]">
                  {{ estadoHospLabel[h.estado] }}
                </span>
                <IconChevronUp v-if="expandedHospedaje === h.id" size="10px" class="hosp-chevron" />
		<IconChevronDown v-else size="10px" class="hosp-chevron" />
              </div>
            </div>

            <!-- Form expandida de edicion -->
            <div v-if="expandedHospedaje === h.id" class="hosp-edit-form">
              <HospedajeForm
                :form="getHospedajeEditForm(h.id)"
                :saving="savingHospedaje === h.id"
                :show-estado="true"
                @save="saveHospedaje(h.id)"
                @cancel="expandedHospedaje = null">
                <template #extra-actions>
                  <button class="btn-danger-outline" @click="confirmDeleteHospedaje(h.id)">
                    Eliminar hospedaje
                  </button>
                </template>
              </HospedajeForm>
            </div>

          </div>

          <div v-if="parkHospedajes.length === 0" class="empty-state">
            No hay hospedajes en este parque
          </div>
        </div>
      </div>

      <!-- TAB: Reservaciones -->
      <div v-show="activeTab === 'reservaciones'" class="tab-content">

        <div class="section-toolbar">
          <p class="results-count">{{ filteredParkReservaciones.length }} reservaciones</p>
          <select v-model="reservFilter" class="filter-select">
            <option value="">Todos los estados</option>
            <option value="ACTIVA">Activa</option>
            <option value="EN_PROCESO">En proceso</option>
            <option value="COMPLETADA">Completada</option>
            <option value="CANCELADA">Cancelada</option>
          </select>
        </div>

	<SearchBar
	  v-model="reservFilters"
	  :filters="reservFilterDefs"
	/>
	
	<div class="reserv-list">
	  <AdminReservationRow
	    v-for="r in filteredParkReservaciones"
	    :key="r.id"
	    :reservacion="r"
	    @cancelar="confirmCancelReserv" />
	  <div v-if="filteredParkReservaciones.length === 0" class="empty-state">
	    No hay reservaciones con este estado
	  </div>
	</div>
	
      </div>

    </template>

    <!-- Modal: Nuevo parque -->
    <transition name="dialog-fade">
      <div v-if="showNewParkModal" class="dialog-backdrop" @click.self="showNewParkModal = false">
        <div class="dialog-box dialog-wide">
          <div class="dialog-info-header">
            <h3 class="dialog-title">Nuevo parque</h3>
            <button class="dialog-close" @click="showNewParkModal = false">
              <svg width="11" height="11" viewBox="0 0 10 10" fill="none">
                <path d="M1 1l8 8M9 1l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="new-park-form">
            <div class="form-row-2">
              <div class="field-content">
                <span class="field-label">Nombre</span>
                <input v-model="newParkForm.nombre" class="field-input active" placeholder="Nombre del parque"/>
              </div>
              <div class="field-content">
                <span class="field-label">Dirección</span>
                <input v-model="newParkForm.direccion" class="field-input active" placeholder="Dirección"/>
              </div>
            </div>
            <div class="field-content">
              <span class="field-label">Descripción</span>
              <textarea v-model="newParkForm.descripcion" class="field-input field-textarea active" rows="2" placeholder="Descripción"/>
            </div>
            <div class="form-row-4">
              <div class="field-content">
                <span class="field-label">Latitud</span>
                <input v-model.number="newParkForm.latitud" type="number" step="0.000001" class="field-input active"/>
              </div>
              <div class="field-content">
                <span class="field-label">Longitud</span>
                <input v-model.number="newParkForm.longitud" type="number" step="0.000001" class="field-input active"/>
              </div>
              <div class="field-content">
                <span class="field-label">Apertura</span>
                <input v-model="newParkForm.horario_apertura" type="time" class="field-input active"/>
              </div>
              <div class="field-content">
                <span class="field-label">Cierre</span>
                <input v-model="newParkForm.horario_cierre" type="time" class="field-input active"/>
              </div>
            </div>
            <div class="dialog-actions">
              <button class="btn-outline-sm" @click="showNewParkModal = false">Cancelar</button>
              <button class="btn-save" :disabled="creatingPark" @click="createPark">
                {{ creatingPark ? 'Creando...' : 'Crear parque' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Dialogos de confirmacion -->
    <AppConfirmDialog
      v-model="showDeletePark"
      title="Eliminar parque"
      confirm-label="Sí, eliminar parque"
      variant="danger"
      @confirm="deletePark">
      Esta acción eliminará el parque <strong>{{ selectedPark?.nombre }}</strong> y todos sus datos de manera permanente.
    </AppConfirmDialog>

    <AppConfirmDialog
      v-model="showDeleteHospedajeDialog"
      title="Eliminar hospedaje"
      confirm-label="Sí, eliminar hospedaje"
      variant="danger"
      @confirm="deleteHospedaje">
      ¿Estás seguro de eliminar este hospedaje? Esta acción es irreversible.
    </AppConfirmDialog>

    <AppConfirmDialog
      v-model="showCancelReservDialog"
      title="Cancelar reservación"
      confirm-label="Cancelar reservación"
      variant="danger"
      @confirm="cancelReservacion">
      ¿Estás seguro de cancelar la reservación <strong>#{{ cancelReservId }}</strong>? Esta acción es irreversible.
    </AppConfirmDialog>

  </div>
</template>

<script setup lang="ts">
 import { ref, reactive, computed, watch } from 'vue'
 import { useAuthStore } from '../../stores/auth'
 import { useNotification } from '../../composables/useNotification'
 import AppConfirmDialog from '../ui/AppConfirmDialog.vue'
 import IconEdit from '../svg/IconEdit.vue'
 import IconPlus from '../svg/IconPlus.vue'
 import IconDot from '../svg/IconDot.vue'
 import IconDotOutline from '../svg/IconDotOutline.vue'
 import IconPeople from '../svg/IconPeople.vue'
 import IconArrow from '../svg/IconArrow.vue'
 import IconChevronUp from '../svg/IconChevronUp.vue'
 import IconChevronDown from '../svg/IconChevronDown.vue'
 import HospedajeForm from './HospedajeForm.vue'
 import IconMinus from '../svg/IconMinus.vue'
 import IconCross from '../svg/IconCross.vue'
 import SearchBar from '../ui/SearchBar.vue'
 import AdminReservationRow from './AdminReservationRow.vue'
 import type { FilterDef, FilterValues } from '../ui/SearchBar.vue'

 const auth = useAuthStore()
 const { show } = useNotification()

 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
 const API = import.meta.env.VITE_API_URL || null

 //Rol
 const isStaff = computed(() => !!(auth.user?.is_staff && !(auth.user as any)?.is_superuser))
 const isSuperuser = computed(() => !!(auth.user as any)?.is_superuser)
 const parqueAsignado = computed<number | null>(() => (auth.user as any)?.parque_asignado ?? null)

 //Tipos
 interface Imagen { id: number | null; url: string; file?: File }

 interface ParqueMock {
   id: number;
   nombre: string;
   direccion: string;
   descripcion: string | null
   latitud: number;
   longitud: number;
   horario_apertura: string;
   horario_cierre: string
   imagen_mapa: string | null;
   activo: boolean
 }

 interface HospedajeMock {
   id: number;
   parque_id: number;
   tipo: 'CABANA' | 'CAMPING'
   categoria: 'INDIVIDUAL' | 'PAREJA' | 'FAMILIAR';
   capacidad: number
   estado: 'DISPONIBLE' | 'OCUPADO' | 'MANTENIMIENTO'
   num_camas: number | null;
   num_banos: number | null
   tiene_agua: boolean;
   tiene_luz: boolean;
   tiene_regadera: boolean
   descripcion: string | null;
   precio: number
 }

 interface ReservMock {
   id: number;
   parque_id: number
   usuario: { nombre: string; apellidos: string; email: string }
   hospedaje: { id: number; tipo: string }
   fecha_inicio: string;
   fecha_fin: string
   num_personas: number;
   tipo_visita: string
   estado: 'ACTIVA' | 'EN_PROCESO' | 'CANCELADA' | 'COMPLETADA'
   created_at: string
 }

 //Mock data
 const mockParques = ref<ParqueMock[]>([
   { id:1, nombre:'Parque Sierra Chincua',  direccion:'Angangueo, Michoacán', descripcion:'Santuario de mariposa monarca en la sierra michoacana.', latitud:19.6186, longitud:-100.2736, horario_apertura:'08:00', horario_cierre:'18:00', imagen_mapa:null, activo:true  },
   { id:2, nombre:'Parque Piedra Herrada',  direccion:'Valle de Bravo, Estado de México', descripcion:'Reserva natural con senderos y avistamiento de monarcas.', latitud:19.1878, longitud:-100.1411, horario_apertura:'09:00', horario_cierre:'17:00', imagen_mapa:null, activo:true  },
   { id:3, nombre:'Parque El Rosario',      direccion:'Ocampo, Michoacán', descripcion:'El mayor santuario de mariposa monarca del mundo.', latitud:19.6472, longitud:-100.2800, horario_apertura:'08:00', horario_cierre:'18:00', imagen_mapa:null, activo:false },
 ])
 const mockHospedajes = ref<HospedajeMock[]>([
   { id:1, parque_id:1, tipo:'CABANA',  categoria:'FAMILIAR',   capacidad:8, estado:'DISPONIBLE',   num_camas:4, num_banos:2, tiene_agua:true, tiene_luz:true, tiene_regadera:true,  descripcion:'Cabaña familiar con vista al bosque', precio:1800 },
   { id:2, parque_id:1, tipo:'CABANA',  categoria:'PAREJA',     capacidad:2, estado:'OCUPADO',       num_camas:1, num_banos:1, tiene_agua:true, tiene_luz:true, tiene_regadera:true,  descripcion:'Cabaña íntima con terraza privada',   precio:900  },
   { id:3, parque_id:1, tipo:'CAMPING', categoria:'INDIVIDUAL', capacidad:2, estado:'DISPONIBLE',   num_camas:null, num_banos:null, tiene_agua:false, tiene_luz:false, tiene_regadera:false, descripcion:'Zona de camping', precio:250 },
   { id:4, parque_id:1, tipo:'CAMPING', categoria:'FAMILIAR',   capacidad:6, estado:'MANTENIMIENTO', num_camas:null, num_banos:null, tiene_agua:true,  tiene_luz:false, tiene_regadera:false, descripcion:'Zona camping familiar', precio:600 },
   { id:5, parque_id:2, tipo:'CABANA',  categoria:'FAMILIAR',   capacidad:6, estado:'DISPONIBLE',   num_camas:3, num_banos:2, tiene_agua:true, tiene_luz:true, tiene_regadera:true,  descripcion:'Cabaña a orillas del río', precio:1500 },
   { id:6, parque_id:2, tipo:'CAMPING', categoria:'PAREJA',     capacidad:2, estado:'DISPONIBLE',   num_camas:null, num_banos:null, tiene_agua:false, tiene_luz:false, tiene_regadera:false, descripcion:'Camping para parejas', precio:350 },
   { id:7, parque_id:3, tipo:'CABANA',  categoria:'FAMILIAR',   capacidad:10, estado:'DISPONIBLE',  num_camas:5, num_banos:3, tiene_agua:true, tiene_luz:true, tiene_regadera:true,  descripcion:'Gran cabaña familiar', precio:2500 },
 ])
 const mockReservas = ref<ReservMock[]>([
   { id:1, parque_id:1, usuario:{ nombre:'Fulanito', apellidos:'Pérez', email:'fulanito@example.com' }, hospedaje:{ id:1, tipo:'CABANA' }, fecha_inicio:'2026-06-15', fecha_fin:'2026-06-18', num_personas:4, tipo_visita:'CABANA', estado:'ACTIVA',     created_at:'2026-05-01T10:00:00Z' },
   { id:2, parque_id:1, usuario:{ nombre:'Ana',      apellidos:'García', email:'ana@example.com'     }, hospedaje:{ id:2, tipo:'CABANA' }, fecha_inicio:'2026-07-01', fecha_fin:'2026-07-05', num_personas:2, tipo_visita:'CABANA', estado:'EN_PROCESO', created_at:'2026-05-10T14:00:00Z' },
   { id:3, parque_id:1, usuario:{ nombre:'Carlos',   apellidos:'López',  email:'carlos@example.com'  }, hospedaje:{ id:3, tipo:'CAMPING'}, fecha_inicio:'2026-04-01', fecha_fin:'2026-04-03', num_personas:1, tipo_visita:'CAMPING', estado:'COMPLETADA', created_at:'2026-03-01T09:00:00Z' },
   { id:4, parque_id:2, usuario:{ nombre:'Fulanito', apellidos:'Pérez',  email:'fulanito@example.com'}, hospedaje:{ id:5, tipo:'CABANA' }, fecha_inicio:'2026-08-10', fecha_fin:'2026-08-15', num_personas:5, tipo_visita:'CABANA', estado:'ACTIVA',     created_at:'2026-05-20T11:00:00Z' },
 ])

 //Seleccion de parque
 const selectedParkId = ref<number | ''>(
   isStaff.value && parqueAsignado.value ? parqueAsignado.value : ''
 )
 const activeTab = ref<'info' | 'hospedajes' | 'reservaciones'>('info')

 const tabs = [
   { key: 'info',          label: 'Información' },
   { key: 'hospedajes',    label: 'Hospedajes'  },
   { key: 'reservaciones', label: 'Reservaciones' },
 ]

 const parquesDisponibles = computed<ParqueMock[]>(() => {
   if (isStaff.value && parqueAsignado.value)
     return mockParques.value.filter(p => p.id === parqueAsignado.value)
   return mockParques.value
 })

 const selectedPark = computed<ParqueMock | null>(() =>
   mockParques.value.find(p => p.id === Number(selectedParkId.value)) ?? null
 )

 //Filtros Hospedajes
 const hospFilterDefs: FilterDef[] = [
   { key: 'nombre',   type: 'text',   placeholder: 'Buscar hospedaje...' },
   { key: 'tipo',     type: 'select', placeholder: 'Tipo',
     options: [
       { label: 'Cabaña',  value: 'CABANA'  },
       { label: 'Camping', value: 'CAMPING' },
     ]
   },
   { key: 'estado',   type: 'select', placeholder: 'Estado',
     options: [
       { label: 'Disponible',    value: 'DISPONIBLE'    },
       { label: 'Ocupado',       value: 'OCUPADO'       },
       { label: 'Mantenimiento', value: 'MANTENIMIENTO' },
     ]
   },
 ]
 const hospFilters = ref<FilterValues>({ nombre: '', tipo: '', estado: '' })

 const reservFilter = ref('')
 
 const parkHospedajes = computed<HospedajeMock[]>(() => {
   let result = mockHospedajes.value.filter(h => h.parque_id === Number(selectedParkId.value))
   if (hospFilters.value.nombre) {
     const q = hospFilters.value.nombre.toLowerCase()
     result = result.filter(h =>
       (h.descripcion ?? '').toLowerCase().includes(q) ||
			       h.categoria.toLowerCase().includes(q)
     )
   }
   if (hospFilters.value.tipo)
     result = result.filter(h => h.tipo   === hospFilters.value.tipo)
   if (hospFilters.value.estado)
     result = result.filter(h => h.estado === hospFilters.value.estado)
   return result
 })
 
 //Filtros Reservaciones
 const reservFilterDefs: FilterDef[] = [
   { key: 'usuario',  type: 'text',      placeholder: 'Buscar por usuario...' },
   { key: 'fechas',   type: 'daterange'                                        },
 ]
 const reservFilters = ref<FilterValues>({ usuario: '', fechas_desde: '', fechas_hasta: '' })
 
 const filteredParkReservaciones = computed<ReservMock[]>(() => {
   let result = mockReservas.value.filter(r => r.parque_id === Number(selectedParkId.value))
   if (reservFilter.value)
     result = result.filter(r => r.estado === reservFilter.value)
   if (reservFilters.value.usuario) {
     const q = reservFilters.value.usuario.toLowerCase()
     result = result.filter(r =>
       `${r.usuario.nombre} ${r.usuario.apellidos} ${r.usuario.email}`.toLowerCase().includes(q)
     )
   }
   if (reservFilters.value.fechas_desde)
     result = result.filter(r => r.fecha_inicio >= reservFilters.value.fechas_desde)
   if (reservFilters.value.fechas_hasta)
     result = result.filter(r => r.fecha_fin <= reservFilters.value.fechas_hasta)
   return result
 })

 //Formulario del parque
 const parkForm = reactive({
   nombre: '', direccion: '', descripcion: '',
   latitud: 0, longitud: 0,
   horario_apertura: '', horario_cierre: '',
   activo: true,
 })

 const parkEditing = reactive({
   nombre: false, direccion: false, descripcion: false,
   latitud: false, longitud: false,
   horario_apertura: false, horario_cierre: false,
 })

 const parkImages = ref<Imagen[]>([])
 const savingPark = ref(false)
 const showDeletePark = ref(false)

 function syncParkForm() {
   if (!selectedPark.value) return
   Object.assign(parkForm, {
     nombre: selectedPark.value.nombre,
     direccion: selectedPark.value.direccion,
     descripcion: selectedPark.value.descripcion ?? '',
     latitud: selectedPark.value.latitud,
     longitud: selectedPark.value.longitud,
     horario_apertura: selectedPark.value.horario_apertura,
     horario_cierre: selectedPark.value.horario_cierre,
     activo: selectedPark.value.activo,
   })
   parkImages.value = []
   Object.keys(parkEditing).forEach(k => (parkEditing as any)[k] = false)
 }

 function toggleParkEdit(field: keyof typeof parkEditing) {
   parkEditing[field] = !parkEditing[field]
 }

 watch(selectedPark, syncParkForm, { immediate: true })

 function onParkChange() {
   activeTab.value = 'info'
   expandedHospedaje.value = null
   showNewHospedaje.value = false
 }

 async function savePark() {
   savingPark.value = true
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 500))
     const idx = mockParques.value.findIndex(p => p.id === Number(selectedParkId.value))
     if (idx >= 0)
       Object.assign(mockParques.value[idx], { ...parkForm, id: mockParques.value[idx].id })
     Object.keys(parkEditing).forEach(k => (parkEditing as any)[k] = false)
     show('exito', 'Parque actualizado correctamente')
   } else {
     // TODO backend: PATCH /api/parques/{id}/
   }
   savingPark.value = false
 }

 async function deletePark() {
   if (USE_MOCK) {
     mockParques.value = mockParques.value.filter(p => p.id !== Number(selectedParkId.value))
     selectedParkId.value = ''
     show('normal', 'Parque eliminado')
   } else {
     // TODO backend: DELETE /api/parques/{id}/
   }
 }

 //Imagenes del parque
 function addParkImages(e: Event) {
   const files = (e.target as HTMLInputElement).files
   if (!files) return
   Array.from(files).forEach(file => {
     const reader = new FileReader()
     reader.onload = ev => {
       parkImages.value.push({ id: null, url: ev.target?.result as string, file })
     }
     reader.readAsDataURL(file)
   })
   // TODO backend: POST /api/parques/{id}/imagenes/
 }

 function removeParkImage(idx: number) {
   // TODO backend: DELETE /api/parques/{id}/imagenes/{imageId}/
   parkImages.value.splice(idx, 1)
 }

 //Nuevo parque
 const showNewParkModal = ref(false)
 const creatingPark = ref(false)
 const newParkForm = reactive({
   nombre: '', direccion: '', descripcion: '',
   latitud: 0, longitud: 0, horario_apertura: '08:00', horario_cierre: '18:00',
 })

 function openNewPark() {
   Object.assign(newParkForm, { nombre:'', direccion:'', descripcion:'', latitud:0, longitud:0, horario_apertura:'08:00', horario_cierre:'18:00' })
   showNewParkModal.value = true
 }

 async function createPark() {
   if (!newParkForm.nombre) return
   creatingPark.value = true
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 500))
     const newId = Math.max(...mockParques.value.map(p => p.id)) + 1
     mockParques.value.push({ ...newParkForm, id: newId, imagen_mapa: null, activo: true })
     selectedParkId.value = newId
     showNewParkModal.value = false
     show('exito', `Parque "${newParkForm.nombre}" creado correctamente`)
   } else {
     // TODO backend: POST /api/parques/
   }
   creatingPark.value = false
 }

 //Hospedajes
 const expandedHospedaje = ref<number | null>(null)
 const showNewHospedaje = ref(false)
 const savingHospedaje = ref<number | null>(null)
 const creatingHospedaje = ref(false)
 const showDeleteHospedajeDialog = ref(false)
 const deleteHospedajeId = ref<number | null>(null)

 const hospedajeEditForms = reactive<Record<number, any>>({})

 const newHospedajeForm = reactive({
   tipo: 'CABANA' as 'CABANA' | 'CAMPING',
   categoria: 'FAMILIAR' as 'INDIVIDUAL' | 'PAREJA' | 'FAMILIAR',
   capacidad: 2, estado: 'DISPONIBLE' as any,
   num_camas: 1, num_banos: 1,
   tiene_agua: true, tiene_luz: true, tiene_regadera: true,
   descripcion: '', precio: 0,
 })

 const categoriaLabel: Record<string, string> = {
   INDIVIDUAL: 'Individual', PAREJA: 'Pareja', FAMILIAR: 'Familiar',
 }
 const estadoHospLabel: Record<string, string> = {
   DISPONIBLE: 'Disponible', OCUPADO: 'Ocupado', MANTENIMIENTO: 'Mantenimiento',
 }
 function estadoHospDot(estado: string) {
   return { DISPONIBLE: 'dot-green', OCUPADO: 'dot-yellow', MANTENIMIENTO: 'dot-red' }[estado] ?? ''
 }

 function toggleHospedajeEdit(id: number) {
   if (expandedHospedaje.value === id) {
     expandedHospedaje.value = null
     return
   }
   expandedHospedaje.value = id
   const h = mockHospedajes.value.find(x => x.id === id)
   if (h)
     hospedajeEditForms[id] = { ...h }
 }

 function getHospedajeEditForm(id: number) {
   if (!hospedajeEditForms[id]) {
     const h = mockHospedajes.value.find(x => x.id === id)
     if (h)
       hospedajeEditForms[id] = { ...h }
   }
   return hospedajeEditForms[id]
 }

 async function saveHospedaje(id: number) {
   savingHospedaje.value = id
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 400))
     const idx = mockHospedajes.value.findIndex(h => h.id === id)
     if (idx >= 0)
       Object.assign(mockHospedajes.value[idx], hospedajeEditForms[id], { id })
     expandedHospedaje.value = null
     show('exito', 'Hospedaje actualizado correctamente')
   } else {
     // TODO backend: PATCH /api/hospedajes/{id}/
   }
   savingHospedaje.value = null
 }

 async function createHospedaje() {
   creatingHospedaje.value = true
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 400))
     const newId = Math.max(...mockHospedajes.value.map(h => h.id)) + 1
     mockHospedajes.value.push({ ...newHospedajeForm, id: newId, parque_id: Number(selectedParkId.value) })
     showNewHospedaje.value = false
     show('exito', 'Hospedaje creado correctamente')
   } else {
     // TODO backend: POST /api/hospedajes/
   }
   creatingHospedaje.value = false
 }

 function confirmDeleteHospedaje(id: number) {
   deleteHospedajeId.value = id
   showDeleteHospedajeDialog.value = true
 }

 async function deleteHospedaje() {
   const id = deleteHospedajeId.value
   if (!id) return
   if (USE_MOCK) {
     mockHospedajes.value = mockHospedajes.value.filter(h => h.id !== id)
     expandedHospedaje.value = null
     show('normal', 'Hospedaje eliminado')
   } else {
     // TODO backend: DELETE /api/hospedajes/{id}/
   }
   deleteHospedajeId.value = null
 }

 //Reservaciones
 const showCancelReservDialog = ref(false)
 const cancelReservId         = ref<number | null>(null)

 function confirmCancelReserv(id: number) {
   cancelReservId.value = id
   showCancelReservDialog.value = true
 }

 async function cancelReservacion() {
   const id = cancelReservId.value
   if (!id) return
   if (USE_MOCK) {
     const idx = mockReservas.value.findIndex(r => r.id === id)
     if (idx >= 0)
       mockReservas.value[idx].estado = 'CANCELADA'
     show('normal', `Reservación #${id} cancelada`)
   } else {
     // TODO backend: PATCH /api/reservaciones/{id}/cancelar/
   }
   cancelReservId.value = null
 }

 //Helpers
 const estadoLabel: Record<string, string> = {
   ACTIVA: 'Activa', EN_PROCESO: 'En proceso', COMPLETADA: 'Completada', CANCELADA: 'Cancelada',
 }

 function formatDate(s: string) {
   const [y, m, d] = s.split('-')
   const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
   return `${parseInt(d)} ${months[parseInt(m)-1]} ${y}`
 }
</script>

<style scoped>
 .parks-admin { display: flex; flex-direction: column; gap: 1.25rem; }

 /* Toolbar */
 .toolbar {
   display: flex; align-items: flex-end; justify-content: space-between;
   gap: 1rem; flex-wrap: wrap;
 }
 .park-selector-wrap { display: flex; flex-direction: column; gap: 0.3rem; flex: 1; max-width: 360px; }
 .park-select {
   height: 40px; padding: 0 0.875rem;
   border-radius: 8px; border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04); color: var(--color-bone);
   font-size: 13.5px; font-family: var(--font-sans); outline: none;
   appearance: none; cursor: pointer; transition: border-color 0.2s;
 }
 .park-select:disabled { opacity: 0.7; cursor: not-allowed; }
 .park-select:focus { border-color: rgba(123,167,212,0.4); }

 /* Botones comunes */
 .btn-nuevo {
   height: 40px; padding: 0 1rem; border-radius: 8px;
   border: 1px solid rgba(123,167,212,0.3);
   background: transparent; color: var(--color-admin-accent, #7BA7D4);
   font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 0.4rem;
   transition: all 0.15s; white-space: nowrap;
 }
 .btn-nuevo:hover { background: rgba(123,167,212,0.1); }
 .btn-save {
   height: 38px; padding: 0 1.5rem; border-radius: 999px; border: none;
   background: var(--color-admin-accent, #7BA7D4); color: #0A1525;
   font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s;
 }
 .btn-save:hover:not(:disabled) { box-shadow: 0 0 20px rgba(123,167,212,0.4); }
 .btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
 .btn-danger-outline {
   height: 38px; padding: 0 1.25rem; border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.3); background: transparent;
   color: var(--color-danger); font-size: 13px; cursor: pointer; transition: all 0.15s;
 }
 .btn-danger-outline:hover { background: rgba(255,138,123,0.08); }
 .btn-toggle {
   height: 30px; padding: 0 0.875rem; border-radius: 999px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); font-size: 12px; cursor: pointer; transition: all 0.15s;
 }
 .btn-toggle:hover { background: rgba(255,255,255,0.05); color: var(--color-bone); }
 .btn-outline-sm {
   height: 36px; padding: 0 1rem; border-radius: 999px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); font-size: 13px; cursor: pointer;
 }

 /* Sin parque */
 .empty-park {
   padding: 4rem 2rem; text-align: center;
   border: 1px dashed rgba(123,167,212,0.15); border-radius: 14px;
   color: var(--color-bone-mute); font-size: 13px;
 }

 /* Tabs */
 .tabs-bar { display: flex; gap: 0.25rem; border-bottom: 1px solid var(--color-border); padding-bottom: 0; }
 .tab-btn {
   height: 38px; padding: 0 1.25rem; border: none;
   background: transparent; color: var(--color-bone-mute);
   font-size: 13.5px; cursor: pointer; border-bottom: 2px solid transparent;
   transition: all 0.15s; margin-bottom: -1px;
 }
 .tab-btn:hover { color: var(--color-bone); }
 .tab-btn.active { color: var(--color-admin-accent, #7BA7D4); border-bottom-color: var(--color-admin-accent, #7BA7D4); }

 .tab-content { display: flex; flex-direction: column; gap: 1.25rem; padding-top: 0.5rem; }

 /* Status */
 .status-row { display: flex; align-items: center; gap: 0.75rem; }
 .status-badge {
   font-size: 12px;
   font-weight: 600;
   padding: 0.25rem 0.75rem;
   border-radius: 999px;
   display: inline-flex;
   align-items: center;
   gap: 0.35rem;
 }
 .badge-activo   { background: rgba(123,216,176,0.12); color: var(--color-green); }
 .badge-inactivo { background: rgba(255,138,123,0.1);  color: var(--color-danger); }

 /*Secciones*/
 .form-section {
   background: rgba(123,167,212,0.03);
   border: 1px solid rgba(123,167,212,0.1);
   border-radius: 12px; padding: 1.25rem;
   display: flex; flex-direction: column; gap: 0.875rem;
 }
 .section-label {
   font-size: 10.5px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.08em;
   color: var(--color-bone-mute);
 }

 /* Campo editable */
 .field-row   { display: flex; align-items: flex-end; gap: 0.5rem; }
 .field-row-2 { display: grid; grid-template-columns: 1fr auto 1fr auto; align-items: flex-end; gap: 0.5rem; }
 .form-row-2  { display: grid; grid-template-columns: 1fr 1fr; gap: 0.875rem; }
 .form-row-4  { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }

 .field-content { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; }
 .field-label {
   font-size: 10.5px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.08em; color: var(--color-bone-mute);
 }
 .field-input {
   width: 100%; padding: 0.5rem 0.75rem;
   border-radius: 8px; border: 1px solid transparent;
   background: transparent; color: var(--color-bone-soft);
   font-size: 13.5px; font-family: var(--font-sans); outline: none;
   transition: all 0.2s; cursor: default; resize: none;
 }
 .field-input:disabled { cursor: default; color: var(--color-bone-soft); }
 .field-input.active {
   border-color: rgba(123,167,212,0.3); background: rgba(255,255,255,0.04);
   color: var(--color-bone); cursor: text;
 }
 .field-textarea { min-height: 72px; resize: vertical; }

 .edit-btn {
   flex-shrink: 0; width: 30px; height: 30px; border-radius: 8px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-mute); cursor: pointer;
   display: flex; align-items: center; justify-content: center; transition: all 0.15s;
 }
 .edit-btn:hover { color: var(--color-bone); background: rgba(255,255,255,0.05); }
 .edit-btn.active { color: var(--color-admin-accent, #7BA7D4); border-color: rgba(123,167,212,0.3); background: rgba(123,167,212,0.06); }

 /* Galeria imagenes */
 .images-gallery { display: flex; flex-wrap: wrap; gap: 0.5rem; }
 .img-thumb {
   position: relative; width: 80px; height: 80px;
   border-radius: 8px; overflow: hidden;
   border: 1px solid var(--color-border);
 }
 .img-thumb img { width: 100%; height: 100%; object-fit: cover; }
 .img-remove {
   position: absolute; top: 2px; right: 2px;
   width: 20px; height: 20px; border-radius: 50%;
   background: rgba(0,0,0,0.6); border: none; color: #fff;
   font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center;
 }
 .img-add {
   width: 80px; height: 80px; border-radius: 8px;
   border: 1px dashed rgba(123,167,212,0.3);
   display: flex; flex-direction: column; align-items: center; justify-content: center;
   cursor: pointer; color: var(--color-admin-accent, #7BA7D4); gap: 0.2rem;
   transition: background 0.15s;
 }
 .img-add:hover { background: rgba(123,167,212,0.06); }
 .img-add span:first-child { font-size: 22px; line-height: 1; }
 .img-add-label { font-size: 10px; }

 /* Acciones parque */
 .park-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; }

 /* Hospedajes */
 .section-toolbar {
   display: flex; align-items: center;
   justify-content: space-between; gap: 1rem;
 }
 .results-count { font-size: 12px; color: var(--color-bone-mute); font-family: var(--font-mono); }

 .hospedajes-list { display: flex; flex-direction: column; gap: 0.5rem; }

 .hospedaje-row {
   border: 1px solid var(--color-border); border-radius: 10px;
   overflow: hidden; background: rgba(255,255,255,0.02);
 }

 .hosp-row-header {
   display: flex; align-items: center; justify-content: space-between;
   padding: 0.75rem 1rem; cursor: pointer; transition: background 0.15s;
 }
 .hosp-row-header:hover { background: rgba(255,255,255,0.03); }
 .hosp-row-left  { display: flex; align-items: center; gap: 0.75rem; }
 .hosp-row-right { display: flex; align-items: center; gap: 0.5rem; }

 .hosp-estado-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
 .dot-green  { background: var(--color-green); }
 .dot-yellow { background: var(--color-accent); }
 .dot-red    { background: var(--color-danger); }

 .hosp-tipo   { font-size: 13px; color: var(--color-bone-soft); }
 .hosp-cap    { display: inline-flex; align-items: center; gap: 0.25rem; font-size: 12px; color: var(--color-bone-mute); }
 .hosp-precio { font-size: 13px; font-weight: 600; color: var(--color-bone); }
 .hosp-chevron{ font-size: 10px; color: var(--color-bone-mute); }

 .hosp-estado-badge {
   font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 999px;
 }
 .hosp-disponible   { background: rgba(123,216,176,0.12); color: var(--color-green); }
 .hosp-ocupado      { background: rgba(232,255,122,0.1);  color: var(--color-accent); }
 .hosp-mantenimiento{ background: rgba(255,138,123,0.1);  color: var(--color-danger); }

 .hosp-edit-form {
   border-top: 1px solid var(--color-border);
   padding: 1rem;
   background: rgba(123,167,212,0.02);
 }

 .hospedaje-form { background: rgba(123,167,212,0.04); border-color: rgba(123,167,212,0.15); }

 /* Reservaciones */
 .filter-select {
   height: 32px; padding: 0 2rem 0 0.75rem;
   border-radius: 999px; border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04); color: var(--color-bone);
   font-size: 12px; font-family: var(--font-sans); outline: none;
   appearance: none; cursor: pointer;
 }

 .reserv-list { display: flex; flex-direction: column; gap: 0.5rem; }

 /* Estado vacio */
 .empty-state {
   padding: 2rem; text-align: center;
   color: var(--color-bone-mute); font-size: 13px;
   border: 1px dashed rgba(255,255,255,0.07); border-radius: 10px;
 }

 /* Dialogo nuevo parque */
 .dialog-backdrop {
   position: fixed; inset: 0; z-index: 9999;
   background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
   display: flex; align-items: center; justify-content: center; padding: 1rem;
 }
 .dialog-box {
   background: #0d1a10; border: 1px solid rgba(123,167,212,0.18);
   border-radius: 16px; padding: 1.75rem; width: 100%;
   box-shadow: 0 24px 48px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 1rem;
 }
 .dialog-wide { max-width: 640px; }
 .dialog-title { font-size: 18px; font-weight: 600; color: var(--color-bone); }
 .dialog-info-header { display: flex; align-items: center; justify-content: space-between; }
 .dialog-close {
   width: 28px; height: 28px; border-radius: 8px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); cursor: pointer;
   display: flex; align-items: center; justify-content: center;
 }
 .dialog-close:hover { background: rgba(255,255,255,0.06); }
 .dialog-actions { display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 0.5rem; }
 .new-park-form { display: flex; flex-direction: column; gap: 0.875rem; }

 /* Animacion dialogo */
 .dialog-fade-enter-active, .dialog-fade-leave-active { transition: opacity 0.2s ease; }
 .dialog-fade-enter-from, .dialog-fade-leave-to { opacity: 0; }
</style>
