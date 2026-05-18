<template>
  <a :href="href" :class="variants[variant]">
    <slot />
  </a>
</template>

<script setup lang="ts">
 interface Props {
   href: string;
   variant?: 'transparent' | 'yellow' | 'brand' | 'popover' | 'outline';
 }

 const props = withDefaults(defineProps<Props>(), {
   variant: 'transparent'
 });
 
 const variants: Record<string, string> = {
   transparent: 'inline-flex items-center justify-center btn-transparent',
   yellow: 'inline-flex items-center justify-center btn-primary',
   outline: 'inline-flex items-center justify-center btn-outline',
   brand: 'flex items-center gap-3 group transition-transform',
   popover: 'flex items-center gap-2.5 px-3 py-2.5 rounded-lg hover:bg-white/5',
 };
</script>
