<template>
  <RouterLink
    :to="href"
    :class="[
      variants[variant],
      isNavVariant && isActive ? 'nav-active' : '',
      isNavVariant && !isActive ? 'hover:bg-white/5 hover:text-bone' : '',
      variant === 'nav-admin' && isActive ? 'nav-admin-active' : '',
    ]"
  >
    <component :is="icon" v-if="icon" class="size-4" shrink-0 />
    <span class="mx-2" v-if="$slots.default && icon"></span>
    <slot />
    <span class="mx-2" v-if="$slots.default && iconRight"></span>
    <component :is="iconRight" v-if="iconRight" class="size-4" shrink-0 />
  </RouterLink>
</template>

<script setup lang="ts">
 import { computed, type Component } from "vue";
 import { useRoute } from "vue-router";

 const route = useRoute();

 interface Props {
   href: string;
   variant?: "transparent" | "yellow" | "brand" | "popover" | "outline" | "nav" | "nav-admin";
   icon?: Component;
   iconRight?: Component;
 }

 const props = withDefaults(defineProps<Props>(), {
   variant: "transparent",
 });
 
 const isActive = computed(() =>
   props.href === "/" ? route.path === "/" : route.path.startsWith(props.href),
 );
 
 const isNavVariant = computed(() =>
   props.variant === 'nav' || props.variant === 'nav-admin'
 );

 const variants: Record<string, string> = {
   transparent: "inline-flex items-center justify-center btn-transparent",
   yellow: "inline-flex items-center justify-center btn-primary",
   outline: "inline-flex items-center justify-center btn-outline",
   brand: "flex items-center gap-3 group transition-transform",
   popover: "flex items-center gap-2.5 px-3 py-2.5 rounded-lg hover:bg-white/5",
   nav: "inline-flex items-center justify-center px-4 py-2 rounded-full transition-colors duration-200 relative nav-link",
   'nav-admin': "inline-flex items-center justify-center px-4 py-2 rounded-full transition-colors duration-200 relative nav-admin-link",
 };
</script>

<style scoped>
 /* Nav User*/
 .nav-link {
   color: var(--color-bone-soft);
 }
 .nav-active {
   color: var(--color-bone);
 }
 /* Punto indicador debajo del texto */
 .nav-active::after {
   content: "";
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
 
 /* Nav Admin */
 .nav-admin-link { color: var(--color-bone-soft); }
 .nav-admin-active { color: var(--color-bone); }
 /* Punto indicador azul para admin */
 .nav-admin-active::after {
   content: '';
   position: absolute;
   bottom: 4px;
   left: 50%;
   transform: translateX(-50%);
   width: 4px;
   height: 4px;
   border-radius: 50%;
   background: var(--color-admin-accent);
   box-shadow: 0 0 6px rgba(123, 167, 212, 0.8);
 }

</style>
