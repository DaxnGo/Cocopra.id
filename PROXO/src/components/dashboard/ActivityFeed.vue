<template>
  <div class="rounded-2xl border border-white/8 p-5" style="background: rgba(255,255,255,0.04);">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-white font-semibold text-sm">Aktivitas Terbaru</h3>
      <button class="text-xs text-emerald-400 hover:text-emerald-300 font-medium tracking-wider transition">
        LIHAT SEMUA
      </button>
    </div>
    <div class="flex flex-col gap-3">
      <div v-for="(item, i) in activities" :key="i"
        class="flex items-start gap-3 py-3 border-b border-white/5 last:border-0">
        <div class="w-9 h-9 rounded-full flex items-center justify-center shrink-0"
          :style="`background: ${item.iconBg}`">
          <component :is="item.icon" class="w-4 h-4" :style="`color: ${item.iconColor}`" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-white text-sm font-medium truncate">{{ item.title }}</p>
          <p class="text-gray-500 text-xs mt-0.5">{{ item.subtitle }}</p>
        </div>
        <span class="text-gray-600 text-xs shrink-0">{{ item.time }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ScanLine, ShieldCheck, TrendingUp, Bot } from 'lucide-vue-next'

const activities = [
  {
    icon: ScanLine,
    iconBg: 'rgba(16,185,129,0.15)',
    iconColor: '#10b981',
    title: 'Scan Hama Berhasil',
    subtitle: 'Kamera AI • Tingkat Sedang',
    time: 'HARI INI'
  },
  {
    icon: ShieldCheck,
    iconBg: 'rgba(16,185,129,0.15)',
    iconColor: '#10b981',
    title: 'Regulatory Check',
    subtitle: 'Regulatory DB • Status: Aman',
    time: 'KEMARIN'
  },
  {
    icon: TrendingUp,
    iconBg: 'rgba(245,158,11,0.15)',
    iconColor: '#f59e0b',
    title: 'Cek Harga Kopra',
    subtitle: 'Adil-Harga Ledger • Terverifikasi',
    time: '12 MAR'
  },
  {
    icon: Bot,
    iconBg: 'rgba(59,130,246,0.15)',
    iconColor: '#3b82f6',
    title: 'Tanya Asisten AI',
    subtitle: '"Cara basmi P. wayi organik"',
    time: '10 MAR'
  },
]
</script>