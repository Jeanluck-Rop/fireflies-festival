<script setup lang="ts">
  import { onMounted, ref } from 'vue'

const message = ref("Loading...")

onMounted(async () => {
  const res = await fetch("http://localhost:8000/api/test/")
  const data = await res.json()
  message.value = data.message
})
</script>

<template>
<h1>Fireflies Festival</h1>
<div class="p-4">
  <h2 class="text-2xl font-bold text-green-600">{{ message }}</h2>
</div>
</template>
