import type { Parque } from '../stores/parks'

export function is24Hours(park: Parque): boolean {
  return park.horario_apertura === park.horario_cierre ||
    (park.horario_apertura === '00:00' && park.horario_cierre === '00:00')
}

export function isParkOpen(park: Parque): boolean {
  if (!park.activo)
    return false

  if (is24Hours(park))
    return true

  const offsetHours = Math.round(park.longitud / 15)
  const nowUtc = new Date()
  const parkTime = new Date(nowUtc.getTime() + offsetHours * 60 * 60 * 1000)
  const parkMinutes = parkTime.getUTCHours() * 60 + parkTime.getUTCMinutes()
  const [aH, aM] = park.horario_apertura.split(':').map(Number)
  const [cH, cM] = park.horario_cierre.split(':').map(Number)

  const openMinutes = aH * 60 + aM
  const closeMinutes = cH * 60 + cM

  // Horario nocturno
  if (openMinutes > closeMinutes) {
    return parkMinutes >= openMinutes || parkMinutes < closeMinutes
  }

  return parkMinutes >= openMinutes && parkMinutes < closeMinutes
}

export function getParkStatusText(park: Parque): string {
  if (!park.activo)
    return 'No disponible'

  return isParkOpen(park) ? 'Abierto' : 'Cerrado'
}

export function getParkStatusClass(park: Parque): string {
  if (!park.activo)
    return 'status-unavailable'

  return isParkOpen(park) ? 'status-open' : 'status-closed'
}