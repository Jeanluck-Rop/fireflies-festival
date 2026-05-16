import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    //Public paths
    { path: '/',       component: () => import('../views/HomeView.vue') },
    { path: '/login',  component: () => import('../views/LoginView.vue') },
    { path: '/signup', component: () => import('../views/SignupView.vue') },
    { path: '/reservar', component: () => import('../views/ReservationView.vue')},

    //Private paths
    {
      path: '/reservaciones',
      component: () => import('../views/UserReservationsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/perfil',
      component: () => import('../views/UserProfileView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    //Keep previous path to redirect after login
    return `/login?redirect=${to.path}`
  }
})

export default router
