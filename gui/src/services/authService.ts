import { useAuthStore } from '../stores/auth'

const API = import.meta.env.VITE_API_URL || null
//const IS_DEV = import.meta.env.DEV
const IS_DEV = false

export const authService = {
  async login(email: string, password: string) {
    
    const auth = useAuthStore()

    //Modo dev no borrar
    // Need to ommit this block when running the project
    if (IS_DEV) {
      //Simulamos delay
      await new Promise(r => setTimeout(r, 600))
      auth.setAuth('mock-token-123', { id: 1, nombre: 'Fulanito', apellidos: 'Perez', email, rol: 'CLIENTE' })
      return
    }
    
    const res = await fetch(`${API}/auth/jwt/create/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    if (!res.ok) throw new Error('Credenciales incorrectas')
    const tokens = await res.json()
    
    // Obtener datos del usuario con el token
    const userRes = await fetch(`${API}/auth/users/me/`, {
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${tokens.access}`
      }
    })
    if (!userRes.ok) throw new Error('Error al obtener datos del usuario')
    const userData = await userRes.json()
    auth.setAuth(tokens.access, userData)
  },

  async signup(nombre: string, apellidos: string, email: string, password: string) {
    const auth = useAuthStore()

    //Modo dev no borrar
    // Need to ommit this block when running the project
    if (IS_DEV) {
      await new Promise(r => setTimeout(r, 600))
      auth.setAuth('mock-token-123', { id: 2, nombre, apellidos, email, rol: 'CLIENTE' })
      return
    }
    
    const res = await fetch(`${API}/auth/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, apellidos, email, password })
    })
    if (!res.ok) {
      const errorData = await res.json()
      console.error(errorData)
      throw new Error('Error al registrarse')
    }
    await this.login(email, password)
   },
  
  async logout() {
    const auth = useAuthStore()

    if (IS_DEV) {
      auth.clearAuth()
      return
    }
    
    //NO ES NECESARIO PORQUE EL BACK USA JWT SIN ESTADO

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
