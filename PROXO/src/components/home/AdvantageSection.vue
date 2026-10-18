<template>
  <!-- SECTION KEUNGGULAN -->
  <section id="keunggulan" class="py-24 px-6">
    <div class="max-w-4xl mx-auto flex flex-col gap-24">
      <!-- Keunggulan 1: Pest Scanner -->
      <div data-aos="fade-up" class="flex flex-col md:flex-row items-center gap-12">
        <div class="md:w-1/2">
          <div class="text-emerald-400 text-xs font-semibold tracking-widest uppercase mb-3">
            {{ $t('advantage.scannerBadge') }}
          </div>
          <h3 class="text-white text-3xl font-bold mb-4">
            {{ $t('advantage.scannerTitle') }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed mb-6">
            {{ $t('advantage.scannerDesc') }}
          </p>
          <div class="flex flex-col gap-2">
            <div class="flex items-center gap-2 text-sm text-gray-300">
              <CheckCircle class="w-4 h-4 text-emerald-400 shrink-0" />
              {{ $t('advantage.check1') }}
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-300">
              <CheckCircle class="w-4 h-4 text-emerald-400 shrink-0" />
              {{ $t('advantage.check2') }}
            </div>
          </div>
        </div>
        <div class="md:w-1/2 flex justify-center">
          <div
            class="w-56 rounded-3xl border border-white/10 overflow-hidden"
            style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px)"
          >
            <div class="bg-white/10 h-6 flex items-center justify-center">
              <div class="w-16 h-1.5 bg-white/20 rounded-full"></div>
            </div>
            <div class="p-4 flex flex-col gap-3">
              <div
                class="w-full h-32 rounded-xl bg-emerald-900/50 flex items-center justify-center"
              >
                <ScanLine class="w-12 h-12 text-emerald-400 opacity-50" />
              </div>
              <div class="bg-white/5 rounded-lg p-3">
                <div class="text-xs text-gray-400 mb-1">
                  {{ $t('scanner.detected') }}
                </div>
                <div class="text-white text-sm font-semibold italic">Oryctes rhinoceros</div>
                <div class="w-full bg-gray-800 rounded-full h-1 mt-2">
                  <div class="bg-emerald-400 h-1 rounded-full" style="width: 98%"></div>
                </div>
              </div>

              <div class="bg-white/5 rounded-lg p-3 text-xs text-gray-400">
                {{ $t('chat.recommendation') }}
                <span class="text-emerald-400">Sycanus</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Keunggulan 2: Adil-Harga Ledger -->
      <div data-aos="fade-up" class="flex flex-col md:flex-row-reverse items-center gap-12">
        <div class="md:w-1/2">
          <div class="text-amber-400 text-xs font-semibold tracking-widest uppercase mb-3">
            {{ $t('advantage.ledgerBadge') }}
          </div>
          <h3 class="text-white text-3xl font-bold mb-4">
            {{ $t('advantage.ledgerTitle') }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed mb-6">
            {{ $t('advantage.ledgerDesc') }}
          </p>
          <button
            class="border border-amber-500/50 text-amber-400 hover:bg-amber-500/10 px-5 py-2 rounded-full text-sm transition"
          >
            {{ $t('advantage.ledgerBtn') }}
          </button>
        </div>
        <div class="md:w-1/2 flex justify-center">
          <div
            class="w-full max-w-xs rounded-2xl border border-white/10 p-4"
            style="background: rgba(255, 255, 255, 0.04)"
          >
            <div class="text-xs text-gray-500 mb-3">{{ $t('chart.title') }}</div>
            <div class="flex items-end gap-2 h-24 mb-2">
              <div class="flex-1 bg-amber-700/60 rounded-t-sm" style="height: 55%"></div>
              <div class="flex-1 bg-amber-600/70 rounded-t-sm" style="height: 70%"></div>
              <div class="flex-1 bg-amber-500/80 rounded-t-sm" style="height: 60%"></div>
              <div class="flex-1 bg-amber-400 rounded-t-sm" style="height: 90%"></div>
              <div class="flex-1 bg-amber-500/80 rounded-t-sm" style="height: 75%"></div>
              <div class="flex-1 bg-amber-600/70 rounded-t-sm" style="height: 65%"></div>
              <div class="flex-1 bg-amber-400 rounded-t-sm" style="height: 85%"></div>
            </div>

            <div class="flex justify-between text-xs text-gray-600">
              <span v-for="day in $t('chart.days').split('|')" :key="day">{{ day }}</span>
            </div>

            <div class="mt-3 flex justify-between items-center">
              <span class="text-xs text-gray-400">Rp14.200/kg</span>
              <span class="text-xs text-emerald-400 font-semibold">+4.2%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Keunggulan 3: RAG Agri-Assistant -->
      <div data-aos="fade-up" class="flex flex-col md:flex-row items-center gap-12">
        <div class="md:w-1/2">
          <div class="text-blue-400 text-xs font-semibold tracking-widest uppercase mb-3">
            {{ $t('advantage.ragBadge') }}
          </div>
          <h3 class="text-white text-3xl font-bold mb-4">
            {{ $t('advantage.ragTitle') }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed mb-6">
            {{ $t('advantage.ragDesc') }}
          </p>

          <div
            class="rounded-xl border border-white/10 px-4 py-3 text-sm text-gray-400 italic"
            style="background: rgba(255, 255, 255, 0.04)"
          >
            {{ $t('chat.quote') }}
          </div>
        </div>
        <div class="md:w-1/2 flex justify-center">
          <div
            class="w-full max-w-xs rounded-2xl border border-white/10 p-4 flex flex-col gap-3"
            style="background: rgba(255, 255, 255, 0.04)"
          >
            <div
              class="bg-blue-900/30 border border-blue-800/30 rounded-xl rounded-tl-sm px-3 py-2 text-xs text-gray-300 self-start max-w-[85%]"
            >
              {{ $t('chat.userMsg') }}
            </div>
            <div
              class="bg-white/5 rounded-xl rounded-tr-sm px-3 py-2 text-xs text-gray-300 self-end max-w-[85%]"
            >
              {{ $t('chat.aiMsg') }}
              <span class="text-emerald-400">Tetrastichus brontispae</span>
              {{ $t('chat.aiMsgEnd') }}
            </div>
            <div
              class="mt-2 bg-white/5 border border-white/10 rounded-full px-3 py-2 flex items-center gap-2"
            >
              <span class="flex-1 text-xs text-gray-600">{{ $t('chat.placeholder') }}</span>
              <div class="w-5 h-5 rounded-full bg-emerald-600 flex items-center justify-center">
                <ArrowRight class="w-3 h-3 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ScanLine, CheckCircle, ArrowRight } from 'lucide-vue-next'
</script>
