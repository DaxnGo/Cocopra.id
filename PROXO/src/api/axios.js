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
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export default api