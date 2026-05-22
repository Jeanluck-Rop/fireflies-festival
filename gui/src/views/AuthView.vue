<template>
  <FormAuth
    :initial-mode="initialMode"
    :loading="loading"
    @login="handleLogin"
    @signup="handleSignup"
  />
</template>

<script setup lang="ts">
 import { ref, computed } from 'vue'
 import { useRouter, useRoute } from 'vue-router'
 import FormAuth from '../components/auth/FormAuth.vue'
 import { authService } from '../services/authService'

 const router = useRouter()
 const route = useRoute()
 const loading = ref(false)

 const initialMode = computed(() => (route.query.mode as 'login' | 'signup' | 'recovery') ?? 'login')

 async function handleLogin(email: string, password: string) {
   loading.value = true
   await authService.login(email, password)
   loading.value = false
   const redirect = route.query.redirect as string || '/'
   router.push(redirect)
 }

 async function handleSignup(name: string, email: string, password: string) {
   loading.value = true
   await authService.signup(name, email, password)
   loading.value = false
   router.push('/')
 }
</script>
