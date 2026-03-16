<template>
  <div class="min-h-screen flex" style="background: #0d2818;">
    <div v-if="sidebarOpen" class="fixed inset-0 z-30 bg-black/60 lg:hidden" @click="sidebarOpen = false" />
    <DashboardSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <div class="flex-1 lg:ml-52 flex flex-col min-h-screen">
      <DashboardHeader
        title="Scanner"
        subtitle="Detect pests from your plant photos"
        userName="Budi Pratama"
        userRole="Petani Kelapa"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
      />

      <main class="flex-1 p-4 md:p-6 overflow-y-auto">

        <!-- HEADER -->
        <div class="mb-6" data-aos="fade-up">
          <div class="text-amber-400 text-xs font-semibold tracking-widest uppercase mb-2 flex items-center gap-2">
            <div class="w-6 h-0.5 bg-amber-400"></div>
            Pest Detection System
          </div>
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-3">
            <div>
              <h2 class="text-white text-2xl md:text-3xl font-bold mb-2">Pest-Vision Scanner</h2>
              <p class="text-gray-400 text-sm max-w-lg leading-relaxed">
                Ambil foto daun atau batang kelapa Anda untuk analisis bepaskuri instan menggunakan model AI yang dilatih khusus untuk komoditas tropis.
              </p>
            </div>
            <div class="flex items-center gap-2 text-xs text-emerald-400 border border-emerald-700/50 bg-emerald-900/20 px-3 py-1.5 rounded-full whitespace-nowrap self-start">
              <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
              Live Analysis • AI Ready
            </div>
          </div>
        </div>

        <!-- STATS CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6" data-aos="fade-up" data-aos-delay="100">
          <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Total Scan</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-white font-bold text-2xl">128 <span class="text-xs font-normal text-gray-500">Analisis</span></div>
                <div class="text-emerald-400 text-xs mt-1 flex items-center gap-1">
                  <TrendingUp class="w-3 h-3" /> +12% vs bulan lalu
                </div>
              </div>
              <ScanLine class="w-5 h-5 text-gray-600" />
            </div>
          </div>

          <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Akurasi AI</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-white font-bold text-2xl">98.4<span class="text-base">%</span></div>
                <div class="text-emerald-400 text-xs mt-1">Model v4.2 Aktif</div>
              </div>
              <Cpu class="w-5 h-5 text-gray-600" />
            </div>
          </div>

          <div class="rounded-xl border border-red-800/30 p-4" style="background: rgba(239,68,68,0.05);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Hama Terdeteksi</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-red-400 font-bold text-2xl">3 <span class="text-xs font-normal">Fokus Alert</span></div>
                <div class="text-red-400 text-xs mt-1 flex items-center gap-1">
                  <TriangleAlert class="w-3 h-3" /> Tindakan Diperlukan
                </div>
              </div>
              <Bug class="w-5 h-5 text-red-400/50" />
            </div>
          </div>

          <div class="rounded-xl border border-white/8 p-4" style="background: rgba(255,255,255,0.03);">
            <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Scan Terakhir</div>
            <div class="flex items-end justify-between">
              <div>
                <div class="text-white font-bold text-2xl">42<span class="text-base text-gray-500">m</span> <span class="text-xs font-normal text-gray-500">lalu</span></div>
                <div class="text-gray-500 text-xs mt-1">08:30 WITA, Hari Ini</div>
              </div>
              <Clock class="w-5 h-5 text-gray-600" />
            </div>
          </div>
        </div>

        <!-- MAIN CONTENT: Upload + Tips -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6" data-aos="fade-up" data-aos-delay="200">

          <!-- Upload Area — 2/3 -->
          <div class="lg:col-span-2 flex flex-col gap-4">

            <!-- Upload Card -->
            <div class="rounded-2xl border border-white/8 p-6"
              style="background: rgba(255,255,255,0.03);">

              <!-- Preview state -->
              <div v-if="!previewImage && !isAnalyzing && !scanResult">
                <div
                  class="border-2 border-dashed border-white/10 rounded-2xl p-8 md:p-12 flex flex-col items-center justify-center text-center hover:border-emerald-700/50 transition cursor-pointer"
                  @dragover.prevent @drop.prevent="handleDrop" @click="triggerFileInput">
                  <div class="w-14 h-14 rounded-2xl bg-amber-900/20 border border-amber-700/30 flex items-center justify-center mb-4">
                    <Camera class="w-7 h-7 text-amber-400" />
                  </div>
                  <h3 class="text-white font-semibold mb-2">Unggah Foto Sampel</h3>
                  <p class="text-gray-500 text-sm mb-6 max-w-xs leading-relaxed">
                    Seret foto ke sini atau ambil langsung dari kamera ponsel Anda.
                  </p>
                  <div class="flex gap-3 flex-wrap justify-center">
                    <button @click.stop="triggerFileInput"
                      class="flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-5 py-2.5 rounded-xl text-sm transition">
                      <Camera class="w-4 h-4" /> Ambil Foto
                    </button>
                    <button @click.stop="triggerFileInput"
                      class="flex items-center gap-2 border border-white/20 hover:border-white/40 text-white px-5 py-2.5 rounded-xl text-sm transition">
                      <Upload class="w-4 h-4" /> Pilih File
                    </button>
                  </div>
                  <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileSelect" />
                </div>
              </div>

              <!-- Analyzing state -->
              <div v-if="isAnalyzing" class="flex flex-col items-center justify-center py-12 text-center">
                <div class="w-20 h-20 rounded-2xl bg-emerald-900/30 border border-emerald-700/30 flex items-center justify-center mb-4 relative">
                  <ScanLine class="w-10 h-10 text-emerald-400" />
                  <div class="absolute inset-0 rounded-2xl border-2 border-emerald-400/30 animate-ping"></div>
                </div>
                <h3 class="text-white font-semibold mb-2">Menganalisis Gambar...</h3>
                <p class="text-gray-500 text-sm mb-4">Model AI sedang memproses foto Anda</p>
                <div class="w-48 h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div class="h-full bg-emerald-400 rounded-full animate-pulse" style="width: 70%"></div>
                </div>
              </div>

              <!-- Result state -->
              <div v-if="scanResult && !isAnalyzing">
                <div class="flex flex-col md:flex-row gap-4">
                  <!-- Image preview -->
                  <div class="relative md:w-2/5 rounded-xl overflow-hidden shrink-0" style="min-height: 200px;">
                    <img :src="previewImage" alt="Scan result" class="w-full h-full object-cover rounded-xl" />
                    <div class="absolute bottom-2 left-2 bg-black/60 rounded-lg px-2 py-1 text-xs text-gray-300 backdrop-blur-sm">
                      LIVE PREVIEW
                    </div>
                  </div>

                  <!-- Result info -->
                  <div class="flex-1">
                    <div class="flex items-start justify-between gap-2 mb-3">
                      <div>
                        <h3 class="text-red-400 font-bold text-lg italic">{{ scanResult.latinName }}</h3>
                        <p class="text-white font-semibold">{{ scanResult.commonName }}</p>
                      </div>
                      <span class="text-xs font-bold px-2.5 py-1 rounded-full shrink-0"
                        :class="scanResult.severity === 'SEDANG' ? 'bg-amber-900/50 text-amber-400 border border-amber-700/50' : 'bg-red-900/50 text-red-400 border border-red-700/50'">
                        {{ scanResult.severity }}
                      </span>
                    </div>

                    <div class="mb-3">
                      <div class="flex justify-between text-xs text-gray-400 mb-1">
                        <span>Tingkat Keyakinan AI</span>
                        <span class="text-amber-400 font-bold">{{ scanResult.confidence }}% Confidence</span>
                      </div>
                      <div class="w-full bg-white/10 rounded-full h-1.5">
                        <div class="bg-amber-400 h-1.5 rounded-full transition-all duration-1000"
                          :style="`width: ${scanResult.confidence}%`"></div>
                      </div>
                    </div>

                    <div>
                      <div class="text-gray-500 text-xs uppercase tracking-widest mb-2">Rekomendasi Tindakan:</div>
                      <div class="flex flex-col gap-1.5">
                        <div v-for="(action, i) in scanResult.actions" :key="i"
                          class="flex items-start gap-2 text-xs text-gray-300">
                          <CheckSquare class="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                          {{ action }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Scan again button -->
                <button @click="resetScan"
                  class="mt-4 flex items-center gap-2 border border-white/20 hover:border-white/40 text-white px-4 py-2 rounded-xl text-sm transition">
                  <RefreshCw class="w-4 h-4" /> Scan Ulang
                </button>
              </div>
            </div>

            <!-- Hasil Analisis Terakhir (selalu tampil) -->
            <div v-if="lastScanPreview" class="rounded-2xl border border-white/8 p-4"
              style="background: rgba(255,255,255,0.03);">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-white font-semibold text-sm">Hasil Analisis Terakhir</h3>
                <span class="text-gray-600 text-xs">REF: #KN-PREV-COCO</span>
              </div>
              <div class="flex flex-col sm:flex-row gap-3">
                <img src="/michael-oxendine-aKvfQV4WpiA-unsplash.jpg"
                  class="w-full sm:w-32 h-24 object-cover rounded-xl shrink-0" alt="Last scan" />
                <div class="flex-1">
                  <div class="flex items-start justify-between gap-2 mb-2">
                    <div>
                      <h4 class="text-red-400 font-semibold italic text-sm">Oryctes rhinoceros</h4>
                      <p class="text-white text-xs">Kumbang Badak Kelapa</p>
                    </div>
                    <span class="text-xs bg-amber-900/50 text-amber-400 border border-amber-700/50 px-2 py-0.5 rounded-full shrink-0">SEDANG</span>
                  </div>
                  <div class="flex justify-between text-xs text-gray-400 mb-1">
                    <span>Tingkat Keyakinan AI</span>
                    <span class="text-amber-400 font-bold">94% Confidence</span>
                  </div>
                  <div class="w-full bg-white/10 rounded-full h-1.5 mb-3">
                    <div class="bg-amber-400 h-1.5 rounded-full" style="width: 94%"></div>
                  </div>
                  <div class="text-gray-500 text-xs uppercase tracking-widest mb-1.5">Rekomendasi Tindakan:</div>
                  <div class="flex flex-col gap-1">
                    <div class="flex items-center gap-2 text-xs text-gray-300">
                      <CheckSquare class="w-3 h-3 text-emerald-400 shrink-0" /> Bersihkan tumpukan sampah di sekitar pohon
                    </div>
                    <div class="flex items-center gap-2 text-xs text-gray-300">
                      <CheckSquare class="w-3 h-3 text-emerald-400 shrink-0" /> Pasang jebakan feromon pada ketinggian 1.5m
                    </div>
                    <div class="flex items-center gap-2 text-xs text-gray-400 line-through opacity-50">
                      <CheckSquare class="w-3 h-3 shrink-0" /> Lakukan penyemprotan biopestisida Metarhizium
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- RIGHT SIDEBAR: Tips + Stats -->
          <div class="flex flex-col gap-4">

            <!-- Tips Foto Terbaik -->
            <div class="rounded-2xl border border-white/8 p-5"
              style="background: rgba(255,255,255,0.03);">
              <h3 class="text-white font-semibold text-sm mb-4">Tips Foto Terbaik</h3>
              <div class="flex flex-col gap-3">
                <div v-for="tip in photoTips" :key="tip.number" class="flex items-start gap-3">
                  <div class="w-6 h-6 rounded-lg bg-amber-900/30 border border-amber-700/30 flex items-center justify-center shrink-0 text-amber-400 text-xs font-bold">
                    {{ tip.number }}
                  </div>
                  <div>
                    <div class="text-white text-xs font-semibold mb-0.5">{{ tip.title }}</div>
                    <div class="text-gray-500 text-xs leading-relaxed">{{ tip.desc }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Statistik Anda -->
            <div class="rounded-2xl border border-white/8 p-5"
              style="background: rgba(255,255,255,0.03);">
              <h3 class="text-white font-semibold text-sm mb-4">Statistik Anda</h3>
              <div class="flex flex-col gap-3">
                <div class="flex justify-between items-center text-sm">
                  <span class="text-gray-500 text-xs">Scan Bulan Ini</span>
                  <span class="text-white font-semibold">42</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-gray-500 text-xs">Rata-rata Akurasi</span>
                  <span class="text-emerald-400 font-semibold">96.8%</span>
                </div>
                <div class="flex justify-between items-center text-sm">
                  <span class="text-gray-500 text-xs">Area Terpindai</span>
                  <span class="text-white font-semibold text-xs">Bitung, Sulut</span>
                </div>
              </div>
              <button class="mt-4 w-full bg-emerald-900/40 hover:bg-emerald-900/60 border border-emerald-700/40 text-emerald-400 font-semibold py-2.5 rounded-xl text-xs transition">
                LIHAT LAPORAN LENGKAP
              </button>
            </div>
          </div>
        </div>

        <!-- RIWAYAT SCAN TABLE -->
        <div class="rounded-2xl border border-white/8 overflow-hidden" data-aos="fade-up" data-aos-delay="300"
          style="background: rgba(255,255,255,0.03);">
          <div class="px-5 py-4 border-b border-white/5 flex items-center justify-between">
            <div>
              <h3 class="text-white font-semibold text-sm">Riwayat Scan</h3>
              <p class="text-gray-600 text-xs mt-0.5 tracking-widest uppercase">Verified on Decentralized Local Network</p>
            </div>
            <button class="flex items-center gap-2 text-xs text-gray-400 hover:text-white border border-white/10 hover:border-white/20 px-3 py-1.5 rounded-lg transition">
              <Download class="w-3 h-3" /> Unduh Ledger
            </button>
          </div>

          <!-- Desktop table -->
          <div class="hidden md:block overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-white/5">
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Waktu Scan</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Identitas Hama</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Tingkat Keparahan</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Akurasi AI</th>
                  <th class="text-left text-gray-600 text-xs uppercase tracking-widest px-5 py-3 font-medium">Status Tindakan</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="scan in scanHistory" :key="scan.id"
                  class="border-b border-white/5 last:border-0 hover:bg-white/2 transition">
                  <td class="px-5 py-4">
                    <div class="text-white text-sm font-medium">{{ scan.date }}</div>
                    <div class="text-gray-500 text-xs">{{ scan.time }}</div>
                  </td>
                  <td class="px-5 py-4">
                    <div class="text-white text-sm font-semibold italic">{{ scan.pestName }}</div>
                    <div class="text-gray-500 text-xs">{{ scan.pestCommon }}</div>
                  </td>
                  <td class="px-5 py-4">
                    <span class="text-xs font-semibold px-2.5 py-1 rounded-full"
                      :class="severityClass(scan.severity)">
                      {{ scan.severity }}
                    </span>
                  </td>
                  <td class="px-5 py-4 text-white text-sm font-medium">{{ scan.accuracy }}%</td>
                  <td class="px-5 py-4">
                    <span class="text-xs font-medium" :class="statusClass(scan.status)">
                      {{ scan.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Mobile cards -->
          <div class="md:hidden flex flex-col divide-y divide-white/5">
            <div v-for="scan in scanHistory" :key="scan.id" class="px-4 py-4">
              <div class="flex items-start justify-between mb-1">
                <div>
                  <div class="text-white text-sm font-semibold italic">{{ scan.pestName }}</div>
                  <div class="text-gray-500 text-xs">{{ scan.date }} • {{ scan.time }}</div>
                </div>
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full shrink-0"
                  :class="severityClass(scan.severity)">
                  {{ scan.severity }}
                </span>
              </div>
              <div class="flex items-center justify-between mt-2">
                <span class="text-xs" :class="statusClass(scan.status)">{{ scan.status }}</span>
                <span class="text-gray-400 text-xs">{{ scan.accuracy }}% akurasi</span>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  ScanLine, TrendingUp, Bug, TriangleAlert, Clock,
  Camera, Upload, CheckSquare, RefreshCw, Download, Cpu
} from 'lucide-vue-next'
import DashboardSidebar from '../../components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '../../components/dashboard/DashboardHeader.vue'
import api from '../../api/axios.js'

const sidebarOpen = ref(false)
const fileInput = ref(null)
const previewImage = ref(null)
const isAnalyzing = ref(false)
const scanResult = ref(null)
const lastScanPreview = ref(true)
const currentFile = ref(null)

const photoTips = [
  { number: '01', title: 'Cahaya Cukup', desc: 'Hindari foto di bawah sinar matahari langsung yang terlalu kontras.' },
  { number: '02', title: 'Fokus Tajam', desc: 'Pastikan tekstur daun atau batang terlihat jelas.' },
  { number: '03', title: 'Jarak Dekat', desc: 'Ambil foto pada jarak 20-50cm untuk deteksi mikroskopis.' },
  { number: '04', title: 'Sudut Tegak', desc: 'Ambil foto tegak lurus terhadap permukaan daun.' },
]

const scanHistory = ref([
  { id: 1, date: '09 Feb 2026', time: '10:42 WIB', pestName: 'Oryctes rhinoceros', pestCommon: 'Kumbang Badak',  severity: 'SEDANG', accuracy: 94, status: 'Dalam Penanganan' },
  { id: 2, date: '08 Feb 2026', time: '08:15 WIB', pestName: 'Rhynchophorus',      pestCommon: 'Kumbang Sagu',  severity: 'AKUT',   accuracy: 98, status: 'Siap Tinggi' },
  { id: 3, date: '07 Feb 2026', time: '14:30 WIB', pestName: 'Sehat',               pestCommon: 'Tidak ada hama', severity: 'SEHAT',  accuracy: 99, status: 'Clear' },
])

// Helper: parse AI result_label menjadi format tampilan
function parseAIResult(resultLabel, confidenceScore) {
  const label = (resultLabel || '').toLowerCase()
  const confidence = Math.round((confidenceScore || 0.85) * 100)

  // Deteksi apakah sehat
  const isHealthy = label.includes('sehat') || label.includes('healthy')
  const severity = isHealthy ? 'SEHAT' : (confidence > 95 ? 'AKUT' : 'SEDANG')

  // Coba ekstrak nama latin dari label
  let latinName = isHealthy ? 'Tanaman Sehat' : 'Hama Terdeteksi'
  let commonName = isHealthy ? 'Tidak ada hama terdeteksi' : resultLabel

  // Pattern matching untuk nama hama umum
  const pestPatterns = [
    { pattern: /oryctes/i, latin: 'Oryctes rhinoceros', common: 'Kumbang Badak Kelapa' },
    { pattern: /brontispa/i, latin: 'Brontispa longissima', common: 'Kumbang Kopra' },
    { pattern: /rhynchophorus/i, latin: 'Rhynchophorus ferrugineus', common: 'Kumbang Sagu' },
    { pattern: /pseudococcus|kutu putih/i, latin: 'Pseudococcus sp.', common: 'Kutu Putih Kelapa' },
  ]
  for (const p of pestPatterns) {
    if (p.pattern.test(resultLabel)) {
      latinName = p.latin
      commonName = p.common
      break
    }
  }

  const actions = isHealthy
    ? ['Lanjutkan perawatan rutin', 'Pantau kondisi daun setiap minggu', 'Pastikan drainase tanah optimal']
    : ['Konsultasikan dengan penyuluh pertanian setempat', 'Lakukan tindakan pengendalian sesuai jenis hama', 'Lakukan monitoring berkala untuk mengevaluasi efektivitas']

  return { latinName, commonName, severity, confidence, actions }
}

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(e) {
  const file = e.target.files[0]
  if (file) processImage(file)
}

function handleDrop(e) {
  const file = e.dataTransfer.files[0]
  if (file && file.type.startsWith('image/')) processImage(file)
}

function processImage(file) {
  currentFile.value = file
  const reader = new FileReader()
  reader.onload = (ev) => {
    previewImage.value = ev.target.result
    lastScanPreview.value = false
    startAnalysis()
  }
  reader.readAsDataURL(file)
}

async function startAnalysis() {
  isAnalyzing.value = true
  scanResult.value = null
  try {
    const payload = {
      image_data: previewImage.value,
      filename: currentFile.value?.name || 'photo.jpg',
      timestamp: new Date().toISOString(),
    }
    const res = await api.post('/pest/scan', payload)
    const data = res.data
    const parsed = parseAIResult(data.result_label, data.confidence_score)
    scanResult.value = { ...parsed }

    // Tambah ke history
    scanHistory.value.unshift({
      id: data.id || Date.now(),
      date: new Date().toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' }),
      time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }) + ' WIB',
      pestName: parsed.latinName,
      pestCommon: parsed.commonName,
      severity: parsed.severity,
      accuracy: parsed.confidence,
      status: parsed.severity === 'SEHAT' ? 'Clear' : 'Dalam Penanganan',
    })
  } catch (err) {
    console.error('Scan error:', err)
    // Fallback: tampilkan pesan error
    scanResult.value = {
      latinName: 'Error',
      commonName: 'Gagal menghubungi server analisis',
      severity: 'SEDANG',
      confidence: 0,
      actions: ['Periksa koneksi internet', 'Pastikan backend server berjalan', 'Coba lagi beberapa saat'],
    }
  } finally {
    isAnalyzing.value = false
  }
}

function resetScan() {
  previewImage.value = null
  scanResult.value = null
  isAnalyzing.value = false
  lastScanPreview.value = true
}

function severityClass(severity) {
  if (severity === 'SEDANG') return 'bg-amber-900/50 text-amber-400 border border-amber-700/50'
  if (severity === 'AKUT')   return 'bg-red-900/50 text-red-400 border border-red-700/50'
  if (severity === 'SEHAT')  return 'bg-emerald-900/50 text-emerald-400 border border-emerald-700/50'
  return 'bg-white/10 text-gray-400'
}

function statusClass(status) {
  if (status === 'Clear')            return 'text-emerald-400'
  if (status === 'Siap Tinggi')      return 'text-red-400'
  if (status === 'Dalam Penanganan') return 'text-amber-400'
  return 'text-gray-400'
}
</script>