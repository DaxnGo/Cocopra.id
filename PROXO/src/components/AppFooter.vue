<template>
  <footer
    class="px-6 pt-16 pb-8 border-t border-white/10"
    style="background: rgba(0, 0, 0, 0.3)"
  >
    <div class="max-w-5xl mx-auto">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-10 mb-12">
        <!-- Features -->
        <div>
          <div
            class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-4"
          >
            {{ $t("footerLinks.featuresTitle") }}
          </div>
          <div class="flex flex-col gap-2">
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >Pest-Vision Scanner</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >Adil-Harga Ledger</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >RAG Agri-Assistant</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >Geo-Alert EWS</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >Regulatory Check</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >Offline PWA</a
            >
          </div>
        </div>

        <!-- Resources -->
        <div>
          <div
            class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-4"
          >
            {{ $t("footerLinks.resourcesTitle") }}
          </div>
          <div class="flex flex-col gap-2">
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.farmerGuide") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.apiDocs") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.regulationBase") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >FAQ</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.privacyPolicy") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.termsOfUse") }}</a
            >
          </div>
        </div>

        <!-- Company -->
        <div>
          <div
            class="text-gray-500 text-xs font-semibold tracking-widest uppercase mb-4"
          >
            {{ $t("footerLinks.companyTitle") }}
          </div>
          <div class="flex flex-col gap-2">
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("nav.home") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.scanner") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.copraPrice") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.pestMap") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("footerLinks.about") }}</a
            >
            <a
              href="#"
              class="text-gray-400 text-sm hover:text-white transition"
              >{{ $t("nav.start") }}</a
            >
          </div>
        </div>

        <!-- Brand -->
        <div>
          <div class="flex items-center gap-3 mb-4">
            <img
              src="/Logo-Cocopra.id.png"
              alt="Logo"
              class="w-12 h-12 object-contain"
            />
            <span class="text-white font-bold text-xl"
              >Cocopra<span class="text-amber-400">.id</span></span
            >
          </div>
          <p class="text-gray-400 text-sm leading-relaxed mb-5">
            {{ $t("footer.desc") }}
          </p>
          <div class="flex flex-col gap-2">
            <input
              type="email"
              :placeholder="$t('footer.emailPlaceholder')"
              class="w-full bg-white/5 border border-white/10 rounded-full px-4 py-2 text-sm text-white placeholder-gray-600 outline-none focus:border-emerald-600"
            />
            <button
              class="w-full bg-amber-500 hover:bg-amber-400 text-black font-semibold px-4 py-2 rounded-full text-xs transition"
            >
              {{ $t("footer.betaBtn") }}
            </button>
          </div>
        </div>
      </div>

      <div
        class="border-t border-white/10 pt-6 flex flex-col md:flex-row items-center justify-between gap-4"
      >
        <p class="text-gray-600 text-xs">{{ $t("footer.copy") }}</p>
        <div class="flex items-center gap-4">
          <a href="#" class="text-gray-600 hover:text-white transition"
            ><Github class="w-4 h-4"
          /></a>
          <a href="#" class="text-gray-600 hover:text-white transition"
            ><Linkedin class="w-4 h-4"
          /></a>
          <a href="#" class="text-gray-600 hover:text-white transition"
            ><Instagram class="w-4 h-4"
          /></a>
        </div>
        <div class="flex gap-4 text-xs text-gray-600">
          <a href="#" class="hover:text-white transition">{{
            $t("footer.privacy")
          }}</a>
          <a href="#" class="hover:text-white transition">{{
            $t("footer.terms")
          }}</a>
          <a href="#" class="hover:text-white transition">{{
            $t("footer.cookie")
          }}</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import { Github, Linkedin, Instagram } from "lucide-vue-next";
const { t } = useI18n();
</script>
