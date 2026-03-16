<template>
  <div class="rounded-2xl border border-white/8 p-5 hover:border-white/15 transition cursor-pointer group"
    style="background: rgba(255,255,255,0.04);">
    <div class="flex items-start justify-between mb-4">
      <div class="w-10 h-10 rounded-xl flex items-center justify-center"
        :style="`background: ${iconBg}`">
        <component :is="icon" class="w-5 h-5" :style="`color: ${iconColor}`" />
      </div>
    </div>
    <h3 class="text-white font-bold text-lg mb-1">{{ title }}</h3>
    <p class="text-gray-500 text-xs mb-3">{{ desc }}</p>
    <span class="text-xs font-semibold transition"
      :style="`color: ${iconColor}`">
      {{ linkText }} →
    </span>
  </div>
</template>

<script setup>
defineProps({
  icon: Object,
  iconBg: { type: String, default: 'rgba(16,185,129,0.15)' },
  iconColor: { type: String, default: '#10b981' },
  title: String,
  desc: String,
  linkText: { type: String, default: 'Buka' },
})
</script>