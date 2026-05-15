<template>
  <a :href="href" :class="variants[variant]">
    <slot />
  </a>
</template>

<script setup lang="ts">
interface Props {
  href: string;
  variant?: 'transparent' | 'yellow' | 'brand' | 'popover';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'transparent'
});

const variants: Record<string, string> = {
  transparent:
    'inline-flex items-center justify-center px-4 py-2 rounded-full hover:bg-white/5 hover:text-bone transition-colors duration-200',

  yellow:
    'inline-flex items-center justify-center btn-glow rounded-full px-5 py-2.5 text-[14px] font-medium transition-colors duration-200',

  brand:
    'flex items-center gap-3 group transition-transform',

  popover:
    'flex items-center gap-2.5 px-3 py-2.5 rounded-lg hover:bg-white/5',
};
</script>