<template>
  <nav class="sticky top-0 z-50 w-full px-4 md:px-6 py-3">
    <div
      class="flex items-center justify-between px-4 md:px-6 py-3 rounded-2xl border border-white/10 max-w-6xl mx-auto"
      style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px)"
    >
      <!-- LOGO -->
      <div class="flex items-center gap-2 shrink-0">
        <img
          src="/Logo-Cocopra.id.png"
          alt="Cocopra Logo"
          class="w-10 h-10 md:w-12 md:h-12 object-contain"
        />
        <span class="text-white font-bold text-lg md:text-xl"
          >Cocopra<span class="text-amber-400">.id</span></span
        >
      </div>

      <!-- MENU DESKTOP -->
      <div
        class="hidden md:flex items-center gap-6 lg:gap-8 text-sm text-gray-300"
      >
        <RouterLink to="/" class="hover:text-white transition">{{
          $t("nav.home")
        }}</RouterLink>
        <a
          href="#tantangan"
          @click.prevent="scrollTo('#tantangan')"
          class="hover:text-white transition cursor-pointer"
          >{{ $t("nav.challenge") }}</a
        >
        <a
          href="#keunggulan"
          @click.prevent="scrollTo('#keunggulan')"
          class="hover:text-white transition cursor-pointer"
          >{{ $t("nav.advantage") }}</a
        >
        <a
          href="#alur"
          @click.prevent="scrollTo('#alur')"
          class="hover:text-white transition cursor-pointer"
          >{{ $t("nav.flow") }}</a
        >
        <a
          href="#faq"
          @click.prevent="scrollTo('#faq')"
          class="hover:text-white transition cursor-pointer"
          >{{ $t("nav.faq") }}</a
        >
      </div>

      <!-- KANAN DESKTOP -->
      <div class="hidden md:flex items-center gap-3 shrink-0">
        <button
          @click="switchLang('en')"
          :class="
            locale === 'en'
              ? 'text-white font-semibold'
              : 'text-gray-400 hover:text-white'
          "
          class="text-sm transition cursor-pointer"
        >
          EN
        </button>
        <span class="text-gray-600">|</span>
        <button
          @click="switchLang('id')"
          :class="
            locale === 'id'
              ? 'text-white font-semibold'
              : 'text-gray-400 hover:text-white'
          "
          class="text-sm transition cursor-pointer"
        >
          ID
        </button>
        <button @click="showAuth = true"
          class="bg-amber-500 hover:bg-amber-400 text-black font-semibold px-4 py-2 rounded-full text-sm transition whitespace-nowrap"
        >
          {{ $t("nav.start") }}
        </button>
      </div>

      <!-- HAMBURGER -->
      <button
        class="md:hidden text-white p-2 shrink-0"
        @click="menuOpen = !menuOpen"
      >
        <Menu v-if="!menuOpen" class="w-6 h-6" />
        <X v-else class="w-6 h-6" />
      </button>
    </div>

    <!-- MOBILE MENU -->
    <div
      v-if="menuOpen"
      class="md:hidden mt-2 rounded-2xl border border-white/10 px-6 py-4 flex flex-col gap-4 max-w-6xl mx-auto"
      style="background: rgba(10, 30, 15, 0.95); backdrop-filter: blur(12px)"
    >
      <RouterLink
        to="/"
        class="text-gray-300 hover:text-white text-sm transition"
        @click="menuOpen = false"
        >{{ $t("nav.home") }}</RouterLink
      >
      <a
        @click="
          scrollTo('#tantangan');
          menuOpen = false;
        "
        class="text-gray-300 hover:text-white text-sm transition cursor-pointer"
        >{{ $t("nav.challenge") }}</a
      >
      <a
        @click="
          scrollTo('#keunggulan');
          menuOpen = false;
        "
        class="text-gray-300 hover:text-white text-sm transition cursor-pointer"
        >{{ $t("nav.advantage") }}</a
      >
      <a
        @click="
          scrollTo('#alur');
          menuOpen = false;
        "
        class="text-gray-300 hover:text-white text-sm transition cursor-pointer"
        >{{ $t("nav.flow") }}</a
      >
      <a
        @click="
          scrollTo('#faq');
          menuOpen = false;
        "
        class="text-gray-300 hover:text-white text-sm transition cursor-pointer"
        >{{ $t("nav.faq") }}</a
      >
      <div class="flex items-center gap-3 pt-2 border-t border-white/10">
        <button
          @click="switchLang('en')"
          :class="
            locale === 'en' ? 'text-white font-semibold' : 'text-gray-400'
          "
          class="text-sm transition"
        >
          EN
        </button>
        <span class="text-gray-600">|</span>
        <button
          @click="switchLang('id')"
          :class="
            locale === 'id' ? 'text-white font-semibold' : 'text-gray-400'
          "
          class="text-sm transition"
        >
          ID
        </button>
        <button @click="showAuth = true; menuOpen = false"
          class="ml-auto bg-amber-500 text-black font-semibold px-4 py-2 rounded-full text-sm"
        >
          {{ $t("nav.start") }}
        </button>
      </div>
    </div>
  </nav>
  <!-- Auth Modal -->
  <AuthModal :is-open="showAuth" @close="showAuth = false" />
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { Menu, X } from 'lucide-vue-next'
import AuthModal from './AuthModal.vue'

const { locale } = useI18n()
const menuOpen = ref(false)
const showAuth = ref(false)

function switchLang(lang) {
  locale.value = lang
}

function scrollTo(selector) {
  const el = document.querySelector(selector)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}
</script>
