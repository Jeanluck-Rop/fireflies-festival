<template>
  <RouterLink
    :to="href"
    :class="[
      variants[variant],
      variant === 'nav' && isActive ? 'nav-active' : '',
      variant === 'nav' && !isActive ? 'hover:bg-white/5 hover:text-bone' : ''
    ]">
    <slot />
  </RouterLink>
</template>

<script setup lang="ts">
 import { computed } from 'vue'
 import { useRoute } from 'vue-router'

 const route = useRoute()

 interface Props {
   href: string;
   variant?: 'transparent' | 'yellow' | 'brand' | 'popover' | 'outline' | 'nav';
 }

 const isActive = computed(() =>
   props.href === '/'
   ? route.path === '/'
   : route.path.startsWith(props.href)
 )
 
 const props = withDefaults(defineProps<Props>(), {
   variant: 'transparent'
 });
 
 const variants: Record<string, string> = {
   transparent: 'inline-flex items-center justify-center btn-transparent',
   yellow: 'inline-flex items-center justify-center btn-primary',
   outline: 'inline-flex items-center justify-center btn-outline',
   brand: 'flex items-center gap-3 group transition-transform',
   popover: 'flex items-center gap-2.5 px-3 py-2.5 rounded-lg hover:bg-white/5',
   nav: 'inline-flex items-center justify-center px-4 py-2 rounded-full transition-colors duration-200 relative nav-link',
 };
</script>

<style scoped>
 .nav-link {
   color: var(--color-bone-soft);
 }

 .nav-active {
   color: var(--color-bone);
 }

 /* Punto indicador debajo del texto */
 .nav-active::after {
   content: '';
   position: absolute;
   bottom: 4px;
   left: 50%;
   transform: translateX(-50%);
   width: 4px;
   height: 4px;
   border-radius: 50%;
   background: var(--color-accent);
   box-shadow: 0 0 6px rgba(232, 255, 122, 0.8);
 }
</style>
