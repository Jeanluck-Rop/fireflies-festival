<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader :user="{ id: 1, name: 'John Doe', email: 'john@example.com' }" />
    <main class="flex-1 flex flex-col items-center justify-center">
      <div>
        <h1 class="text-4xl font-bold text-center text-bone">
          Bienvenido al Festival de Luciérnagas
        </h1>
      </div>
      <div>
        <p class="mt-4 text-center text-bone-mute max-w-md">
          Explora los parques, descubre eventos y sumérgete en la magia de las
          luciérnagas.
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from "../components/ui/AppHeader.vue";
</script>
