<template>
  <teleport to="body">
    <transition name="dialog-fade">
      <div
        v-if="modelValue"
        class="dialog-backdrop"
        @click.self="$emit('update:modelValue', false)">
        <div class="dialog-box" :class="variantClass">

          <!-- Header -->
          <div class="dialog-header">
            <h3 class="dialog-title">{{ title }}</h3>
            <button class="dialog-close" @click="$emit('update:modelValue', false)">
              <svg width="11" height="11" viewBox="0 0 10 10" fill="none">
                <path d="M1 1l8 8M9 1l-8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Mensaje -->
          <p class="dialog-text">
            <slot>{{ message }}</slot>
          </p>

          <!-- Acciones -->
          <div class="dialog-actions">
            <button
              class="dialog-btn dialog-btn-back"
              @click="$emit('update:modelValue', false)">
              {{ cancelLabel }}
            </button>
            <button
              class="dialog-btn dialog-btn-confirm"
              :class="'confirm-' + variant"
              :disabled="loading"
              @click="$emit('confirm')">
              {{ loading ? loadingLabel : confirmLabel }}
            </button>
          </div>

        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup lang="ts">
 import { computed } from 'vue'

 const props = withDefaults(defineProps<{
   modelValue:   boolean
   title:        string
   message?:     string
   confirmLabel?: string
   cancelLabel?:  string
   loadingLabel?: string
   loading?:      boolean
   variant?:      'danger' | 'warning' | 'normal'
 }>(), {
   confirmLabel: 'Confirmar',
   cancelLabel:  'Cancelar',
   loadingLabel: 'Procesando...',
   loading:      false,
   variant:      'danger',
 })

 defineEmits<{
   'update:modelValue': [value: boolean]
   'confirm':           []
 }>()

 const variantClass = computed(() => 'box-' + props.variant)
</script>

<style scoped>
 /* Backdrop */
 .dialog-backdrop {
   position: fixed;
   inset: 0;
   z-index: 9999;
   background: rgba(0, 0, 0, 0.6);
   backdrop-filter: blur(4px);
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 1rem;
 }

 /* Box */
 .dialog-box {
   background: #0d1a10;
   border-radius: 16px;
   padding: 1.75rem;
   width: 100%;
   max-width: 420px;
   box-shadow: 0 24px 48px rgba(0, 0, 0, 0.5);
   display: flex;
   flex-direction: column;
   gap: 1rem;
 }

 /* Variantes de borde */
 .box-danger  { border: 1px solid rgba(255, 138, 123, 0.2); }
 .box-warning { border: 1px solid rgba(232, 255, 122, 0.15); }
 .box-normal  { border: 1px solid rgba(123, 216, 176, 0.15); }

 /* Header */
 .dialog-header {
   display: flex;
   align-items: center;
   justify-content: space-between;
   gap: 1rem;
 }

 .dialog-title {
   font-size: 18px;
   font-weight: 600;
   letter-spacing: -0.01em;
 }

 /* Color del titulo segun variante */
 .box-danger  .dialog-title { color: var(--color-danger); }
 .box-warning .dialog-title { color: var(--color-accent); }
 .box-normal  .dialog-title { color: var(--color-bone); }

 .dialog-close {
   flex-shrink: 0;
   width: 28px;
   height: 28px;
   border-radius: 8px;
   border: 1px solid var(--color-border);
   background: transparent;
   color: var(--color-bone-mute);
   cursor: pointer;
   display: flex;
   align-items: center;
   justify-content: center;
   transition: color 0.2s, background 0.2s;
 }
 .dialog-close:hover {
   background: rgba(255, 255, 255, 0.06);
   color: var(--color-bone);
 }

 /* Texto*/
 .dialog-text {
   font-size: 13.5px;
   color: var(--color-bone-soft);
   line-height: 1.6;
 }
 .dialog-text :deep(strong) { color: var(--color-bone); }

 /* Acciones */
 .dialog-actions {
   display: flex;
   gap: 0.75rem;
   justify-content: flex-end;
   margin-top: 0.5rem;
 }

 .dialog-btn {
   height: 36px;
   padding: 0 1.25rem;
   border-radius: 999px;
   font-size: 13px;
   font-family: var(--font-sans);
   cursor: pointer;
   transition: all 0.2s;
 }

 .dialog-btn-back {
   border: 1px solid var(--color-border);
   background: transparent;
   color: var(--color-bone-soft);
 }
 .dialog-btn-back:hover {
   background: rgba(255, 255, 255, 0.05);
   color: var(--color-bone);
 }

 .dialog-btn-confirm {
   border: none;
   color: #fff;
   font-weight: 500;
 }
 .confirm-danger  { background: var(--color-danger); }
 .confirm-warning { background: rgba(232, 255, 122, 0.85); color: #161D1A; }
 .confirm-normal  { background: var(--color-green); color: #07090A; }

 .dialog-btn-confirm:hover    { opacity: 0.88; }
 .dialog-btn-confirm:disabled { opacity: 0.4; cursor: not-allowed; }

 /* Animacion */
 .dialog-fade-enter-active,
 .dialog-fade-leave-active { transition: opacity 0.2s ease; }

 .dialog-fade-enter-active .dialog-box,
 .dialog-fade-leave-active .dialog-box {
   transition: transform 0.2s ease, opacity 0.2s ease;
 }

 .dialog-fade-enter-from,
 .dialog-fade-leave-to { opacity: 0; }

 .dialog-fade-enter-from .dialog-box,
 .dialog-fade-leave-to   .dialog-box {
   transform: scale(0.96) translateY(8px);
   opacity: 0;
 }
</style>
