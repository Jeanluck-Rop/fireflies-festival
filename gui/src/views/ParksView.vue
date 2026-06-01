<template>
  <div class="parks-view">
    <ParkSearch class="p-4" />
    <Parks class="p-4" />
    <FoundParks class="p-4" />
    <RecomendationsParks class="p-4" />
    <FooterSection />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import Parks from "../components/parks/Parks.vue";
import { useParksStore } from "../stores/parks";
import FoundParks from "../components/parks/FoundParks.vue";
import RecomendationsParks from "../components/parks/RecomendationsParks.vue";
import FooterSection from "../components/landing/FooterSection.vue";
import ParkSearch from "../components/parks/ParkSearch.vue";

const parksStore = useParksStore();

onMounted(() => {
  parksStore.loadParks();
});
</script>

<style scoped>
.parks-view {
  height: calc(100vh - 80px);
  margin-top: 80px;
  box-sizing: border-box;
}
</style>
