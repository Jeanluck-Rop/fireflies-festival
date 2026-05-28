import { ref, onMounted, onUnmounted } from 'vue'

export function useCarousel(length: number, delay = 2500) {
  const currentIndex = ref(0)

  let timer: ReturnType<typeof setInterval> | null = null

  function next() {
    currentIndex.value = (currentIndex.value + 1) % length
  }

  function prev() {
    currentIndex.value = (currentIndex.value - 1 + length) % length
  }

  function goTo(index: number) {
    currentIndex.value = index
  }

  function start() {
    if (length <= 1)
      return
    stop()
    timer = setInterval(next, delay)
  }

  function stop() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onMounted(start)
  onUnmounted(stop)

  return { currentIndex, next, prev, goTo, start, stop }
}