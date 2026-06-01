<template>
  <div class="reservation-row">

    <!-- Imagen del parque -->
    <div class="row-image" :class="estadoClass">
      <IconCompletada v-if="reservacion.estado === 'COMPLETADA'" size="22px" />
      <IconCancelada v-else-if="reservacion.estado === 'CANCELADA'"  size="22px" />
      <IconEnProceso v-else-if="reservacion.estado === 'EN_PROCESO'" size="22px" />
      <IconActiva v-else size="22px" />
    </div>

    <!-- Info principal -->
    <div class="row-main">
      <div class="row-top">
        <span class="row-id">#{{ reservacion.id }}</span>
        <h3 class="row-parque">{{ reservacion.parque.nombre }}</h3>
      </div>
      <div class="row-meta">
        <span class="meta-item">
          <!-- Icono calendario -->
          <IconCalendar />
          {{ formatDate(reservacion.fecha_inicio) }}
          <!-- Flecha SVG entre fechas -->
          <IconArrow />
          {{ formatDate(reservacion.fecha_fin) }}
        </span>
	<IconDot class="meta-sep" />
        <span class="meta-item">
          <!-- Icono personas -->
          <IconPeople />
          {{ reservacion.num_personas }} {{ reservacion.num_personas === 1 ? 'persona' : 'personas' }}
        </span>
	<IconDot class="meta-sep" />
        <span class="meta-item">
          <!-- Icono tipo visita -->
          <IconHome v-if="reservacion.tipo_visita === 'CABANA'" />
	  <IconEnProceso v-else size="12px" />
          {{ tipoLabel }}
        </span>
	<IconDot class="meta-sep" />
        <span class="meta-item meta-hospedaje">
          {{ reservacion.hospedaje.nombre }}
        </span>
      </div>
    </div>

    <!-- Monto -->
    <div class="row-precio">
      <template v-if="reservacion.monto != null">
	<span class="precio-value">${{ reservacion.monto.toLocaleString('es-MX') }}</span>
	<span class="precio-label">MXN</span>
      </template>
      <span v-else class="precio-pending">— —</span>
    </div>

    <!-- Estado -->
    <div class="row-estado">
      <span class="estado-badge" :class="estadoClass">
	<IconCompletada v-if="reservacion.estado === 'COMPLETADA'" size="13px" />
	<IconCancelada v-else-if="reservacion.estado === 'CANCELADA'" size="13px" />
	<IconEnProceso v-else-if="reservacion.estado === 'EN_PROCESO'" size="13px" />
	<IconActiva v-else-if="reservacion.estado === 'ACTIVA'" size="13px" />
	{{ estadoLabel }}
      </span>
      <span class="row-date">{{ formatCreatedAt(reservacion.created_at) }}</span>
    </div>

    <!-- Acciones -->
    <div class="row-actions">
      <!-- Ver detalles -->
      <button class="action-btn" title="Ver detalles" @click="showInfo = true">
        <IconInfo />
      </button>
      <button
        v-if="reservacion.estado === 'ACTIVA' || reservacion.estado === 'EN_PROCESO'"
        class="action-btn action-cancel-btn"
        :disabled="cancelando"
        @click="showCancel= true">
        Cancelar
      </button>
    </div>

    <!-- Dialogo: Informacion -->
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

 const emit = defineEmits<{
   cancelar: [reservacion: Reservacion]
 }>()

 const showInfo = ref(false)
 const showCancel = ref(false)
 
 //Tipo de visita
 const tipoLabel = computed(() =>
   props.reservacion.tipo_visita === 'CABANA' ? 'Cabaña' : 'Camping'
 )

 //Estado
 const estadoMap: Record<string, { label: string; cls: string }> = {
   ACTIVA:     { label: 'Activa',      cls: 'estado-activa' },
   EN_PROCESO: { label: 'En proceso',  cls: 'estado-proceso' },
   COMPLETADA: { label: 'Completada',  cls: 'estado-completada' },
   CANCELADA:  { label: 'Cancelada',   cls: 'estado-cancelada' },
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
   // try {
   //   const res = await fetch(`${API}/api/reservaciones/${props.reservacion.id}/cancelar/`, {
   //     method: 'PATCH',
   //     headers: { Authorization: `Bearer ${useAuthStore().token}` }
   //   })
   //   if (!res.ok) throw new Error('No se pudo cancelar')
   //   showDialog.value = false
   //   emit('cancelar', props.reservacion)
   // } catch (e) {
   //   console.error(e)
   // }
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
 .reservation-row {
   display: flex;
   align-items: center;
   gap: 1rem;
   padding: 0.9rem 1rem;
   border-radius: 12px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.02);
   transition: background 0.15s, border-color 0.15s;
 }
 .reservation-row:hover {
   background: rgba(255,255,255,0.04);
   border-color: rgba(255,255,255,0.12);
 }

 /* Imagen */
 .row-image {
   flex-shrink: 0;
   width: 52px;
   height: 52px;
   border-radius: 8px;
   border: 1px solid var(--color-border);
   display: flex;
   align-items: center;
   justify-content: center;
 }
 /* Color del icono según estado */
 .row-image.estado-activa    { background: rgba(123,216,176,0.08); color: var(--color-green) }
 .row-image.estado-proceso   { background: rgba(232,255,122,0.08); color: var(--color-accent) }
 .row-image.estado-completada{ background: rgba(255,255,255,0.04); color: var(--color-bone-soft) }
 .row-image.estado-cancelada { background: rgba(255,138,123,0.08); color: var(--color-danger) }

 /* Info principal */
 .row-main {
   flex: 1;
   min-width: 0;
   display: flex;
   flex-direction: column;
   gap: 0.3rem;
 }
 .row-top {
   display: flex;
   align-items: center;
   gap: 0.5rem;
 }
 .row-id {
   font-size: 11px;
   color: var(--color-bone-mute);
   font-family: var(--font-mono);
   flex-shrink: 0;
 }
 .row-parque {
   font-size: 14px;
   font-weight: 600;
   color: var(--color-bone);
   white-space: nowrap;
   overflow: hidden;
   text-overflow: ellipsis;
 }
 .row-meta {
   display: flex;
   align-items: center;
   flex-wrap: wrap;
   gap: 0.35rem;
 }
 .meta-item {
   display: inline-flex;
   align-items: center;
   gap: 0.3rem;
   font-size: 11.5px;
   color: var(--color-bone-soft);
 }
 .meta-hospedaje {
   color: var(--color-bone-mute);
 }
 .meta-sep {
   font-size: 11px;
   color: var(--color-bone-mute);
 }

 /* Precio */
 .row-precio {
   flex-shrink: 0;
   text-align: right;
   min-width: 70px;
 }
 .precio-value {
   font-size: 15px;
   font-weight: 600;
   color: var(--color-bone);
   display: block;
 }
 .precio-label {
   font-size: 10px;
   color: var(--color-bone-mute);
   font-family: var(--font-mono);
 }
 .precio-pending {
   font-size: 13px;
   color: var(--color-bone-mute);
   letter-spacing: 0.05em;
 }

 /* Estado */
 .row-estado {
   flex-shrink: 0;
   display: flex;
   flex-direction: column;
   align-items: flex-end;
   gap: 0.3rem;
   min-width: 100px;
 }
 .estado-badge {
   display: inline-flex;
   align-items: center;
   gap: 0.35rem;
   padding: 0.2rem 0.6rem;
   border-radius: 999px;
   font-size: 11px;
   font-weight: 600;
   letter-spacing: 0.03em;
 }
 .estado-activa {
   background: rgba(123,216,176,0.12);
   color: var(--color-green);
 }
 .estado-proceso {
   background: rgba(232,255,122,0.1);
   color: var(--color-accent);
 }
 .estado-completada {
   background: rgba(255,255,255,0.06);
   color: var(--color-bone-soft);
 }
 .estado-cancelada {
   background: rgba(255,138,123,0.1);
   color: var(--color-danger);
 }
 .row-date {
   font-size: 10.5px;
   color: var(--color-bone-mute);
   white-space: nowrap;
 }

 /* Acciones */
 .row-actions { flex-shrink: 0; display: flex; align-items: center; gap: 0.4rem; }

 .action-btn {
   width: 30px; height: 30px; border-radius: 8px;
   border: 1px solid var(--color-border);
   background: transparent; color: var(--color-bone-soft);
   cursor: pointer; display: flex; align-items: center; justify-content: center;
   transition: background 0.15s, color 0.15s, border-color 0.15s;
 }
 .action-btn:hover {
   background: rgba(255,255,255,0.06);
   color: var(--color-bone);
   border-color: rgba(255,255,255,0.15);
 }

 .action-cancel-btn {
   height: 30px;
   width: 80px;
   padding: 0 0.75rem;
   border-radius: 8px;
   border: 1px solid rgba(255,138,123,0.3);
   background: transparent;
   color: var(--color-danger);
   font-size: 12px; cursor: pointer;
   transition: background 0.15s, border-color 0.15s;
   white-space: nowrap;
 }
 .action-cancel-btn:hover {
   background: rgba(255,138,123,0.08);
   border-color: rgba(255,138,123,0.5);
 }
 .action-cancel-btn:disabled { opacity: 0.4; cursor: not-allowed; }

 /* Dialogo */
 .dialog-backdrop {
   position: fixed; inset: 0; z-index: 9999;
   background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
   display: flex; align-items: center; justify-content: center;
   padding: 1rem;
 }
 .dialog-box {
   background: #0d1a10;
   border: 1px solid rgba(123,216,176,0.15);
   border-radius: 16px; padding: 1.75rem;
   width: 100%; max-width: 420px;
   box-shadow: 0 24px 48px rgba(0,0,0,0.5);
   display: flex; flex-direction: column; gap: 1rem;
 }
 .dialog-title {
   font-size: 18px; font-weight: 600;
   color: var(--color-bone); letter-spacing: -0.01em;
 }

 /* Dialogo info mas ancho */
 .dialog-info-box { max-width: 480px; }

 .dialog-info-header {
   display: flex; align-items: center;
   justify-content: space-between;
 }
 .dialog-close {
   width: 28px; height: 28px; border-radius: 8px;
   border: 1px solid var(--color-border);
   background: transparent; color: var(--color-bone-soft);
   cursor: pointer; display: flex; align-items: center;
   justify-content: center; transition: color 0.2s, background 0.2s;
 }
 .dialog-close:hover { background: rgba(255,255,255,0.06); color: var(--color-bone); }

 .info-estado { align-self: flex-start; }

 /* Grid de datos */
 .info-grid { display: flex; flex-direction: column; gap: 0.5rem; }
 .info-row {
   display: flex; justify-content: space-between;
   align-items: baseline; gap: 1rem;
   padding: 0.4rem 0;
   border-bottom: 1px solid rgba(255,255,255,0.04);
 }
 .info-row:last-child { border-bottom: none; }
 .info-label {
   font-size: 11.5px; color: var(--color-bone-mute);
   font-family: var(--font-mono); text-transform: uppercase;
   letter-spacing: 0.06em; flex-shrink: 0;
 }
 .info-value {
   font-size: 13px; color: var(--color-bone);
   text-align: right;
 }
 .info-pending { color: var(--color-bone-mute); font-style: italic; }

 /* Animaciones */
 .dialog-fade-enter-active, .dialog-fade-leave-active { transition: opacity 0.2s ease; }
 .dialog-fade-enter-active .dialog-box,
 .dialog-fade-leave-active .dialog-box { transition: transform 0.2s ease, opacity 0.2s ease; }
 .dialog-fade-enter-from, .dialog-fade-leave-to { opacity: 0; }
 .dialog-fade-enter-from .dialog-box,
 .dialog-fade-leave-to   .dialog-box { transform: scale(0.96) translateY(8px); opacity: 0; }
</style>
