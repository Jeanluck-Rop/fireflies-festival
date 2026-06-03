import { ref } from 'vue'

export type NotificationType = 'exito' | 'error' | 'normal'

export interface Notification {
  id: number
  type: NotificationType
  message: string
}

//Estado global, singleton fuera del componente
const notification = ref<Notification | null>(null)
let timer: ReturnType<typeof setTimeout> | null = null
let nextId = 0

export function useNotification() {
  function show(type: NotificationType, message: string, duration = 8000) {
    //Cancela el timer anterior si había una notificacion
    if (timer)
      clearTimeout(timer)

    notification.value = { id: ++nextId, type, message }

    timer = setTimeout(() => {
      notification.value = null
      timer = null
    }, duration)
  }

  function dismiss() {
    if (timer)
      clearTimeout(timer)
    notification.value = null
    timer = null
  }

  return { notification, show, dismiss }
}
