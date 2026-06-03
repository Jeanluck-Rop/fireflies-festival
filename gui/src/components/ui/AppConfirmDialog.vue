<template>
  <teleport to="body">
    <transition name="dialog-fade">
      <div
        v-if="modelValue"
        class="dialog-backdrop"
        @click.self="$emit('update:modelValue', false)">
        <div class="dialog-box" :class="variantClass">
	    
          <!-- Header -->
          <div class="dialog-body">
            <h3 class="dialog-title">{{ title }}</h3>
            <p class="dialog-text">
              <slot>{{ message }}</slot>
            </p>
	  </div>
	  
          <!-- Acciones -->
          <div class="dialog-footer" :class="variantClass">
            <button
              class="dialog-btn dialog-btn-cancel"
	      :class="variantClass" 
              @click="$emit('update:modelValue', false)">
              {{ cancelLabel }}
            </button>
            <button
              class="dialog-btn dialog-btn-confirm"
              :class="['dialog-btn-confirm', 'confirm-' + variant, variantClass]"
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
   position: fixed; inset: 0; z-index: 9999;
   background: rgba(0, 0, 0, 0.7);
   backdrop-filter: blur(4px);
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 1rem;
 }

 /* Caja principal */
 .dialog-box {
   width: 100%;
   max-width: 400px;
   border-radius: 16px;
   overflow: hidden;
   box-shadow: 0 32px 64px rgba(0,0,0,0.55);
   display: flex;
   flex-direction: column;
   background: #0f1410;
 }

 /* Borde del box segun variante */
 .dialog-box.v-danger  {
   background: #0f1410;
   border: 1px solid rgba(255,138,123,0.22);
 }
 .dialog-box.v-warning {
   background: #0f1410;
   border: 1px solid rgba(232,255,122,0.18);
 }
 .dialog-box.v-normal  {
   background: #0f1410;
   border: 1px solid rgba(123,216,176,0.18);
 }

 /* Cuerpo: titulo + texto centrados */
 .dialog-body {
   padding: 1.75rem 1.75rem 1.5rem;
   display: flex;
   flex-direction: column;
   align-items: center;
   gap: 0.65rem;
   text-align: center;
 }

 .dialog-title {
   font-size: 17px;
   font-weight: 700;
   letter-spacing: -0.01em;
   color: var(--color-bone);
 }

 .dialog-text {
   font-size: 13.5px;
   color: var(--color-bone-soft);
   line-height: 1.6;
   max-width: 32ch;
 }
 .dialog-text :deep(strong) { color: var(--color-bone); font-weight: 600; }

 /* Footer con botones pegados al borde */
 .dialog-footer {
   display: flex;
   border-top-width: 1px;
   border-top-style: solid;
 }

 /* Color del borde superior del footer según variante */
 .dialog-footer.v-danger  { border-top-color: rgba(255,138,123,0.18); }
 .dialog-footer.v-warning { border-top-color: rgba(232,255,122,0.14); }
 .dialog-footer.v-normal  { border-top-color: rgba(123,216,176,0.14); }

 /* Botones */
 .dialog-btn {
   flex: 1;
   height: 46px;
   border: none;
   background: transparent;
   font-size: 13.5px;
   font-weight: 500;
   font-family: var(--font-sans);
   cursor: pointer;
   transition: background 0.18s, color 0.18s;
   border-radius: 0;
 }

 /* Cancelar: texto muted, separador derecho */
 .dialog-btn-cancel {
   color: var(--color-bone-soft);
   border-right-width: 1px;
   border-right-style: solid;
 }
 .dialog-btn-cancel.v-danger  { border-right-color: rgba(255,138,123,0.18); }
 .dialog-btn-cancel.v-warning { border-right-color: rgba(232,255,122,0.14); }
 .dialog-btn-cancel.v-normal  { border-right-color: rgba(123,216,176,0.14); }

 .dialog-btn-cancel:hover {
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
 }

 /* Confirmar: texto en color de variante, bold */
 .dialog-btn-confirm { font-weight: 600; }

 .confirm-danger  { color: var(--color-danger); }
 .confirm-warning { color: var(--color-accent); }
 .confirm-normal  { color: var(--color-green);  }

 .dialog-btn-confirm:hover { background: rgba(255,255,255,0.04); }

 /* Hover específico por variante para el confirm */
 .dialog-btn-confirm.confirm-danger:hover  { background: rgba(255,138,123,0.08); }
 .dialog-btn-confirm.confirm-warning:hover { background: rgba(232,255,122,0.06); }
 .dialog-btn-confirm.confirm-normal:hover  { background: rgba(123,216,176,0.07); }

 .dialog-btn-confirm:disabled {
   opacity: 0.35;
   cursor: not-allowed;
 }

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
