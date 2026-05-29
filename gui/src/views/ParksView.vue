<template>
  <div class="parks-view">
    <Parks />
    <FoundParks />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import Parks from "../components/parks/Parks.vue";
import { parkService } from "../services/parkService";
import FoundParks from "../components/parks/FoundParks.vue";

onMounted(async () => {
  await parkService.getParks();
});
</script>

<style scoped>
.parks-view {
  height: calc(100vh - 80px);
  margin-top: 80px;
  padding: 1rem;
  box-sizing: border-box;
}
</style>
