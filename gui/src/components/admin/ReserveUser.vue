<template>
  <div class="reserve-form">

    <!-- Detalles -->
    <section class="form-section">
      <div class="section-header">
        <span class="section-num">1</span>
        <h2 class="section-title">Detalles de la reservación</h2>
      </div>
      
      <div class="form-row">
        <!-- Parque -->
        <div class="form-field">
          <label class="form-label">Parque</label>
          <select
            v-model="form.parque_id"
            :disabled="isStaff"
            class="form-select"
            @change="onParqueChange">
            <option value="">Selecciona un parque</option>
            <option v-for="p in parquesDisponibles" :key="p.id" :value="p.id">
              {{ p.nombre }}
            </option>
          </select>
          <span v-if="isStaff" class="field-hint">Restringido a tu parque asignado</span>
        </div>

        <!-- Tipo de visita -->
        <div class="form-field">
          <label class="form-label">Tipo de visita</label>
          <div class="tipo-group">
            <button
              :class="['tipo-btn', form.tipo === 'CABANA' && 'active']"
              @click="setTipo('CABANA')">
              Cabaña
            </button>
            <button
              :class="['tipo-btn', form.tipo === 'CAMPING' && 'active']"
              @click="setTipo('CAMPING')">
              Camping
            </button>
          </div>
        </div>
      </div>

      <div class="form-row form-row-3">
        <div class="form-field">
          <label class="form-label">Fecha de entrada</label>
          <input
	    v-model="form.fecha_inicio"
	    type="date"
	    :min="FECHA_MIN"
	    :max="FECHA_MAX"
	    class="form-input"
	    style="color-scheme: dark"
	    @change="onFechaInicioChange"
	  />
	  <span v-if="dateErrorInicio" class="date-error">{{ dateErrorInicio }}</span>
        </div>
        <div class="form-field">
          <label class="form-label">Fecha de salida</label>
          <input
	    v-model="form.fecha_fin"
	    type="date"
	    :min="form.fecha_inicio || FECHA_MIN"
	    :max="FECHA_MAX"
	    class="form-input"
	    style="color-scheme: dark"
	    @change="onFechaFinChange"
	  />
	  <span v-if="dateErrorFin" class="date-error">{{ dateErrorFin }}</span>
        </div>
        <div class="form-field">
          <label class="form-label">Número de personas</label>
          <input
            v-model.number="form.num_personas"
            type="number"
            min="1"
            max="50"
            class="form-input"
            @change="selectedHospedaje = null"
          />
        </div>
      </div>
    </section>

    <!-- Hospedaje -->
    <section v-if="canShowHospedajes" class="form-section">
      <div class="section-header">
        <span class="section-num">2</span>
        <h2 class="section-title">
          Hospedaje disponible
          <span class="section-badge">{{ hospedajesFiltrados.length }} disponibles</span>
        </h2>
      </div>

      <div v-if="hospedajesFiltrados.length === 0" class="empty-state">
        No hay hospedajes disponibles para las fechas, tipo y número de personas seleccionados.
      </div>

      <div v-else class="hospedajes-grid">
        <button
          v-for="h in hospedajesFiltrados"
          :key="h.id"
          :class="['hospedaje-card', selectedHospedaje?.id === h.id && 'selected']"
          @click="selectHospedaje(h)">

          <div class="hosp-top">
            <span class="hosp-badge">
              {{ h.tipo === 'CABANA' ? 'Cabaña' : 'Camping' }} #{{ h.id }} · {{ categoriaLabel[h.categoria] }}
            </span>
            <div class="hosp-precio">
              ${{ h.precio.toLocaleString('es-MX') }}<span class="precio-unit">/noche</span>
            </div>
          </div>

	  <div class="hosp-stats">
	    <span><IconPeople size="11px" /> {{ h.capacidad }} personas max.</span>
	    <span v-if="h.num_camas"><IconBed size="11px" /> {{ h.num_camas }} cama{{ h.num_camas > 1 ? 's' : '' }}</span>
	    <span v-if="h.num_banos"><IconShower size="11px" /> {{ h.num_banos }} baño{{ h.num_banos > 1 ? 's' : '' }}</span>
	  </div>
	  
	  <div class="hosp-amenidades">
	    <span v-if="h.tiene_agua"     class="amen"><IconWater  size="10px" /> Agua</span>
	    <span v-if="h.tiene_luz"      class="amen"><IconLight  size="10px" /> Luz</span>
	    <span v-if="h.tiene_regadera" class="amen"><IconShower size="10px" /> Regadera</span>
	  </div>
	  
          <p v-if="h.descripcion" class="hosp-desc">{{ h.descripcion }}</p>
        </button>
      </div>
    </section>

    <!-- Cliente -->
    <section v-if="selectedHospedaje" class="form-section">
      <div class="section-header">
        <span class="section-num">3</span>
        <h2 class="section-title">Cliente</h2>
      </div>

      <div class="form-row">
        <div class="form-field" style="flex: 1">
          <label class="form-label">Correo electrónico del cliente</label>
          <div class="search-row">
            <input
              v-model="clienteForm.email"
              type="email"
              placeholder="cliente@correo.com"
              class="form-input"
              @keydown.enter="buscarCliente"
            />
            <button
              class="btn-buscar"
              :disabled="buscandoCliente || !clienteForm.email"
              @click="buscarCliente">
              {{ buscandoCliente ? 'Buscando...' : 'Buscar' }}
            </button>
          </div>
	  <span v-if="clienteError" class="cliente-error">{{ clienteError }}</span>
        </div>
      </div>

      <!-- Cliente encontrado -->
      <div v-if="clienteEncontrado" class="cliente-found">
        <div class="found-check">✓</div>
        <div>
          <p class="cliente-nombre">{{ clienteEncontrado.nombre }} {{ clienteEncontrado.apellidos }}</p>
          <p class="cliente-correo">{{ clienteEncontrado.email }}</p>
        </div>
      </div>

      <!-- Cliente nuevo -->
      <div v-else-if="clienteBuscado" class="cliente-new">
        <p class="new-hint">Correo no registrado, ingresa los datos del nuevo cliente:</p>
        <div class="form-row">
          <div class="form-field">
            <label class="form-label">Nombre</label>
            <input v-model="clienteForm.nombre" type="text" placeholder="Nombre" class="form-input" />
          </div>
          <div class="form-field">
            <label class="form-label">Apellidos</label>
            <input v-model="clienteForm.apellidos" type="text" placeholder="Apellidos" class="form-input" />
          </div>
        </div>
        <p class="pass-hint">
          La contraseña será generada automáticamente por el sistema y enviada al correo del cliente.
        </p>
      </div>
    </section>

    <!-- Pago y Total -->
    <section v-if="clienteCompleto" class="form-section">
      <div class="section-header">
        <span class="section-num">4</span>
        <h2 class="section-title">Pago y total</h2>
      </div>

      <div class="form-field">
        <label class="form-label">Método de pago</label>
        <div class="pago-group">
          <button
            v-for="p in metodosPago"
            :key="p.value"
            :class="['pago-btn', form.metodo_pago === p.value && 'active']"
            @click="form.metodo_pago = p.value">
            {{ p.label }}
          </button>
        </div>
      </div>

      <!-- Resumen -->
      <div class="resumen-card">
        <p class="resumen-label">Resumen de la reservación</p>
        <div class="res-rows">
          <div class="res-row">
            <span>Parque</span>
            <span>{{ parqueSeleccionado?.nombre }}</span>
          </div>
          <div class="res-row">
            <span>Hospedaje</span>
            <span>
              {{ selectedHospedaje!.tipo === 'CABANA' ? 'Cabaña' : 'Camping' }}
              · {{ categoriaLabel[selectedHospedaje!.categoria] }}
            </span>
          </div>
          <div class="res-row">
            <span>Fechas</span>
            <span>{{ formatDate(form.fecha_inicio) }} → {{ formatDate(form.fecha_fin) }}</span>
          </div>
          <div class="res-row">
            <span>Noches</span>
            <span>{{ totalNights }}</span>
          </div>
          <div class="res-row">
            <span>Personas</span>
            <span>{{ form.num_personas }}</span>
          </div>
          <div class="res-row">
            <span>Precio por noche</span>
            <span>${{ selectedHospedaje!.precio.toLocaleString('es-MX') }} MXN</span>
          </div>
          <div class="res-row">
            <span>Cliente</span>
            <span>
              {{ clienteEncontrado
                ? `${clienteEncontrado.nombre} ${clienteEncontrado.apellidos}`
                : `${clienteForm.nombre} ${clienteForm.apellidos}` }}
            </span>
          </div>
          <div class="res-row">
            <span>Método de pago</span>
            <span>{{ metodosPago.find(p => p.value === form.metodo_pago)?.label || '--' }}</span>
          </div>
        </div>
        <div class="res-total">
          <span>Total</span>
          <span class="total-value">${{ total.toLocaleString('es-MX') }} MXN</span>
        </div>
      </div>

      <button
        class="btn-confirmar"
        :disabled="!form.metodo_pago || confirmando"
        @click="handleConfirmar">
        {{ confirmando ? 'Procesando reservación...' : 'Aceptar Reservación' }}
      </button>
    </section>

  </div>
</template>
<script setup lang="ts">
 import { ref, reactive, computed } from 'vue'
 import { useAuthStore } from '../../stores/auth'
 import { useNotification } from '../../composables/useNotification'
 import IconPeople from '../svg/IconPeople.vue'
 import IconBed from '../svg/IconBed.vue'
 import IconShower from '../svg/IconShower.vue'
 import IconWater from '../svg/IconWater.vue'
 import IconLight from '../svg/IconLight.vue'
 
 import { useFestivalDates } from '../../composables/useFestivalDates'

 const auth = useAuthStore()
 const { show } = useNotification()

 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
 const API = import.meta.env.VITE_API_URL || null

 //Rol del admin
 const isStaff = computed(() => !!(auth.user?.is_staff && !(auth.user as any)?.is_superuser))
 const parqueAsignado = computed<number | null>(() => (auth.user as any)?.parque_asignado ?? null)

 const { FECHA_MIN, FECHA_MAX, dateErrorInicio, dateErrorFin, checkInicio, checkFin } = useFestivalDates()
 
 function onFechaInicioChange() {
   if (!checkInicio(form.fecha_inicio))
     form.fecha_inicio = ''
   // Re-valida fin si ya tenía valor
   if (form.fecha_fin && !checkFin(form.fecha_fin)) form.fecha_fin = ''
   selectedHospedaje.value = null
 }
 
 function onFechaFinChange() {
   if (!checkFin(form.fecha_fin)) form.fecha_fin = ''
   selectedHospedaje.value = null
 }
 
 //Tipos
 interface Parque { id: number; nombre: string; activo: boolean }
 interface Hospedaje {
   id: number;
   parque_id: number;
   tipo: 'CABANA' | 'CAMPING'
   categoria: 'INDIVIDUAL' | 'PAREJA' | 'FAMILIAR';
   capacidad: number
   estado: string;
   num_camas: number | null;
   num_banos: number | null
   tiene_agua: boolean;
   tiene_luz: boolean;
   tiene_regadera: boolean
   descripcion: string | null;
   precio: number
 }
 
 interface ClienteMock {
   id: number;
   nombre: string;
   apellidos: string;
   email: string;
   rol: 'CLIENTE' | 'ADMIN'
 }
 //Mock data
 const MOCK_PARQUES: Parque[] = [
   { id: 1, nombre: 'Parque Sierra Chincua', activo: true },
   { id: 2, nombre: 'Parque Piedra Herrada', activo: true },
   { id: 3, nombre: 'Parque El Rosario', activo: true },
 ]
 const MOCK_HOSPEDAJES: Hospedaje[] = [
   { id:1,  parque_id:1, tipo:'CABANA',  categoria:'FAMILIAR',   capacidad:8, estado:'DISPONIBLE', num_camas:4, num_banos:2, tiene_agua:true,  tiene_luz:true,  tiene_regadera:true,  descripcion:'Cabaña familiar con vista al bosque y chimenea interior', precio:1800 },
   { id:2,  parque_id:1, tipo:'CABANA',  categoria:'PAREJA',     capacidad:2, estado:'DISPONIBLE', num_camas:1, num_banos:1, tiene_agua:true,  tiene_luz:true,  tiene_regadera:true,  descripcion:'Cabaña íntima con terraza privada',                        precio:900  },
   { id:3,  parque_id:1, tipo:'CABANA',  categoria:'INDIVIDUAL', capacidad:1, estado:'DISPONIBLE', num_camas:1, num_banos:1, tiene_agua:true,  tiene_luz:true,  tiene_regadera:false, descripcion:'Cabaña individual compacta',                               precio:500  },
   { id:4,  parque_id:1, tipo:'CAMPING', categoria:'INDIVIDUAL', capacidad:2, estado:'DISPONIBLE', num_camas:null, num_banos:null, tiene_agua:false, tiene_luz:false, tiene_regadera:false, descripcion:'Zona de camping con vista al claro del bosque',      precio:250  },
   { id:5,  parque_id:1, tipo:'CAMPING', categoria:'FAMILIAR',   capacidad:6, estado:'DISPONIBLE', num_camas:null, num_banos:null, tiene_agua:true,  tiene_luz:false, tiene_regadera:false, descripcion:'Zona de camping familiar con punto de agua cercano', precio:600  },
   { id:6,  parque_id:2, tipo:'CABANA',  categoria:'FAMILIAR',   capacidad:6, estado:'DISPONIBLE', num_camas:3, num_banos:2, tiene_agua:true,  tiene_luz:true,  tiene_regadera:true,  descripcion:'Cabaña familiar a orillas del río',                        precio:1500 },
   { id:7,  parque_id:2, tipo:'CABANA',  categoria:'PAREJA',     capacidad:2, estado:'DISPONIBLE', num_camas:1, num_banos:1, tiene_agua:true,  tiene_luz:true,  tiene_regadera:true,  descripcion:'Cabaña romántica con deck exterior',                       precio:1100 },
   { id:8,  parque_id:2, tipo:'CAMPING', categoria:'PAREJA',     capacidad:2, estado:'DISPONIBLE', num_camas:null, num_banos:null, tiene_agua:false, tiene_luz:false, tiene_regadera:false, descripcion:'Zona de camping para parejas junto al sendero',     precio:350  },
   { id:9,  parque_id:3, tipo:'CABANA',  categoria:'FAMILIAR',   capacidad:10, estado:'DISPONIBLE', num_camas:5, num_banos:3, tiene_agua:true, tiene_luz:true, tiene_regadera:true, descripcion:'Gran cabaña familiar con múltiples áreas comunes',         precio:2500 },
   { id:10, parque_id:3, tipo:'CAMPING', categoria:'FAMILIAR',   capacidad:8, estado:'DISPONIBLE', num_camas:null, num_banos:null, tiene_agua:true, tiene_luz:true, tiene_regadera:false, descripcion:'Zona de camping con servicios básicos',               precio:700  },
 ]
 // Reservaciones activas para checar disponibilidad
 const MOCK_RESERVACIONES = [
   { hospedaje_id:1, fecha_inicio:'2026-06-01', fecha_fin:'2026-06-05', estado:'ACTIVA'   },
   { hospedaje_id:6, fecha_inicio:'2026-06-10', fecha_fin:'2026-06-15', estado:'ACTIVA'   },
   { hospedaje_id:2, fecha_inicio:'2026-07-01', fecha_fin:'2026-07-07', estado:'EN_PROCESO'},
 ]
 const MOCK_USUARIOS: ClienteMock[] = [
   { id:1, nombre:'Fulanito',  apellidos:'Pérez',   email:'fulanito@example.com', rol:'ADMIN' },
   { id:2, nombre:'Ana',       apellidos:'García',  email:'ana@example.com', rol:'CLIENTE' },
   { id:3, nombre:'Carlos',    apellidos:'López',   email:'carlos@example.com', rol:'CLIENTE' },
 ]

 const form = reactive({
   parque_id:  isStaff.value && parqueAsignado.value ? parqueAsignado.value : ('' as number | ''),
   tipo: 'CABANA' as 'CABANA' | 'CAMPING',
   fecha_inicio: '',
   fecha_fin: '',
   num_personas: 1,
   metodo_pago: '',
 })

 const clienteForm = reactive({ email: '', nombre: '', apellidos: '' })

 const selectedHospedaje = ref<Hospedaje | null>(null)
 const clienteEncontrado = ref<ClienteMock | null>(null)
 const clienteBuscado = ref(false)
 const buscandoCliente = ref(false)
 const confirmando = ref(false)

 //Catalogos
 const categoriaLabel: Record<string, string> = {
   INDIVIDUAL: 'Individual', PAREJA: 'Pareja', FAMILIAR: 'Familiar',
 }

 const metodosPago = [
   { value: 'CREDITO',  label: 'Crédito' },
   { value: 'DEBITO',   label: 'Débito'  },
   { value: 'EFECTIVO', label: 'Efectivo'},
 ]

 //Computed
 const parquesDisponibles = computed<Parque[]>(() => {
   if (isStaff.value && parqueAsignado.value)
     return MOCK_PARQUES.filter(p => p.id === parqueAsignado.value)
   return MOCK_PARQUES.filter(p => p.activo)
 })

 const parqueSeleccionado = computed<Parque | null>(() =>
   MOCK_PARQUES.find(p => p.id === Number(form.parque_id)) ?? null
 )

 const canShowHospedajes = computed<boolean>(() =>
   !!form.parque_id && !!form.fecha_inicio && !!form.fecha_fin && form.fecha_inicio < form.fecha_fin && form.num_personas >= 1
 )

 const hospedajesFiltrados = computed<Hospedaje[]>(() => {
   if (!canShowHospedajes.value) return []

   return MOCK_HOSPEDAJES.filter(h => {
     if (h.parque_id !== Number(form.parque_id))
       return false
     if (h.tipo !== form.tipo)
       return false
     if (h.capacidad < form.num_personas)
       return false
     if (h.estado === 'MANTENIMIENTO')
       return false

     // Chequeo de solapamiento de fechas
     const ocupado = MOCK_RESERVACIONES.some(r => {
       if (r.hospedaje_id !== h.id)
	 return false
       if (r.estado === 'CANCELADA')
	 return false
       // Overlap: rInicio < formFin && rFin > formInicio
       return r.fecha_inicio < form.fecha_fin && r.fecha_fin > form.fecha_inicio
     })
     return !ocupado
   })
 })

 const totalNights = computed<number>(() => {
   if (!form.fecha_inicio || !form.fecha_fin) return 0
   const diff = new Date(form.fecha_fin).getTime() - new Date(form.fecha_inicio).getTime()
   return Math.max(0, Math.round(diff / 86_400_000))
 })

 const total = computed<number>(() =>
   selectedHospedaje.value ? selectedHospedaje.value.precio * totalNights.value : 0
 )

 const clienteCompleto = computed<boolean>(() => {
   if (!selectedHospedaje.value || !clienteBuscado.value)
     return false
   if (clienteEncontrado.value)
     return true
   return !!(clienteForm.nombre && clienteForm.apellidos && clienteForm.email)
 })

 //Funciones
 function setTipo(t: 'CABANA' | 'CAMPING') {
   form.tipo = t
   selectedHospedaje.value = null
 }

 function onParqueChange() {
   selectedHospedaje.value = null
   resetCliente()
 }

 function selectHospedaje(h: Hospedaje) {
   selectedHospedaje.value = h
   resetCliente()
 }
 
 function resetCliente() {
   clienteEncontrado.value = null
   clienteBuscado.value = false
   clienteError.value = ''
   clienteForm.email = ''
   clienteForm.nombre = ''
   clienteForm.apellidos = ''
 }

 const clienteError = ref('')
 
 async function buscarCliente() {
   if (!clienteForm.email) return
   buscandoCliente.value = true
   clienteError.value = ''

   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 450))
     const found = MOCK_USUARIOS.find(
       u => u.email.toLowerCase() === clienteForm.email.toLowerCase()
     )

     if (found && found.rol === 'ADMIN') {
       clienteError.value = 'No se puede hacer una reservación a una cuenta de administrador.'
       clienteEncontrado.value = null
       clienteBuscado.value    = false
       buscandoCliente.value   = false
       return
     }
     
     clienteEncontrado.value = found ?? null
     clienteBuscado.value = true
     buscandoCliente.value = false
     return
   }

   // TODO backend: GET /api/usuarios/?email={email}
   // try {
   //   const res = await fetch(
   //     `${API}/api/usuarios/?email=${encodeURIComponent(clienteForm.email)}`,
   //     { headers: { Authorization: `Bearer ${auth.token}` } }
   //   )
   //   if (res.ok) {
   //     const data = await res.json()
   //     clienteEncontrado.value = data.results?.[0] ?? null
   //   }
   // } catch {}
   clienteBuscado.value  = true
   buscandoCliente.value = false
 }

 async function handleConfirmar() {
   if (!form.metodo_pago || !selectedHospedaje.value) return
   confirmando.value = true

   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 900))
     const esNuevo = !clienteEncontrado.value
     show('exito',
	  `Reservación creada exitosamente.${esNuevo
        ? ' Se envió el correo de bienvenida al nuevo cliente.'
        : ''}`
     )
     resetForm()
     confirmando.value = false
     return
   }

   // TODO backend: POST /api/reservaciones/admin/
   // Payload incluye:
   //   parque_id, hospedaje_id, fecha_inicio, fecha_fin,
   //   tipo_visita, num_personas, metodo_pago
   //   + usuario_id (cliente existente) O nuevo_usuario { email, nombre, apellidos }
   // El backend envía:
   //   - Correo de bienvenida + contraseña generada si es usuario nuevo
   //   - Correo de confirmación de reservación
   // try {
   //   const body = {
   //     parque_id:    Number(form.parque_id),
   //     hospedaje_id: selectedHospedaje.value.id,
   //     fecha_inicio: form.fecha_inicio,
   //     fecha_fin:    form.fecha_fin,
   //     tipo_visita:  form.tipo,
   //     num_personas: form.num_personas,
   //     metodo_pago:  form.metodo_pago,
   //     ...(clienteEncontrado.value
   //       ? { usuario_id: clienteEncontrado.value.id }
   //       : { nuevo_usuario: { email: clienteForm.email, nombre: clienteForm.nombre, apellidos: clienteForm.apellidos } }
   //     )
   //   }
   //   const res = await fetch(`${API}/api/reservaciones/admin/`, {
   //     method: 'POST',
   //     headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${auth.token}` },
   //     body: JSON.stringify(body)
   //   })
   //   if (!res.ok) throw new Error()
   //   show('exito', 'Reservación creada exitosamente')
   //   resetForm()
   // } catch {
   //   show('error', 'Error al crear la reservación. Intenta de nuevo')
   // }

   confirmando.value = false
 }

 function resetForm() {
   if (!isStaff.value)
     form.parque_id = ''
   form.tipo = 'CABANA'
   form.fecha_inicio = ''
   form.fecha_fin = ''
   form.num_personas = 1
   form.metodo_pago = ''
   selectedHospedaje.value = null
   resetCliente()
 }

 function formatDate(dateStr: string): string {
   if (!dateStr)
     return '-'
   const [y, m, d] = dateStr.split('-')
   const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
   return `${parseInt(d)} ${months[parseInt(m) - 1]} ${y}`
 }
</script>
<style scoped>
 .reserve-form { display: flex; flex-direction: column; gap: 1.5rem; }

 /* Seccion */
 .form-section {
   background: rgba(123,167,212,0.03);
   border: 1px solid rgba(123,167,212,0.12);
   border-radius: 14px;
   padding: 1.5rem;
   display: flex;
   flex-direction: column;
   gap: 1.25rem;
 }

 .section-header { display: flex; align-items: center; gap: 0.75rem; }

 .section-num {
   width: 26px; height: 26px; border-radius: 50%;
   background: var(--color-admin-accent, #7BA7D4);
   color: #0A1525;
   font-size: 12px; font-weight: 700;
   display: flex; align-items: center; justify-content: center;
   flex-shrink: 0;
 }

 .section-title {
   font-size: 15px; font-weight: 600; color: var(--color-bone);
   display: flex; align-items: center; gap: 0.5rem;
 }

 .section-badge {
   font-size: 11px; font-family: var(--font-mono);
   background: rgba(123,167,212,0.15);
   color: var(--color-admin-accent, #7BA7D4);
   padding: 2px 8px; border-radius: 999px;
 }

 /* Grids */
 .form-row   { display: grid; grid-template-columns: 1fr 1fr;       gap: 1rem; }
 .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr;   gap: 1rem; }

 @media (max-width: 640px) {
   .form-row, .form-row-3 { grid-template-columns: 1fr; }
 }

 .form-field { display: flex; flex-direction: column; gap: 0.35rem; }

 .form-label {
   font-size: 11px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.08em;
   color: var(--color-bone-mute);
 }

 /* Inputs */
 .form-input, .form-select {
   height: 40px; padding: 0 0.875rem;
   border-radius: 8px; border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone); font-size: 13.5px;
   font-family: var(--font-sans); outline: none;
   transition: border-color 0.2s; width: 100%;
 }
 .form-input:focus, .form-select:focus {
   border-color: rgba(123,167,212,0.4);
 }
 .form-input::placeholder { color: var(--color-bone-mute); }
 .form-select { appearance: none; cursor: pointer; }
 .form-select:disabled { opacity: 0.7; cursor: not-allowed; }
 .field-hint { font-size: 10.5px; color: var(--color-admin-accent, #7BA7D4); opacity: 0.8; }

 /* Tipo selector */
 .tipo-group { display: flex; gap: 0.5rem; }
 .tipo-btn {
   flex: 1; height: 40px; border-radius: 8px;
   border: 1px solid var(--color-border);
   background: transparent; color: var(--color-bone-soft);
   font-size: 13px; cursor: pointer; transition: all 0.15s;
 }
 .tipo-btn:hover { border-color: rgba(123,167,212,0.3); color: var(--color-bone); }
 .tipo-btn.active {
   border-color: var(--color-admin-accent, #7BA7D4);
   background: rgba(123,167,212,0.12);
   color: var(--color-admin-accent, #7BA7D4);
   font-weight: 500;
 }

 /* Hospedajes */
 .empty-state {
   text-align: center; padding: 2rem;
   color: var(--color-bone-mute); font-size: 13px;
   border: 1px dashed rgba(123,167,212,0.15);
   border-radius: 10px;
 }

 .hospedajes-grid {
   display: grid;
   grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
   gap: 0.75rem;
 }

 .hospedaje-card {
   background: rgba(255,255,255,0.02);
   border: 1px solid var(--color-border);
   border-radius: 10px; padding: 1rem;
   cursor: pointer; text-align: left;
   display: flex; flex-direction: column; gap: 0.6rem;
   transition: all 0.15s;
 }
 .hospedaje-card:hover {
   border-color: rgba(123,167,212,0.3);
   background: rgba(123,167,212,0.04);
 }
 .hospedaje-card.selected {
   border-color: var(--color-admin-accent, #7BA7D4);
   background: rgba(123,167,212,0.08);
   box-shadow: 0 0 0 1px rgba(123,167,212,0.2);
 }

 .hosp-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; }
 .hosp-badge {
   font-size: 10.5px; font-weight: 600;
   color: var(--color-admin-accent, #7BA7D4);
   background: rgba(123,167,212,0.12);
   padding: 2px 7px; border-radius: 999px;
 }
 .hosp-precio { font-size: 16px; font-weight: 700; color: var(--color-bone); white-space: nowrap; }
 .precio-unit { font-size: 10px; color: var(--color-bone-mute); font-weight: 400; }

 .hosp-stats { display: flex; flex-wrap: wrap; gap: 0.35rem; }
 .hosp-stats span {
   display: inline-flex;
   align-items: center;
   gap: 0.25rem;
   font-size: 11.5px;
   color: var(--color-bone-soft);
 }
 .hosp-amenidades { display: flex; flex-wrap: wrap; gap: 0.3rem; }
 .amen {
   display: inline-flex;
   align-items: center;
   gap: 0.25rem;
   font-size: 10.5px; color: var(--color-bone-mute);
   background: rgba(255,255,255,0.04);
   padding: 1px 6px; border-radius: 4px;
   border: 1px solid rgba(255,255,255,0.06);
 }

 .hosp-desc { font-size: 11.5px; color: var(--color-bone-mute); line-height: 1.4; margin: 0; }

 /* Busqueda cliente */
 .search-row { display: flex; gap: 0.5rem; }
 .search-row .form-input { flex: 1; }

 .btn-buscar {
   height: 40px; padding: 0 1.25rem; border-radius: 8px;
   border: 1px solid rgba(123,167,212,0.3);
   background: transparent; color: var(--color-admin-accent, #7BA7D4);
   font-size: 13px; white-space: nowrap; cursor: pointer;
   transition: all 0.15s;
 }
 .btn-buscar:hover:not(:disabled) { background: rgba(123,167,212,0.1); }
 .btn-buscar:disabled { opacity: 0.5; cursor: not-allowed; }

 .cliente-found {
   display: flex; align-items: center; gap: 0.75rem;
   padding: 0.875rem 1rem;
   background: rgba(123,216,176,0.06);
   border: 1px solid rgba(123,216,176,0.2);
   border-radius: 10px;
 }
 .found-check {
   width: 28px; height: 28px; border-radius: 50%;
   background: rgba(123,216,176,0.2); color: var(--color-green);
   font-size: 14px; font-weight: 700;
   display: flex; align-items: center; justify-content: center; flex-shrink: 0;
 }
 .cliente-nombre { font-size: 14px; font-weight: 500; color: var(--color-bone); margin: 0; }
 .cliente-correo { font-size: 11.5px; color: var(--color-bone-mute); margin: 0; }

 .cliente-new {
   display: flex; flex-direction: column; gap: 0.875rem;
   padding: 1rem;
   background: rgba(232,255,122,0.03);
   border: 1px solid rgba(232,255,122,0.1);
   border-radius: 10px;
 }
 .new-hint  { font-size: 12.5px; color: var(--color-bone-soft); margin: 0; }
 .pass-hint { font-size: 11.5px; color: var(--color-bone-mute); margin: 0; font-style: italic; }

 /* Metodo de pago */
 .pago-group { display: flex; gap: 0.5rem; }
 .pago-btn {
   flex: 1; height: 40px; border-radius: 8px;
   border: 1px solid var(--color-border);
   background: transparent; color: var(--color-bone-soft);
   font-size: 13px; cursor: pointer; transition: all 0.15s;
 }
 .pago-btn:hover { border-color: rgba(123,167,212,0.3); color: var(--color-bone); }
 .pago-btn.active {
   border-color: var(--color-admin-accent, #7BA7D4);
   background: rgba(123,167,212,0.12);
   color: var(--color-admin-accent, #7BA7D4);
   font-weight: 500;
 }

 /* Resumen */
 .resumen-card {
   background: rgba(255,255,255,0.02);
   border: 1px solid rgba(123,167,212,0.1);
   border-radius: 10px; padding: 1.25rem;
   display: flex; flex-direction: column; gap: 0.5rem;
 }
 .resumen-label {
   font-size: 10.5px; font-family: var(--font-mono);
   text-transform: uppercase; letter-spacing: 0.08em;
   color: var(--color-bone-mute); margin-bottom: 0.25rem;
 }
 .res-rows { display: flex; flex-direction: column; }
 .res-row {
   display: flex; justify-content: space-between;
   align-items: center; padding: 0.3rem 0;
   border-bottom: 1px solid rgba(255,255,255,0.04);
   font-size: 12.5px;
 }
 .res-row:last-child { border-bottom: none; }
 .res-row span:first-child { color: var(--color-bone-mute); }
 .res-row span:last-child  { color: var(--color-bone-soft); text-align: right; }
 .res-total {
   display: flex; justify-content: space-between; align-items: center;
   padding-top: 0.75rem; border-top: 1px solid rgba(123,167,212,0.15);
   margin-top: 0.25rem;
 }
 .res-total > span:first-child { font-size: 14px; font-weight: 600; color: var(--color-bone); }
 .total-value { font-size: 22px; font-weight: 700; color: var(--color-admin-accent, #7BA7D4); }

 /* Boton confirmar */
 .btn-confirmar {
   width: 100%; height: 48px;
   border-radius: var(--radius-full); border: none;
   background: var(--color-admin-accent, #7BA7D4);
   color: #0A1525; font-size: 15px; font-weight: 600;
   font-family: var(--font-sans); cursor: pointer;
   transition: all var(--transition-normal);
   box-shadow: 0 0 20px rgba(123,167,212,0.25);
 }
 .btn-confirmar:hover:not(:disabled) {
   box-shadow: 0 0 30px rgba(123,167,212,0.45);
   transform: translateY(-1px);
 }
 .btn-confirmar:disabled {
   opacity: 0.5; cursor: not-allowed;
   box-shadow: none; transform: none;
 }

 .cliente-error {
   font-size: 12px;
   color: var(--color-danger);
   display: block;
   margin-top: 0.25rem;
 }
 .date-error {
   font-size: 11px;
   color: var(--color-danger);
   line-height: 1.4;
 }
</style>
