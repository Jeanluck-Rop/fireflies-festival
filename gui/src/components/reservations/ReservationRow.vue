<template>
  <div class="reservation-row" :class="{ 'row-cancelada': reservacion.estado === 'CANCELADA' }">

    <!-- 1. Imagenes del hospedaje -->
    <div class="row-media">
      <template v-if="images.length > 0">
        <img
          :src="images[imgIdx]"
          :alt="`${tipoLabel} #${reservacion.hospedaje.id}`"
          class="media-img"
        />
        <!-- Controles carousel -->
        <template v-if="images.length > 1">
          <button class="carousel-btn carousel-prev" @click.stop="prevImg">
            <svg width="7" height="12" viewBox="0 0 7 12" fill="none">
              <path d="M6 1L1 6l5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <button class="carousel-btn carousel-next" @click.stop="nextImg">
            <svg width="7" height="12" viewBox="0 0 7 12" fill="none">
              <path d="M1 1l5 5-5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
          <div class="carousel-dots">
            <span
              v-for="(_, i) in images" :key="i"
              :class="['carousel-dot', i === imgIdx && 'active']"
              @click.stop="imgIdx = i" />
          </div>
        </template>
      </template>
      <!-- Placeholder sin imagenes -->
      <div v-else class="media-placeholder">
        <FireflyLogo :pulse="true" :drift="false" size="w-10 h-10" />
      </div>
    </div>

    <!-- 2. Informacion de la reservacion-->
    <div class="row-info">
      <!-- Cabecera: tipo+id | id reservacion -->
      <div class="info-head">
        <span class="info-reserv-id">#{{ reservacion.id }}</span>
        <h3 class="info-title">
          {{ tipoLabel }}
          <span class="info-hospedaje-num">#{{ reservacion.hospedaje.id }}</span>
        </h3>
        <span class="info-parque">{{ reservacion.parque.nombre }}</span>
      </div>
      <!-- Detalles: fechas + personas -->
      <div class="info-meta">
        <span class="meta-item">
          <IconCalendar size="13px" />
          {{ formatDate(reservacion.fecha_inicio) }}
          <IconArrow size="10px" />
          {{ formatDate(reservacion.fecha_fin) }}
        </span>
        <span class="meta-sep">·</span>
        <span class="meta-item">
          <IconPeople size="13px" />
          {{ reservacion.num_personas }}
          {{ reservacion.num_personas === 1 ? 'persona' : 'personas' }}
        </span>
      </div>
    </div>

    <!-- 3. Estado, precio, acciones -->
    <div class="row-side">
      <!-- Icono de estado grande -->
      <div class="side-icon" :class="estadoClass">
        <IconCompletada v-if="reservacion.estado === 'COMPLETADA'" size="30px" />
        <IconCancelada  v-else-if="reservacion.estado === 'CANCELADA'"  size="30px" />
        <IconEnProceso  v-else-if="reservacion.estado === 'EN_PROCESO'" size="30px" />
        <IconActiva     v-else size="30px" />
      </div>
      <!-- Badge estado -->
      <span class="estado-badge" :class="estadoClass">{{ estadoLabel }}</span>
      <!-- Precio total -->
      <div class="side-precio">
        <template v-if="reservacion.monto != null">
          <span class="precio-num">${{ reservacion.monto.toLocaleString('es-MX') }}</span>
          <span class="precio-cur">MXN</span>
        </template>
        <span v-else class="precio-pending">— —</span>
      </div>
      <!-- Botones -->
      <div class="side-btns">
        <button class="btn-detalles" @click="showInfo = true">
          <IconInfo size="12px" /> Detalles
        </button>
        <button
          v-if="reservacion.estado === 'ACTIVA' || reservacion.estado === 'EN_PROCESO'"
          class="btn-cancelar"
          :disabled="cancelando"
          @click="showCancel = true">
          Cancelar
        </button>
      </div>
    </div>

    <!-- Dialogo: Detalles -->
    <transition name="dialog-fade">
      <div v-if="showInfo" class="dialog-backdrop" @click.self="showInfo = false">
        <div class="dialog-box dialog-info-box">

          <!-- Header con X -->
          <div class="dialog-info-header">
            <h3 class="dialog-title">Reservación #{{ reservacion.id }}</h3>
            <button class="dialog-close" @click="showInfo = false">
              <svg width="12" height="12" viewBox="0 0 10 10" fill="none">
                <path d="M1 1l8 8M9 1l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Badge de estado -->
          <span class="estado-badge info-estado" :class="estadoClass">
            <IconCompletada v-if="reservacion.estado === 'COMPLETADA'"    size="13px" />
            <IconCancelada  v-else-if="reservacion.estado === 'CANCELADA'" size="13px" />
            <IconEnProceso  v-else-if="reservacion.estado === 'EN_PROCESO'" size="13px" />
            <IconActiva     v-else-if="reservacion.estado === 'ACTIVA'"    size="13px" />
            {{ estadoLabel }}
          </span>

          <!-- Datos -->
          <div class="info-grid">
            <div class="info-row">
              <span class="info-label">Parque</span>
              <span class="info-value">{{ reservacion.parque.nombre }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Hospedaje</span>
              <span class="info-value">{{ reservacion.hospedaje.nombre }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Tipo de visita</span>
              <span class="info-value">{{ tipoLabel }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Fecha de entrada</span>
              <span class="info-value">{{ formatDate(reservacion.fecha_inicio) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Fecha de salida</span>
              <span class="info-value">{{ formatDate(reservacion.fecha_fin) }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Personas</span>
              <span class="info-value">{{ reservacion.num_personas }}</span>
            </div>
	    <div class="info-row">
	      <span class="info-label">Total</span>
	      <span class="info-value" style="font-weight: 600;">
		{{ reservacion.monto != null
		? `$${reservacion.monto.toLocaleString('es-MX')} MXN`
		: 'Por confirmar' }}
	      </span>
	    </div>
	    <div class="info-row">
              <span class="info-label">Fecha de creación</span>
              <span class="info-value">{{ formatCreatedAt(reservacion.created_at) }}</span>
            </div>
          </div>

        </div>
      </div>
    </transition>
    
    <!-- Dialogo de cancelacion -->
    <AppConfirmDialog
      v-model="showCancel"
      title="Cancelar Reservación"
      confirm-label="Confirmar cancelación"
      loading-label="Cancelando..."
      :loading="cancelando"
      variant="danger"
      @confirm="confirmarCancelacion">
      ¿Estás seguro de cancelar la reservación <strong>#{{ reservacion.id }}</strong>
      en <strong>{{ reservacion.parque.nombre }}</strong>?
      Ten en cuenta que este proceso es irreversible.
    </AppConfirmDialog>
    
  </div>
</template>

<script setup lang="ts">
 import { ref, computed } from 'vue'
 import type { Reservacion } from '../../stores/reservations'
 import FireflyLogo    from '../ui/FireflyLogo.vue'
 import IconDot from '../svg/IconDot.vue'
 import IconInfo from '../svg/IconInfo.vue'
 import IconHome from '../svg/IconHome.vue'
 import IconArrow from '../svg/IconArrow.vue'
 import IconActiva from '../svg/IconActiva.vue'
 import IconPeople from '../svg/IconPeople.vue'
 import IconCalendar from '../svg/IconCalendar.vue'
 import IconCancelada from '../svg/IconCancelada.vue'
 import IconEnProceso from '../svg/IconEnProceso.vue'
 import IconCompletada from '../svg/IconCompletada.vue'
 import AppConfirmDialog from '../ui/AppConfirmDialog.vue'

 const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
 const API = import.meta.env.VITE_API_URL || null
 
 const props = defineProps<{
   reservacion: Reservacion
   cancelando?: boolean
 }>()

 const emit = defineEmits<{ cancelar: [reservacion: Reservacion] }>()

 //Caroussel
 const images = computed(() => props.reservacion.hospedaje.imagenes ?? [])
 const imgIdx = ref(0)
 function prevImg() { imgIdx.value = (imgIdx.value - 1 + images.value.length) % images.value.length }
 function nextImg() { imgIdx.value = (imgIdx.value + 1) % images.value.length }
 
 const showInfo = ref(false)
 const showCancel = ref(false)
 
 //Tipo de visita
 const tipoLabel = computed(() =>
   props.reservacion.tipo_visita === 'CABANA' ? 'Cabaña' : 'Camping'
 )

 //Estado
 const estadoMap: Record<string, { label: string; cls: string }> = {
   ACTIVA: { label: 'Activa', cls: 'estado-activa' },
   EN_PROCESO: { label: 'En proceso', cls: 'estado-proceso' },
   COMPLETADA: { label: 'Completada', cls: 'estado-completada' },
   CANCELADA: { label: 'Cancelada', cls: 'estado-cancelada' },
 }

 const estadoLabel = computed(() => estadoMap[props.reservacion.estado]?.label ?? props.reservacion.estado)
 const estadoClass = computed(() => estadoMap[props.reservacion.estado]?.cls ?? '')

 //Confirmar cancelacion
 async function confirmarCancelacion() {
   if (USE_MOCK) {
     showCancel.value = false
     emit('cancelar', props.reservacion)
     return
   }
   // TODO backend: PATCH /api/reservaciones/:id/cancelar/
 }
 
 //Fechas
 function formatDate(dateStr: string): string {
   const [y, m, d] = dateStr.split('-')
   const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
   return `${parseInt(d)} ${months[parseInt(m) - 1]} ${y}`
 }

 function formatCreatedAt(dateStr: string): string {
   const d = new Date(dateStr)
   return `Creada el ${formatDate(d.toISOString().split('T')[0])}`
 }
</script>

<style scoped>
 /* Row */
 .reservation-row {
   display: flex;
   align-items: stretch;
   border-radius: 14px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.02);
   overflow: hidden;
   min-height: 160px;
   transition: border-color 0.2s, background 0.2s;
 }
 .reservation-row:hover {
   background: rgba(255,255,255,0.035);
   border-color: rgba(255,255,255,0.13);
 }
 .row-cancelada { opacity: 0.65; }

 /* 1. Media / Carousel */
 .row-media {
   flex-shrink: 0;
   width: 190px;
   position: relative;
   overflow: hidden;
   background: rgba(255,255,255,0.015);
 }
 .media-img {
   width: 100%;
   height: 100%;
   object-fit: cover;
   display: block;
 }

 /* Placeholder sin imágenes */
 .media-placeholder {
   width: 100%;
   height: 100%;
   display: flex;
   align-items: center;
   justify-content: center;
   background:
     radial-gradient(ellipse at 50% 80%, rgba(123,216,176,0.06) 0%, transparent 70%),
     rgba(255,255,255,0.01);
 }

 /* Controles carousel */
 .carousel-btn {
   position: absolute;
   top: 50%;
   transform: translateY(-50%);
   width: 28px; height: 28px; border-radius: 50%;
   background: rgba(0,0,0,0.55);
   border: 1px solid rgba(255,255,255,0.12);
   color: rgba(255,255,255,0.85);
   cursor: pointer;
   display: flex; align-items: center; justify-content: center;
   transition: background 0.15s;
   z-index: 2;
 }
 .carousel-btn:hover { background: rgba(0,0,0,0.75); }
 .carousel-prev { left: 6px; }
 .carousel-next { right: 6px; }

 .carousel-dots {
   position: absolute;
   bottom: 8px;
   left: 50%;
   transform: translateX(-50%);
   display: flex;
   gap: 4px;
   z-index: 2;
 }
 .carousel-dot {
   width: 5px; height: 5px; border-radius: 50%;
   background: rgba(255,255,255,0.35);
   cursor: pointer; transition: background 0.2s;
 }
 .carousel-dot.active { background: rgba(255,255,255,0.9); }

 /* 2. Info */
 .row-info {
   flex: 1;
   min-width: 0;
   padding: 1.25rem 1.5rem;
   display: flex;
   flex-direction: column;
   justify-content: space-between;
   gap: 0.75rem;
 }

 .info-head {
   display: flex;
   flex-direction: column;
   gap: 0.25rem;
 }
 .info-reserv-id {
   font-size: 10.5px;
   font-family: var(--font-mono);
   color: var(--color-bone-mute);
   letter-spacing: 0.06em;
 }
 .info-title {
   font-family: var(--font-serif);
   font-size: 28px;
   font-weight: 400;
   color: var(--color-bone);
   line-height: 1.1;
   letter-spacing: -0.01em;
 }
 .info-hospedaje-num {
   font-family: var(--font-mono);
   font-size: 22px;
   color: var(--color-bone-mute);
   font-weight: 400;
 }
 .info-parque {
   font-size: 16px;
   font-family: var(--font-mono);
   text-transform: uppercase;
   letter-spacing: 0.12em;
   color: var(--color-accent);
   opacity: 0.8;
 }

 .info-meta {
   display: flex;
   align-items: center;
   flex-wrap: wrap;
   gap: 0.4rem;
 }
 .meta-item {
   display: inline-flex;
   align-items: center;
   gap: 0.3rem;
   font-size: 14px;
   color: var(--color-bone-soft);
 }
 .meta-sep {
   color: var(--color-bone-mute);
   font-size: 11px;
 }

 /* 3. Side: estado + precio + acciones */
 .row-side {
   flex-shrink: 0;
   width: 165px;
   padding: 1.25rem 1rem;
   border-left: 1px solid var(--color-border);
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: space-between;
   gap: 0.5rem;
 }

 /* Icono de estado grande */
 .side-icon { display: flex; align-items: center; justify-content: center; }
 .side-icon.estado-activa     { color: var(--color-green); }
 .side-icon.estado-proceso    { color: var(--color-accent); }
 .side-icon.estado-completada { color: var(--color-bone-soft); }
 .side-icon.estado-cancelada  { color: var(--color-danger); }

 /* Badge estado */
 .estado-badge {
   display: inline-flex;
   align-items: center;
   gap: 0.3rem;
   padding: 0.2rem 0.65rem;
   border-radius: 999px;
   font-size: 10.5px;
   font-weight: 600;
   letter-spacing: 0.03em;
 }
 .estado-activa     { background: rgba(123,216,176,0.12); color: var(--color-green); }
 .estado-proceso    { background: rgba(232,255,122,0.10); color: var(--color-accent); }
 .estado-completada { background: rgba(255,255,255,0.06); color: var(--color-bone-soft); }
 .estado-cancelada  { background: rgba(255,138,123,0.10); color: var(--color-danger); }

 /* Precio */
 .side-precio {
   display: flex;
   flex-direction: column;
   align-items: center;
   line-height: 1;
 }
 .precio-num {
   font-size: 24px;
   font-weight: 700;
   color: var(--color-bone);
   letter-spacing: -0.03em;
 }
 .precio-cur {
   font-size: 9px;
   font-family: var(--font-mono);
   text-transform: uppercase;
   letter-spacing: 0.12em;
   color: var(--color-bone-mute);
   margin-top: 2px;
 }
 .precio-pending {
   font-size: 14px;
   color: var(--color-bone-mute);
   letter-spacing: 0.05em;
 }

 /* Botones */
 .side-btns { display: flex; flex-direction: column; gap: 0.35rem; width: 100%; }

 .btn-detalles {
   width: 100%; height: 32px; border-radius: 999px;
   border: 1px solid var(--color-border);
   background: transparent; color: var(--color-bone-soft);
   font-size: 11.5px; font-family: var(--font-sans);
   cursor: pointer; transition: all 0.15s;
   display: flex; align-items: center; justify-content: center; gap: 0.35rem;
 }
 .btn-detalles:hover {
   background: rgba(255,255,255,0.06);
   color: var(--color-bone);
   border-color: rgba(255,255,255,0.15);
 }

 .btn-cancelar {
   width: 100%; height: 32px; border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.3);
   background: transparent; color: var(--color-danger);
   font-size: 11.5px; font-family: var(--font-sans);
   cursor: pointer; transition: all 0.15s;
 }
 .btn-cancelar:hover { background: rgba(255,138,123,0.08); }
 .btn-cancelar:disabled { opacity: 0.35; cursor: not-allowed; }

 /* Dialogos */
 .dialog-backdrop {
   position: fixed; inset: 0; z-index: 9999;
   background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
   display: flex; align-items: center; justify-content: center; padding: 1rem;
 }
 .dialog-box {
   background: #0d1a10;
   border: 1px solid rgba(123,216,176,0.15);
   border-radius: 16px; padding: 1.75rem;
   width: 100%; max-width: 420px;
   box-shadow: 0 24px 48px rgba(0,0,0,0.5);
   display: flex; flex-direction: column; gap: 1rem;
 }
 .dialog-info-box { max-width: 480px; }

 .dialog-header { display: flex; align-items: center; justify-content: space-between; }
 .dialog-title  { font-size: 18px; font-weight: 600; color: var(--color-bone); }
 .dialog-close  {
   width: 28px; height: 28px; border-radius: 8px;
   border: 1px solid var(--color-border); background: transparent;
   color: var(--color-bone-soft); cursor: pointer;
   display: flex; align-items: center; justify-content: center; transition: all 0.2s;
 }
 .dialog-close:hover { background: rgba(255,255,255,0.06); color: var(--color-bone); }

 .info-estado { align-self: flex-start; }

 .info-grid { display: flex; flex-direction: column; }
 .info-row {
   display: flex; justify-content: space-between;
   align-items: baseline; gap: 1rem;
   padding: 0.4rem 0;
   border-bottom: 1px solid rgba(255,255,255,0.04);
 }
 .info-row:last-child { border-bottom: none; }
 .info-label {
   font-size: 11px; color: var(--color-bone-mute);
   font-family: var(--font-mono); text-transform: uppercase;
   letter-spacing: 0.06em; flex-shrink: 0;
 }
 .info-value { font-size: 13px; color: var(--color-bone); text-align: right; }

 /* Animaciones dialogo */
 .dialog-fade-enter-active, .dialog-fade-leave-active { transition: opacity 0.2s ease; }
 .dialog-fade-enter-active .dialog-box,
 .dialog-fade-leave-active .dialog-box { transition: transform 0.2s ease, opacity 0.2s ease; }
 .dialog-fade-enter-from, .dialog-fade-leave-to { opacity: 0; }
 .dialog-fade-enter-from .dialog-box,
 .dialog-fade-leave-to   .dialog-box { transform: scale(0.96) translateY(8px); opacity: 0; }
</style>
