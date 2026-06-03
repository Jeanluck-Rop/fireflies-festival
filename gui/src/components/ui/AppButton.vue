<template>
  <button
    :class="variants[variant]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <span v-if="loading" class="opacity-60">Loading...</span>
    <slot v-else />
  </button>
</template>

<script setup lang="ts">
 interface Props {
   variant?: 'primary' | 'outline' | 'ghost'
   disabled?: boolean
   loading?: boolean
 }
 withDefaults(defineProps<Props>(), {
   variant: 'primary',
   disabled: false,
   loading: false,
 })

 const variants: Record<string, string> = {
   primary: 'btn-primary inline-flex items-center justify-center',
   outline: 'btn-outline inline-flex items-center justify-center',
   ghost: 'btn-ghost inline-flex items-center justify-center',
 }
</script>
