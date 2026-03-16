<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="isOpen"
        class="fixed inset-0 z-[9999] flex items-center justify-center p-4 md:p-8"
        style="background: rgba(0,0,0,0.85); backdrop-filter: blur(6px);"
        @click.self="close">

        <div class="relative w-full max-w-4xl" data-aos="zoom-in">
          <!-- Close button -->
          <button @click="close"
            class="absolute -top-10 right-0 flex items-center gap-2 text-gray-400 hover:text-white transition text-sm">
            <span>{{ $t('video.close') }}</span>
            <X class="w-4 h-4" />
          </button>

          <!-- Video container dengan aspect ratio 16:9 -->
          <div class="relative rounded-2xl overflow-hidden border border-white/10"
            style="padding-bottom: 56.25%;">
            <iframe
              v-if="isOpen"
              class="absolute inset-0 w-full h-full"
              :src="`https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1`"
              title="Cocopra.id Demo"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen>
            </iframe>
          </div>

          <!-- Caption -->
          <div class="mt-3 text-center">
            <p class="text-gray-400 text-sm">
              🌴 <span class="text-white font-medium">Cocopra.id</span> —
              {{ $t('video.caption') }}
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { X } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  isOpen: Boolean,
  videoId: { type: String, default: 'NpEaa2P7qZI' }
})

const emit = defineEmits(['close'])

function close() {
  emit('close')
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>