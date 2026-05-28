<template>
  <div class="auth-scene">
    <RouterLink to="/admin/login" class="admin-access-link">
      Acceso Admin
    </RouterLink>
    
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

        <div class="flex items-center gap-3">
          <div class="strength flex-1">
            <span :style="`width:${strength.pct}%; background:${strength.color}`"></span>
          </div>
          <span class="text-[11px] font-mono uppercase tracking-[0.14em]" :style="`color:${strength.color}`">{{ strength.label }}</span>
        </div>
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
	      :loading="recoveryLoading"
	      class="submit-btn"
	      @click="handleRecoveryStep1">
	      Enviar enlace
	    </AppButton>
	  </template>

	  <!-- Fase 2: codigo de validacion -->
          <template v-else-if="recoveryStep === 2">
	    <h1 class="form-title">Revisa tu correo</h1>
	    <p class="form-sub">
	      Enviamos un enlace a
	      <strong class="email-highlight">{{ recovery.email }}</strong>.
	      Haz click en él para continuar.
	    </p>
	    <p class="form-sub" style="margin-top: 0.5rem; font-size: 13px;">
	      El enlace expira en 24 horas.
	    </p>
	    <AppButton
	      variant="primary"
	      :loading="recoveryLoading"
	      class="submit-btn"
	      @click="handleResend">
	      {{ recoveryLoading ? 'Reenviando...' : 'Reenviar enlace' }}
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
	    <div class="success-screen">
	      <svg class="success-check" viewBox="0 0 80 80" fill="none">
		<circle cx="40" cy="40" r="38" stroke="#7BD8B0" stroke-width="2" stroke-opacity="0.3"/>
		<circle cx="40" cy="40" r="30" fill="#7BD8B0" fill-opacity="0.08"/>
		<path d="M24 40l11 11 21-22" stroke="#7BD8B0" stroke-width="3"
		      stroke-linecap="round" stroke-linejoin="round" class="check-path"/>
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
 import { zxcvbn, Match } from '@zxcvbn-ts/core';

 const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
 const router = useRouter()
 const bg = bgImage
 
 type Mode = 'login' | 'signup' | 'recovery'
 
 const props = defineProps<{
   initialMode?: Mode
   loading?: boolean
   loginError?: 'credentials' | null
   signupError?: 'email_in_use' | null
   signupPasswordError?: string | null
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
 // Cuando AuthView informa error de contraseña en signup
 watch(() => props.signupPasswordError, (err) => {
   if (err) {
     signupErrors.password = err
   }
 })
 
 const login = reactive({ email: '', password: '' })
 const signup = reactive({ nombre: '', apellidos: '', email: '', password: '' })
 const loginErrors = reactive({ email: '', password: '' })
 const signupErrors = reactive({ nombre: '', apellidos: '', email: '', password: '' })

 const recoveryStep = ref(1)
 const recoveryLoading = ref(false)
 const recovery = reactive({
   email: ''
 })
 
 const recoveryErrors = reactive({
   email: ''
 })
 
 const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

 function setMode(m: Mode) {
   mode.value = m
   if (m === 'recovery') {
     recoveryStep.value = 1
     recovery.email       = ''
     recoveryErrors.email = ''
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
   signupErrors.password = validatePassword(signup.password, signup.email) || ''
   return !signupErrors.nombre && !signupErrors.apellidos && !signupErrors.email && !signupErrors.password
 }

const strength = computed(() => {
  const p = signup.password || '';
  const email = signup.email || '';
  if (!p || p.length < 8) {
    return { pct: 0, label: '—', color: '#5C645F' };
  }
  if (/^\d+$/.test(p)) {
    return { pct: 25, label: 'Muy Débil', color: '#FF8A7B' };
  }

  const emailUser = email ? email.split('@')[0] : '';
  const emailLimpio = emailUser.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
  const result = zxcvbn(p, [email, emailUser, emailLimpio]);
  const score = result.score;
  const pclean = p.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
  const emailClean = emailLimpio.replace(/[0-9]/g, '');
  if (emailClean && pclean.includes(emailClean)) {
    return { pct: 25, label: 'Muy Débil', color: '#FF8A7B' };
  }
  
  const map = [
    { pct: 25,  label: 'Muy Débil', color: '#FF8A7B' }, 
    { pct: 40,  label: 'Débil',     color: '#FFB87B' }, 
    { pct: 60,  label: 'Aceptable', color: '#E8FF7A' }, 
    { pct: 80,  label: 'Buena',     color: '#7BD8B0' }, 
    { pct: 100, label: 'Excelente', color: '#7BD882' },
  ];

  return map[score];
});

function validatePassword(password: string, email: string) {
  if (!password) {
    return 'La contraseña es requerida';
  }
  if (password.length < 8) {
    return 'Mínimo 8 caracteres';
  }
  if (/^\d+$/.test(password)) {
    return 'La contraseña no puede contener solo números';
  }
  if (!/[A-Z]/.test(password)) {
    return 'Debe incluir al menos una mayúscula';
  }
  if (!/[a-z]/.test(password)) {
    return 'Debe incluir al menos una minúscula';
  }
  if (!/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/.test(password)) {
    return 'Debe incluir al menos un símbolo';
  }
  if (!/\d/.test(password)) {
    return 'Debe incluir al menos un número';
  }
  
  const nombreEmail = email.split('@')[0];
  const emailLimpio = nombreEmail.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
  const resultadoZxcvbn = zxcvbn(password, [email, nombreEmail, emailLimpio]);

  if (resultadoZxcvbn.score < 2) {
    const coincidioConEmail = resultadoZxcvbn.sequence.some(
      (seq: Match) => seq.dictionaryName === 'user_inputs'
    );

    if (coincidioConEmail) {
      return 'La contraseña no puede ser similar a tu correo electrónico';
    }
    return 'La contraseña es demasiado común o fácil de adivinar';
  }
  const pClean = password.toLowerCase().replace(/[^a-zA-Z0-9]/g, '');
  const emailClean = emailLimpio.replace(/[0-9]/g, '');
  if (emailClean && pClean.includes(emailClean)) {
    return 'La contraseña no puede ser similar a tu correo electrónico';
  }

  const passStrength = strength.value;
  if (passStrength.pct < 60) {
    return 'La contraseña es demasiado débil. ' + passStrength.label;
  }

  return '';
}

 function handleLogin() {
   if (validateLogin())
     emit('login', login.email, login.password)
 }
 function handleSignup() {
   if (validateSignup())
     emit('signup', signup.nombre, signup.apellidos, signup.email, signup.password)
 }

 //Fase 1: solicitar enlace
 async function handleRecoveryStep1() {
   recoveryErrors.email = ''
   if (!recovery.email) {
     recoveryErrors.email = 'El correo es requerido';
     return
   }
   if (!EMAIL_RE.test(recovery.email)) {
     recoveryErrors.email = 'Formato de correo inválido';
     return
   }
   
   recoveryLoading.value = true
   
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 600))
     recoveryStep.value = 2
   } else {
     // BACKEND: POST /auth/users/reset_password/
     // try {
     //   const res = await fetch(`${API}/auth/users/reset_password/`, {
     //     method: 'POST',
     //     headers: { 'Content-Type': 'application/json' },
     //     body: JSON.stringify({ email: recovery.email })
     //   })
     //   // Djoser responde 204 siempre por seguridad
     //   if (res.ok || res.status === 204) recoveryStep.value = 2
     // } catch {
     //   recoveryErrors.email = 'Error al enviar el correo'
     // }
   }
   
   recoveryLoading.value = false
 }
 
 //Reenviar enlace, mismo endpoint
 async function handleResend() {
   recoveryLoading.value = true
   
   if (USE_MOCK) {
     await new Promise(r => setTimeout(r, 400))
   } else {
     // BACKEND: POST /auth/users/reset_password/ { email: recovery.email }
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

 .admin-access-link {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 10;
  font-size: 11.5px;
  font-family: var(--font-mono);
  letter-spacing: 0.05em;
  color: var(--color-bone-mute);
  text-decoration: none;
  padding: 0.35rem 0.85rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  transition: color 0.2s, border-color 0.2s;
}
 .admin-access-link:hover {
   color: var(--color-admin-accent);
   border-color: rgba(123,167,212,0.3);
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

 .strength {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.strength span {
  display: block;
  height: 100%;
  transition: width 0.3s ease, background-color 0.3s ease;
}
</style>
