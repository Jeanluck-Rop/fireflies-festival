<template>
  <svg xmlns="http://www.w3.org/2000/svg" :height="size" :width="size" viewBox="0 0 16 16">
    <path d="m 2.292969 6.707031 l 5 5 c 0.390625 0.390625 1.023437 0.390625 1.414062 0 l 5 -5 c 0.390625 -0.390625 0.390625 -1.023437 0 -1.414062 s -1.023437 -0.390625 -1.414062 0 l -4.292969 4.292969 l -4.292969 -4.292969 c -0.390625 -0.390625 -1.023437 -0.390625 -1.414062 0 s -0.390625 1.023437 0 1.414062 z m 0 0" fill="currentColor" fill-rule="evenodd"/>
  </svg>
</template>
<script setup lang="ts">
 withDefaults(defineProps<{ size?: string }>(), { size: '10px' })
</script>
