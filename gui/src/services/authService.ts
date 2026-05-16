import { useAuthStore } from '../stores/auth'

export const authService = {
  async login(email: string, password: string) {
    //Simulamos delay de red
    await new Promise(r => setTimeout(r, 600))

    //Aqui iria el fetch al backend
    const auth = useAuthStore()
    auth.setAuth('mock-token-123', {
      id: 1,
      name: 'Fulanito',
      email: email  // usamos el email que escribio
    })
  },

  logout() {
    const auth = useAuthStore()
    auth.clearAuth()
  }
}
