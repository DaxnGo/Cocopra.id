<template>
  <!-- HERO SECTION -->
  <section data-aos="fade-up" class="text-center px-6 pt-16 pb-10 max-w-4xl mx-auto">
    <div
      class="inline-flex items-center gap-2 text-emerald-400 text-xs font-medium tracking-widest uppercase mb-6 border border-emerald-800/50 rounded-full px-3 py-1"
      style="background: rgba(16, 185, 129, 0.08)"
    >
      <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
      {{ $t('hero.badge') }}
    </div>

    <h1 class="text-5xl md:text-6xl font-bold leading-tight mb-6">
      <span
        style="
          color: transparent;
          background: linear-gradient(180deg, #ffffff 0%, #a0c4a8 100%);
          -webkit-background-clip: text;
          background-clip: text;
        "
      >
        {{ $t('hero.title1') }} <br />{{ $t('hero.title2') }}
      </span>
      <span class="text-emerald-400"> {{ $t('hero.title3') }}</span>
    </h1>

    <p class="text-gray-400 text-lg max-w-2xl mx-auto mb-10">
      {{ $t('hero.desc') }}
    </p>

    <div class="flex items-center justify-center gap-4 flex-wrap">
      <button
        class="flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-6 py-3 rounded-full transition"
      >
        <ScanLine class="w-5 h-5" /> {{ $t('hero.btnScan') }}
      </button>
      <button
        @click="emit('open-demo')"
        class="flex items-center gap-2 border border-gray-600 hover:border-white text-white px-6 py-3 rounded-full transition"
      >
        <PlayCircle class="w-5 h-5" /> {{ $t('hero.btnDemo') }}
      </button>
    </div>
  </section>
</template>

<script setup>
import { ScanLine, PlayCircle } from 'lucide-vue-next'

const emit = defineEmits(['open-demo'])
</script>
