import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/axios.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const userName = computed(() => user.value?.name || 'Pengguna')
  const userEmail = computed(() => user.value?.email || '')
  const userRole = computed(() => user.value?.role || 'petani')

  // Ambil pesan error dari balasan FastAPI ({ detail }) atau masalah koneksi
  function _getErrorMessage(err, fallback) {
    if (!err.response) return 'Tidak dapat terhubung ke server.'
    const data = err.response.data
    return (typeof data?.detail === 'string' && data.detail) || data?.message || fallback
  }

  async function login(email, password) {
    loading.value = true
    error.value = null
    try {
      const res = await api.post('/auth/login', { email, password })
      setAuth(res.data.token, res.data.user)
      return { success: true }
    } catch (err) {
      error.value = _getErrorMessage(err, 'Login gagal.')
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  async function register(payload) {
    loading.value = true
    error.value = null
    try {
      const res = await api.post('/auth/register', payload)
      setAuth(res.data.token, res.data.user)
      return { success: true }
    } catch (err) {
      error.value = _getErrorMessage(err, 'Registrasi gagal.')
      return { success: false, message: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      const res = await api.get('/auth/me')
      user.value = res.data.user
      localStorage.setItem('user', JSON.stringify(res.data.user))
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
