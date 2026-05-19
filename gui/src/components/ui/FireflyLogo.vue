<template>
  <svg
    viewBox="0 0 40 40"
    class="firefly-base"
    :class="[animationClass, props.size]"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <!-- Outer glow -->
    <circle cx="20" cy="20" r="18" fill="#E8FF7A" fill-opacity="0.12" />
    <circle cx="20" cy="20" r="13" fill="#E8FF7A" fill-opacity="0.2" />

    <!-- Body -->
    <ellipse cx="20" cy="22" rx="5" ry="8" fill="#161D1A" stroke="#E8FF7A" stroke-width="1.2" />

    <!-- Wings -->
    <ellipse cx="13" cy="17" rx="5" ry="3" fill="#E8FF7A" fill-opacity="0.35" transform="rotate(-25 13 17)" />
    <ellipse cx="27" cy="17" rx="5" ry="3" fill="#E8FF7A" fill-opacity="0.35" transform="rotate(25 27 17)" />

    <!-- Glow tail -->
    <ellipse cx="20" cy="28" rx="3" ry="3.5" fill="#F4FFA0" />
    <ellipse cx="20" cy="28" rx="1.6" ry="2" fill="#FFFDE8" />

    <!-- Antennae -->
    <path d="M18 14 Q16 11 14 12" stroke="#E8FF7A" stroke-width="1" stroke-linecap="round" />
    <path d="M22 14 Q24 11 26 12" stroke="#E8FF7A" stroke-width="1" stroke-linecap="round" />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
   pulse?: boolean
   drift?: boolean
   size?: string //para el redimencionar en FormAuth
 }>(), {
   pulse: true,
   drift: true,
   size: 'w-9 h-9' 
 });

 const animationClass = computed(() => {
  if (props.pulse && props.drift) return 'anim-both';
  if (props.pulse) return 'anim-pulse';
  if (props.drift) return 'anim-drift';
  return '';
});
</script>

<style scoped>
.firefly-base {
  filter:
    drop-shadow(0 0 4px rgba(232, 255, 122, 0.9))
    drop-shadow(0 0 12px rgba(232, 255, 122, 0.45))
    drop-shadow(0 0 24px rgba(232, 255, 122, 0.2));
}

.anim-both {
  animation:
    firefly-logo-pulse 2.6s ease-in-out infinite,
    firefly-logo-drift 10s ease-in-out infinite;
}

.anim-pulse {
  animation: firefly-logo-pulse 2.6s ease-in-out infinite;
}

.anim-drift {
  animation: firefly-logo-drift 10s ease-in-out infinite;
}

@keyframes firefly-logo-pulse {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.15); }
}

@keyframes firefly-logo-drift {
  0%   { transform: translate(0, 10px); }
  25%  { transform: translate(15px, -7px); }
  37%  { transform: translate(10px, 5px); }
  50%  { transform: translate(-3px, -15px); }
  62%  { transform: translate(-10px, 2px); }
  75%  { transform: translate(-17px, -6px); }
  100% { transform: translate(0, 10px); }
}
</style>
