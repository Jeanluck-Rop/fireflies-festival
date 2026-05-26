<template>
  <AppHeader v-if="!hideHeader" :user="auth.user" />
  <RouterView />
  <AppNotification />
</template>

<script setup lang="ts">
 import { computed } from 'vue'
 import { useRoute } from 'vue-router'
 import { useAuthStore } from './stores/auth'

 import AppHeader from './components/ui/AppHeader.vue'
 import AppNotification from './components/ui/AppNotification.vue'

 const auth = useAuthStore()
 const route = useRoute()

 const ROUTES_WITHOUT_HEADER = ['/auth', '/password/reset/confirm']

 const hideHeader = computed(() =>
   ROUTES_WITHOUT_HEADER.some(r => route.path.startsWith(r))
 )
</script>
