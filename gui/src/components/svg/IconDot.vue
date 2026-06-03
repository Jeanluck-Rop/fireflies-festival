<template>
  <svg xmlns="http://www.w3.org/2000/svg" :height="size" :width="size" viewBox="0 0 16 16">
    <path d="m 11.019531 7.996094 c 0 1.65625 -1.34375 3 -3 3 s -3 -1.34375 -3 -3 s 1.34375 -3 3 -3 s 3 1.34375 3 3 z m 0 0" fill="currentColor"/>
  </svg>
</template>
<script setup lang="ts">
 withDefaults(defineProps<{ size?: string }>(), { size: '8px' })
</script>
