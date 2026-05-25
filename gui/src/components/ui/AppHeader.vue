<template>
  <header
    :class="[
      'fixed top-0 inset-x-0 z-50 transition-transform duration-500 ease-out',
      showHeader ? 'translate-y-0' : '-translate-y-full'
    ]"
  >
    <div class="mx-auto max-w-330 px-6 pt-5">
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

	<div class="flex-1" />
	<ul class="flex items-center gap-1">
          <li><AppLink href="/" variant="nav">Inicio</AppLink></li>
          <li><AppLink href="/parques" variant="nav">Parques</AppLink></li>
	  <li>
	    <AppLink :href="auth.isLoggedIn ? '/reservar' : '/auth'" variant="nav">Reservar</AppLink>
	  </li>
        </ul>
	
        <div class="flex items-center gap-2">
          <template v-if="!user">
            <AppLink href="/auth" variant="outline">Iniciar sesión</AppLink>
            <AppLink href="/auth?mode=signup" variant="yellow">Registrarse</AppLink>
          </template>
	  
          <template v-else>
	    <div class="w-px h-4 bg-white/10 mx-1" />
	    
            <AppLink href="/reservaciones" variant="nav">Mis Reservaciones</AppLink>
            <div class="relative" ref="dropdownRef">
	      
              <button class="flex items-center gap-2 pl-2 pr-1 py-1 rounded-full hover:bg-white/5 transition" @click="profileOpen = !profileOpen">
                <span class="hidden text-[13px]">{{ userShortName }}</span>
                <span class="w-9 h-9 rounded-full bg-linear-to-br from-[#7BD8B0] to-[#E8FF7A]
			     inline-flex items-center justify-center
			     text-[#07090A] font-semibold text-[13px]
			     border border-white/15">
                  {{ userInitials }}
                </span>
              </button>
	      
              <transition name="pop">
                <div v-if="profileOpen" class="absolute right-0 mt-2 w-60 glass rounded-2xl p-2 shadow-2xl">
                  <div class="px-3 py-3 border-b border-white/5 flex items-center gap-3">
                    <span class="w-9 h-9 rounded-full bg-linear-to-br from-[#7BD8B0] to-[#E8FF7A]
				 inline-flex items-center justify-center
				 text-[#07090A] font-semibold text-[13px]">
                      {{ userInitials }}
                    </span>
                    <div class="min-w-0">
                      <div class="text-[14px] font-medium leading-tight truncate">
			{{ user.nombre }} {{ user.apellidos }}
		      </div>
                      <div class="text-[11.5px] text-bone-soft truncate">{{ user.email }}</div>
                    </div>
                  </div>
                  <ul class="py-1 text-[13.5px]">
                    <li><AppLink href="/perfil" variant="popover">Perfil</AppLink></li>
                    <li><AppLink href="/ayuda" variant="popover">Ayuda</AppLink></li>
                    <li class="border-t border-white/5 mt-1 pt-1">
		      <button
			class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg hover:bg-white/5 w-full text-left text-[13.5px] hover:text-[#FF8A7B] transition-colors"
			@click="handleLogout">
			Cerrar sesión
		      </button>
		    </li>
                  </ul>
                </div>
              </transition>
            </div>
          </template>
        </div>
	
      </nav>
    </div>
    
  </header>
</template>

<script setup lang="ts">
 import { useRouter } from 'vue-router'
 import { ref, onMounted, onUnmounted, computed } from 'vue';
 import { useAuthStore } from '../../stores/auth';
 import { authService } from '../../services/authService';
import type { Usuario } from '../../stores/auth'

 import AppLink from './AppLink.vue';
 import FireflyLogo from './FireflyLogo.vue';
 
 const router = useRouter()
 const auth = useAuthStore();
 const showHeader = ref(true);
 let lastScrollY = 0;

 const handleScroll = () => {
   const currentScrollY = window.scrollY;
   showHeader.value = currentScrollY < lastScrollY || currentScrollY <= 50;
   lastScrollY = currentScrollY;
 };

 onMounted(() => window.addEventListener('scroll', handleScroll));
 onUnmounted(() => window.removeEventListener('scroll', handleScroll));

 const props = defineProps<{
   user: Usuario | null;
 }>();

 const profileOpen = ref(false);
 const dropdownRef = ref<HTMLElement | null>(null);

 const handleClickOutside = (event: MouseEvent) => {
   if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
     profileOpen.value = false;
   }
 };

 async function handleLogout() {
   await authService.logout()
   router.push('/')
 }
 
 onMounted(() => document.addEventListener('click', handleClickOutside));
 onUnmounted(() => document.removeEventListener('click', handleClickOutside));

 const userInitials = computed(() => {
   if (!props.user)
     return '';
   const n = props.user.nombre[0] ?? '';
   const a = props.user.apellidos[0] ?? '';
   return (n + a).toUpperCase();
 });
 const userShortName = computed(() => {
   if (!props.user)
     return '';
   return `${props.user.nombre} ${props.user.apellidos[0]}.`
 });
</script>

<style scoped>
 .pop-enter-active,
 .pop-leave-active {
   transition:
     opacity 0.15s ease,
     transform 0.15s ease;
 }

 .pop-enter-from,
 .pop-leave-to {
   opacity: 0;
   transform: translateY(-4px) scale(0.98);
 }
</style>
