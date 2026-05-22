<template>
  <div class="w-full mb-4">
    <label
      v-if="label"
      class="flex items-center justify-between mb-2 font-sans text-[11px] tracking-[0.14em] uppercase text-bone-soft"
      >
      <span>{{ label }}</span>
      <span
        v-if="hint"
        class="text-bone-soft normal-case tracking-normal text-[10px]"
      >
        {{ hint }}
      </span>
    </label>

    <div class="relative">
      <span
        v-if="icon"
        class="absolute left-4 top-1/2 -translate-y-1/2 text-bone-muted pointer-events-none"
      >
        <svg v-if="iconName === 'email'" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <rect x="2" y="3.5" width="12" height="9" rx="2" stroke="currentColor" stroke-width="1.4"/>
          <path d="M2.5 4.5l5.5 4 5.5-4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg v-else-if="iconName === 'lock'" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <rect x="3" y="7" width="10" height="6.5" rx="1.5" stroke="currentColor" stroke-width="1.4"/>
          <path d="M5.2 7V5a2.8 2.8 0 1 1 5.6 0v2" stroke="currentColor" stroke-width="1.4"/>
        </svg>
        <svg v-else-if="iconName === 'user'" width="16" height="16" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="1.4"/>
          <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
      </span>
      
      <input
        v-model="model"
        :type="inputType"
        :placeholder="placeholder"
        :disabled="disabled"
        :class="[
          'w-full h-13 px-4 rounded-xl outline-none',
          'bg-ink border border-bone-line text-bone text-[15px]',
          'placeholder:text-bone-muted',
          'transition-[border-color,background-color,box-shadow] duration-200',
          'hover:border-yellow-400',
          'focus:border-yellow-500 focus:bg-ink-deep focus:ring-[3px] focus:ring-yellow-500/15',
          'disabled:opacity-60 disabled:cursor-not-allowed',
          icon && 'pl-11.5',
          type === 'password' && 'pr-11.5',
        ]"
      />

      <button
        v-if="type === 'password'"
        type="button"
        class="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 rounded-lg text-bone-soft cursor-pointer transition-colors duration-200 hover:bg-bone-line-soft hover:text-bone"
        :aria-label="showPassword ? 'Ocultar' : 'Mostrar'"
        @click="togglePassword"
      >
        <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M1.5 8c1.4-3 4-5 6.5-5s5.1 2 6.5 5c-1.4 3-4 5-6.5 5S2.9 11 1.5 8z" stroke="currentColor" stroke-width="1.4"/>
          <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.4"/>
        </svg>
        <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path d="M2 2l12 12M6.5 6.5A2 2 0 0 0 8 10a2 2 0 0 0 1.5-3.5M3.5 4.7C2.4 5.6 1.6 6.7 1.5 8c1.4 3 4 5 6.5 5 1.1 0 2.1-.3 3-.7M11.5 11.3c1.1-.9 1.9-2 2-3.3-1.4-3-4-5-6.5-5-.6 0-1.1.1-1.7.2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
    <span v-if="error" class="text-[var(--color-danger)] text-[11px] mt-1 block">
      {{ error }}
    </span>
    
  </div>
</template>

<script setup lang="ts">
 import { computed, ref } from 'vue'
 
 interface Props {
   label?: string
   hint?: string
   placeholder?: string
   type?: 'text' | 'email' | 'password'
   disabled?: boolean
   icon?: boolean
   iconName?: 'email' | 'lock' | 'user' | string
   error?: string
 }
 
 const props = withDefaults(defineProps<Props>(), {
   type: 'text',
   disabled: false,
   icon: false,
 })
 
 const model = defineModel<string>()
 const showPassword = ref(false)
 
 const inputType = computed(() =>
   props.type === 'password' ? (showPassword.value ? 'text' : 'password') : props.type,
 )
 
 const togglePassword = () => {
   showPassword.value = !showPassword.value
 }
</script>
