<template>
  <!-- SCANNER MOCKUP -->
  <section data-aos="fade-up" class="max-w-4xl mx-auto px-6 pb-20">
    <div
      class="rounded-2xl border border-white/10 overflow-hidden"
      style="background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(10px)"
    >
      <div class="flex items-center justify-between px-5 py-3 border-b border-white/10">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-red-500"></span>
          <span class="w-3 h-3 rounded-full bg-amber-400"></span>
          <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
          <span class="text-gray-400 text-sm ml-3">{{ $t('scanner.title') }}</span>
        </div>
        <div class="flex gap-2">
          <span class="text-xs text-gray-500 border border-gray-700 px-2 py-1 rounded">{{
            $t('scanner.liveFeed')
          }}</span>
          <span
            class="text-xs text-emerald-400 border border-emerald-700 bg-emerald-900/30 px-2 py-1 rounded"
            >{{ $t('scanner.aiActive') }}</span
          >
        </div>
      </div>

      <div class="flex flex-col md:flex-row">
        <div class="md:w-3/5 relative" style="min-height: 300px">
          <div
            class="absolute inset-0"
            :style="
              leafImageLoaded
                ? 'background:none'
                : 'background: linear-gradient(135deg, #0a2e18 0%, #1a5c35 100%)'
            "
          >
            <img
              v-if="!leafImageError"
              src="/michael-oxendine-aKvfQV4WpiA-unsplash.jpg"
              alt="Daun Kelapa"
              class="w-full h-full object-cover"
              @error="leafImageError = true"
              @load="leafImageLoaded = true"
            />
            <div
              v-if="leafImageError"
              class="w-full h-full flex flex-col items-center justify-center gap-2 opacity-40"
            >
              <Leaf class="w-16 h-16 text-emerald-400" />
            </div>
          </div>
          <div class="absolute inset-0 p-4 flex flex-col">
            <div class="bg-black/60 rounded-lg px-3 py-2 self-start backdrop-blur-sm">
              <div class="text-gray-400 text-xs tracking-wider">
                {{ $t('scanner.detected') }}
              </div>
              <div class="text-white text-sm font-semibold italic">Oryctes rhinoceros</div>
            </div>
            <div class="flex-1 flex items-center justify-center">
              <div
                class="border-2 border-emerald-400 rounded-sm opacity-80"
                style="width: 45%; height: 55%"
              ></div>
            </div>
          </div>
        </div>

        <div
          class="md:w-2/5 p-5 flex flex-col gap-4 border-t md:border-t-0 md:border-l border-white/10"
        >
          <div class="bg-white/5 rounded-xl p-4">
            <h3 class="text-white font-semibold text-sm mb-3 flex items-center gap-2">
              <BarChart2 class="w-4 h-4 text-emerald-400" />
              {{ $t('scanner.confidence') }}
            </h3>
            <div class="mb-3">
              <div class="flex justify-between text-xs text-gray-300 mb-1">
                <span>{{ $t('scanner.pest') }}</span>
                <span class="text-emerald-400 font-bold">98.2%</span>
              </div>
              <div class="w-full bg-gray-800 rounded-full h-1.5">
                <div class="bg-emerald-400 h-1.5 rounded-full" style="width: 98.2%"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-xs text-gray-300 mb-1">
                <span>{{ $t('scanner.nutrisi') }}</span>
                <span class="text-gray-400">1.8%</span>
              </div>
              <div class="w-full bg-gray-800 rounded-full h-1.5">
                <div class="bg-gray-600 h-1.5 rounded-full" style="width: 1.8%"></div>
              </div>
            </div>
          </div>

          <div class="border border-red-900/50 bg-red-950/30 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-amber-400 text-sm font-semibold">{{ $t('scanner.warning') }}</span>
              <TriangleAlert class="w-4 h-4 text-amber-400" />
            </div>
            <p class="text-gray-400 text-xs leading-relaxed">
              {{ $t('scanner.warningDesc') }}
            </p>
            <a
              href="#"
              class="text-amber-400 text-xs font-semibold mt-2 inline-flex items-center gap-1 hover:text-amber-300 transition"
            >
              {{ $t('scanner.openMap') }} <ArrowRight class="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 border-t border-white/10">
        <div class="p-4 border-r border-white/10">
          <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
            {{ $t('scanner.totalScan') }}
          </div>
          <div class="text-white font-bold text-xl">128,402</div>
        </div>
        <div class="p-4 md:border-r border-white/10">
          <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
            {{ $t('scanner.accuracy') }}
          </div>
          <div class="text-emerald-400 font-bold text-xl">99.1%</div>
        </div>
        <div class="p-4 border-r border-t md:border-t-0 border-white/10">
          <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
            {{ $t('scanner.activeMap') }}
          </div>
          <div class="text-white font-bold text-xl">24 Prov</div>
        </div>
        <div class="p-4 border-t md:border-t-0 border-white/10">
          <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
            {{ $t('scanner.copricePrice') }}
          </div>
          <div class="text-amber-400 font-bold text-xl">Rp14.200</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { BarChart2, TriangleAlert, ArrowRight, Leaf } from 'lucide-vue-next'

const leafImageError = ref(false)
const leafImageLoaded = ref(false)
</script>
