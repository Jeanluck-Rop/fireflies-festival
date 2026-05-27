<template>
  <teleport to="body">
    <transition name="notif">
      <div
        v-if="notification"
        :key="notification.id"
        class="notif-wrapper"
        :class="'notif-' + notification.type"
        role="alert">

        <!-- Icono segun tipo -->
        <span class="notif-icon">
          <!-- Exito: checkmark -->
          <svg v-if="notification.type === 'exito'" width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.4"/>
            <path d="M4.5 8l2.5 2.5 4.5-5" stroke="currentColor" stroke-width="1.5"
              stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <!-- Error: X circular -->
          <svg v-else-if="notification.type === 'error'" width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.4"/>
            <path d="M5.5 5.5l5 5M10.5 5.5l-5 5" stroke="currentColor" stroke-width="1.5"
              stroke-linecap="round"/>
          </svg>
          <!-- Normal: info -->
          <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.4"/>
            <path d="M8 7v5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            <circle cx="8" cy="5" r="0.8" fill="currentColor"/>
          </svg>
        </span>

        <!-- Mensaje -->
        <span class="notif-message">{{ notification.message }}</span>

        <!-- Barra de progreso -->
        <div class="notif-progress" :key="'p-' + notification.id" />

        <!-- Boton cerrar -->
        <button class="notif-close" aria-label="Cerrar" @click="dismiss">
          <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
            <path d="M1 1l8 8M9 1l-8 8" stroke="currentColor" stroke-width="1.5"
              stroke-linecap="round"/>
          </svg>
        </button>

      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
 import { useNotification } from '../../composables/useNotification'

 const { notification, dismiss } = useNotification()
</script>

<style scoped>
 /* Contenedor */
 .notif-wrapper {
   position: fixed;
   bottom: 1.5rem;
   right: 1.5rem;
   z-index: 99999;
   display: flex;
   align-items: center;
   gap: 0.85rem;
   min-width: 360px;
   max-width: 520px;
   padding: 1.1rem 1.3rem;
   border-radius: 14px;
   border: 1px solid transparent;
   font-size: 15px;
   font-family: var(--font-sans);
   box-shadow:
     0 8px 24px rgba(0,0,0,0.3),
     0 0 0 1px rgba(255,255,255,0.04);
   overflow: hidden;
   cursor: default;
 }

 /* Variantes de color */
 .notif-exito {
   background: rgba(13, 32, 20, 0.95);
   border-color: rgba(123, 216, 176, 0.25);
   color: var(--color-green);
 }
 .notif-error {
   background: rgba(32, 10, 10, 0.95);
   border-color: rgba(255, 138, 123, 0.25);
   color: var(--color-danger);
 }
 .notif-normal {
   background: rgba(10, 18, 32, 0.95);
   border-color: rgba(100, 160, 255, 0.25);
   color: #7ab4ff;
 }

 /* Icono */
 .notif-icon {
   flex-shrink: 0;
   display: flex;
   align-items: center;
 }

 /* Mensaje */
 .notif-message {
   flex: 1;
   color: var(--color-bone);
   line-height: 1.4;
 }

 /* Boton cerrar */
 .notif-close {
   flex-shrink: 0;
   background: none;
   border: none;
   color: var(--color-bone-mute);
   cursor: pointer;
   padding: 2px;
   display: flex;
   align-items: center;
   transition: color 0.15s;
 }
 .notif-close:hover { color: var(--color-bone) }

 /* Barra de progreso */
 .notif-progress {
   position: absolute;
   bottom: 0;
   left: 0;
   height: 2px;
   width: 100%;
   transform-origin: left;
   animation: progress-shrink 8s linear forwards;
 }
 .notif-exito  .notif-progress { background: var(--color-green) }
 .notif-error  .notif-progress { background: var(--color-danger) }
 .notif-normal .notif-progress { background: #7ab4ff }

 @keyframes progress-shrink {
   from { transform: scaleX(1) }
   to   { transform: scaleX(0) }
 }

 /* Animacion entrada/salida */
 .notif-enter-active {
   transition: opacity 0.25s ease, transform 0.25s ease;
 }
 .notif-leave-active {
   transition: opacity 0.3s ease, transform 0.3s ease;
 }
 .notif-enter-from {
   opacity: 0;
   transform: translateY(12px) scale(0.97);
 }
 .notif-leave-to {
   opacity: 0;
   transform: translateY(6px) scale(0.98);
 }
</style>
