<template>
  <div
    class="min-h-screen flex flex-col"
    style="
      background: radial-gradient(
        ellipse at top,
        #1a4a2e 0%,
        #0d2818 40%,
        #061510 100%
      );
    "
  >
    <AppNavbar />

    <div
      class="flex-1 flex flex-col items-center justify-center px-6 py-16 text-center"
    >
      <div class="relative mb-8">
        <span
          class="font-bold select-none block"
          style="
            font-size: clamp(6rem, 20vw, 10rem);
            line-height: 1;
            color: transparent;
            -webkit-text-stroke: 2px rgba(16, 185, 129, 0.15);
          "
        >
          404
        </span>
        <div class="absolute inset-0 flex items-center justify-center">
          <div
            class="w-24 h-24 rounded-full flex items-center justify-center"
            style="
              background: radial-gradient(
                circle,
                rgba(16, 185, 129, 0.2) 0%,
                transparent 70%
              );
            "
          ></div>
        </div>
      </div>

      <h2 class="text-2xl md:text-3xl font-bold text-white mb-3">
        {{ $t("error.notFound") }}
      </h2>
      <p
        class="text-gray-400 text-sm max-w-xs md:max-w-sm mb-8 leading-relaxed"
      >
        {{ $t("error.notFoundDesc") }}
      </p>

      <div
        class="flex flex-col sm:flex-row gap-3 w-full max-w-xs sm:max-w-none sm:w-auto justify-center"
      >
        <RouterLink
          to="/"
          class="flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-6 py-3 rounded-full text-sm transition"
        >
          <ArrowLeft class="w-4 h-4" /> {{ $t("error.backHome") }}
        </RouterLink>
        <button
          class="flex items-center justify-center gap-2 border border-white/20 hover:border-white/40 text-gray-300 hover:text-white px-6 py-3 rounded-full text-sm transition"
        >
          {{ $t("error.report") }}
        </button>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ArrowLeft } from "lucide-vue-next";
import AppNavbar from "../components/AppNavbar.vue";
import AppFooter from "../components/AppFooter.vue";
</script>
