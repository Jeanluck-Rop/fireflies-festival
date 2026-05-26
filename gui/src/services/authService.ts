import { useAuthStore } from '../stores/auth'

const API = import.meta.env.VITE_API_URL || null
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

export class EmailNotFoundError extends Error {}
export class WrongPasswordError extends Error {}
export class EmailAlreadyInUseError extends Error {}

export const authService = {
  async login(email: string, password: string) {
    
    const auth = useAuthStore()

    if (USE_MOCK) {
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
    if (USE_MOCK) {
      await new Promise(r => setTimeout(r, 600))
      throw new EmailAlreadyInUseError()
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

    if (USE_MOCK) {
      auth.clearAuth()
      return
    }
    
    auth.clearAuth()
  }
}
