<template>
  <div class="min-h-screen flex" style="background: #0d2818;">
    <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/60 lg:hidden" @click="sidebarOpen = false" />
    <DashboardSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex-1 lg:ml-52 flex flex-col min-h-screen">
      <DashboardHeader
        title="Regulatory Check"
        subtitle="Verify pesticide legality instantly"
        userName="Budi Pratama"
        userRole="Petani Kelapa"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
      />

      <main class="flex-1 p-4 md:p-6 overflow-y-auto">

        <!-- HERO SEARCH CARD -->
        <div class="rounded-2xl border border-white/8 p-5 md:p-8 mb-6 relative overflow-hidden"
          style="background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(255,255,255,0.03) 100%);">

          <!-- Background decoration — hidden di mobile agar tidak ganggu -->
          <div class="absolute right-6 top-6 opacity-5 hidden md:block">
            <ShieldCheck class="w-32 h-32 text-white" />
          </div>

          <!-- Badge -->
          <div class="inline-flex items-center gap-2 text-emerald-400 text-xs font-semibold tracking-widest uppercase mb-4 border border-emerald-700/50 rounded-full px-3 py-1 max-w-full"
            style="background: rgba(16,185,129,0.08);">
            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse shrink-0"></span>
            <span class="truncate">Official National Registry Access</span>
          </div>

          <h2 class="text-white text-xl md:text-3xl font-bold mb-1">
            Cek Legalitas Produk
          </h2>
          <h2 class="text-amber-400 text-xl md:text-3xl font-bold mb-3 md:mb-4">
            Pestisida Nasional
          </h2>
          <p class="text-gray-400 text-sm max-w-lg mb-5 md:mb-6 leading-relaxed">
            Verifikasi status izin edar resmi Kementerian Pertanian melalui nomor pendaftaran, nama dagang, atau bahan aktif.
          </p>

          <!-- Search Bar -->
          <div class="flex gap-3 flex-col sm:flex-row">
            <div class="flex-1 flex items-center gap-3 bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus-within:border-emerald-500/50 transition">
              <Search class="w-4 h-4 text-gray-500 shrink-0" />
              <input
                v-model="searchQuery"
                @keydown.enter="doSearch"
                type="text"
                placeholder="Cari RI. 0101012023 atau Nama Produk..."
                class="flex-1 bg-transparent text-sm text-white placeholder-gray-600 outline-none min-w-0"
              />
              <button v-if="searchQuery" @click="searchQuery = ''" class="text-gray-500 hover:text-white transition shrink-0">
                <X class="w-4 h-4" />
              </button>
            </div>
            <button @click="doSearch"
              class="flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-6 py-3 rounded-xl text-sm transition">
              <ShieldCheck class="w-4 h-4" /> Verifikasi
            </button>
          </div>
        </div>

        <!-- STATS ROW -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <div v-for="stat in stats" :key="stat.label"
            class="rounded-xl border border-white/8 px-3 md:px-4 py-3 md:py-4"
            style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-wide leading-tight mb-2">{{ stat.label }}</div>
            <div class="flex items-center justify-between">
              <span class="text-white font-bold text-lg md:text-2xl">{{ stat.value }}</span>
              <component :is="stat.icon" class="w-4 h-4 md:w-5 md:h-5 shrink-0" :class="stat.iconColor" />
            </div>
          </div>
        </div>

        <!-- SEARCH RESULTS GRID -->
        <div v-if="searchResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div v-for="result in searchResults" :key="result.id" 
            class="rounded-2xl border p-4 md:p-5 transition hover:border-white/20"
            :class="statusStyle(result.status).cardClass"
            data-aos="fade-up">

            <!-- Header result -->
            <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-4">
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 md:w-12 md:h-12 rounded-xl flex items-center justify-center shrink-0"
                  :class="statusStyle(result.status).iconBg">
                  <component :is="statusStyle(result.status).icon" class="w-5 h-5 md:w-6 md:h-6"
                    :class="statusStyle(result.status).iconColor" />
                </div>
                <div class="min-w-0">
                  <h3 class="text-white font-bold text-base md:text-lg leading-tight">{{ result.name }}</h3>
                  <p class="text-gray-400 text-xs md:text-sm mt-0.5 truncate">{{ result.regNumber }} • {{ result.company }}</p>
                  <p class="text-gray-500 text-xs mt-1">Bahan Aktif: {{ result.activeIngredient }}</p>
                </div>
              </div>
              <div class="flex sm:flex-col items-center sm:items-end gap-2 shrink-0">
                <span class="text-xs font-bold px-2.5 py-1.5 rounded-full whitespace-nowrap"
                  :class="statusStyle(result.status).badgeClass">
                  {{ statusStyle(result.status).label }}
                </span>
              </div>
            </div>

            <!-- Detail info -->
            <div class="pt-4 border-t border-white/5 grid grid-cols-2 gap-3">
              <div>
                <div class="text-gray-600 text-xs mb-1">Kategori</div>
                <div class="text-gray-300 text-xs font-medium">{{ result.category }}</div>
              </div>
              <div>
                <div class="text-gray-600 text-xs mb-1">Tanaman Sasaran</div>
                <div class="text-gray-300 text-xs font-medium truncate">{{ result.targetCrop || '-' }}</div>
              </div>
            </div>
            
            <!-- Warning for limited/illegal -->
            <div v-if="result.status === 'terbatas'"
              class="mt-3 flex items-start gap-2 text-[10px] text-amber-400 bg-amber-900/20 border border-amber-800/30 rounded-lg px-2 py-1.5">
              <TriangleAlert class="w-3 h-3 shrink-0 mt-0.5" />
              <span>Perlu sertifikasi khusus (Dinas Pertanian).</span>
            </div>
          </div>
        </div>

        <!-- NO RESULTS PLACEHOLDER -->
        <div v-else-if="searchQuery && !isSearching" class="mb-6 p-10 text-center rounded-2xl border border-dashed border-white/10 bg-white/2">
          <ShieldCheck class="w-12 h-12 text-gray-700 mx-auto mb-3 opacity-20" />
          <h3 class="text-gray-400 font-medium">Produk tidak terdaftar</h3>
          <p class="text-gray-600 text-sm">Coba cari dengan kata kunci lain atau periksa ejaan.</p>
        </div>

        <!-- RIWAYAT PENCARIAN -->
        <div data-aos="fade-up">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-2 text-white font-semibold text-sm">
              <History class="w-4 h-4 text-amber-400 shrink-0" />
              Hasil Pencarian Terakhir
            </div>
            <button @click="clearHistory"
              class="text-xs text-gray-500 hover:text-red-400 transition font-medium shrink-0">
              HAPUS RIWAYAT
            </button>
          </div>

          <div v-if="searchHistory.length === 0"
            class="text-center py-8 text-gray-600 text-sm">
            Belum ada riwayat pencarian
          </div>

          <div class="flex flex-col gap-3">
            <div v-for="item in searchHistory" :key="item.id"
              class="rounded-xl border border-white/8 px-3 md:px-4 py-3 md:py-4 flex items-center gap-3 hover:border-white/15 transition cursor-pointer group"
              style="background: rgba(255,255,255,0.03);"
              @click="searchQuery = item.name; doSearch()">

              <!-- Status icon -->
              <div class="w-9 h-9 md:w-10 md:h-10 rounded-xl flex items-center justify-center shrink-0"
                :class="statusStyle(item.status).iconBg">
                <component :is="statusStyle(item.status).icon" class="w-4 h-4 md:w-5 md:h-5"
                  :class="statusStyle(item.status).iconColor" />
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0">
                <h4 class="text-white text-sm font-semibold group-hover:text-emerald-400 transition truncate">
                  {{ item.name }}
                </h4>
                <p class="text-gray-500 text-xs truncate">{{ item.regNumber }} • {{ item.company }}</p>
              </div>

              <!-- Badge & expiry — responsive -->
              <div class="shrink-0 text-right">
                <span class="text-xs font-semibold px-2 py-1 rounded-full whitespace-nowrap hidden sm:inline-block"
                  :class="statusStyle(item.status).badgeClass">
                  {{ statusStyle(item.status).label }}
                </span>
                <!-- Mobile: hanya dot warna -->
                <div class="sm:hidden flex justify-end mb-1">
                  <span class="w-2 h-2 rounded-full shrink-0"
                    :class="item.status === 'aktif' ? 'bg-emerald-400' : item.status === 'terbatas' ? 'bg-amber-400' : 'bg-red-400'">
                  </span>
                </div>
                <p class="text-gray-600 text-xs mt-1 hidden sm:block truncate max-w-[120px]">{{ item.expiry }}</p>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Search, ShieldCheck, CheckCircle, TriangleAlert, XCircle, X, History, FileText } from 'lucide-vue-next'
import DashboardSidebar from '../../components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'
import api from '../../api/axios.js'

const sidebarOpen = ref(false)
const searchQuery = ref('')
const searchResult = ref(null)
const isSearching = ref(false)

const stats = [
  { label: 'Total Produk Terdaftar', value: '12,482', icon: FileText,      iconColor: 'text-gray-400' },
  { label: 'Izin Aktif (Safe)',      value: '8,902',  icon: CheckCircle,   iconColor: 'text-emerald-400' },
  { label: 'Penggunaan Terbatas',    value: '2,140',  icon: TriangleAlert, iconColor: 'text-amber-400' },
  { label: 'Izin Dicabut / Ilegal',  value: '1,440',  icon: XCircle,       iconColor: 'text-red-400' },
]

const localDB = ref([])
const dbLoaded = ref(false)

const searchHistory = ref([])

onMounted(async () => {
  try {
    const res = await fetch('/pestisida.json')
    if (res.ok) {
      localDB.value = await res.json()
      dbLoaded.value = true
      // Optional: seed history with random items or leave empty
    }
  } catch (err) {
    console.error("Gagal memuat pestisida.json:", err)
  }
})

function statusStyle(status) {
  const styles = {
    aktif: {
      label: 'Terdaftar & Legal',
      icon: CheckCircle,
      iconColor: 'text-emerald-400',
      iconBg: 'bg-emerald-900/40',
      badgeClass: 'bg-emerald-900/50 text-emerald-400 border border-emerald-700/50',
      cardClass: 'border-emerald-800/30 bg-emerald-900/10',
    },
    terbatas: {
      label: 'Penggunaan Terbatas',
      icon: TriangleAlert,
      iconColor: 'text-amber-400',
      iconBg: 'bg-amber-900/40',
      badgeClass: 'bg-amber-900/50 text-amber-400 border border-amber-700/50',
      cardClass: 'border-amber-800/30 bg-amber-900/10',
    },
    ilegal: {
      label: 'Ilegal / Dicabut',
      icon: XCircle,
      iconColor: 'text-red-400',
      iconBg: 'bg-red-900/40',
      badgeClass: 'bg-red-900/50 text-red-400 border border-red-700/50',
      cardClass: 'border-red-800/30 bg-red-900/10',
    },
  }
  return styles[status] || styles.aktif
}

const searchResults = ref([])

// Live Search with Debounce
let searchTimeout = null
watch(searchQuery, (newQuery) => {
  clearTimeout(searchTimeout)
  if (!newQuery.trim()) {
    searchResults.value = []
    return
  }
  searchTimeout = setTimeout(() => {
    doSearch()
  }, 300)
})

async function doSearch() {
  if (!searchQuery.value.trim() || !dbLoaded.value) {
    searchResults.value = []
    return
  }
  const query = searchQuery.value.toLowerCase().trim()
  isSearching.value = true

  // Cari di database lokal (filter semua yang cocok, bukan cuma satu)
  const matches = localDB.value.filter(p =>
    (p.name && p.name.toLowerCase().includes(query)) ||
    (p.regNumber && p.regNumber.toLowerCase().includes(query)) ||
    (p.activeIngredient && p.activeIngredient.toLowerCase().includes(query))
  )

  searchResults.value = matches.slice(0, 20) // Limit ke 20 hasil teratas agar performa tetap ringan

  // Update history dengan hasil pertama yang paling cocok jika ada
  if (matches.length > 0) {
    const first = matches[0]
    const exists = searchHistory.value.find(h => h.id === first.id)
    if (!exists) {
      searchHistory.value.unshift({ ...first })
      if (searchHistory.value.length > 5) searchHistory.value.pop()
    }
  }

  isSearching.value = false
}

function clearHistory() {
  searchHistory.value = []
}
</script>