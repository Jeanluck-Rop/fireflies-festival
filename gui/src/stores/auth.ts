import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 1. Creamos una interfaz limpia para que TypeScript sepa qué campos tiene el usuario de Django
export interface Usuario {
  id: number
  nombre: string
  apellidos: string
  email: string
  rol: 'CLIENTE' | 'ADMIN'
  metodo_pago?: string | null
  created_at?: string | null
  is_staff?: boolean
  is_superuser?: boolean
  nivel_admin?: number | null 
}

const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

export const useAuthStore = defineStore('auth', () => {
  // Cambiamos el tipo de 'user' para que use la interfaz 'Usuario'
  const token = ref<string | null>(USE_MOCK ? null : localStorage.getItem('token'))
  const user = ref<Usuario | null>(
    USE_MOCK ? null : JSON.parse(localStorage.getItem('user') || 'null')
  )
  
  const isLoggedIn = computed(() => !!token.value)

  // 2. Agregamos getters para proteger rutas o vistas del Festival fácilmente más adelante
  const esAdmin = computed(() => user.value?.rol === 'ADMIN')
  const esCliente = computed(() => user.value?.rol === 'CLIENTE')

  // Aquí cambiamos 'typeof user.value' por 'Usuario' para solucionar tu error de tipado
  function setAuth(newToken: string, newUser: Usuario) {
    token.value = newToken
    user.value = newUser
    if (!USE_MOCK) {
      localStorage.setItem('token', newToken)
      localStorage.setItem('user', JSON.stringify(newUser))
    }
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // Retornamos también los nuevos getters (esAdmin, esCliente) para que puedas usarlos en tus componentes
  return { token, user, isLoggedIn, esAdmin, esCliente, setAuth, clearAuth }
})
