<template>
  <header
    :class="[
      'fixed top-0 inset-x-0 z-50 transition-transform duration-500 ease-out',
      showHeader ? 'translate-y-0' : '-translate-y-full'
    ]"
  >
    <div class="mx-auto max-w-330 px-6 lg:px-10 pt-5">
      <nav class="glass relative rounded-full pl-5 pr-3 py-2.5 flex items-center justify-between">
        
        <div class="shrink-0">
          <AppLink href="/" variant="brand">
            <FireflyLogo :pulse="true" :drift="true" />
            <span class="font-serif text-[22px] tracking-tightest leading-none">
              Luciernagas
            </span>
            <span class="text-[10px] font-mono uppercase tracking-[0.18em] text-bone-soft pl-2 border-l border-white/10 ml-2">
              Festival 2026
            </span>
          </AppLink>
        </div>

        <ul class="md:flex items-center gap-1 text-[14px] text-bone-mute absolute left-1/2 -translate-x-1/2">
          <li><AppLink href="/" variant="transparent">Inicio</AppLink></li>
          <li><AppLink href="/parques" variant="transparent">Parques</AppLink></li>
        </ul>

        <div class="flex items-center gap-1">
          <div>
            <AppLink href="/login" variant="transparent">
              <span class="text-[14px] text-bone-mute hover:text-bone">Iniciar sesión</span>
            </AppLink>
          </div>
          <AppLink href="/registro" variant="yellow">
            Registrarse
          </AppLink>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import AppLink from './AppLink.vue';
import FireflyLogo from './FireflyLogo.vue';

const showHeader = ref(true);
let lastScrollY = 0;

const handleScroll = () => {
  const currentScrollY = window.scrollY;
  showHeader.value = currentScrollY < lastScrollY || currentScrollY <= 50;
  lastScrollY = currentScrollY;
};

onMounted(() => window.addEventListener('scroll', handleScroll));
onUnmounted(() => window.removeEventListener('scroll', handleScroll));
</script>