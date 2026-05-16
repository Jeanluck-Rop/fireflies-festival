<!-- components/auth/FormLogin.vue -->
<template>
  <div style="padding: 2rem">
    <input v-model="email" placeholder="Email" /><br/>
    <input v-model="password" type="password" placeholder="Password" /><br/>
    <button @click="$emit('submit', email, password)">Entrar</button>
  </div>
</template>

<script setup lang="ts">
 import { ref } from 'vue'
 defineEmits(['submit'])
 const email = ref('')
 const password = ref('')
</script>
