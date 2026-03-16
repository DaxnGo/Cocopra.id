<template>
  <div class="min-h-screen flex" style="background: #0d2818;">
    <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/60 lg:hidden" @click="sidebarOpen = false" />
    <DashboardSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex-1 lg:ml-52 flex flex-col min-h-screen">
      <DashboardHeader
        title="Harga Kopra"
        subtitle="Monitor and report daily kopra prices"
        userName="Budi Pratama"
        userRole="Petani Kelapa"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
      />

      <main class="flex-1 p-4 md:p-6 overflow-y-auto">

        <!-- HEADER SECTION -->
        <div class="mb-6" data-aos="fade-up">
          <div class="text-amber-400 text-xs font-semibold tracking-widest uppercase mb-2 flex items-center gap-2">
            <div class="w-6 h-0.5 bg-amber-400"></div>
            Transparency Ledger
          </div>
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-3">
            <div>
              <h2 class="text-white text-2xl md:text-3xl font-bold mb-1">Adil-Harga Ledger</h2>
              <p class="text-gray-400 text-sm max-w-lg leading-relaxed">
                Pantau transparansi harga pasar secara langsung untuk melindungi ekosistem petani dari praktek harga yang tidak adil.
              </p>
            </div>
            <div class="flex items-center gap-2 text-xs text-emerald-400 border border-emerald-700/50 bg-emerald-900/20 px-3 py-1.5 rounded-full whitespace-nowrap self-start">
              <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
              Live Updates • {{ lastUpdate }}
            </div>
          </div>
        </div>

        <!-- STATS CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6" data-aos="fade-up" data-aos-delay="100">
          <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Average Price</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-white font-bold text-xl md:text-2xl">Rp 4.033 <span class="text-xs font-normal text-gray-500">/kg</span></div>
                <div class="text-emerald-400 text-xs mt-1 flex items-center gap-1">
                  <TrendingUp class="w-3 h-3" /> +2.4% vs yesterday
                </div>
              </div>
              <BarChart2 class="w-5 h-5 text-gray-600" />
            </div>
          </div>

          <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Highest Price</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-white font-bold text-xl md:text-2xl">Rp 4.500 <span class="text-xs font-normal text-gray-500">/kg</span></div>
                <div class="text-gray-500 text-xs mt-1 flex items-center gap-1">
                  <MapPin class="w-3 h-3" /> Bitung Region
                </div>
              </div>
              <TrendingUp class="w-5 h-5 text-gray-600" />
            </div>
          </div>

          <div class="rounded-xl border border-red-800/30 p-4" style="background: rgba(239,68,68,0.05);">
            <div class="text-red-400 text-xs uppercase tracking-widest mb-2">Lowest Price</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-red-400 font-bold text-xl md:text-2xl">Rp 2.800 <span class="text-xs font-normal">/kg</span></div>
                <div class="text-red-400 text-xs mt-1 flex items-center gap-1">
                  <TriangleAlert class="w-3 h-3" /> Anomaly Detected
                </div>
              </div>
              <TriangleAlert class="w-5 h-5 text-red-400/50" />
            </div>
          </div>

          <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Active Buyers</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-white font-bold text-xl md:text-2xl">12</div>
                <div class="text-gray-500 text-xs mt-1">Within 20km radius</div>
              </div>
              <Users class="w-5 h-5 text-gray-600" />
            </div>
          </div>
        </div>

        <!-- CHART + FORM -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6" data-aos="fade-up" data-aos-delay="200">

          <!-- Chart - 2/3 width -->
          <div class="lg:col-span-2 rounded-2xl border border-white/8 p-5"
            style="background: rgba(255,255,255,0.03);">
            <div class="flex items-start justify-between mb-1">
              <div>
                <h3 class="text-white font-semibold">Tren Harga Regional</h3>
                <p class="text-gray-500 text-xs mt-0.5">Monitoring pergerakan harian Sulawesi Utara</p>
              </div>
              <!-- Time filter -->
              <div class="flex items-center gap-1 bg-white/5 rounded-lg p-1">
                <button v-for="period in ['7H', '30H', '90H']" :key="period"
                  @click="activePeriod = period"
                  class="px-2.5 py-1 rounded-md text-xs font-medium transition"
                  :class="activePeriod === period ? 'bg-amber-500 text-black' : 'text-gray-400 hover:text-white'">
                  {{ period }}
                </button>
              </div>
            </div>

            <!-- Chart -->
            <div class="h-48 md:h-56 mt-4">
              <Line :data="chartData" :options="chartOptions" />
            </div>

            <!-- Anomaly threshold label -->
            <div class="mt-3 flex items-center gap-2 text-xs text-red-400/60">
              <div class="w-8 h-px bg-red-400/40 border-dashed"></div>
              Anomaly Threshold
            </div>
          </div>

          <!-- Form Input Laporan - 1/3 width -->
          <div class="rounded-2xl border border-white/8 p-5"
            style="background: rgba(255,255,255,0.03);">
            <h3 class="text-white font-semibold mb-4">Input Laporan Baru</h3>
            <div class="flex flex-col gap-3">
              <div>
                <label class="text-gray-500 text-xs uppercase tracking-widest mb-1.5 block">Nama Pengepul</label>
                <input v-model="form.collectorName" type="text" placeholder="UD. Berkat Jaya"
                  class="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-sm text-white placeholder-gray-600 outline-none focus:border-amber-500/50 transition" />
              </div>
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="text-gray-500 text-xs uppercase tracking-widest mb-1.5 block">Harga (Rp/kg)</label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-xs">Rp</span>
                    <input v-model="form.price" type="number" placeholder="0"
                      class="w-full bg-white/5 border border-white/10 rounded-xl pl-8 pr-3 py-2.5 text-sm text-white placeholder-gray-600 outline-none focus:border-amber-500/50 transition" />
                  </div>
                </div>
                <div>
                  <label class="text-gray-500 text-xs uppercase tracking-widest mb-1.5 block">Kualitas</label>
                  <select v-model="form.quality"
                    class="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2.5 text-sm text-white outline-none focus:border-amber-500/50 transition">
                    <option value="A">A (Kering)</option>
                    <option value="B">B (Standar)</option>
                    <option value="C">C (Basah)</option>
                  </select>
                </div>
              </div>
              <div>
                <label class="text-gray-500 text-xs uppercase tracking-widest mb-1.5 block">Lokasi Transaksi</label>
                <div class="relative">
                  <MapPin class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-500" />
                  <input v-model="form.location" type="text" placeholder="Koordinat atau Alamat"
                    class="w-full bg-white/5 border border-white/10 rounded-xl pl-8 pr-3 py-2.5 text-sm text-white placeholder-gray-600 outline-none focus:border-amber-500/50 transition" />
                </div>
              </div>
              <button @click="submitReport"
                class="w-full bg-amber-500 hover:bg-amber-400 text-black font-bold py-2.5 rounded-xl text-sm transition mt-1">
                KIRIM LAPORAN HARGA
              </button>

              <!-- Success state -->
              <div v-if="reportSubmitted"
                class="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-900/20 border border-emerald-700/30 rounded-lg px-3 py-2">
                <CheckCircle class="w-3 h-3 shrink-0" />
                Laporan berhasil dikirim! Terima kasih.
              </div>
            </div>
          </div>
        </div>

        <!-- LEDGER TABLE -->
        <div class="rounded-2xl border border-white/8 overflow-hidden" data-aos="fade-up" data-aos-delay="300"
          style="background: rgba(255,255,255,0.03);">

          <!-- Table header -->
          <div class="px-5 py-4 border-b border-white/5 flex items-center justify-between">
            <div>
              <h3 class="text-white font-semibold text-sm">Ledger Harga Komunitas</h3>
              <p class="text-gray-600 text-xs mt-0.5 tracking-widest uppercase">Verified Ledger on Decentralized Local Network</p>
            </div>
            <button class="flex items-center gap-2 text-xs text-gray-400 hover:text-white border border-white/10 hover:border-white/20 px-3 py-1.5 rounded-lg transition">
              <Download class="w-3 h-3" /> Unduh Ledger
            </button>
          </div>

          <!-- Table desktop -->
          <div class="hidden md:block overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/5">
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Pengepul</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Wilayah</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Harga</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Mutu</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Verifikasi</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Update</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in ledgerData" :key="item.id"
                  class="border-b border-white/5 last:border-0 hover:bg-white/2 transition">
                  <td class="px-5 py-4">
                    <span class="text-sm font-medium"
                      :class="item.anomaly ? 'text-red-400' : 'text-white'">
                      {{ item.collector }}
                    </span>
                  </td>
                  <td class="px-5 py-4 text-gray-400 text-sm">{{ item.region }}</td>
                  <td class="px-5 py-4">
                    <span class="font-semibold text-sm"
                      :class="item.anomaly ? 'text-red-400' : 'text-white'">
                      Rp {{ item.price.toLocaleString('id-ID') }}
                    </span>
                  </td>
                  <td class="px-5 py-4 text-gray-400 text-sm">{{ item.quality }}</td>
                  <td class="px-5 py-4">
                    <span v-if="!item.anomaly"
                      class="text-xs text-emerald-400 bg-emerald-900/30 border border-emerald-700/40 px-2.5 py-1 rounded-full font-medium">
                      ✓ Terverifikasi
                    </span>
                    <span v-else
                      class="text-xs text-amber-400 bg-amber-900/30 border border-amber-700/40 px-2.5 py-1 rounded-full font-medium">
                      ⚠ Anomali
                    </span>
                  </td>
                  <td class="px-5 py-4 text-gray-500 text-sm">{{ item.updatedAt }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Table mobile — card style -->
          <div class="md:hidden flex flex-col divide-y divide-white/5">
            <div v-for="item in ledgerData" :key="item.id" class="px-4 py-4">
              <div class="flex items-start justify-between mb-2">
                <span class="text-sm font-semibold"
                  :class="item.anomaly ? 'text-red-400' : 'text-white'">
                  {{ item.collector }}
                </span>
                <span v-if="!item.anomaly"
                  class="text-xs text-emerald-400 bg-emerald-900/30 border border-emerald-700/40 px-2 py-0.5 rounded-full">
                  ✓ Verified
                </span>
                <span v-else
                  class="text-xs text-amber-400 bg-amber-900/30 border border-amber-700/40 px-2 py-0.5 rounded-full">
                  ⚠ Anomali
                </span>
              </div>
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span>{{ item.region }} • {{ item.quality }}</span>
                <span class="font-semibold" :class="item.anomaly ? 'text-red-400' : 'text-white'">
                  Rp {{ item.price.toLocaleString('id-ID') }}
                </span>
              </div>
              <div class="text-gray-600 text-xs mt-1">{{ item.updatedAt }}</div>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale,
  PointElement, LineElement, Filler, Tooltip
} from 'chart.js'
import {
  TrendingUp, BarChart2, MapPin, TriangleAlert,
  Users, CheckCircle, Download
} from 'lucide-vue-next'
import DashboardSidebar from '../../components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'
import api from '../../api/axios.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler, Tooltip)

const sidebarOpen = ref(false)
const activePeriod = ref('30H')
const reportSubmitted = ref(false)
const lastUpdate = ref('5M AGO')

const form = ref({
  collectorName: '',
  price: '',
  quality: 'A',
  location: '',
})

// Data trend dari backend
const trendData = ref([])

// Chart data — gunakan data dari backend jika tersedia
const chartData = computed(() => {
  // Jika ada data trend dari API, gunakan itu
  if (trendData.value.length > 0) {
    return {
      labels: trendData.value.map(t => t.date),
      datasets: [
        {
          label: 'Harga Pasar',
          data: trendData.value.map(t => t.harga),
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245,158,11,0.08)',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: '#f59e0b',
          pointBorderColor: 'transparent',
        }
      ]
    }
  }

  // Fallback ke mock data berdasarkan period
  const datasets = {
    '7H': [4100, 4050, 4200, 4150, 4300, 4250, 4033],
    '30H': [3800, 3850, 3900, 3750, 3950, 4000, 3900, 4100, 4050, 3800, 2800, 3900, 4000, 4100, 4200, 4150, 4300, 4250, 4033, 4100, 4050, 4200, 4300, 4100, 4000, 3950, 4050, 4100, 4150, 4033],
    '90H': [3500, 3600, 3700, 3800, 3750, 3900, 4000, 3950, 4100, 4050, 4200, 4150, 4300, 4250, 4033],
  }
  const labels = {
    '7H': ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'],
    '30H': Array.from({ length: 30 }, (_, i) => `${i + 1}`),
    '90H': Array.from({ length: 15 }, (_, i) => `M${i + 1}`),
  }
  return {
    labels: labels[activePeriod.value],
    datasets: [
      {
        label: 'Harga Pasar',
        data: datasets[activePeriod.value],
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245,158,11,0.08)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointBackgroundColor: '#f59e0b',
        pointBorderColor: 'transparent',
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(10,31,18,0.95)',
      borderColor: 'rgba(245,158,11,0.3)',
      borderWidth: 1,
      titleColor: '#9ca3af',
      bodyColor: '#f59e0b',
      callbacks: {
        label: (ctx) => ` Rp ${ctx.raw.toLocaleString('id-ID')}/kg`
      }
    }
  },
  scales: {
    x: {
      grid: { color: 'rgba(255,255,255,0.03)' },
      ticks: { color: '#4b5563', font: { size: 10 } },
    },
    y: {
      grid: { color: 'rgba(255,255,255,0.05)' },
      ticks: {
        color: '#4b5563',
        font: { size: 10 },
        callback: (val) => `${(val/1000).toFixed(1)}k`
      },
    }
  }
}

// Ledger data — mulai kosong, diisi dari API
const ledgerData = ref([
  { id: 1, collector: 'PT. Kelapa Berkah',  region: 'Bitung Selatan', price: 4250, quality: 'Premium (A)', anomaly: false, updatedAt: '08:45' },
  { id: 2, collector: 'Pengepul Rahasia',   region: 'Kauditan',       price: 2800, quality: 'Kualitas A',  anomaly: true,  updatedAt: '09:12' },
  { id: 3, collector: 'CV. Mandiri Jaya',   region: 'Airmadidi',      price: 4100, quality: 'Standar (B)', anomaly: false, updatedAt: '07:30' },
  { id: 4, collector: 'UD. Sulut Makmur',   region: 'Likupang',       price: 4300, quality: 'Premium (A)', anomaly: false, updatedAt: '08:15' },
  { id: 5, collector: 'Toko Sumber Rejeki', region: 'Tondano',        price: 3950, quality: 'Standar (B)', anomaly: false, updatedAt: '06:50' },
])

// Fetch ledger dari backend
async function fetchLedger() {
  try {
    const res = await api.get('/harga/')
    if (res.data && res.data.length > 0) {
      ledgerData.value = res.data.map(item => {
        const ts = new Date(item.timestamp)
        return {
          id: item.id,
          collector: item.pembeli || 'Tidak diketahui',
          region: item.lokasi,
          price: item.harga,
          quality: 'Kualitas -',
          anomaly: item.is_anomaly,
          updatedAt: ts.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        }
      })
    }
  } catch (err) {
    console.warn('fetchLedger fallback ke mock:', err.message)
  }
}

// Fetch trend dari backend
async function fetchTrend() {
  try {
    const res = await api.get('/harga/trend')
    if (res.data && res.data.length > 0) {
      trendData.value = res.data
    }
  } catch (err) {
    console.warn('fetchTrend fallback ke mock chart:', err.message)
  }
}

// Load data saat komponen dimuat
onMounted(() => {
  fetchLedger()
  fetchTrend()
})

async function submitReport() {
  if (!form.value.collectorName || !form.value.price) return

  try {
    const payload = {
      harga: Number(form.value.price),
      lokasi: form.value.location || 'Tidak diketahui',
      pembeli: form.value.collectorName,
      timestamp: new Date().toISOString(),
    }
    const res = await api.post('/harga/', payload)
    const item = res.data

    // Tambah ke ledger lokal
    ledgerData.value.unshift({
      id: item.id,
      collector: item.pembeli || form.value.collectorName,
      region: item.lokasi,
      price: item.harga,
      quality: form.value.quality === 'A' ? 'Kualitas A' : form.value.quality === 'B' ? 'Standar (B)' : 'Basah (C)',
      anomaly: item.is_anomaly,
      updatedAt: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
    })

    reportSubmitted.value = true
    form.value = { collectorName: '', price: '', quality: 'A', location: '' }
    setTimeout(() => reportSubmitted.value = false, 3000)

    // Refresh trend data
    fetchTrend()
  } catch (err) {
    console.error('submitReport error:', err)
    // Fallback: simpan lokal saja
    ledgerData.value.unshift({
      id: Date.now(),
      collector: form.value.collectorName,
      region: form.value.location || 'Tidak diketahui',
      price: Number(form.value.price),
      quality: form.value.quality === 'A' ? 'Kualitas A' : form.value.quality === 'B' ? 'Standar (B)' : 'Basah (C)',
      anomaly: Number(form.value.price) < 3500,
      updatedAt: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
    })
    reportSubmitted.value = true
    form.value = { collectorName: '', price: '', quality: 'A', location: '' }
    setTimeout(() => reportSubmitted.value = false, 3000)
  }
}
</script>