import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    //Public paths
    { path: '/', component: () => import('../views/HomeView.vue') },
    { path: '/auth',  component: () => import('../views/AuthView.vue') },
    { path: '/reservar', component: () => import('../views/ReservationView.vue')},
    { path: '/parques', component: () => import('../views/ParksView.vue') },
    {
      path: '/password/reset/confirm/:uid/:token',
      component: () => import('../views/PasswordResetConfirmView.vue')
    },
    { path: '/admin/login', component: () => import('../views/admin/LoginAdminView.vue') },
    
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
    },

    //Admin
    {
      path: '/admin/reservaciones',
      component: () => import('../views/admin/ReserveUserView.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/parques',
      component: () => import('../views/admin/ParksInfoView.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/admin/usuarios',
      component: () => import('../views/admin/UsersInfoView.vue'),
      meta: { requiresAdmin: true }
    },

    //Solo superuser
    {
      path: '/admin/staff',
      component: () => import('../views/admin/StaffInfoView.vue'),
      meta: { requiresAdmin: true, requiresSuperuser: true }
    },
  ]
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAdmin && auth.user?.rol !== 'ADMIN')
    return '/admin/login'

  if (to.meta.requiresSuperuser && !(auth.user as any)?.is_superuser)
    return '/admin/reservaciones'

  //Keep previous path to redirect after login
  if (to.meta.requiresAuth && !auth.isLoggedIn)
    return `/auth?redirect=${to.path}`
})

export default router
