<template>
  <div class="reset-scene">
    <div class="reset-card">

      <!-- Formulario nueva contraseña -->
      <template v-if="step === 1">
        <h1 class="form-title">Nueva contraseña</h1>
        <p class="form-sub">Elige una contraseña segura</p>

        <div class="fields">
          <AppInput
            v-model="newPassword"
            label="Nueva contraseña"
            placeholder="Mínimo 8 caracteres"
            type="password"
            :icon="true"
            icon-name="lock"
            :error="errors.newPassword"
            @input="errors.newPassword = ''"/>
          <AppInput
            v-model="confirmPassword"
            label="Confirmar contraseña"
            placeholder="Repite la contraseña"
            type="password"
            :icon="true"
            icon-name="lock"
            :error="errors.confirmPassword"
            @input="errors.confirmPassword = ''"/>

          <div class="flex items-center gap-3">
            <div class="strength flex-1">
              <span :style="`width:${strength.pct}%; background:${strength.color}`"></span>
            </div>
            <span class="text-[11px] font-mono uppercase tracking-[0.14em]" :style="`color:${strength.color}`">{{ strength.label }}</span>
          </div>
        </div>

        <AppButton variant="primary" :loading="loading" class="submit-btn" @click="handleSubmit">
          Cambiar contraseña
        </AppButton>
      </template>

      <!-- Éxito -->
      <template v-else-if="step === 2">
        <div class="success-screen">
          <svg class="success-check" viewBox="0 0 80 80" fill="none">
            <circle cx="40" cy="40" r="38" stroke="#7BD8B0" stroke-width="2" stroke-opacity="0.3"/>
            <circle cx="40" cy="40" r="30" fill="#7BD8B0" fill-opacity="0.08"/>
            <path d="M24 40l11 11 21-22" stroke="#7BD8B0" stroke-width="3"
              stroke-linecap="round" stroke-linejoin="round" class="check-path"/>
          </svg>
          <h2 class="success-title">Contraseña cambiada</h2>
          <p class="success-sub">Redirigiendo al inicio de sesión...</p>
        </div>
      </template>

      <!-- Link inválido o sin params -->
      <template v-else-if="step === 0">
        <h1 class="form-title">Enlace inválido</h1>
        <p class="form-sub">Usa el enlace del correo o solicita uno nuevo.</p>
        <AppButton variant="outline" class="submit-btn" @click="router.push('/auth?mode=recovery')">
          Solicitar nuevo enlace
        </AppButton>
      </template>

    </div>
  </div>
</template>

<script setup lang="ts">
 import { ref, reactive, computed } from 'vue'
 import { useRoute, useRouter } from 'vue-router'
 import AppInput  from '../components/ui/AppInput.vue'
 import AppButton from '../components/ui/AppButton.vue'
 import { useNotification } from '../composables/useNotification'
 import { getPasswordStrength, validatePassword } from '../utils/password.ts'

 const route  = useRoute()
 const router = useRouter()
 const { show } = useNotification()

 const API      = import.meta.env.VITE_API_URL || null
 const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

 const uid   = route.params.uid   as string
 const token = route.params.token as string

 // 0 = link inválido, 1 = formulario, 2 = éxito
 const step = ref(uid && token ? 1 : 0)

 const loading         = ref(false)
 const newPassword     = ref('')
 const confirmPassword = ref('')
 const errors = reactive({ newPassword: '', confirmPassword: '' })

 const strength = computed(() => 
  getPasswordStrength(newPassword.value, '')
);

 async function handleSubmit() {
   errors.newPassword     = ''
   errors.confirmPassword = ''

   const passwordError = validatePassword( newPassword.value, '');
   if (passwordError) {
     errors.newPassword = passwordError;
     return;
   }
   if (!confirmPassword.value)
   { errors.confirmPassword = 'Confirma tu contraseña'; return }
   if (newPassword.value !== confirmPassword.value)
   { errors.confirmPassword = 'Las contraseñas no coinciden'; return }

   loading.value = true

   if (USE_MOCK) {
     // MOCK: éxito directo
     await new Promise(r => setTimeout(r, 600))
     step.value = 2
     setTimeout(() => router.push('/auth'), 2500)
   } else {
     // BACKEND: POST /auth/users/reset_password_confirm/
     try {
       const res = await fetch(`${API}/auth/users/reset_password_confirm/`, {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({
           uid:          uid,
           token:        token,
           new_password: newPassword.value
         })
       })
       if (res.ok || res.status === 204) {
         step.value = 2
         setTimeout(() => router.push('/auth'), 2500)
       } else {
         const data = await res.json()
         // Djoser puede devolver errores en token, uid o new_password
         if (data.token || data.uid) {
           show('error', 'El enlace expiró o ya fue usado. Solicita uno nuevo')
           step.value = 0
         } else if (data.new_password) {
           errors.newPassword = data.new_password[0] ?? 'Contraseña inválida'
         }
       }
     } catch {
       show('error', 'Error al cambiar la contraseña. Intenta de nuevo')
     }
   }

   loading.value = false
 }
</script>

<style scoped>
 .reset-scene {
   min-height: 100vh;
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 2rem 1rem;
   background:
     radial-gradient(ellipse at 20% 50%, rgba(123,216,176,0.12) 0%, transparent 50%),
     radial-gradient(ellipse at 80% 20%, rgba(232,255,122,0.07) 0%, transparent 45%),
     #07090A;
 }
 .reset-card {
   width: min(420px, 100%);
   background: rgba(255,255,255,0.03);
   border: 1px solid var(--color-border);
   border-radius: 24px;
   padding: 2.5rem;
   display: flex;
   flex-direction: column;
   gap: 1rem;
   box-shadow: 0 32px 64px rgba(0,0,0,0.5);
 }
 .form-title {
   font-size: 26px; font-weight: 600;
   color: var(--color-bone); letter-spacing: -0.02em;
 }
 .form-sub {
   font-size: 14px; color: var(--color-bone-soft);
   line-height: 1.5; margin-top: -0.25rem;
 }
 .fields { display: flex; flex-direction: column; gap: 0.25rem; }
 .submit-btn { width: 100%; margin-top: 0.25rem; }
 .success-screen {
   display: flex; flex-direction: column;
   align-items: center; gap: 1rem;
   padding: 1.5rem 0; text-align: center;
 }
 .success-check { width: 72px; height: 72px; }
 .check-path {
   stroke-dasharray: 50; stroke-dashoffset: 50;
   animation: draw-check 0.6s ease forwards 0.2s;
 }
 @keyframes draw-check { to { stroke-dashoffset: 0 } }
 .success-title { font-size: 20px; font-weight: 600; color: var(--color-bone); }
 .success-sub   { font-size: 13px; color: var(--color-bone-soft); }
</style>
