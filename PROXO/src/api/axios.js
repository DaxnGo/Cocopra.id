import axios from 'axios'

// Di production (Vercel), kita akan set environment variable VITE_API_URL
// mengarah ke URL backend Render (contoh: https://cocopra-backend.onrender.com/api)
// Jika tidak ada (saat dev lokal), fallback ke localhost:8000/api
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: baseURL,
  headers: { 'Content-Type': 'application/json' },
})

// Auto attach JWT token ke setiap request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle response error global
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || ''
    const isAuthAttempt = url.includes('/auth/login') || url.includes('/auth/register')
    // Hapus sesi & kembali ke beranda hanya jika BUKAN percobaan login/register,
    // supaya gagal login (401) tidak memicu reload halaman.
    if (error.response?.status === 401 && !isAuthAttempt) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // Navigasi lewat router tanpa reload penuh (dynamic import mencegah circular dependency)
      if (window.location.pathname !== '/') {
        import('../router/index.js').then(({ default: router }) => router.push('/'))
      }
    }
    return Promise.reject(error)
  },
)

export default api
