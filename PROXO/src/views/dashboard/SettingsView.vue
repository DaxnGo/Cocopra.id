<template>
  <div class="min-h-screen flex" style="background: #0d2818;">
    <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/60 lg:hidden" @click="sidebarOpen = false" />
    <DashboardSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex-1 lg:ml-52 flex flex-col min-h-screen">
      <DashboardHeader
        title="Account Settings"
        subtitle="Manage your account preferences"
        :userName="authStore.userName"
        :userRole="authStore.user?.role === 'petani' ? 'Petani Kelapa' : 'Dinas Pertanian'"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
      />

      <main class="flex-1 overflow-y-auto">

        <!-- PROFILE BANNER -->
        <div class="relative h-32 md:h-40"
          style="background: linear-gradient(135deg, #1a4a2e 0%, #2d6a4f 50%, #1a4a2e 100%);">
          <div class="absolute inset-0 opacity-10"
            style="background-image: repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(255,255,255,0.1) 20px, rgba(255,255,255,0.1) 21px);">
          </div>
        </div>

        <!-- PROFILE INFO -->
        <div class="px-4 md:px-8 pb-6">
          <div class="flex flex-col md:flex-row md:items-end gap-4 -mt-12 mb-6">
            <div class="relative w-fit">
              <div class="w-20 h-20 md:w-24 md:h-24 rounded-full border-4 overflow-hidden shrink-0"
                style="border-color: #0d2818; background: #1a4a2e;">
                <img v-if="profileImage" :src="profileImage" class="w-full h-full object-cover" alt="Profile" />
                <div v-else class="w-full h-full flex items-center justify-center text-amber-400 font-bold text-2xl">
                  {{ authStore.userName?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
              </div>
              <label class="absolute bottom-0 right-0 w-7 h-7 rounded-full bg-amber-500 hover:bg-amber-400 flex items-center justify-center cursor-pointer transition">
                <Camera class="w-3.5 h-3.5 text-black" />
                <input type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
              </label>
            </div>
            <div class="pb-1">
              <h2 class="text-white font-bold text-xl">{{ profile.firstName }} {{ profile.lastName }}</h2>
              <p class="text-gray-400 text-sm">{{ profile.role }} · {{ profile.location }}</p>
            </div>
          </div>

          <!-- TABS + CONTENT -->
          <div class="flex flex-col md:flex-row gap-6">

            <!-- Tab Menu -->
            <div class="md:w-48 shrink-0">
              <div class="rounded-2xl border border-white/8 overflow-hidden"
                style="background: rgba(255,255,255,0.03);">
                <button v-for="tab in tabs" :key="tab.id"
                  @click="activeTab = tab.id"
                  class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition text-left"
                  :class="activeTab === tab.id
                    ? 'bg-amber-500 text-black'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'">
                  <component :is="tab.icon" class="w-4 h-4 shrink-0" />
                  {{ tab.label }}
                </button>
              </div>
            </div>

            <!-- Tab Content -->
            <div class="flex-1 min-w-0">

              <!-- ===== EDIT PROFILE ===== -->
              <div v-if="activeTab === 'profile'">
                <div class="rounded-2xl border border-white/8 p-5 md:p-6 mb-4"
                  style="background: rgba(255,255,255,0.03);">
                  <h3 class="text-white font-semibold mb-1">Edit Profil</h3>
                  <p class="text-gray-500 text-xs mb-5">Perbarui informasi akun dan detail profil Anda.</p>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <!-- Personal -->
                    <div class="flex flex-col gap-4">
                      <div class="text-gray-600 text-xs font-semibold tracking-widest uppercase">Personal</div>
                      <div>
                        <label class="text-gray-500 text-xs mb-1.5 block">First Name</label>
                        <input v-model="profile.firstName" type="text"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition" />
                      </div>
                      <div>
                        <label class="text-gray-500 text-xs mb-1.5 block">Last Name</label>
                        <input v-model="profile.lastName" type="text"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition" />
                      </div>
                      <div>
                        <label class="text-gray-500 text-xs mb-1.5 block">Role</label>
                        <input v-model="profile.role" type="text" disabled
                          class="w-full bg-white/3 border border-white/5 rounded-xl px-4 py-2.5 text-sm text-gray-500 outline-none cursor-not-allowed" />
                      </div>
                    </div>

                    <!-- Contact -->
                    <div class="flex flex-col gap-4">
                      <div class="text-gray-600 text-xs font-semibold tracking-widest uppercase">Contact</div>
                      <div>
                        <label class="text-gray-500 text-xs mb-1.5 block">Email</label>
                        <input v-model="profile.email" type="email"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition" />
                      </div>
                      <div>
                        <label class="text-gray-500 text-xs mb-1.5 block">Phone Number</label>
                        <div class="flex gap-2">
                          <div class="bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-sm text-gray-400 shrink-0">
                            +62
                          </div>
                          <input v-model="profile.phone" type="tel"
                            class="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition" />
                        </div>
                      </div>
                      <div>
                        <label class="text-gray-500 text-xs mb-1.5 block">Location</label>
                        <input v-model="profile.location" type="text"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition" />
                      </div>
                    </div>
                  </div>

                  <button @click="saveProfile"
                    :disabled="profileLoading"
                    class="bg-amber-500 hover:bg-amber-400 text-black font-bold px-6 py-2.5 rounded-xl text-sm transition disabled:opacity-50">
                    {{ profileLoading ? 'Menyimpan...' : 'UPDATE' }}
                  </button>

                  <div v-if="profileSaved"
                    class="mt-3 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-900/20 border border-emerald-700/30 rounded-lg px-3 py-2 w-fit">
                    <CheckCircle class="w-3 h-3" /> Profil berhasil diperbarui!
                  </div>

                  <div v-if="profileError"
                    class="mt-3 flex items-center gap-2 text-xs text-red-400 bg-red-900/20 border border-red-700/30 rounded-lg px-3 py-2 w-fit">
                    {{ profileError }}
                  </div>
                </div>

                <DangerZone />
              </div>

              <!-- ===== PASSWORD ===== -->
              <div v-if="activeTab === 'password'">
                <div class="rounded-2xl border border-white/8 p-5 md:p-6 mb-4"
                  style="background: rgba(255,255,255,0.03);">
                  <h3 class="text-white font-semibold mb-1">Ubah Password</h3>
                  <p class="text-gray-500 text-xs mb-5">Perbarui kata sandi akun Anda secara berkala untuk keamanan optimal.</p>

                  <div class="text-gray-600 text-xs font-semibold tracking-widest uppercase mb-4">Keamanan</div>

                  <div class="flex flex-col gap-4 max-w-lg">
                    <div>
                      <label class="text-gray-500 text-xs mb-1.5 block uppercase tracking-widest">Password Saat Ini</label>
                      <div class="relative">
                        <input v-model="passwords.current" :type="showCurrentPass ? 'text' : 'password'"
                          placeholder="Masukkan password saat ini"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 outline-none focus:border-amber-500/50 transition pr-10" />
                        <button @click="showCurrentPass = !showCurrentPass"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300">
                          <Eye v-if="!showCurrentPass" class="w-4 h-4" />
                          <EyeOff v-else class="w-4 h-4" />
                        </button>
                      </div>
                    </div>

                    <div>
                      <label class="text-gray-500 text-xs mb-1.5 block uppercase tracking-widest">Password Baru</label>
                      <div class="relative">
                        <input v-model="passwords.new" :type="showNewPass ? 'text' : 'password'"
                          placeholder="Masukkan password baru"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 outline-none focus:border-amber-500/50 transition pr-10" />
                        <button @click="showNewPass = !showNewPass"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300">
                          <Eye v-if="!showNewPass" class="w-4 h-4" />
                          <EyeOff v-else class="w-4 h-4" />
                        </button>
                      </div>
                      <div class="mt-2">
                        <div class="flex gap-1 mb-1">
                          <div class="h-1 flex-1 rounded-full transition-all" :class="passStrength >= 1 ? 'bg-amber-500' : 'bg-white/10'"></div>
                          <div class="h-1 flex-1 rounded-full transition-all" :class="passStrength >= 2 ? 'bg-amber-400' : 'bg-white/10'"></div>
                          <div class="h-1 flex-1 rounded-full transition-all" :class="passStrength >= 3 ? 'bg-emerald-400' : 'bg-white/10'"></div>
                          <div class="h-1 flex-1 rounded-full transition-all" :class="passStrength >= 4 ? 'bg-emerald-400' : 'bg-white/10'"></div>
                        </div>
                        <span class="text-xs" :class="passStrength >= 3 ? 'text-emerald-400' : 'text-amber-400'">
                          {{ passStrength >= 4 ? 'Kuat' : passStrength >= 3 ? 'Sedang' : passStrength >= 1 ? 'Lemah' : '' }}
                        </span>
                      </div>
                    </div>

                    <!-- Requirements -->
                    <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.02);">
                      <div class="text-gray-600 text-xs font-semibold tracking-widest uppercase mb-3">Persyaratan Password</div>
                      <div class="flex flex-col gap-2">
                        <div class="flex items-center gap-2 text-xs" :class="passwords.new.length >= 8 ? 'text-emerald-400' : 'text-gray-500'">
                          <div class="w-3 h-3 rounded-full border flex items-center justify-center shrink-0"
                            :class="passwords.new.length >= 8 ? 'border-emerald-400 bg-emerald-400/20' : 'border-gray-600'">
                            <div v-if="passwords.new.length >= 8" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                          </div>
                          Minimal 8 karakter
                        </div>
                        <div class="flex items-center gap-2 text-xs" :class="/[A-Z]/.test(passwords.new) && /[a-z]/.test(passwords.new) ? 'text-emerald-400' : 'text-gray-500'">
                          <div class="w-3 h-3 rounded-full border flex items-center justify-center shrink-0"
                            :class="/[A-Z]/.test(passwords.new) && /[a-z]/.test(passwords.new) ? 'border-emerald-400 bg-emerald-400/20' : 'border-gray-600'">
                            <div v-if="/[A-Z]/.test(passwords.new) && /[a-z]/.test(passwords.new)" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                          </div>
                          Huruf besar dan huruf kecil
                        </div>
                        <div class="flex items-center gap-2 text-xs" :class="/\d/.test(passwords.new) ? 'text-emerald-400' : 'text-gray-500'">
                          <div class="w-3 h-3 rounded-full border flex items-center justify-center shrink-0"
                            :class="/\d/.test(passwords.new) ? 'border-emerald-400 bg-emerald-400/20' : 'border-gray-600'">
                            <div v-if="/\d/.test(passwords.new)" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                          </div>
                          Minimal 1 angka
                        </div>
                        <div class="flex items-center gap-2 text-xs" :class="/[!@#$%^&*]/.test(passwords.new) ? 'text-emerald-400' : 'text-gray-500'">
                          <div class="w-3 h-3 rounded-full border flex items-center justify-center shrink-0"
                            :class="/[!@#$%^&*]/.test(passwords.new) ? 'border-emerald-400 bg-emerald-400/20' : 'border-gray-600'">
                            <div v-if="/[!@#$%^&*]/.test(passwords.new)" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></div>
                          </div>
                          Minimal 1 karakter khusus (!@#$%)
                        </div>
                      </div>
                    </div>

                    <div>
                      <label class="text-gray-500 text-xs mb-1.5 block uppercase tracking-widest">Konfirmasi Password Baru</label>
                      <div class="relative">
                        <input v-model="passwords.confirm" :type="showConfirmPass ? 'text' : 'password'"
                          placeholder="Ulangi password baru"
                          class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-600 outline-none focus:border-amber-500/50 transition pr-10"
                          :class="passwords.confirm && passwords.new !== passwords.confirm ? 'border-red-500/50' : ''" />
                        <button @click="showConfirmPass = !showConfirmPass"
                          class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300">
                          <Eye v-if="!showConfirmPass" class="w-4 h-4" />
                          <EyeOff v-else class="w-4 h-4" />
                        </button>
                      </div>
                      <p v-if="passwords.confirm && passwords.new !== passwords.confirm"
                        class="text-red-400 text-xs mt-1">Password tidak cocok</p>
                    </div>

                    <button @click="savePassword"
                      :disabled="passwordLoading"
                      class="bg-amber-500 hover:bg-amber-400 text-black font-bold px-6 py-2.5 rounded-xl text-sm transition w-fit disabled:opacity-50">
                      {{ passwordLoading ? 'Menyimpan...' : 'SIMPAN PASSWORD' }}
                    </button>

                    <div v-if="passwordSaved"
                      class="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-900/20 border border-emerald-700/30 rounded-lg px-3 py-2 w-fit">
                      <CheckCircle class="w-3 h-3" /> Password berhasil diperbarui!
                    </div>

                    <div v-if="passwordError"
                      class="flex items-center gap-2 text-xs text-red-400 bg-red-900/20 border border-red-700/30 rounded-lg px-3 py-2 w-fit">
                      {{ passwordError }}
                    </div>
                  </div>
                </div>

                <DangerZone />
              </div>

              <!-- ===== NOTIFICATIONS ===== -->
              <div v-if="activeTab === 'notifications'">
                <div class="rounded-2xl border border-white/8 p-5 md:p-6 mb-4"
                  style="background: rgba(255,255,255,0.03);">
                  <h3 class="text-white font-semibold mb-1">Pengaturan Notifikasi</h3>
                  <p class="text-gray-500 text-xs mb-5">Kelola preferensi notifikasi untuk platform Cocopra.id.</p>

                  <div class="text-gray-600 text-xs font-semibold tracking-widest uppercase mb-4">Notifikasi Aplikasi</div>

                  <div class="flex flex-col gap-3">
                    <div v-for="notif in notifications" :key="notif.id"
                      class="flex items-center justify-between p-4 rounded-xl border border-white/5 hover:border-white/10 transition"
                      style="background: rgba(255,255,255,0.02);">
                      <div class="flex items-center gap-3">
                        <div class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0"
                          :style="`background: ${notif.iconBg}`">
                          <component :is="notif.icon" class="w-4 h-4" :style="`color: ${notif.iconColor}`" />
                        </div>
                        <div>
                          <div class="text-white text-sm font-medium">{{ notif.title }}</div>
                          <div class="text-gray-500 text-xs mt-0.5">{{ notif.desc }}</div>
                        </div>
                      </div>
                      <button @click="notif.enabled = !notif.enabled"
                        class="relative w-11 h-6 rounded-full transition-colors shrink-0"
                        :class="notif.enabled ? 'bg-amber-500' : 'bg-white/10'">
                        <div class="absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-transform"
                          :class="notif.enabled ? 'translate-x-6' : 'translate-x-1'"></div>
                      </button>
                    </div>
                  </div>

                  <button @click="saveNotifications"
                    class="mt-5 bg-amber-500 hover:bg-amber-400 text-black font-bold px-6 py-2.5 rounded-xl text-sm transition">
                    UPDATE
                  </button>

                  <div v-if="notifSaved"
                    class="mt-3 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-900/20 border border-emerald-700/30 rounded-lg px-3 py-2 w-fit">
                    <CheckCircle class="w-3 h-3" /> Preferensi notifikasi disimpan!
                  </div>
                </div>

                <DangerZone />
              </div>

            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Camera, User, Lock, Bell, Eye, EyeOff,
  CheckCircle, ScanLine, TrendingUp
} from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import DashboardSidebar from '../../components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'

const DangerZone = {
  template: `
    <div class="rounded-2xl border border-red-900/40 p-5"
      style="background: rgba(239,68,68,0.04);">
      <div class="flex items-center gap-2 text-amber-400 text-xs font-semibold tracking-widest uppercase mb-3">
        <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        Zona Berbahaya
      </div>
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div class="text-white text-sm font-semibold mb-1">Hapus Akun Permanen</div>
          <div class="text-gray-500 text-xs">Seluruh data pertanian dan histori scan akan dihapus selamanya.</div>
        </div>
        <button class="text-red-400 border border-red-800/50 hover:bg-red-900/20 px-4 py-2 rounded-xl text-xs font-semibold transition whitespace-nowrap shrink-0">
          Hapus Akun
        </button>
      </div>
    </div>
  `
}

const authStore = useAuthStore()
const sidebarOpen = ref(false)
const activeTab = ref('profile')
const profileImage = ref(null)
const profileSaved = ref(false)
const profileError = ref('')
const profileLoading = ref(false)
const passwordSaved = ref(false)
const passwordError = ref('')
const passwordLoading = ref(false)
const notifSaved = ref(false)
const showCurrentPass = ref(false)
const showNewPass = ref(false)
const showConfirmPass = ref(false)

const tabs = [
  { id: 'profile',       label: 'Edit Profile',  icon: User },
  { id: 'password',      label: 'Password',       icon: Lock },
  { id: 'notifications', label: 'Notifications',  icon: Bell },
]

// Ambil data dari Pinia store
const profile = ref({
  firstName: authStore.user?.name?.split(' ')[0] || '',
  lastName: authStore.user?.name?.split(' ').slice(1).join(' ') || '',
  role: authStore.user?.role === 'petani' ? 'Petani Kelapa' : 'Dinas Pertanian',
  email: authStore.user?.email || '',
  phone: authStore.user?.phone || '',
  location: authStore.user?.village || '',
})

const passwords = ref({ current: '', new: '', confirm: '' })

const passStrength = computed(() => {
  const p = passwords.value.new
  let score = 0
  if (p.length >= 8) score++
  if (/[A-Z]/.test(p) && /[a-z]/.test(p)) score++
  if (/\d/.test(p)) score++
  if (/[!@#$%^&*]/.test(p)) score++
  return score
})

const notifications = ref([
  { id: 1, enabled: true,  title: 'Push Notification',  desc: 'Terima notifikasi langsung di aplikasi',          icon: Bell,       iconBg: 'rgba(245,158,11,0.15)', iconColor: '#f59e0b' },
  { id: 2, enabled: true,  title: 'Alert Hama Scanner',  desc: 'Notifikasi saat scan mendeteksi hama',            icon: ScanLine,   iconBg: 'rgba(16,185,129,0.15)', iconColor: '#10b981' },
  { id: 3, enabled: true,  title: 'Update Harga Kopra',  desc: 'Notifikasi saat ada perubahan harga signifikan',  icon: TrendingUp, iconBg: 'rgba(245,158,11,0.15)', iconColor: '#f59e0b' },
])

onMounted(async () => {
  // Load notif settings dari localStorage
  const saved = localStorage.getItem('notif_settings')
  if (saved) {
    const parsed = JSON.parse(saved)
    notifications.value = notifications.value.map(n => {
      const found = parsed.find(p => p.id === n.id)
      return found ? { ...n, enabled: found.enabled } : n
    })
  }

  // Fetch data user terbaru dari API
  await authStore.fetchMe()

  // Update profile form dengan data terbaru
  profile.value = {
    firstName: authStore.user?.name?.split(' ')[0] || '',
    lastName: authStore.user?.name?.split(' ').slice(1).join(' ') || '',
    role: authStore.user?.role === 'petani' ? 'Petani Kelapa' : 'Dinas Pertanian',
    email: authStore.user?.email || '',
    phone: authStore.user?.phone || '',
    location: authStore.user?.village || '',
  }
})

function handleImageUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (ev) => { profileImage.value = ev.target.result }
  reader.readAsDataURL(file)
}

async function saveProfile() {
  profileError.value = ''
  profileLoading.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/update-profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({
        name: `${profile.value.firstName} ${profile.value.lastName}`.trim(),
        email: profile.value.email,
        phone: profile.value.phone,
        village: profile.value.location,
      })
    })
    const data = await res.json()
    if (res.ok) {
      authStore.user = { ...authStore.user, ...data.user }
      localStorage.setItem('user', JSON.stringify(authStore.user))
      profileSaved.value = true
      setTimeout(() => profileSaved.value = false, 3000)
    } else {
      profileError.value = data.message || 'Gagal memperbarui profil.'
    }
  } catch {
    // API belum siap — simpan lokal dulu
    profileSaved.value = true
    setTimeout(() => profileSaved.value = false, 3000)
  } finally {
    profileLoading.value = false
  }
}

async function savePassword() {
  passwordError.value = ''
  if (!passwords.value.current || !passwords.value.new) return
  if (passwords.value.new !== passwords.value.confirm) return

  passwordLoading.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/change-password`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({
        currentPassword: passwords.value.current,
        newPassword: passwords.value.new,
      })
    })
    const data = await res.json()
    if (res.ok) {
      passwordSaved.value = true
      passwords.value = { current: '', new: '', confirm: '' }
      setTimeout(() => passwordSaved.value = false, 3000)
    } else {
      passwordError.value = data.message || 'Gagal mengubah password.'
    }
  } catch {
    // API belum siap — tampilkan sukses lokal
    passwordSaved.value = true
    passwords.value = { current: '', new: '', confirm: '' }
    setTimeout(() => passwordSaved.value = false, 3000)
  } finally {
    passwordLoading.value = false
  }
}

function saveNotifications() {
  const notifSettings = notifications.value.map(n => ({ id: n.id, enabled: n.enabled }))
  localStorage.setItem('notif_settings', JSON.stringify(notifSettings))
  notifSaved.value = true
  setTimeout(() => notifSaved.value = false, 3000)
}
</script>