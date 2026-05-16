import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<{ id: number; name: string; email: string } | null>(
    JSON.parse(localStorage.getItem('user') || 'null')
  )
  
  const isLoggedIn = computed(() => !!token.value)

  function setAuth(newToken: string, newUser: typeof user.value) {
    token.value = newToken
    user.value = newUser
    //Bakcend feat, aqui lleva el token como un JWT real
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isLoggedIn, setAuth, clearAuth }
})
