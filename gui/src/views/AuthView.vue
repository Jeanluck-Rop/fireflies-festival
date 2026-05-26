<template>
  <FormAuth
    :initial-mode="initialMode"
    :loading="loading"
    :login-error="loginError"
    :signup-error="signupError"
    @login="handleLogin"
    @signup="handleSignup"
  />
</template>

<script setup lang="ts">
 import { ref, computed } from 'vue'
 import { useRouter, useRoute } from 'vue-router'
 import FormAuth from '../components/auth/FormAuth.vue'
 import { authService, EmailNotFoundError, WrongPasswordError, EmailAlreadyInUseError } from '../services/authService'
 import { useNotification } from '../composables/useNotification'

 const router = useRouter()
 const route = useRoute()
 const loading = ref(false)

 const { show } = useNotification()
 const loginError = ref<'credentials' | null>(null)
 const signupError = ref<'email_in_use' | null>(null)

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
   try {
     await authService.signup(nombre, apellidos, email, password)
     show('exito', 'Cuenta creada con éxito. ¡Bienvenido!')
     router.push('/')
   } catch (e) {
     if (e instanceof EmailAlreadyInUseError) {
       signupError.value = 'email_in_use'
       show('error', 'El correo ya pertenece a una cuenta.')
     } else {
       show('error', 'Error al crear la cuenta, inténtalo de nuevo.')
     }
   } finally {
     loading.value = false
   }
 }
</script>
