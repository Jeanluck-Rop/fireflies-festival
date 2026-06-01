import { ref } from 'vue'

//Constantes del festival
export const FESTIVAL_YEAR = 2026
export const FECHA_MIN = `${FESTIVAL_YEAR}-06-01` // 1 junio
export const FECHA_MAX = `${FESTIVAL_YEAR}-08-31` // 31 agosto

//Validacion pura (exportable sin estado reactivo)
/**
 * Devuelve un mensaje de error si la fecha viola las reglas
 * del festival, o '' si es valida
 * - Solo junio, julio y agosto del anio del festival
 * - Sin martes (mantenimiento del parque)
 */
export function validarFechaFestival(dateStr: string): string {
  if (!dateStr)
    return ''

  //T12:00:00 evita desfases de zona horaria al parsear YYYY-MM-DD
  const d   = new Date(`${dateStr}T12:00:00`)
  const mes = d.getMonth() + 1 //1 = enero ... 12 = diciembre
  const dow = d.getDay()      //0 = domingo ... 2 = martes ... 6 = sabado

  if (mes < 6 || mes > 8)
    return 'Solo se permiten fechas entre junio y agosto (temporada del festival)'
  if (dow === 2)
    return 'Los martes no están disponibles, día de mantenimiento del parque'
  return ''
}

/**
 * Uso en cada componente:
 *
 *   const { FECHA_MIN, FECHA_MAX, dateErrorInicio, dateErrorFin, checkInicio, checkFin } =
 *     useFestivalDates()
 *
 * checkInicio / checkFin devuelven true si la fecha es válida.
 * El componente decide los efectos secundarios (limpiar campo,
 * resetear hospedaje, etc.) según el valor de retorno.
 */
export function useFestivalDates() {
  const dateErrorInicio = ref('')
  const dateErrorFin    = ref('')

  function checkInicio(value: string): boolean {
    const err = validarFechaFestival(value)
    dateErrorInicio.value = err
    return !err
  }

  function checkFin(value: string): boolean {
    const err = validarFechaFestival(value)
    dateErrorFin.value = err
    return !err
  }

  function clearDateErrors() {
    dateErrorInicio.value = ''
    dateErrorFin.value    = ''
  }

  return {
    FECHA_MIN,
    FECHA_MAX,
    dateErrorInicio,
    dateErrorFin,
    checkInicio,
    checkFin,
    clearDateErrors,
  }
}
