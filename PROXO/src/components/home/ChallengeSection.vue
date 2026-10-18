<template>
  <!-- SECTION TANTANGAN -->
  <section
    id="tantangan"
    class="py-24 px-6"
    style="background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.3) 100%)"
  >
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
          {{ $t('challenge.title') }}
          <span class="text-amber-400">{{ $t('challenge.titleHighlight') }}</span>
        </h2>
        <p class="text-gray-400 text-base max-w-xl mx-auto">
          {{ $t('challenge.desc') }}
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div
          data-aos="fade-up"
          data-aos-delay="0"
          class="rounded-2xl border border-white/10 p-6 hover:border-red-800/50 transition group"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <div
            class="w-12 h-12 rounded-2xl bg-red-900/40 flex items-center justify-center mb-5 group-hover:bg-red-800/50 transition"
          >
            <Bug class="w-6 h-6 text-red-400" />
          </div>
          <h3 class="text-white font-semibold text-lg mb-2">
            {{ $t('challenge.pest') }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t('challenge.pestDesc') }}
          </p>
        </div>
        <div
          data-aos="fade-up"
          data-aos-delay="100"
          class="rounded-2xl border border-white/10 p-6 hover:border-amber-800/50 transition group"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <div
            class="w-12 h-12 rounded-2xl bg-amber-900/40 flex items-center justify-center mb-5 group-hover:bg-amber-800/50 transition"
          >
            <Banknote class="w-6 h-6 text-amber-400" />
          </div>
          <h3 class="text-white font-semibold text-lg mb-2">
            {{ $t('challenge.price') }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t('challenge.priceDesc') }}
          </p>
        </div>
        <div
          data-aos="fade-up"
          data-aos-delay="200"
          class="rounded-2xl border border-white/10 p-6 hover:border-blue-800/50 transition group"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <div
            class="w-12 h-12 rounded-2xl bg-blue-900/40 flex items-center justify-center mb-5 group-hover:bg-blue-800/50 transition"
          >
            <FileText class="w-6 h-6 text-blue-400" />
          </div>
          <h3 class="text-white font-semibold text-lg mb-2">
            {{ $t('challenge.regulation') }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t('challenge.regulationDesc') }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Bug, Banknote, FileText } from 'lucide-vue-next'
</script>
