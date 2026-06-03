<template>
  <ParksHero />
  <ListParks :highlighted-park-id="highlightedParkId" />
  <FooterSection />
</template>

<script setup lang="ts">
import { onMounted, ref, watch, nextTick } from 'vue'
import ParksHero from '../components/parks/ParksHero.vue'
import ListParks from '../components/parks/ListParks.vue'
import FooterSection from '../components/landing/FooterSection.vue'
import { useParksStore } from '../stores/parks'
import { useRoute } from 'vue-router'

const parksStore = useParksStore();
const route = useRoute();
const highlightedParkId = ref<number | null>(null)

const handleHashScroll = async (currentHash: string) => {
  if (!currentHash || !currentHash.startsWith('#park-')) return;

  const parkId = Number(currentHash.replace('#park-', ''))
  highlightedParkId.value = parkId

  await nextTick();

  setTimeout(() => {
    const element = document.querySelector(currentHash)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 150)

  setTimeout(() => {
    highlightedParkId.value = null
  }, 2000)
}
onMounted(async () => {
  parksStore.loadParks();

  handleHashScroll(route.hash);
});
watch(() => route.hash, (newHash) => {
  handleHashScroll(newHash);
});
</script>