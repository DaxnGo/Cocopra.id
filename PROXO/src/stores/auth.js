import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => user.value?.name || 'Pengguna')
  const userEmail = computed(() => user.value?.email || '')
  const userRole = computed(() => user.value?.role || 'petani')

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await res.json()
      if (!res.ok) {
        error.value = data.message || 'Login gagal.'
        return { success: false, message: error.value }
      }
      setAuth(data.token, data.user)
      return { success: true }
    } catch (err) {
      error.value = 'Tidak dapat terhubung ke server.'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  async function register(payload) {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      const data = await res.json()
      if (!res.ok) {
        error.value = data.message || 'Registrasi gagal.'
        return { success: false, message: error.value }
      }
      setAuth(data.token, data.user)
      return { success: true }
    } catch (err) {
      error.value = 'Tidak dapat terhubung ke server.'
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      const data = await res.json()
      if (res.ok) {
        user.value = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
      } else {
        logout()
      }
    } catch {
      logout()
    }
  }

  function setAuth(newToken, newUser) {
    token.value = newToken
    user.value = newUser
    localStorage.setItem('token', newToken)
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token, user, loading, error,
    isLoggedIn, userName, userEmail, userRole,
    login, register, fetchMe, logout
  }
})