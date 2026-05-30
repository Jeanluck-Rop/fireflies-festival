<template>
  <svg xmlns="http://www.w3.org/2000/svg" :height="size" :width="size" viewBox="0 0 16 16">
    <path d="m 0 3 v 11 h 2 v -2 h 12 v 2 h 2 v -7 c 0 -1.109375 -0.890625 -2 -2 -2 h -6 v 4 h -6 v -6 z m 5 1 c -1.105469 0 -2 0.894531 -2 2 s 0.894531 2 2 2 s 2 -0.894531 2 -2 s -0.894531 -2 -2 -2 z m 0 0" fill="currentColor"/>
  </svg>
</template>
<script setup lang="ts">
 withDefaults(defineProps<{ size?: string }>(), { size: '12px' })
</script>
