<template>
  <div v-if="isActivated" class="konami-monkey" :style="monkeyStyle">
    <!-- Renderizamos el emoji actual usando el índice -->
    {{ monkeyEmojis[currentEmojiIndex] }}
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'

// --- ESTADOS ---
const isActivated = ref(false)
const mouse = reactive({ x: 0, y: 0 })
const monkey = reactive({ x: 0, y: 0 })
const monkeyEmojis = ['🙈', '🙉'] // Lista de emojis
const currentEmojiIndex = ref(0) // Empieza con el primero
let lastEmojiSwitchTime = 0 // Control de tiempo para el cambio

// --- CONFIGURACIÓN KONAMI ---
const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a']
let konamiIndex = 0

// --- DETECTAR TECLADO ---
const checkKonami = (e) => {
  const key = e.key.length === 1 ? e.key.toLowerCase() : e.key
  if (key === konamiCode[konamiIndex]) {
    konamiIndex++
    if (konamiIndex === konamiCode.length) {
      isActivated.value = true
      startAnimation() 
      window.removeEventListener('keydown', checkKonami)
    }
  } else {
    konamiIndex = 0
  }
}

// --- SEGUIMIENTO DEL MOUSE ---
const updateMouse = (e) => {
  mouse.x = e.clientX
  mouse.y = e.clientY
}

// --- ANIMACIÓN CON INERCIA Y CAMBIO DE EMOJI ---
const startAnimation = () => {
  const animate = (time) => {
    if (!isActivated.value) return

    // --- 1. LÓGICA DE MOVIMIENTO (INERCIA) ---
    const ease = 0.05 
    monkey.x += (mouse.x - monkey.x) * ease
    monkey.y += (mouse.y - monkey.y) * ease

    // --- 2. LÓGICA DE CAMBIO DE EMOJI (SECUENCIAL) ---
    const switchInterval = 1000 // Tiempo en milisegundos entre cambios (300ms)

    if (time - lastEmojiSwitchTime > switchInterval) {
      lastEmojiSwitchTime = time // Actualizamos el marcador de tiempo
      
      // Cambiamos al siguiente índice (ciclando secuencialmente)
      currentEmojiIndex.value = (currentEmojiIndex.value + 1) % monkeyEmojis.length
    }

    requestAnimationFrame(animate)
  }
  requestAnimationFrame(animate)
}

// --- CICLO DE VIDA ---
onMounted(() => {
  window.addEventListener('keydown', checkKonami)
  window.addEventListener('mousemove', updateMouse)
})

onUnmounted(() => {
  window.removeEventListener('keydown', checkKonami)
  window.removeEventListener('mousemove', updateMouse)
})

// --- ESTILOS DINÁMICOS ---
const monkeyStyle = computed(() => {
  return {
    transform: `translate(${monkey.x - 25}px, ${monkey.y - 25}px)`
  }
})
</script>

<style scoped>
.konami-monkey {
  position: fixed;
  top: 0;
  left: 0;
  font-size: 50px;
  pointer-events: none; 
  z-index: 9999;
  will-change: transform;
  /* Centramos el emoji con flexbox para que no salte al cambiar de tamaño */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>