<template>
  <div class="profile-view">
    <div class="profile-inner">

      <!-- Columna izquierda: datos del usuario -->
      <div class="profile-card">

        <!-- Foto de perfil -->
        <div class="avatar-section">
          <div class="avatar-wrapper" @click="triggerFileInput">
            <img
              v-if="avatarPreview || (user as any)?.avatar"
	      :src="avatarPreview || (user as any).avatar"
              :alt="user.nombre"
              class="avatar-img"
            />
            <img
              v-else
              src="../assets/profile_white.svg"
              alt="Foto de perfil"
              class="avatar-img avatar-default"
            />
	    <!-- Overlay al hacer hover -->
	    <div class="avatar-overlay">
	      <IconEdit size="18px" />
	      <span>Cambiar foto</span>
	    </div>
	  </div>
	  
	  <!-- Input oculto -->
	  <input
	    ref="fileInput"
	    type="file"
	    accept="image/*"
	    class="avatar-file-input"
	    @change="handleFileChange"
	  />
          <div class="avatar-name">
            {{ user?.nombre }} {{ user?.apellidos }}
          </div>
          <div class="avatar-email">
	    {{ user?.email }}
	  </div>
        </div>

        <div class="divider" />

        <!-- Campos editables -->
        <div class="fields-section">

          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Nombre</span>
              <input
                v-model="form.nombre"
                :disabled="!editing.nombre"
                :class="['field-input', { 'field-input-active': editing.nombre }]"
                placeholder="Tu nombre"
              />
              <span v-if="errors.nombre" class="field-error">{{ errors.nombre }}</span>
            </div>
            <button class="edit-btn" :class="{ active: editing.nombre }" @click="toggleEdit('nombre')">
              <IconEdit />
            </button>
          </div>

          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Apellidos</span>
              <input
                v-model="form.apellidos"
                :disabled="!editing.apellidos"
                :class="['field-input', { 'field-input-active': editing.apellidos }]"
                placeholder="Tus apellidos"
              />
              <span v-if="errors.apellidos" class="field-error">{{ errors.apellidos }}</span>
            </div>
            <button class="edit-btn" :class="{ active: editing.apellidos }" @click="toggleEdit('apellidos')">
              <IconEdit />
            </button>
          </div>

          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Correo electrónico</span>
              <input
                v-model="form.email"
                :disabled="!editing.email"
                :class="['field-input', { 'field-input-active': editing.email }]"
                type="email"
                placeholder="tu@correo.com"
              />
              <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
            </div>
            <button class="edit-btn" :class="{ active: editing.email }" @click="toggleEdit('email')">
              <IconEdit />
            </button>
          </div>

          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Género</span>
              <select
                v-model="form.genero"
                :disabled="!editing.genero"
                :class="['field-input field-select', { 'field-input-active': editing.genero }]">
                <option value="">Sin especificar</option>
                <option value="M">Masculino</option>
                <option value="F">Femenino</option>
                <option value="NB">No binario</option>
                <option value="NE">Prefiero no decir</option>
              </select>
            </div>
            <button class="edit-btn" :class="{ active: editing.genero }" @click="toggleEdit('genero')">
              <IconEdit />
            </button>
          </div>

          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Fecha de nacimiento</span>
              <input
                v-model="form.fecha_nacimiento"
                :disabled="!editing.fecha_nacimiento"
                :class="['field-input', { 'field-input-active': editing.fecha_nacimiento }]"
                type="date"
                style="color-scheme: dark"
              />
            </div>
            <button class="edit-btn" :class="{ active: editing.fecha_nacimiento }" @click="toggleEdit('fecha_nacimiento')">
              <IconEdit />
            </button>
          </div>

          <div class="field-row">
            <div class="field-content">
              <span class="field-label">Método de pago preferido</span>
              <div v-if="!editing.metodo_pago" class="pm-preview">
		<PaymentMethodBadge :method="form.metodo_pago" />
	      </div>
              <select
		v-else
		v-model="form.metodo_pago"
		class="field-input field-select field-input-active">
		<option value="">Sin configurar</option>
		<option value="PAYPAL">PayPal</option>
		<option value="STRIPE">Stripe</option>
		<option value="DEBITO">Tarjeta de débito</option>
		<option value="CREDITO">Tarjeta de crédito</option>
	      </select>
	    </div>
            <button class="edit-btn" :class="{ active: editing.metodo_pago }" @click="toggleEdit('metodo_pago')">
              <IconEdit />
            </button>
          </div>

        </div>

        <!-- Boton guardar -->
        <AppButton
          variant="primary"
          :loading="saving"
          class="save-btn"
          @click="handleSave">
          Guardar cambios
        </AppButton>

      </div>

      <!-- Columna derecha: datos de la cuenta -->
      <div class="account-card">

        <!-- Tipo de cuenta -->
        <div class="account-section">
          <h2 class="account-title">Datos de la cuenta</h2>
          <div class="account-row">
            <span class="account-label">Tipo de cuenta</span>
            <span class="account-badge" :class="user?.rol === 'ADMIN' ? 'badge-admin' : 'badge-cliente'">
              {{ user?.rol === 'ADMIN' ? 'Administrador' : 'Cliente' }}
            </span>
          </div>
          <div class="account-row">
            <span class="account-label">Miembro desde</span>
            <span class="account-value">{{ formatDate(user?.created_at) }}</span>
          </div>
          <div class="account-row">
            <span class="account-label">Método de pago</span>
	    <PaymentMethodBadge :method="user?.metodo_pago" />
          </div>
        </div>

        <div class="divider" />

        <!-- Estadisticas de reservaciones -->
        <div class="account-section">
          <h2 class="account-title">Reservaciones</h2>

          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-number">{{ stats.total }}</span>
              <span class="stat-label">Total</span>
            </div>
            <div class="stat-card stat-activa">
              <span class="stat-number">{{ stats.activas }}</span>
              <span class="stat-label">Activas</span>
            </div>
            <div class="stat-card stat-proceso">
              <span class="stat-number">{{ stats.en_proceso }}</span>
              <span class="stat-label">En proceso</span>
            </div>
            <div class="stat-card stat-cancelada">
              <span class="stat-number">{{ stats.canceladas }}</span>
              <span class="stat-label">Canceladas</span>
            </div>
          </div>

          <AppButton
            variant="outline"
            class="ver-reservaciones-btn"
            @click="router.push('/reservaciones')">
            Ver mis reservaciones
          </AppButton>
        </div>

        <div class="divider" />

        <!-- Eliminar cuenta -->
        <div class="account-section">
	  <button class="delete-btn" @click="showDeleteDialog = true">
            Eliminar cuenta
          </button>
          <p class="danger-desc">
            Eliminar tu cuenta es una acción irreversible. Todos tus datos y reservaciones serán eliminados permanentemente y no se otorgará ningún reembolso.
          </p>
        </div>
      </div>

    </div>

    <!-- Dialogo eliminar cuenta -->
    <AppConfirmDialog
      v-model="showDeleteDialog"
      title="Eliminar cuenta"
      confirm-label="Sí, eliminar mi cuenta"
      variant="danger"
      @confirm="handleDeleteAccount">
      ¿Estás seguro de que quieres eliminar tu cuenta? Esta acción es
      <strong>irreversible</strong> y elimina todos tus datos y reservaciones sin opción de reembolsos.
    </AppConfirmDialog>

  </div>
</template>

<script setup lang="ts">
 import { ref, reactive, computed, onMounted } from 'vue'
 import { useRouter } from 'vue-router'
 import { useAuthStore } from '../stores/auth'
 import { useReservationsStore } from '../stores/reservations'
 import { reserveService } from '../services/reserveService'
 import { useNotification } from '../composables/useNotification'
 import AppButton from '../components/ui/AppButton.vue'
 import IconEdit  from '../components/svg/IconEdit.vue'
 import AppConfirmDialog from '../components/ui/AppConfirmDialog.vue'
 import PaymentMethodBadge from '../components/ui/PaymentMethodBadge.vue'

 const router = useRouter()
 const auth = useAuthStore()
 const reservationsStore = useReservationsStore()
 const { show } = useNotification()

 const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
 const API = import.meta.env.VITE_API_URL || null

 const user = computed(() => auth.user)
 const saving = ref(false)
 const showDeleteDialog = ref(false)

 const fileInput    = ref<HTMLInputElement | null>(null)
 const avatarPreview = ref<string | null>(null)
 
 function triggerFileInput() {
   fileInput.value?.click()
 }
 
 function handleFileChange(event: Event) {
   const file = (event.target as HTMLInputElement).files?.[0]
   if (!file)
     return
   
   // Preview local inmediato
   const reader = new FileReader()
   reader.onload = (e) => { avatarPreview.value = e.target?.result as string }
   reader.readAsDataURL(file)
   
   // TODO backend: subir imagen
   // const formData = new FormData()
   // formData.append('avatar', file)
   // await fetch(`${API}/auth/users/me/avatar/`, {
   //   method: 'PATCH',
   //   headers: { Authorization: `Bearer ${auth.token}` },
   //   body: formData
   // })
 }
 
 //Formulario
 const form = reactive({
   nombre: user.value?.nombre ?? '',
   apellidos: user.value?.apellidos ?? '',
   email: user.value?.email ?? '',
   genero: (user.value as any)?.genero ?? '',
   fecha_nacimiento: (user.value as any)?.fecha_nacimiento ?? '',
   metodo_pago: user.value?.metodo_pago ?? '',
 })

 const errors = reactive({
   nombre: '', apellidos: '', email: '',
   genero: '', fecha_nacimiento: '', metodo_pago: '',
 })

 //Estado de edicion por campo
 const editing = reactive({
   nombre: false, apellidos: false, email: false,
   genero: false, fecha_nacimiento: false, metodo_pago: false,
 })

 function toggleEdit(field: keyof typeof editing) {
   editing[field] = !editing[field]
   if (!editing[field])
     errors[field] = ''
 }

 //Validacion
 const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

 function validate(): boolean {
   let ok = true
   errors.nombre = errors.apellidos = errors.email = ''
   if (!form.nombre || form.nombre.length < 2) {
     errors.nombre = 'Mínimo 2 caracteres';
     ok = false
   }
   if (!form.apellidos || form.apellidos.length < 2) {
     errors.apellidos = 'Mínimo 2 caracteres';
     ok = false
   }
   if (!form.email || !EMAIL_RE.test(form.email)) {
     errors.email = 'Correo inválido';
     ok = false
   }
   return ok
 }

 //Guardar
 async function handleSave() {
   if (!validate())
     return
   saving.value = true
   if (USE_MOCK) {
     //MOCK: actualiza el store local
     await new Promise(r => setTimeout(r, 600))
     auth.user!.nombre    = form.nombre
     auth.user!.apellidos = form.apellidos
     auth.user!.email     = form.email
     auth.user!.metodo_pago = form.metodo_pago as any
     //Cierra todos los campos en edicion
     Object.keys(editing).forEach(k => (editing as any)[k] = false)
     show('exito', 'Perfil actualizado correctamente')
   } else {
     // TODO backend: PATCH /auth/users/me/
     // try {
     //   const res = await fetch(`${API}/auth/users/me/`, {
     //     method: 'PATCH',
     //     headers: {
     //       'Content-Type': 'application/json',
     //       Authorization: `Bearer ${auth.token}`
     //     },
     //     body: JSON.stringify({
     //       nombre:           form.nombre,
     //       apellidos:        form.apellidos,
     //       email:            form.email,
     //       genero:           form.genero,
     //       fecha_nacimiento: form.fecha_nacimiento,
     //       metodo_pago:      form.metodo_pago,
     //     })
     //   })
     //   if (!res.ok) throw new Error()
     //   const updated = await res.json()
     //   auth.setAuth(auth.token!, updated)
     //   Object.keys(editing).forEach(k => (editing as any)[k] = false)
     //   show('exito', 'Perfil actualizado correctamente')
     // } catch {
     //   show('error', 'Error al guardar los datos')
     // }
   }
   saving.value = false
 }

 //Eliminar cuenta
 async function handleDeleteAccount() {
   if (USE_MOCK) {
     //MOCK: cierra sesion y redirige
     showDeleteDialog.value = false
     auth.clearAuth()
     show('normal', 'Cuenta eliminada')
     router.push('/')
   } else {
     // TODO backend: DELETE /auth/users/me/
     // try {
     //   const res = await fetch(`${API}/auth/users/me/`, {
     //     method: 'DELETE',
     //     headers: { Authorization: `Bearer ${auth.token}` }
     //   })
     //   if (!res.ok) throw new Error()
     //   showDeleteDialog.value = false
     //   auth.clearAuth()
     //   show('normal', 'Cuenta eliminada')
     //   router.push('/')
     // } catch {
     //   show('error', 'Error al eliminar la cuenta')
     // }
   }
 }

 //Estadisticas reservaciones
 const stats = computed(() => {
   const all = reservationsStore.reservaciones
   return {
     total: all.length,
     activas: all.filter(r => r.estado === 'ACTIVA').length,
     en_proceso: all.filter(r => r.estado === 'EN_PROCESO').length,
     canceladas: all.filter(r => r.estado === 'CANCELADA').length,
   }
 })

 //Helpers
 const metodoPagoMap: Record<string, string> = {
   PAYPAL: 'PayPal',
   STRIPE: 'Stripe',
   DEBITO: 'Tarjeta de débito',
   CREDITO: 'Tarjeta de crédito',
 }
 const metodoPagoLabel = computed(() =>
   metodoPagoMap[user.value?.metodo_pago ?? ''] ?? 'Sin configurar'
 )

 function formatDate(dateStr?: string | null): string {
   if (!dateStr)
     return 'N/A'
   const d = new Date(dateStr)
   const months = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic']
   return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`
 }

 onMounted(async () => {
   if (!reservationsStore.reservaciones.length)
     await reserveService.getReservaciones()
 })
</script>

<style scoped>
 .profile-view {
   min-height: calc(100vh - 80px);
   margin-top: 80px;
   display: flex;
   justify-content: center;
   padding: 2rem 1.5rem;
   box-sizing: border-box;
 }

 .profile-inner {
   width: 100%;
   max-width: 82.5rem;
   display: grid;
   grid-template-columns: 1fr 1fr;
   gap: 1.5rem;
   align-items: start;
 }

 @media (max-width: 768px) {
   .profile-inner { grid-template-columns: 1fr; }
 }

 /* Cards */
 .profile-card,
 .account-card {
   background: rgba(255,255,255,0.02);
   border: 1px solid var(--color-border);
   border-radius: 16px;
   padding: 1.75rem;
   display: flex;
   flex-direction: column;
   gap: 1.25rem;
 }

 .divider {
   height: 1px;
   background: var(--color-border);
   margin: 0 -1.75rem;
 }

 /* Avatar */
 .avatar-section {
   display: flex;
   flex-direction: column;
   align-items: center;
   gap: 0.5rem;
 }
 .avatar-wrapper {
   position: relative;
   width: 160px;
   height: 160px;
   border-radius: 50%;
   cursor: pointer;
   overflow: hidden;
   border: 2px solid var(--color-border);
   transition: border-color 0.2s;
 }
 .avatar-wrapper:hover {
   border-color: rgba(123,216,176,0.4);
 }
 .avatar-img {
   width: 100%;
   height: 100%;
   object-fit: cover;
   display: block;
 }
 .avatar-default {
   background: rgba(123,216,176,0.08);
   padding: 20px;
   box-sizing: border-box;
 }
 .avatar-overlay {
   position: absolute;
   inset: 0;
   background: rgba(0,0,0,0.55);
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   gap: 0.3rem;
   color: var(--color-bone);
   font-size: 11px;
   opacity: 0;
   transition: opacity 0.2s;
 }
 .avatar-wrapper:hover .avatar-overlay {
   opacity: 1;
 }
 .avatar-file-input { display: none; }
 .avatar-name {
   font-size: 16px;
   font-weight: 600;
   color: var(--color-bone);
   margin-top: 0.5rem;
 }
 .avatar-email { font-size: 12px; color: var(--color-bone-mute); }

 /* Campos editables */
 .fields-section { display: flex; flex-direction: column; gap: 0.75rem; }

 .field-row {
   display: flex;
   align-items: flex-end;
   gap: 0.5rem;
 }
 .field-content { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; }
 .field-label {
   font-size: 10.5px;
   color: var(--color-bone-mute);
   font-family: var(--font-mono);
   text-transform: uppercase;
   letter-spacing: 0.08em;
 }
 .field-input {
   width: 100%;
   padding: 0.5rem 0.75rem;
   border-radius: 8px;
   border: 1px solid transparent;
   background: transparent;
   color: var(--color-bone-soft);
   font-size: 13.5px;
   font-family: var(--font-sans);
   outline: none;
   transition: all 0.2s;
   cursor: default;
 }
 .field-input:disabled { color: var(--color-bone-soft); cursor: default; }
 .field-input-active {
   border-color: rgba(123,216,176,0.3);
   background: rgba(255,255,255,0.04);
   color: var(--color-bone);
   cursor: text;
 }
 .field-select { appearance: none; cursor: default; }
 .field-select.field-input-active { cursor: pointer; }
 .field-error { font-size: 11px; color: var(--color-danger); }

 .edit-btn {
   flex-shrink: 0;
   width: 30px;
   height: 30px;
   border-radius: 8px;
   border: 1px solid var(--color-border);
   background: transparent;
   color: var(--color-bone-mute);
   cursor: pointer;
   display: flex;
   align-items: center;
   justify-content: center;
   transition: all 0.15s;
   margin-bottom: 2px;
 }
 .edit-btn:hover { color: var(--color-bone); background: rgba(255,255,255,0.05); }
 .edit-btn.active {
   color: var(--color-green);
   border-color: rgba(123,216,176,0.3);
   background: rgba(123,216,176,0.06);
 }

 .save-btn { width: 100%; margin-top: 0.25rem; }

 /* Cuenta */
 .account-section { display: flex; flex-direction: column; gap: 0.75rem; }
 .account-title {
   font-size: 14px;
   font-weight: 600;
   color: var(--color-bone);
   letter-spacing: -0.01em;
 }
 .account-row {
   display: flex;
   justify-content: space-between;
   align-items: center;
   gap: 1rem;
 }
 .account-label { font-size: 12.5px; color: var(--color-bone-mute); }
 .account-value { font-size: 12.5px; color: var(--color-bone-soft); }
 .account-badge {
   font-size: 11px;
   font-weight: 600;
   padding: 0.2rem 0.6rem;
   border-radius: 999px;
   letter-spacing: 0.03em;
 }
 .badge-cliente { background: rgba(123,216,176,0.12); color: var(--color-green); }
 .badge-admin   { background: rgba(232,255,122,0.1);  color: var(--color-accent); }

 /* Stats */
 .stats-grid {
   display: grid;
   grid-template-columns: repeat(4, 1fr);
   gap: 0.5rem;
 }
 .stat-card {
   display: flex;
   flex-direction: column;
   align-items: center;
   gap: 0.2rem;
   padding: 0.75rem 0.5rem;
   border-radius: 10px;
   border: 1px solid var(--color-border);
   background: rgba(255,255,255,0.02);
 }
 .stat-number { font-size: 20px; font-weight: 700; color: var(--color-bone); }
 .stat-label  { font-size: 10px; color: var(--color-bone-mute); text-align: center; }
 .stat-activa    .stat-number { color: var(--color-green); }
 .stat-proceso   .stat-number { color: var(--color-accent); }
 .stat-cancelada .stat-number { color: var(--color-danger); }

 .ver-reservaciones-btn { width: 100%; }

 /* Zona peligro */
 .danger-title { color: var(--color-danger); }
 .danger-desc {
   font-size: 12.5px;
   color: var(--color-bone-mute);
   line-height: 1.5;
 }
 .delete-btn {
   height: 36px;
   padding: 0 1.25rem;
   border-radius: 999px;
   border: 1px solid rgba(255,138,123,0.3);
   background: transparent;
   color: var(--color-danger);
   font-size: 13px;
   cursor: pointer;
   transition: all 0.2s;
   align-self: flex-start;
 }
 .delete-btn:hover {
   background: rgba(255,138,123,0.08);
   border-color: rgba(255,138,123,0.5);
 }
 .pm-preview {
   padding: 0.35rem 0.75rem;
   min-height: 38px;
   display: flex;
   align-items: center;
 }
</style>
