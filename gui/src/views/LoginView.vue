<template>
  <div>
    <FormLogin @submit="handleLogin" :loading="loading" />
  </div>
</template>

<script setup lang="ts">
 import { ref } from 'vue'
 import { useRouter, useRoute } from 'vue-router'
 import FormLogin from '../components/auth/FormAuth.vue'
 import { authService } from '../services/authService'

 const router = useRouter()
 const route = useRoute()
 const loading = ref(false)

 async function handleLogin(email: string, password: string) {
   loading.value = true
   await authService.login(email, password)
   loading.value = false

   const redirect = route.query.redirect as string || '/'
   router.push(redirect)
 }
</script>
