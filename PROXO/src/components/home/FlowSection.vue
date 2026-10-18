<template>
  <!-- SECTION ALUR KERJA -->
  <section id="alur" class="py-24 px-6">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-white mb-2">
          {{ $t('flow.title') }}
          <span class="text-amber-400">{{ $t('flow.titleHighlight') }}</span>
        </h2>
        <div class="w-12 h-0.5 bg-amber-400 mx-auto mt-3"></div>
      </div>
      <div class="flex flex-col md:flex-row items-start">
        <div
          data-aos="zoom-in"
          data-aos-delay="0"
          class="flex-1 flex flex-col items-center text-center px-4"
        >
          <div
            class="w-16 h-16 rounded-full border-2 border-amber-500/60 flex items-center justify-center mb-4"
            style="background: rgba(180, 100, 0, 0.15)"
          >
            <span class="text-amber-400 font-bold text-xl">1</span>
          </div>
          <h4 class="text-white font-semibold mb-2">{{ $t('flow.step1') }}</h4>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t('flow.step1Desc') }}
          </p>
        </div>
        <div class="hidden md:flex items-start pt-8 shrink-0">
          <div class="w-16 h-px bg-amber-800/50"></div>
        </div>
        <div
          data-aos="zoom-in"
          data-aos-delay="100"
          class="flex-1 flex flex-col items-center text-center px-4 mt-8 md:mt-0"
        >
          <div
            class="w-16 h-16 rounded-full border-2 border-amber-500/60 flex items-center justify-center mb-4"
            style="background: rgba(180, 100, 0, 0.15)"
          >
            <span class="text-amber-400 font-bold text-xl">2</span>
          </div>
          <h4 class="text-white font-semibold mb-2">{{ $t('flow.step2') }}</h4>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t('flow.step2Desc') }}
          </p>
        </div>
        <div class="hidden md:flex items-start pt-8 shrink-0">
          <div class="w-16 h-px bg-amber-800/50"></div>
        </div>
        <div
          data-aos="zoom-in"
          data-aos-delay="200"
          class="flex-1 flex flex-col items-center text-center px-4 mt-8 md:mt-0"
        >
          <div
            class="w-16 h-16 rounded-full border-2 border-amber-500/60 flex items-center justify-center mb-4"
            style="background: rgba(180, 100, 0, 0.15)"
          >
            <span class="text-amber-400 font-bold text-xl">3</span>
          </div>
          <h4 class="text-white font-semibold mb-2">{{ $t('flow.step3') }}</h4>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t('flow.step3Desc') }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// Seksi statis — seluruh teks berasal dari i18n
</script>
