<template>
  <!-- Sidebar: fixed di desktop, slide-in di mobile -->
  <aside
    class="fixed left-0 top-0 h-screen w-52 flex flex-col z-40 transition-transform duration-300"
    :class="isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
    style="background: #0a1f12; border-right: 1px solid rgba(255,255,255,0.06);">

    <!-- Logo + Close button mobile -->
    <div class="px-5 py-5 border-b border-white/5 flex items-center justify-between">
      <RouterLink to="/" class="flex items-center gap-2">
        <img src="/Logo-Cocopra.id.png" alt="Logo" class="w-8 h-8 object-contain" />
        <span class="text-white font-bold text-lg">Cocopra<span class="text-amber-400">.id</span></span>
      </RouterLink>
      <button @click="$emit('close')" class="lg:hidden text-gray-400 hover:text-white p-1">
        <X class="w-5 h-5" />
      </button>
    </div>

    <!-- Menu -->
    <nav class="flex-1 px-3 py-4 flex flex-col gap-1 overflow-y-auto">
      <p class="text-gray-600 text-xs font-semibold tracking-widest uppercase px-3 mb-2">Utama</p>

      <RouterLink to="/dashboard" @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
        :class="$route.path === '/dashboard' ? 'bg-emerald-900/50 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-white/5'">
        <LayoutDashboard class="w-4 h-4 shrink-0" /> Dashboard
      </RouterLink>

      <RouterLink to="/dashboard/scanner" @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
        :class="$route.path === '/dashboard/scanner' ? 'bg-emerald-900/50 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-white/5'">
        <ScanLine class="w-4 h-4 shrink-0" /> Scanner
      </RouterLink>

      <RouterLink to="/dashboard/harga-kopra" @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
        :class="$route.path === '/dashboard/harga-kopra' ? 'bg-emerald-900/50 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-white/5'">
        <TrendingUp class="w-4 h-4 shrink-0" /> Harga Kopra
      </RouterLink>

      <RouterLink to="/dashboard/asisten-ai" @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
        :class="$route.path === '/dashboard/asisten-ai' ? 'bg-emerald-900/50 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-white/5'">
        <Bot class="w-4 h-4 shrink-0" /> Asisten AI
      </RouterLink>

      <RouterLink to="/dashboard/regulatory" @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition"
        :class="$route.path === '/dashboard/regulatory' ? 'bg-emerald-900/50 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-white/5'">
        <ShieldCheck class="w-4 h-4 shrink-0" /> Regulatory Check
      </RouterLink>
    </nav>

    <!-- Bottom -->
    <div class="px-3 py-4 border-t border-white/5 flex flex-col gap-1">
      <RouterLink to="/dashboard/settings" @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition w-full"
        :class="$route.path === '/dashboard/settings' ? 'bg-emerald-900/50 text-emerald-400' : 'text-gray-400 hover:text-white hover:bg-white/5'">
        <Settings class="w-4 h-4 shrink-0" /> Settings
      </RouterLink>
      <button @click="handleLogout"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-red-400 hover:text-red-300 hover:bg-red-900/20 transition w-full">
        <LogOut class="w-4 h-4 shrink-0" /> Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { LayoutDashboard, ScanLine, TrendingUp, Bot, ShieldCheck, Settings, LogOut, X } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useRouter } from 'vue-router'

defineProps({ isOpen: Boolean })
defineEmits(['close'])

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>