import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: HomeView,
      meta: { title: 'Cocopra.id — Platform Agritech AI untuk Petani Kelapa' }
    },
    {
      path: '/dashboard',
      component: () => import('../views/dashboard/DashboardView.vue'),
      meta: { title: 'Dashboard — Cocopra.id', requiresAuth: true }
    },
    {
      path: '/dashboard/scanner',
      component: () => import('../views/dashboard/ScannerView.vue'),
      meta: { title: 'Scanner — Cocopra.id', requiresAuth: true }
    },
    {
      path: '/dashboard/harga-kopra',
      component: () => import('../views/dashboard/HargaKopraView.vue'),
      meta: { title: 'Harga Kopra — Cocopra.id', requiresAuth: true }
    },
    {
      path: '/dashboard/asisten-ai',
      component: () => import('../views/dashboard/AsistenAIView.vue'),
      meta: { title: 'Asisten AI — Cocopra.id', requiresAuth: true }
    },
    {
      path: '/dashboard/regulatory',
      component: () => import('../views/dashboard/RegulatoryView.vue'),
      meta: { title: 'Regulatory Check — Cocopra.id', requiresAuth: true }
    },
    {
      path: '/dashboard/settings',
      component: () => import('../views/dashboard/SettingsView.vue'),
      meta: { title: 'Account Settings — Cocopra.id', requiresAuth: true }
    },
    {
      path: '/500',
      component: () => import('../views/ServerError.vue'),
      meta: { title: 'Server Error — Cocopra.id' }
    },
    {
      path: '/503',
      component: () => import('../views/Maintenance.vue'),
      meta: { title: 'Maintenance — Cocopra.id' }
    },
    {
      path: '/403',
      component: () => import('../views/Forbidden.vue'),
      meta: { title: 'Akses Ditolak — Cocopra.id' }
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('../views/NotFound.vue'),
      meta: { title: 'Halaman Tidak Ditemukan — Cocopra.id' }
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth', top: 80 }
    }
    return { top: 0, behavior: 'smooth' }
  }
})

// Dynamic page title
router.afterEach((to) => {
  document.title = to.meta?.title || 'Cocopra.id'
})

// Navigation guard — protect dashboard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/')
  } else {
    next()
  }
})

export default router