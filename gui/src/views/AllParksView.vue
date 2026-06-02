<template>
  <ParksHero />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import ParksHero from '../components/parks/ParksHero.vue'
import { useParksStore } from '../stores/parks'

const parksStore = useParksStore();

onMounted(() => {
  parksStore.loadParks();
});
</script>