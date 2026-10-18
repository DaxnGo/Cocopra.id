<template>
  <!-- SECTION FITUR -->
  <section data-aos="fade-up" class="max-w-4xl mx-auto px-6 pb-24">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <div
        class="rounded-2xl border border-white/10 p-6 hover:border-emerald-700/50 transition group"
        style="background: rgba(255, 255, 255, 0.04)"
      >
        <div
          class="w-12 h-12 rounded-2xl bg-emerald-900/50 flex items-center justify-center mb-5 group-hover:bg-emerald-800/50 transition"
        >
          <ScanLine class="w-6 h-6 text-emerald-400" />
        </div>
        <h3 class="text-white font-semibold text-lg mb-2">
          {{ $t('features.scanner') }}
        </h3>
        <p class="text-gray-400 text-sm leading-relaxed">
          {{ $t('features.scannerDesc') }}
        </p>
      </div>
      <div
        class="rounded-2xl border border-white/10 p-6 hover:border-emerald-700/50 transition group"
        style="background: rgba(255, 255, 255, 0.04)"
      >
        <div
          class="w-12 h-12 rounded-2xl bg-emerald-900/50 flex items-center justify-center mb-5 group-hover:bg-emerald-800/50 transition"
        >
          <TrendingUp class="w-6 h-6 text-emerald-400" />
        </div>
        <h3 class="text-white font-semibold text-lg mb-2">
          {{ $t('features.price') }}
        </h3>
        <p class="text-gray-400 text-sm leading-relaxed">
          {{ $t('features.priceDesc') }}
        </p>
      </div>
      <div
        class="rounded-2xl border border-white/10 p-6 hover:border-emerald-700/50 transition group"
        style="background: rgba(255, 255, 255, 0.04)"
      >
        <div
          class="w-12 h-12 rounded-2xl bg-emerald-900/50 flex items-center justify-center mb-5 group-hover:bg-emerald-800/50 transition"
        >
          <MapPin class="w-6 h-6 text-emerald-400" />
        </div>
        <h3 class="text-white font-semibold text-lg mb-2">
          {{ $t('features.warning') }}
        </h3>
        <p class="text-gray-400 text-sm leading-relaxed">
          {{ $t('features.warningDesc') }}
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ScanLine, TrendingUp, MapPin } from 'lucide-vue-next'
</script>
