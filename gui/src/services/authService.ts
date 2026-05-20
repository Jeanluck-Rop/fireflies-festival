import { useAuthStore } from '../stores/auth'

const API = import.meta.env.VITE_API_URL || null
const IS_DEV = import.meta.env.DEV

export const authService = {
  async login(email: string, password: string) {
    
    const auth = useAuthStore()

    //Modo dev no borrar
    if (IS_DEV && !API) {
      //Simulamos delay
      await new Promise(r => setTimeout(r, 600))
      auth.setAuth('mock-token-123', { id: 1, name: 'Fulanito', email })
      return
    }
    
    //Descomentamos cuando el back este listo
    //const res = await fetch(`${API}/api/auth/login/`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ email, password })
    // })
    // if (!res.ok) throw new Error('Credenciales incorrectas')
    // const data = await res.json()
    // auth.setAuth(data.token, data.user)
  },

  async signup(name: string, email: string, password: string) {
    const auth = useAuthStore()

    //Modo dev no borrar
    if (IS_DEV && !API) {
      await new Promise(r => setTimeout(r, 600))
      auth.setAuth('mock-token-123', { id: 2, name, email })
      return
    }
    
    //Descomentamos cuando el back este listo
    // const res = await fetch(`${API}/api/auth/signup/`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({ name, email, password })
    // })
    // if (!res.ok)
    //   throw new Error('Error al registrarse')
    // const data = await res.json()
    // auth.setAuth(data.token, data.user)
   },
  
  async logout() {
    const auth = useAuthStore()

    if (IS_DEV && !API) {
      auth.clearAuth()
      return
    }
    
    // TODO backend: invalidar token en el servidor antes de limpiar el front
    // El back debe eliminar el token de su lista de tokens válidos
    // Solo al recibir confirmación (res.ok) limpiamos el front y redirigimos
    // try {
    //   const res = await fetch(`${API}/api/auth/logout/`, {
    //     method: 'POST',
    //     headers: { Authorization: `Bearer ${auth.token}` }
    //   })
    //   if (!res.ok) throw new Error('Error al cerrar sesión')
    // } catch (e) {
    //   console.error(e)
    // } finally {
    //   auth.clearAuth()  // limpia siempre, incluso si el back falla
    // }
    
    auth.clearAuth()
  }
}
