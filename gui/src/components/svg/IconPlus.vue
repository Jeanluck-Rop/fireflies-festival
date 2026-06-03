<template>
  <svg xmlns="http://www.w3.org/2000/svg" :height="size" :width="size" viewBox="0 0 16 16">
    <path d="m 7 1 v 6 h -6 v 2 h 6 v 6 h 2 v -6 h 6 v -2 h -6 v -6 z m 0 0" fill="currentColor"/>
  </svg>
</template>
<script setup lang="ts">
 withDefaults(defineProps<{ size?: string }>(), { size: '14px' })
</script>
