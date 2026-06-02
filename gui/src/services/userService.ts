import type { UsuarioAdmin } from '../components/admin/AdminUserRow.vue' // Ajusta la ruta según tu carpeta

const API = import.meta.env.VITE_API_URL || null

export const userService = {
  /**
   * Brings all users for admin management, requires admin token
   */
  async obtenerClientes(token: string): Promise<UsuarioAdmin[]> {
    const res = await fetch(`${API}/api/clientes/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    if (!res.ok) throw new Error('Error al obtener la lista de usuarios')
    return await res.json()
  },

  /**
   * Elimina/Desactiva un usuario por su ID
   */
  async eliminarUsuario(id: number, token: string): Promise<void> {
    const res = await fetch(`${API}/api/clientes/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (!res.ok) throw new Error('No se pudo eliminar al usuario')
  }
}