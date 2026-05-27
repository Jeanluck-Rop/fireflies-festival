<template>
  <span v-if="!method" class="pm-empty">Sin configurar</span>

  <div v-else-if="method === 'PAYPAL'" class="pm-badge pm-png">
    <img src="../../assets/paypal_logo.png" alt="PayPal" class="pm-logo" />
  </div>

  <div v-else-if="method === 'STRIPE'" class="pm-badge pm-png">
    <img src="../../assets/stripe_logo.png" alt="Stripe" class="pm-logo" />
  </div>

  <div v-else-if="method === 'DEBITO'" class="pm-badge pm-icon">
    <IconDebit :size="iconSize" />
    <span class="pm-label">Débito</span>
  </div>
  
  <div v-else-if="method === 'CREDITO'" class="pm-badge pm-icon">
    <IconCredit :size="iconSize" />
    <span class="pm-label">Crédito</span>
  </div>
</template>

<script setup lang="ts">
 import IconDebit  from '../svg/IconDebit.vue'
 import IconCredit from '../svg/IconCredit.vue'

 withDefaults(defineProps<{
   method?:   string | null
   iconSize?: string
 }>(), {
   iconSize: '18px'
 })
</script>

<style scoped>
 /* Badge contenedor compartido */
 .pm-badge {
   display: inline-flex;
   align-items: center;
   justify-content: center;
   border-radius: 8px;
   overflow: hidden;
 }

 /* PNG logos, fondo blanco porque los PNGs son transparentes */
 .pm-png {
   width: 72px;
   height: 36px;
   background: #fff;
   padding: 4px 8px;
 }

 .pm-logo {
   width: 100%;
   height: 100%;
   object-fit: contain;
 }

 /* SVG icon cards, fondo oscuro, icono y texto blancos */
 .pm-icon {
   gap: 0.4rem;
   padding: 0.25rem 0.65rem;
   background: rgba(255,255,255,0.08);
   border: 1px solid rgba(255,255,255,0.1);
   color: var(--color-bone);
   height: 36px;
 }

 .pm-label {
   font-size: 12px;
   font-weight: 500;
   color: var(--color-bone);
   white-space: nowrap;
 }

 /* Sin metodo */
 .pm-empty {
   font-size: 12.5px;
   color: var(--color-bone-mute);
 }
</style>
