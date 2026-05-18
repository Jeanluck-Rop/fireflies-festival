<template>
  <div class="min-h-screen flex flex-col">
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
      <br>
      <p>Probando inputs</p>
      <div>
        <AppInput
          v-model="email"
          label="Correo Electrónico"
          placeholder="Ingresa tu correo"
          type="email"
          icon
          icon-name="email"
        />
        <AppInput
          v-model="password"
          label="Contraseña"
          placeholder="Ingresa tu contraseña"
          type="password"
          icon
          icon-name="lock"
          hint="Mínimo 8 caracteres"
        />
        <AppInput
          label="Nombre de Usuario"
          placeholder="Ingresa tu nombre de usuario"
          type="text"
          icon
          icon-name="user"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">

import AppHeader from "../components/ui/AppHeader.vue";
import AppInput from "../components/ui/AppInput.vue";
import { ref } from "vue";
const email = ref("");
const password = ref("");

</script>
