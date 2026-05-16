import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(null)
  const user = ref<{ id: number; name: string; email: string } | null>(null)

  const isLoggedIn = computed(() => !!token.value)

  function setAuth(newToken: string, newUser: typeof user.value) {
    token.value = newToken
    user.value = newUser
  }

  function clearAuth() {
    token.value = null
    user.value = null
  }

  return { token, user, isLoggedIn, setAuth, clearAuth }
})
