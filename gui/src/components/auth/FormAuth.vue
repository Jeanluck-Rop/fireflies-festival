<template>
  <div class="auth-scene">
    <div class="auth-card" :class="'mode-' + mode">
      
      <!-- Panel formulario Login -->
      <div class="form-panel panel-login">
        <div class="form-inner">
          <h1 class="form-title">Iniciar sesión</h1>
          <p class="form-sub">Bienvenido de vuelta</p>
	  
          <div class="fields">
	    <AppInput
	      v-model="login.email"
	      label="Correo electrónico"
	      placeholder="Ingresa tu correo electrónico"
	      type="email"
	      :icon="true"
	      icon-name="email"
	      :error="loginErrors.email"
	      @input="loginErrors.email = ''"/>
	    <AppInput
	      v-model="login.password"
	      label="Contraseña"
	      placeholder="Ingresa tu contraseña"
	      type="password"
	      :icon="true"
	      icon-name="lock"
	      :error="loginErrors.password"
	      @input="loginErrors.password = ''"/>
	  </div>
	  
	  <button class="link-btn" @click="setMode('recovery')">
            ¿Olvidaste tu contraseña?
          </button>
	    
	  <AppButton
	    variant="primary"
	    :loading="props.loading"
	    class="submit-btn"
	    @click="handleLogin">
	    Acceder
	  </AppButton>
	</div>
      </div>
	
      <!-- Panel Signup -->
      <div class="form-panel panel-signup">
        <div class="form-inner">
          <h1 class="form-title">Crear cuenta</h1>
          <p class="form-sub">Únete al festival</p>
	  <div class="fields">
            <AppInput
	      v-model="signup.nombre"
	      label="Nombre"
	      placeholder="Tu nombre"
	      type="text"
	      :icon="true"
	      icon-name="user"
	      :error="signupErrors.nombre"
	      @input="signupErrors.nombre = ''"/>
	    <AppInput
	      v-model="signup.apellidos"
	      label="Apellidos"
	      placeholder="Tus apellidos"
	      type="text"
	      :icon="true"
	      icon-name="user"
	      :error="signupErrors.apellidos"
	      @input="signupErrors.apellidos = ''"/>
            <AppInput
	      v-model="signup.email"
	      label="Correo electrónico"
	      placeholder="Ingresa tu correo electrónico"
	      type="email"
	      :icon="true"
	      icon-name="email"
	      :error="signupErrors.email"
	      @input="signupErrors.email = ''"/>
            <AppInput
	      v-model="signup.password"
	      label="Contraseña"
	      placeholder="Escribe una contraseña"
	      type="password"
	      :icon="true"
	      icon-name="lock"
	      :error="signupErrors.password"
	      @input="signupErrors.password = ''"/>
          </div>
	    
          <AppButton
            variant="primary"
            :loading="props.loading"
            class="submit-btn"
            @click="handleSignup">
            Registrarse
          </AppButton>
        </div>
      </div>
	
      <!-- Panel formulario Recovery -->
      <div class="form-panel panel-recovery">
        <div class="form-inner">
	  
	  <!-- Fase 1: solicitar correo -->
          <template v-if="recoveryStep === 1">
            <h1 class="form-title">Recuperar contraseña</h1>
            <p class="form-sub">Ingresa tu correo y te enviamos un código</p>
	    <div class="fields">
              <AppInput
		v-model="recovery.email"
		label="Correo electrónico"
		placeholder="Ingresa tu correo electrónico"
		type="email"
		:icon="true"
		icon-name="email"
		:error="recoveryErrors.email"
		@input="recoveryErrors.email = ''"/>
            </div>
	    
            <AppButton
              variant="primary"
              :loading="props.loading"
              class="submit-btn"
              @click="handleRecoveryStep1">
              Enviar código
            </AppButton>
	  </template>

	  <!-- Fase 2: codigo de validacion -->
          <template v-else-if="recoveryStep === 2">
            <h1 class="form-title">Código de verificación</h1>
            <p class="form-sub">Revisa tu correo <strong class="email-highlight">{{ recovery.email }}</strong></p>
            <div class="fields">
              <AppInput
                v-model="recovery.code"
                label="Código de verificación"
                placeholder="Ingresa el código"
                type="text"
                :icon="true"
                icon-name="lock"
                :error="recoveryErrors.code"
                @input="recoveryErrors.code = ''"/>
            </div>

            <!-- Contador / Reenviar -->
            <div class="resend-row">
              <span v-if="resendCountdown > 0" class="resend-countdown">
                Reenviar código en {{ resendCountdown }}s
              </span>
              <button
                v-else
                class="link-btn"
                :disabled="recoveryLoading"
                @click="handleResend">
                Reenviar código
              </button>
            </div>
	    <AppButton
	      variant="primary"
	      :loading="recoveryLoading"
	      class="submit-btn"
	      @click="handleRecoveryStep2">
              Verificar código
            </AppButton>
            <AppButton
	      variant="outline"
	      class="submit-btn"
	      @click="recoveryStep = 1">
	      Cambiar correo
	    </AppButton>
          </template>

          <!-- Fase 3: nueva contrasena -->
          <template v-else-if="recoveryStep === 3">
            <h1 class="form-title">Nueva contraseña</h1>
            <p class="form-sub">Elige una contraseña segura</p>
            <div class="fields">
              <AppInput
                v-model="recovery.newPassword"
                label="Nueva contraseña"
                placeholder="Mínimo 8 caracteres"
                type="password"
                :icon="true"
                icon-name="lock"
                :error="recoveryErrors.newPassword"
                @input="recoveryErrors.newPassword = ''"/>
              <AppInput
                v-model="recovery.confirmPassword"
                label="Confirmar contraseña"
                placeholder="Repite la contraseña"
                type="password"
                :icon="true"
                icon-name="lock"
                :error="recoveryErrors.confirmPassword"
                @input="recoveryErrors.confirmPassword = ''"/>
            </div>
            <AppButton variant="primary" :loading="recoveryLoading" class="submit-btn" @click="handleRecoveryStep3">
              Cambiar contraseña
            </AppButton>
          </template>
	  
          <!-- Fase 4: exito -->
          <template v-else-if="recoveryStep === 4">
            <div class="success-screen">
              <svg class="success-check" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="40" cy="40" r="38" stroke="#7BD8B0" stroke-width="2" stroke-opacity="0.3"/>
                <circle cx="40" cy="40" r="30" fill="#7BD8B0" fill-opacity="0.08"/>
                <path
                  d="M24 40l11 11 21-22"
                  stroke="#7BD8B0"
                  stroke-width="3"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="check-path"/>
              </svg>
              <h2 class="success-title">Contraseña cambiada</h2>
              <p class="success-sub">Tu contraseña fue actualizada correctamente</p>
            </div>
          </template>
        </div>
      </div>
      
      <!-- Panel deslizante -->
      <div class="slide-panel">
        <div class="slide-inner">
	  
          <!-- Luciernaga -->
	  <FireflyLogo :pulse="true" :drift="false" size="w-16 h-16" />
	    
          <transition name="slide-content" mode="out-in">
            <div :key="slideContent.title" class="slide-text">
	      <h2 class="slide-title">{{ slideContent.title }}</h2>
	      <p class="slide-sub">{{ slideContent.sub }}</p>
	      <button class="slide-cta" @click="slideContent.action">
                {{ slideContent.cta }}
	      </button>
            </div>
          </transition>
	  
          <!-- Particulas decorativas -->
          <span class="particle p1" aria-hidden="true"/>
          <span class="particle p2" aria-hidden="true"/>
          <span class="particle p3" aria-hidden="true"/>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script setup lang="ts">
 import { ref, computed, reactive, onUnmounted, watch } from 'vue'
 import { useRouter } from 'vue-router' 
 import AppInput from '../ui/AppInput.vue'
 import AppButton from '../ui/AppButton.vue'
 import FireflyLogo from '../ui/FireflyLogo.vue'
 import bgImage from '../../assets/fireflires_auth_background2.jpg'

 const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
 const router = useRouter()
 const bg = bgImage
 
 type Mode = 'login' | 'signup' | 'recovery'
 
 const props = defineProps<{
   initialMode?: Mode
   loading?: boolean
   loginError?: 'credentials' | null
   signupError?: 'email_in_use' | null
 }>()

 const emit = defineEmits<{
   login: [email: string, password: string]
   signup: [nombre: string, apellidos: string, email: string, password: string]
   recovery: [email: string]
 }>()

 const mode = ref<Mode>(props.initialMode ?? 'login')

 // Cuando AuthView informa error de credenciales en login
 watch(() => props.loginError, (err) => {
   if (err === 'credentials') {
     loginErrors.email    = 'Verifica la dirección de correo ingresada'
     loginErrors.password = 'Verifica la contraseña ingresada'
   }
 })
 
 // Cuando AuthView informa correo ya en uso en signup
 watch(() => props.signupError, (err) => {
   if (err === 'email_in_use') {
     signupErrors.email = 'Utiliza otra dirección de correo electrónico'
   }
 })
 
 const login = reactive({ email: '', password: '' })
 const signup = reactive({ nombre: '', apellidos: '', email: '', password: '' })
 const recovery = reactive({
   email: '',
   code: '',
   newPassword: '',
   confirmPassword: ''
 })

 const loginErrors = reactive({ email: '', password: '' })
 const signupErrors = reactive({ nombre: '', apellidos: '', email: '', password: '' })
 const recoveryErrors = reactive({
   email: '',
   code: '',
   newPassword: '',
   confirmPassword: ''
 })

 const recoveryStep = ref(1)
 const recoveryLoading = ref(false)
 
 const RESEND_SECONDS = 45
 const resendCountdown = ref(0)
 let countdownTimer: ReturnType<typeof setInterval> | null = null
 
 function startCountdown() {
   resendCountdown.value = RESEND_SECONDS
   if (countdownTimer) clearInterval(countdownTimer)
   countdownTimer = setInterval(() => {
     resendCountdown.value--
     if (resendCountdown.value <= 0 && countdownTimer) {
       clearInterval(countdownTimer)
       countdownTimer = null
     }
   }, 1000)
 }
 
 onUnmounted(() => {
   if (countdownTimer) clearInterval(countdownTimer)
 })
 
 const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

 function setMode(m: Mode) {
   mode.value = m
   if (m === 'recovery') {
     recoveryStep.value = 1
     recovery.email = ''
     recovery.code  = ''
     recovery.newPassword     = ''
     recovery.confirmPassword = ''
     recoveryErrors.email = ''
     recoveryErrors.code  = ''
   }
 }

 //Validaciones
 function validateLogin() {
   loginErrors.email = ''
   loginErrors.password = ''
   if (!login.email)
     loginErrors.email = 'El correo es requerido'
   else if (!EMAIL_RE.test(login.email))
     loginErrors.email = 'Formato de correo inválido'
   if (!login.password)
     loginErrors.password = 'La contraseña es requerida'
   return !loginErrors.email && !loginErrors.password
 }

 function validateSignup() {
   signupErrors.nombre   = ''
   signupErrors.apellidos = ''
   signupErrors.email = ''
   signupErrors.password = ''
   if (!signup.nombre || signup.nombre.length < 2)
     signupErrors.nombre = 'Nombre requerido (mín. 2 caracteres)'
   if (!signup.apellidos || signup.apellidos.length < 2)
     signupErrors.apellidos = 'Apellidos requeridos'
   if (!signup.email)
     signupErrors.email = 'El correo es requerido'
   else if (!EMAIL_RE.test(signup.email))
     signupErrors.email = 'Formato de correo inválido'
   if (!signup.password)
     signupErrors.password = 'La contraseña es requerida'
   else if (signup.password.length < 8)
     signupErrors.password = 'Mínimo 8 caracteres'
   return !signupErrors.nombre && !signupErrors.apellidos && !signupErrors.email && !signupErrors.password
 }

 function handleLogin() {
   if (validateLogin())
     emit('login', login.email, login.password)
 }
 function handleSignup() {
   if (validateSignup())
     emit('signup', signup.nombre, signup.apellidos, signup.email, signup.password)
 }
 
 // Fase 1: solicitamos correo
 async function handleRecoveryStep1() {
   recoveryErrors.email = ''
   if (!recovery.email) {
     recoveryErrors.email = 'El correo electrónico es requerido';
     return
   }
   if (!EMAIL_RE.test(recovery.email)) {
     recoveryErrors.email = 'Formato de correo inválido';
     return
   }

   recoveryLoading.value = true

   if (USE_MOCK) {
     // MOCK: simula envio exitoso
     await new Promise(r => setTimeout(r, 600))
     recoveryStep.value = 2
     startCountdown()
   } else {
     // TODO backend: POST /api/auth/recovery/request/ { email }
     // try {
     //   const res = await fetch(`${API}/api/auth/recovery/request/`, {
     //     method: 'POST',
     //     headers: { 'Content-Type': 'application/json' },
     //     body: JSON.stringify({ email: recovery.email })
     //   })
     //   if (res.status === 404) {
     //     recoveryErrors.email = 'Correo no encontrado'
     //   } else if (res.ok) {
     //     recoveryStep.value = 2
     //     startCountdown()
     //   }
     // } catch {
     //   recoveryErrors.email = 'Error al enviar el código'
     // }
   }

   recoveryLoading.value = false
 }

 //Fase 2, validar codigo
 async function handleRecoveryStep2() {
   recoveryErrors.code = ''
   if (!recovery.code) {
     recoveryErrors.code = 'Ingresa el código de verificación';
     return
   }
   recoveryLoading.value = true

   if (USE_MOCK) {
     //MOCK: cualquier codigo es valido
     await new Promise(r => setTimeout(r, 600))
     recoveryStep.value = 3
   } else {
     // TODO backend: POST /api/auth/recovery/validate/ { email, code }
     // try {
     //   const res = await fetch(`${API}/api/auth/recovery/validate/`, {
     //     method: 'POST',
     //     headers: { 'Content-Type': 'application/json' },
     //     body: JSON.stringify({ email: recovery.email, code: recovery.code })
     //   })
     //   if (res.status === 400) {
     //     recoveryErrors.code = 'Código inválido o expirado'
     //   } else if (res.ok) {
     //     recoveryStep.value = 3
     //   }
     // } catch {
     //   recoveryErrors.code = 'Error al verificar el código'
     // }
   }

   recoveryLoading.value = false
 }

 //Fase 2, reenviar codigo
 async function handleResend() {
   recoveryLoading.value = true

   if (USE_MOCK) {
     //MOCK: solo reiniciamos el contador
     await new Promise(r => setTimeout(r, 400))
     startCountdown()     
   } else {
     // TODO backend: POST /api/auth/recovery/request/ { email } (mismo endpoint)
     // await fetch(...)
     // startCountdown()
   }

   recoveryLoading.value = false
 }

 //Fase 3, nueva contrasena
 async function handleRecoveryStep3() {
   recoveryErrors.newPassword = ''
   recoveryErrors.confirmPassword = ''
   if (!recovery.newPassword) {
     recoveryErrors.newPassword = 'La contraseña es requerida';
     return
   }
   if (recovery.newPassword.length < 8) {
     recoveryErrors.newPassword = 'Mínimo 8 caracteres';
     return
   }
   if (!recovery.confirmPassword) {
     recoveryErrors.confirmPassword = 'Confirma tu contraseña';
     return
   }
   if (recovery.newPassword !== recovery.confirmPassword) {
     recoveryErrors.confirmPassword = 'Las contraseñas no coinciden';
     return
   }

   recoveryLoading.value = true

   if (USE_MOCK) {
     //MOCK: exito directo, mostrar checkmark, redirigir
     await new Promise(r => setTimeout(r, 600))
     recoveryStep.value = 4
     setTimeout(() => router.push('/auth'), 2000)
   } else {
     // TODO backend: POST /api/auth/recovery/reset/ { email, code, newPassword }
     // try {
     //   const res = await fetch(`${API}/api/auth/recovery/reset/`, {
     //     method: 'POST',
     //     headers: { 'Content-Type': 'application/json' },
     //     body: JSON.stringify({
     //       email:       recovery.email,
     //       code:        recovery.code,
     //       newPassword: recovery.newPassword
     //     })
     //   })
     //   if (res.ok) {
     //     recoveryStep.value = 4
     //     setTimeout(() => router.push('/auth'), 2000)
     //   }
     // } catch {
     //   recoveryErrors.confirmPassword = 'Error al cambiar la contraseña'
     // }
   }

   recoveryLoading.value = false
 }

 // Contenido del panel deslizante
 const slideContent = computed(() => {
   if (mode.value === 'login') return {
     title: '¿Aún no tienes cuenta?',
     sub: 'Crea tu cuenta y reserva tu lugar en el festival de luciérnagas',
     cta: 'Crear cuenta',
     action: () => setMode('signup'),
   }
   if (mode.value === 'signup') return {
     title: '¿Ya tienes una cuenta?',
     sub: 'Inicia sesión para ver tus reservaciones y explorar los parques',
     cta: 'Iniciar sesión',
     action: () => setMode('login'),
   }
   return {
     title: 'Recupera tu acceso',
     sub: 'Te enviaremos un código de verificación a tu correo registrado',
     cta: 'Volver al inicio',
     action: () => setMode('login'),
   }
 })
</script>

<style scoped>
 /* Fondo */
 .auth-scene {
   min-height: 100vh;
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 2rem 1rem;
   background:
     radial-gradient(ellipse at 20% 50%, rgba(123,216,176,0.12) 0%, transparent 50%),
     radial-gradient(ellipse at 80% 20%, rgba(232,255,122,0.07) 0%, transparent 45%),
     radial-gradient(ellipse at 60% 80%, rgba(123,216,176,0.06) 0%, transparent 40%),
     #07090A;
 }

 .auth-scene::before {
   content: '';
   position: absolute;
   inset: 0;
   background-image: v-bind("'url(' + bg + ')'");
   opacity: 0.45;
   z-index: 0;
 }
 
 /* Contenedor del forms  */
 .auth-card {
   position: relative;
   width: min(780px, 100%);
   height: 650px;
   border-radius: 24px;
   overflow: hidden;
   display: flex;
   background: rgba(255,255,255,0.03);
   border: 1px solid var(--color-border);
   box-shadow:
     0 0 0 1px rgba(232,255,122,0.04),
     0 32px 64px rgba(0,0,0,0.5);
 }

 /* Paneles de formulario */
 .form-panel {
   position: absolute;
   top: 0;
   width: 55%;
   height: 100%;
   display: flex;
   align-items: center;
   justify-content: center;
   transition: transform 0.65s cubic-bezier(.77,0,.18,1), opacity 0.4s ease;
   z-index: 2;
   background: transparent;
   backdrop-filter: blur(20px);
   -webkit-backdrop-filter: blur(20px);
 }

 .panel-login { left: 0; }

 .panel-signup,
 .panel-recovery { right: 0; left: auto; }
 
 /* Login visible por defecto */
 .mode-login  .panel-login    { transform: translateX(0);    opacity: 1; pointer-events: all }
 .mode-login  .panel-signup   { transform: translateX(110%); opacity: 0; pointer-events: none }
 .mode-login  .panel-recovery { transform: translateX(110%);opacity: 0; pointer-events: none }
 
 /* Signup form a la derecha, slide a la izquierda */
 .mode-signup .panel-login    { transform: translateX(-110%);opacity: 0; pointer-events: none }
 .mode-signup .panel-signup   { transform: translateX(0);    opacity: 1; pointer-events: all }
 .mode-signup .panel-recovery { transform: translateX(-110%);opacity: 0; pointer-events: none }
 
 /* Recovery */
 .mode-recovery .panel-login    { transform: translateX(-110%); opacity: 0; pointer-events: none }
 .mode-recovery .panel-signup   { transform: translateX(-110%); opacity: 0; pointer-events: none }
 .mode-recovery .panel-recovery { transform: translateX(0);     opacity: 1; pointer-events: all }


 .form-inner {
   width: 100%;
   padding: 2.5rem 2.5rem 2.5rem 2.5rem;
   display: flex;
   flex-direction: column;
   gap: 1rem;
 }

 .form-title {
   font-size: 26px;
   font-weight: 600;
   color: var(--color-bone);
   letter-spacing: -0.02em;
   line-height: 1.2;
 }

 .form-sub {
   font-size: 16px;
   color: var(--color-bone-soft);
   margin-top: -0.5rem;
 }

 .fields {
   display: flex;
   flex-direction: column;
   gap: 0.25rem;
 }

 .submit-btn {
   width: 100%;
   margin-top: 0.25rem;
 }

 .link-btn {
   background: none;
   border: none;
   color: var(--color-bone-mute);
   font-size: 14px;
   cursor: pointer;
   text-align: left;
   padding: 0;
   transition: color 0.2s;
   width: fit-content;
 }
 .link-btn:hover { color: var(--color-bone-soft) }

 .back-btn {
   text-align: center;
   width: 100%;
   margin-top: 0.25rem;
 }

 /* Panel deslizante */
 .slide-panel {
   position: absolute;
   top: 0;
   right: 0;
   width: 45%;
   height: 100%;
   background:
     radial-gradient(ellipse at 30% 40%, rgba(123,216,176,0.18) 0%, transparent 60%),
     radial-gradient(ellipse at 70% 70%, rgba(232,255,122,0.10) 0%, transparent 55%),
     #0d1a10;
   border-left: 1px solid rgba(123,216,176,0.15);
   z-index: 3;
   transition: transform 0.65s cubic-bezier(.77,0,.18,1), border-radius 0.65s ease;
   border-radius: 0 24px 24px 0;
   overflow: hidden;
 }

 /* Slide se mueve a la izquierda en signup y recovery */
 .mode-signup   .slide-panel,
 .mode-recovery .slide-panel {
   transform: translateX(-122%);
   border-radius: 24px 0 0 24px;
   border-left: none;
   border-right: 1px solid rgba(123,216,176,0.15);
 }

 .slide-inner {
   position: relative;
   height: 100%;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   padding: 2.5rem 2rem;
   gap: 1.5rem;
 }

 /* Texto del slide */
 .slide-text {
   text-align: center;
   display: flex;
   flex-direction: column;
   align-items: center;
   gap: 0.75rem;
 }

 .slide-title {
   font-size: 20px;
   font-weight: 600;
   color: var(--color-accent);
   line-height: 1.3;
   letter-spacing: -0.01em;
 }

 .slide-sub {
   font-size: 13px;
   color: rgba(232,255,122,0.5);
   line-height: 1.6;
   max-width: 200px;
 }

 .slide-cta {
   margin-top: 0.5rem;
   padding: 0.55rem 1.6rem;
   border-radius: 999px;
   border: 1.5px solid var(--color-accent);
   background: transparent;
   color: var(--color-accent);
   font-size: 13px;
   font-weight: 500;
   cursor: pointer;
   transition: background 0.2s, color 0.2s;
   letter-spacing: 0.02em;
 }
 .slide-cta:hover {
   background: var(--color-accent);
   color: #161D1A;
 }

 /* Transicion del contenido interno del slide */
 .slide-content-enter-active,
 .slide-content-leave-active {
   transition: opacity 0.25s ease, transform 0.25s ease;
 }
 .slide-content-enter-from {
   opacity: 0;
   transform: translateY(8px);
 }
 .slide-content-leave-to {
   opacity: 0;
   transform: translateY(-8px);
 }

 /* Particulas decorativas */
 .particle {
   position: absolute;
   border-radius: 50%;
   background: var(--color-accent);
   opacity: 0.15;
   animation: particle-drift 6s ease-in-out infinite;
 }
 .p1 { width: 4px;  height: 4px;  top: 20%; left: 15%; animation-delay: 0s }
 .p2 { width: 3px;  height: 3px;  top: 65%; left: 75%; animation-delay: 1.5s }
 .p3 { width: 5px;  height: 5px;  top: 45%; left: 85%; animation-delay: 3s }

 @keyframes particle-drift {
   0%, 100% {
     transform: translate(0, 0);
     opacity: 0.15;
   }
   33% {
     transform: translate(-6px, -10px);
     opacity: 0.4;
   }
   66% {
     transform: translate(8px, -5px);
     opacity: 0.2;
   }
 }

 /* Responsive */
 @media (max-width: 600px) {
   .auth-card {
     height: auto;
     flex-direction: column;
     border-radius: 16px;
   }
   .form-panel {
     position: relative;
     width: 100%;
     height: auto;
     transform: none !important;
     opacity: 1 !important;
     pointer-events: all !important;
   }
   .mode-login  .panel-signup,
   .mode-login  .panel-recovery,
   .mode-signup .panel-login,
   .mode-signup .panel-recovery,
   .mode-recovery .panel-login,
   .mode-recovery .panel-signup {
     display: none;
   }
   .slide-panel {
     position: relative;
     width: 100%;
     height: 160px;
     border-radius: 0 0 16px 16px !important;
     border-left: none !important;
     border-top: 1px solid rgba(123,216,176,0.15);
     transform: none !important;
   }
   .mode-signup .slide-panel,
   .mode-recovery .slide-panel {
     border-radius: 0 0 16px 16px !important;
   }
   .firefly-deco { display: none }
 }

 .email-highlight {
   color: var(--color-bone);
   font-weight: 500;
 }
 .resend-row {
   display: flex;
   align-items: center;gi
   min-height: 20px;
 }
 .resend-countdown {
   font-size: 12px;
   color: var(--color-bone-mute);
 }
 .link-btn:disabled { opacity: 0.4; cursor: not-allowed }
 .success-screen {
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   gap: 1rem;
   height: 100%;
   padding: 2rem 0;
 }
 .success-check { width: 80px; height: 80px }
 .check-path {
   stroke-dasharray: 50;
   stroke-dashoffset: 50;
   animation: draw-check 0.6s ease forwards 0.2s;
 }
 @keyframes draw-check { to { stroke-dashoffset: 0 } }
 .success-title {
   font-size: 20px;
   font-weight: 600;
   color: var(--color-bone);
 }
 .success-sub {
   font-size: 13px;
   color: var(--color-bone-soft);
   text-align: center;
 }
</style>
