import { useAuthStore } from '../stores/auth'

const API = import.meta.env.VITE_API_URL || null
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

const DJANGO_ERROR_MAP: Record<string, string> = {
  'This password is entirely numeric.': 'La contraseña no puede contener solo números.',
  'The password is too similar to the email.': 'La contraseña es demasiado parecida al correo.',
  'The password is too short.': 'La contraseña es demasiado corta.',
  'This password is too common.': 'La contraseña es demasiado común.',
  'Usuario with this email already exists.': 'Ya existe una cuenta con este correo.',
  'No active account found with the given credentials': 'Correo o contraseña incorrectos.',
  'Unable to log in with provided credentials.': 'Correo o contraseña incorrectos.',
  'This field may not be blank.': 'Este campo no puede estar vacío.',
}

export class EmailNotFoundError extends Error {}
export class WrongPasswordError extends Error {}

export class ValidationError extends Error {
  public fields: Record<string, string>;
  constructor(fields: Record<string, string>) {
    super('Error de validación en el servidor');
    this.fields = fields;
  }
}

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
      throw new ValidationError({ email: 'Ya existe una cuenta con este correo.' })
    }
    
    const res = await fetch(`${API}/auth/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, apellidos, email, password })
    })
    if (!res.ok) {
      const errorData = await res.json()
      console.error(errorData)
      if (typeof errorData === 'object' && !errorData.detail) {
        const errorsPerField: Record<string, string> = {}
        
        for (const campo in errorData) {
          if (Array.isArray(errorData[campo]) && errorData[campo].length > 0) {
            const msgNativo = errorData[campo][0]
            errorsPerField[campo] = DJANGO_ERROR_MAP[msgNativo] ?? msgNativo
          }
        }
        throw new ValidationError(errorsPerField)
      }
      const msgGlobal = errorData.detail || 'Error al registrarse en el servidor.'
      throw new Error(DJANGO_ERROR_MAP[msgGlobal] ?? msgGlobal)
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
