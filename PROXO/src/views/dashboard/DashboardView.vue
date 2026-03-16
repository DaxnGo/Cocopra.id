<template>
  <div class="min-h-screen flex" style="background: #0d2818;">

    <div v-if="sidebarOpen"
      class="fixed inset-0 z-30 bg-black/60 lg:hidden"
      @click="sidebarOpen = false" />

    <DashboardSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex-1 lg:ml-52 flex flex-col min-h-screen">
      <DashboardHeader
        title="Dashboard"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
      />

      <main class="flex-1 p-4 md:p-6 overflow-y-auto">

        <!-- Greeting -->
        <div class="mb-6" data-aos="fade-up">
          <h2 class="text-white text-xl md:text-2xl font-bold">
            {{ greeting }}, {{ authStore.userName }} 👋
          </h2>
          <p class="text-gray-500 text-sm mt-1">{{ currentDate }}</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4 mb-6"
          data-aos="fade-up" data-aos-delay="100">
          <StatsCard
            v-for="card in statsCards"
            :key="card.title"
            :icon="card.icon"
            :iconBg="card.iconBg"
            :iconColor="card.iconColor"
            :title="card.title"
            :desc="card.desc"
            linkText="Buka"
          />
        </div>

        <!-- Bottom Section -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div class="lg:col-span-2" data-aos="fade-up" data-aos-delay="200">
            <ActivityFeed />
          </div>
          <div data-aos="fade-up" data-aos-delay="300">
            <KopraPriceWidget />
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ScanLine, TrendingUp, Bot, ShieldCheck } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import DashboardSidebar from '../../components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'
import StatsCard from '../../components/dashboard/StatsCard.vue'
import ActivityFeed from '../../components/dashboard/ActivityFeed.vue'
import KopraPriceWidget from '../../components/dashboard/KopraPriceWidget.vue'

const authStore = useAuthStore()
const sidebarOpen = ref(false)

// Greeting otomatis sesuai jam
const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 12)  return 'Selamat pagi'
  if (hour >= 12 && hour < 15) return 'Selamat siang'
  if (hour >= 15 && hour < 19) return 'Selamat sore'
  return 'Selamat malam'
})

const currentDate = computed(() => {
  return new Date().toLocaleDateString('id-ID', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  })
})

const statsCards = [
  { icon: ScanLine,    title: 'Scanner',    desc: 'Deteksi hama tanaman kelapa secara instan', iconBg: 'rgba(245,158,11,0.15)', iconColor: '#f59e0b' },
  { icon: TrendingUp,  title: 'Ledger',     desc: 'Pantau harga kopra harian transparan',       iconBg: 'rgba(245,158,11,0.15)', iconColor: '#f59e0b' },
  { icon: Bot,         title: 'Assistant',  desc: 'Tanya asisten AI berbasis dokumen resmi',    iconBg: 'rgba(245,158,11,0.15)', iconColor: '#f59e0b' },
  { icon: ShieldCheck, title: 'Regulatory', desc: 'Cek legalitas pestisida secara instan',      iconBg: 'rgba(245,158,11,0.15)', iconColor: '#f59e0b' },
]
</script>