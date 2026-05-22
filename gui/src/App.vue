<template>
  <AppHeader v-if="!hideHeader" :user="auth.user" />
  <RouterView />
</template>

<script setup lang="ts">
 import { computed } from 'vue'
 import { useRoute } from 'vue-router'
 import { useAuthStore } from './stores/auth'

 import AppHeader from './components/ui/AppHeader.vue'

 const auth = useAuthStore()
 const route = useRoute()

 const ROUTES_WITHOUT_HEADER = ['/auth']

 const hideHeader = computed(() =>
   ROUTES_WITHOUT_HEADER.includes(route.path)
 )
</script>
