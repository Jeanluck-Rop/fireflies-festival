<template>
  <div class="admin-reserv-row">

    <!-- Columna izquierda: info -->
    <div class="row-info">

      <!-- Fila 1: ID + estado -->
      <div class="row-top">
        <span class="reserv-id">#{{ reservacion.id }}</span>
        <span :class="['estado-badge', `estado-${reservacion.estado.toLowerCase().replace('_','-')}`]">
          {{ estadoLabel[reservacion.estado] }}
        </span>
      </div>

      <!-- Fila 2: Nombre · Email en la misma línea -->
      <div class="row-usuario">
        <span class="usuario-nombre">
          {{ reservacion.usuario.nombre }} {{ reservacion.usuario.apellidos }}
        </span>
        <IconDot size="4px" class="sep" />
        <span class="usuario-email">{{ reservacion.usuario.email }}</span>
      </div>

      <!-- Fila 3: fechas → fechas · personas · tipo -->
      <div class="row-meta">
        <span class="meta-fechas">
          {{ formatDate(reservacion.fecha_inicio) }}
          <IconArrow size="10px" />
          {{ formatDate(reservacion.fecha_fin) }}
        </span>
        <IconDot size="4px" class="sep" />
        <span>{{ reservacion.num_personas }} {{ reservacion.num_personas === 1 ? 'persona' : 'personas' }}</span>
        <IconDot size="4px" class="sep" />
        <span>{{ reservacion.tipo_visita === 'CABANA' ? 'Cabaña' : 'Camping' }}</span>
      </div>

    </div>

    <!-- Columna derecha: acción -->
    <button
      v-if="reservacion.estado === 'ACTIVA' || reservacion.estado === 'EN_PROCESO'"
      class="btn-cancel"
      @click="$emit('cancelar', reservacion.id)">
      Cancelar
    </button>

  </div>
</template>

<script setup lang="ts">
 import IconDot   from '../svg/IconDot.vue'
 import IconArrow from '../svg/IconArrow.vue'

 interface Usuario { nombre: string; apellidos: string; email: string }

 interface Reservacion {
   id:           number
   usuario:      Usuario
   hospedaje:    { id: number; tipo: string }
   fecha_inicio: string
   fecha_fin:    string
   num_personas: number
   tipo_visita:  string
   estado:       'ACTIVA' | 'EN_PROCESO' | 'CANCELADA' | 'COMPLETADA'
 }

 defineProps<{ reservacion: Reservacion }>()
 defineEmits<{ cancelar: [id: number] }>()

 const estadoLabel: Record<string, string> = {
   ACTIVA:     'Activa',
   EN_PROCESO: 'En proceso',
   COMPLETADA: 'Completada',
   CANCELADA:  'Cancelada',
 }

 function formatDate(s: string): string {
   const [y, m, d] = s.split('-')
   const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
   return `${parseInt(d)} ${months[parseInt(m) - 1]} ${y}`
 }
</script>

<style scoped>
 .admin-reserv-row {
   display: flex;
   align-items: center;
   justify-content: space-between;
   gap: 1rem;
   padding: 0.875rem 1rem;
   border-radius: 10px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.02);
   transition: background 0.15s;
 }
 .admin-reserv-row:hover { background: rgba(255,255,255,0.03); }

 /* Info */
 .row-info { flex: 1; display: flex; flex-direction: column; gap: 0.3rem; min-width: 0; }

 /* Fila 1: ID + estado */
 .row-top { display: flex; align-items: center; gap: 0.5rem; }
 .reserv-id {
   font-size: 11px;
   color: var(--color-bone-mute);
   font-family: var(--font-mono);
 }

 /* Fila 2: nombre · email */
 .row-usuario {
   display: flex;
   align-items: center;
   gap: 0.4rem;
   flex-wrap: wrap;
 }
 .usuario-nombre {
   font-size: 13.5px;
   font-weight: 500;
   color: var(--color-bone);
   white-space: nowrap;
 }
 .usuario-email {
   font-size: 12px;
   color: var(--color-bone-mute);
   white-space: nowrap;
   overflow: hidden;
   text-overflow: ellipsis;
 }

 /* Fila 3: meta */
 .row-meta {
   display: flex;
   align-items: center;
   gap: 0.4rem;
   flex-wrap: wrap;
   font-size: 11.5px;
   color: var(--color-bone-soft);
 }
 .meta-fechas {
   display: inline-flex;
   align-items: center;
   gap: 0.3rem;
 }

 /* Separador */
 .sep {
   color: var(--color-bone-mute);
   display: flex;
   align-items: center;
   flex-shrink: 0;
 }

 /* Badges de estado */
 .estado-badge {
   font-size: 10px;
   font-weight: 600;
   padding: 2px 8px;
   border-radius: 999px;
 }
 .estado-activa     { background: rgba(123,216,176,0.12); color: var(--color-green); }
 .estado-en-proceso { background: rgba(232,255,122,0.1);  color: var(--color-accent); }
 .estado-completada { background: rgba(255,255,255,0.06); color: var(--color-bone-soft); }
 .estado-cancelada  { background: rgba(255,138,123,0.1);  color: var(--color-danger); }

 /* Botón cancelar */
 .btn-cancel {
   flex-shrink: 0;
   height: 32px;
   padding: 0 0.875rem;
   border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.3);
   background: transparent;
   color: var(--color-danger);
   font-size: 12px;
   cursor: pointer;
   transition: all 0.15s;
   white-space: nowrap;
 }
 .btn-cancel:hover { background: rgba(255,138,123,0.08); }
</style>
