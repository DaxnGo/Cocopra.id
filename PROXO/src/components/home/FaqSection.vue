<template>
  <!-- SECTION FAQ -->
  <section data-aos="fade-up" id="faq" class="py-24 px-6">
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-white mb-3">
          {{ $t('faq.title') }}
          <span class="text-amber-400">{{ $t('faq.titleHighlight') }}</span>
        </h2>
        <p class="text-gray-400 text-sm">{{ $t('faq.desc') }}</p>
      </div>
      <div class="flex flex-col gap-3">
        <div
          v-for="(item, index) in faqs"
          :key="index"
          class="rounded-xl border border-white/10 overflow-hidden"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <button
            class="w-full flex items-center justify-between px-5 py-4 text-left"
            @click="activeFaq = activeFaq === index ? null : index"
          >
            <span class="text-amber-400 text-sm font-medium">{{ item.q }}</span>
            <ChevronDown
              class="w-4 h-4 text-gray-400 transition-transform shrink-0 ml-4"
              :class="{ 'rotate-180': activeFaq === index }"
            />
          </button>
          <div
            v-if="activeFaq === index"
            class="px-5 pb-4 text-gray-400 text-sm leading-relaxed border-t border-white/5 pt-3"
          >
            {{ item.a }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ChevronDown } from 'lucide-vue-next'

const { t } = useI18n()
const activeFaq = ref(null)

// FAQ otomatis ikut bahasa
const faqs = computed(() => [
  { q: t('faq.q1'), a: t('faq.a1') },
  { q: t('faq.q2'), a: t('faq.a2') },
  { q: t('faq.q3'), a: t('faq.a3') },
  { q: t('faq.q4'), a: t('faq.a4') },
])
</script>
