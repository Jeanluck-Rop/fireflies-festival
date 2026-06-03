<template>
  <FormAuth
    :initial-mode="initialMode"
    :loading="loading"
    :login-error="loginError"
    :signup-error="signupError"
    :signup-password-error="signupPasswordError"
    @login="handleLogin"
    @signup="handleSignup"
  />
</template>

<script setup lang="ts">
 import { ref, computed } from 'vue'
 import { useRouter, useRoute } from 'vue-router'
 import FormAuth from '../components/auth/FormAuth.vue'
 import { authService, EmailNotFoundError, WrongPasswordError, ValidationError } from '../services/authService'
 import { useNotification } from '../composables/useNotification'

 const router = useRouter()
 const route = useRoute()
 const loading = ref(false)

 const { show } = useNotification()
 const loginError = ref<'credentials' | null>(null)
 const signupError = ref<'email_in_use' | null>(null)
 const signupPasswordError = ref<string | null>(null)

 const initialMode = computed(() => (route.query.mode as 'login' | 'signup' | 'recovery') ?? 'login')

 async function handleLogin(email: string, password: string) {
   loading.value = true
   loginError.value = null
   try {
     await authService.login(email, password)
     const redirect = route.query.redirect as string || '/'
     router.push(redirect)
   } catch (e) {
     if (e instanceof EmailNotFoundError || e instanceof WrongPasswordError) {
       loginError.value = 'credentials'
       show('error', 'El correo no es válido o la contraseña es incorrecta.')
     } else {
       show('error', 'Error al iniciar sesión, inténtalo de nuevo.')
     }
   } finally {
     loading.value = false
   }
 }
 
 async function handleSignup(nombre: string, apellidos: string, email: string, password: string) {
   loading.value = true
   signupError.value = null
   signupPasswordError.value = null
   try {
     await authService.signup(nombre, apellidos, email, password)
     show('exito', 'Cuenta creada con éxito. ¡Bienvenido!')
     router.push('/')
   } catch (e) {
     if (e instanceof ValidationError) {
      if (e.fields.email) {
        signupError.value = 'email_in_use'
        show('error', e.fields.email) 
      }
      if (e.fields.password) {
        signupPasswordError.value = e.fields.password
      }
      if (e.fields.nombre || e.fields.apellidos) {
        show('error', e.fields.nombre || e.fields.apellidos)
      }
     } else if (e instanceof Error) {
       show('error', e.message)
     } else {
      show('error', 'Error inesperado al crear la cuenta.')
     }
   } finally {
     loading.value = false
   }
 }
</script>
