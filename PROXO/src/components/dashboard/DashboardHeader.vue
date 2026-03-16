<template>
  <header class="flex items-center justify-between px-4 md:px-6 py-4 border-b border-white/5 sticky top-0 z-20"
    style="background: #0d2818;">
    <div class="flex items-center gap-3">
      <!-- Hamburger — hanya di mobile -->
      <button @click="$emit('toggle-sidebar')"
        class="lg:hidden text-gray-400 hover:text-white transition p-1">
        <Menu class="w-5 h-5" />
      </button>
      <div>
        <h1 class="text-white font-bold text-lg md:text-xl">{{ title }}</h1>
        <p v-if="subtitle" class="text-gray-500 text-xs">{{ subtitle }}</p>
      </div>
    </div>

    <div class="flex items-center gap-3 md:gap-4">
      <!-- Notifikasi -->
      <button class="relative text-gray-400 hover:text-white transition">
        <Bell class="w-5 h-5" />
        <span class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center font-bold">3</span>
      </button>

      <!-- User info -->
      <div class="flex items-center gap-2 md:gap-3">
        <div class="text-right hidden sm:block">
          <div class="text-white text-sm font-semibold">{{ displayName }}</div>
          <div class="text-gray-500 text-xs">{{ displayRole }}</div>
        </div>
        <div class="w-9 h-9 rounded-full bg-amber-500 flex items-center justify-center text-black font-bold text-sm shrink-0">
          {{ userInitial }}
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { Bell, Menu } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'

const props = defineProps({
  title: { type: String, default: 'Dashboard' },
  subtitle: { type: String, default: '' },
  // Props ini tetap ada sebagai fallback jika store kosong
  userName: { type: String, default: '' },
  userRole: { type: String, default: '' },
})

defineEmits(['toggle-sidebar'])

const authStore = useAuthStore()

// Prioritas: dari store → dari props → default
const displayName = computed(() =>
  authStore.userName || props.userName || 'Pengguna'
)

const displayRole = computed(() => {
  if (authStore.user?.role) {
    return authStore.user.role === 'petani' ? 'Petani Kelapa' :
           authStore.user.role === 'dinas' ? 'Dinas Pertanian' :
           'Petani Kelapa' // default fallback
  }
  return props.userRole || 'Petani Kelapa'
})

const userInitial = computed(() =>
  displayName.value.charAt(0).toUpperCase()
)
</script>