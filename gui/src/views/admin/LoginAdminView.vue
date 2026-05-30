<template>
  <div class="admin-scene">
    <div class="admin-scene-bg" />

    <!-- Card de login -->
    <div class="admin-card">
      
      <!-- Marca -->
      <div class="admin-brand">
        <FireflyLogo :pulse="true" :drift="false" size="w-8 h-8" />
        <div class="admin-brand-text">
          <span class="admin-brand-name">Luciérnagas</span>
          <span class="admin-brand-label">Panel de Administración</span>
        </div>
      </div>
      
      <!-- Campos -->
      <div class="admin-fields">
        <div class="admin-field">
          <label class="admin-label">Correo electrónico</label>
          <input
            v-model="form.email"
            type="email"
            class="admin-input"
            :class="{ 'admin-input-error': errors.email }"
            placeholder="Ingresa tu correo electrónico"
            @input="errors.email = ''"
            @keydown.enter="handleLogin"
          />
          <span v-if="errors.email" class="admin-error-span">{{ errors.email }}</span>
        </div>
	
        <div class="admin-field">
          <label class="admin-label">Contraseña</label>
          <div class="admin-input-wrapper">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="admin-input"
              :class="{ 'admin-input-error': errors.password }"
              placeholder="Ingresa tu contraseña"
              @input="errors.password = ''"
              @keydown.enter="handleLogin"
            />
            <button class="admin-toggle-pass" tabindex="-1" @click="showPassword = !showPassword">
              <svg v-if="!showPassword" width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M1 7s2.5-5 6-5 6 5 6 5-2.5 5-6 5-6-5-6-5z" stroke="currentColor" stroke-width="1.3"/>
                <circle cx="7" cy="7" r="1.8" stroke="currentColor" stroke-width="1.3"/>
              </svg>
              <svg v-else width="14" height="14" viewBox="0 0 14 14" fill="none">
                <path d="M1 1l12 12M5.5 5.6A2 2 0 009.4 9.4M2.5 4C1.6 5 1 7 1 7s2.5 5 6 5c1 0 2-.3 2.8-.7M4 2.5C5 2.2 6 2 7 2c3.5 0 6 5 6 5s-.6 2-2 3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <span v-if="errors.password" class="admin-error-span">{{ errors.password }}</span>
        </div>
      </div>

      <!-- Acciones -->
      <div class="admin-actions">
        <button
          class="btn-admin-primary"
          :disabled="loading"
          @click="handleLogin">
          <span v-if="loading" class="admin-loading-dot" />
          {{ loading ? 'Accediendo...' : 'Acceder' }}
        </button>

        <RouterLink to="/auth" class="admin-exit-btn">
          Salir
        </RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
 import { ref, reactive } from 'vue'
 import { useRouter } from 'vue-router'
 import { useAuthStore } from '../../stores/auth'
 import { useNotification } from '../../composables/useNotification'
 import FireflyLogo from '../../components/ui/FireflyLogo.vue'

 const router = useRouter()
 const auth   = useAuthStore()
 const { show } = useNotification()

 const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
 const API = import.meta.env.VITE_API_URL || null

 const loading = ref(false)
 const showPassword = ref(false)

 const form = reactive({ email: '', password: '' })
 const errors = reactive({ email: '', password: '' })

 const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

 function validate(): boolean {
   errors.email = errors.password = ''
   if (!form.email || !EMAIL_RE.test(form.email)) {
     errors.email = 'Verifica la dirección de correo';
     return false
   }
   if (!form.password) {
     errors.password = 'Verifica la contraseña';
     return false
   }
   return true
 }

 async function handleLogin() {
   if (!validate())
     return
   
   loading.value = true
   try {
     if (USE_MOCK) {
       //MOCK: acceso admin directo
       await new Promise(r => setTimeout(r, 600))
       auth.setAuth('mock-admin-token-123', {
         id: 99,
         nombre: 'Admin',
         apellidos: 'Sistema',
         email: form.email,
         rol: 'ADMIN',
         is_staff: false,
         is_superuser: true,
         nivel_admin: 1,
	 parque_asignado: null,
       })
       router.push('/admin/reservaciones')
       return
     }

     // TODO backend: POST /auth/jwt/create/
     // El mismo endpoint la diferencia está en que el usuario retornado tiene rol='ADMIN'
     // try {
     //   const res = await fetch(`${API}/auth/jwt/create/`, {
     //     method: 'POST',
     //     headers: { 'Content-Type': 'application/json' },
     //     body: JSON.stringify({ email: form.email, password: form.password })
     //   })
     //   if (!res.ok) throw new Error('credentials')
     //   const tokens = await res.json()
     //   const userRes = await fetch(`${API}/auth/users/me/`, {
     //     headers: { Authorization: `Bearer ${tokens.access}` }
     //   })
     //   const userData = await userRes.json()
     //   if (userData.rol !== 'ADMIN') {
     //     show('error', 'Esta cuenta no tiene permisos de administrador')
     //     return
     //   }
     //   auth.setAuth(tokens.access, userData)
     //   router.push('/admin/reservaciones')
     // } catch {
     //   errors.email = 'Verifica la dirección de correo'
     //   errors.password = 'Verifica la contraseña'
     //   show('error', 'Correo o contraseña incorrectos')
     // }

   } finally {
     loading.value = false
   }
 }
</script>

<style scoped>
 /* Escena */
 .admin-scene {
   min-height: 100vh;
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 2rem 1rem;
   position: relative;
   background:
     radial-gradient(ellipse at 20% 50%, rgba(123,167,212,0.1) 0%, transparent 55%),
     radial-gradient(ellipse at 80% 20%, rgba(123,167,212,0.06) 0%, transparent 45%),
     #07100D;
 }
 .admin-scene-bg {
   position: absolute;
   inset: 0;
   background-image:
     radial-gradient(ellipse at 50% 100%, rgba(123,167,212,0.06) 0%, transparent 60%);
   pointer-events: none;
 }

 /* Card */
 .admin-card {
   position: relative;
   z-index: 1;
   width: min(420px, 100%);
   background: rgba(123,167,212,0.04);
   border: 1px solid rgba(123,167,212,0.15);
   border-radius: 20px;
   padding: 2.25rem;
   display: flex;
   flex-direction: column;
   gap: 1.75rem;
   box-shadow:
     0 32px 64px rgba(0,0,0,0.4),
     0 0 0 1px rgba(123,167,212,0.06);
   backdrop-filter: blur(20px);
 }

 /* Marca */
 .admin-brand {
   display: flex;
   align-items: center;
   gap: 0.75rem;
 }
 .admin-brand-text {
   display: flex;
   flex-direction: column;
   gap: 0.1rem;
 }
 .admin-brand-name {
   font-family: var(--font-serif);
   font-size: 18px;
   color: var(--color-bone);
   line-height: 1;
 }
 .admin-brand-label {
   font-size: 10px;
   font-family: var(--font-mono);
   text-transform: uppercase;
   letter-spacing: 0.1em;
   color: var(--color-admin-accent, #7BA7D4);
 }

 /* Campos */
 .admin-fields { display: flex; flex-direction: column; gap: 1rem; }
 .admin-field  { display: flex; flex-direction: column; gap: 0.3rem; }
 .admin-label  {
   font-size: 11px;
   font-family: var(--font-mono);
   text-transform: uppercase;
   letter-spacing: 0.08em;
   color: var(--color-bone-mute);
 }
 .admin-input-wrapper { position: relative; }
 .admin-input {
   width: 100%;
   height: 42px;
   padding: 0 0.875rem;
   border-radius: 10px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
   font-size: 13.5px;
   font-family: var(--font-sans);
   outline: none;
   transition: border-color 0.2s, background 0.2s;
 }
 .admin-input:focus {
   border-color: rgba(123,167,212,0.4);
   background: rgba(255,255,255,0.06);
 }
 .admin-input-error { border-color: rgba(255,138,123,0.4) !important; }
 .admin-input::placeholder { color: var(--color-bone-mute); }
 .admin-input-wrapper .admin-input { padding-right: 2.5rem; }
 .admin-toggle-pass {
   position: absolute;
   right: 10px; top: 50%;
   transform: translateY(-50%);
   background: none; border: none;
   color: var(--color-bone-mute); cursor: pointer;
   display: flex; align-items: center;
   transition: color 0.2s;
 }
 .admin-toggle-pass:hover { color: var(--color-bone-soft); }
 .admin-error-span {
   font-size: 11px;
   color: var(--color-danger);
 }

 /* Acciones */
 .admin-actions { display: flex; flex-direction: column; gap: 0.75rem; }
 .btn-admin-primary {
   width: 100%;
   height: 42px;
   border: none;
   border-radius: var(--radius-full);
   background: var(--color-admin-accent, #7BA7D4);
   color: #0A1525;
   font-size: 14px;
   font-weight: 600;
   font-family: var(--font-sans);
   cursor: pointer;
   transition: all var(--transition-normal);
   display: flex;
   align-items: center;
   justify-content: center;
   gap: 0.5rem;
   box-shadow: 0 0 15px rgba(123,167,212,0.35);
 }
 .btn-admin-primary:hover:not(:disabled) {
   box-shadow: 0 0 25px rgba(123,167,212,0.5);
   transform: translateY(-1px);
 }
 .btn-admin-primary:disabled { opacity: 0.6; cursor: not-allowed; }

 .admin-exit-btn {
   text-align: center;
   font-size: 13px;
   color: var(--color-bone-mute);
   text-decoration: none;
   transition: color 0.2s;
 }
 .admin-exit-btn:hover { color: var(--color-bone-soft); }

 /* Loading dot */
 .admin-loading-dot {
   width: 6px; height: 6px;
   border-radius: 50%;
   background: #0A1525;
   animation: blink 0.9s ease infinite;
 }
 @keyframes blink {
   0%, 100% { opacity: 1 } 50% { opacity: 0.3 }
 }
</style>
