<template>
  <div class="rounded-2xl border border-white/8 p-5" style="background: rgba(255,255,255,0.04);">
    <!-- Harga Kopra -->
    <div class="mb-5">
      <p class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-2">Harga Kopra Hari Ini</p>
      <div class="flex items-baseline gap-2">
        <span class="text-white font-bold text-2xl">Rp 4.033</span>
        <span class="text-emerald-400 text-sm font-semibold">+2.1%</span>
      </div>
      <p class="text-gray-600 text-xs mt-1">Terakhir diperbarui: 08:00 WIB</p>
      <!-- Mini chart -->
      <div class="mt-3 h-16">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </div>

    <!-- Status Kebun -->
    <div class="border-t border-white/5 pt-4">
      <p class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-3">Status Kebun</p>
      <div class="flex items-center justify-center mb-4">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse"></span>
          <span class="text-amber-400 font-bold text-lg tracking-wider">WASPADA</span>
        </div>
      </div>
      <div class="flex flex-col gap-2 text-xs mb-4">
        <div class="flex justify-between">
          <span class="text-gray-500">Total Scan</span>
          <span class="text-white font-medium">24</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">Hama Terdeteksi</span>
          <span class="text-red-400 font-medium">8</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-500">Scan Terakhir</span>
          <span class="text-white font-medium">Hari ini, 09:12</span>
        </div>
      </div>
      <button class="w-full flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold py-2.5 rounded-xl text-sm transition">
        <ScanLine class="w-4 h-4" /> Scan Sekarang →
      </button>
    </div>
  </div>
</template>

<script setup>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Filler } from 'chart.js'
import { ScanLine } from 'lucide-vue-next'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Filler)

const chartData = {
  labels: ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'],
  datasets: [{
    data: [3800, 3900, 3750, 3950, 4000, 3980, 4033],
    borderColor: '#10b981',
    backgroundColor: 'rgba(16,185,129,0.1)',
    borderWidth: 2,
    fill: true,
    tension: 0.4,
    pointRadius: 0,
  }]
}

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { display: false },
    y: { display: false }
  }
}
</script>