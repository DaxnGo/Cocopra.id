<template>
  <div
    class="min-h-screen"
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

    <!-- HERO SECTION -->
    <section
      data-aos="fade-up"
      class="text-center px-6 pt-16 pb-10 max-w-4xl mx-auto"
    >
      <div
        class="inline-flex items-center gap-2 text-emerald-400 text-xs font-medium tracking-widest uppercase mb-6 border border-emerald-800/50 rounded-full px-3 py-1"
        style="background: rgba(16, 185, 129, 0.08)"
      >
        <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
        {{ $t("hero.badge") }}
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
          {{ $t("hero.title1") }} <br />{{ $t("hero.title2") }}
        </span>
        <span class="text-emerald-400"> {{ $t("hero.title3") }}</span>
      </h1>

      <p class="text-gray-400 text-lg max-w-2xl mx-auto mb-10">
        {{ $t("hero.desc") }}
      </p>

      <div class="flex items-center justify-center gap-4 flex-wrap">
        <button
          class="flex items-center gap-2 bg-amber-500 hover:bg-amber-400 text-black font-semibold px-6 py-3 rounded-full transition"
        >
          <ScanLine class="w-5 h-5" /> {{ $t("hero.btnScan") }}
        </button>
        <button
          @click="showVideo = true"
          class="flex items-center gap-2 border border-gray-600 hover:border-white text-white px-6 py-3 rounded-full transition"
        >
          <PlayCircle class="w-5 h-5" /> {{ $t("hero.btnDemo") }}
        </button>
      </div>
    </section>

    <!-- SCANNER MOCKUP -->
    <section data-aos="fade-up" class="max-w-4xl mx-auto px-6 pb-20">
      <div
        class="rounded-2xl border border-white/10 overflow-hidden"
        style="
          background: rgba(255, 255, 255, 0.04);
          backdrop-filter: blur(10px);
        "
      >
        <div
          class="flex items-center justify-between px-5 py-3 border-b border-white/10"
        >
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-red-500"></span>
            <span class="w-3 h-3 rounded-full bg-amber-400"></span>
            <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
            <span class="text-gray-400 text-sm ml-3">{{
              $t("scanner.title")
            }}</span>
          </div>
          <div class="flex gap-2">
            <span
              class="text-xs text-gray-500 border border-gray-700 px-2 py-1 rounded"
              >{{ $t("scanner.liveFeed") }}</span
            >
            <span
              class="text-xs text-emerald-400 border border-emerald-700 bg-emerald-900/30 px-2 py-1 rounded"
              >{{ $t("scanner.aiActive") }}</span
            >
          </div>
        </div>

        <div class="flex flex-col md:flex-row">
          <div class="md:w-3/5 relative" style="min-height: 300px">
            <div
              class="absolute inset-0"
              :style="
                leafImageLoaded
                  ? 'background:none'
                  : 'background: linear-gradient(135deg, #0a2e18 0%, #1a5c35 100%)'
              "
            >
              <img
                v-if="!leafImageError"
                src="/michael-oxendine-aKvfQV4WpiA-unsplash.jpg"
                alt="Daun Kelapa"
                class="w-full h-full object-cover"
                @error="leafImageError = true"
                @load="leafImageLoaded = true"
              />
              <div
                v-if="leafImageError"
                class="w-full h-full flex flex-col items-center justify-center gap-2 opacity-40"
              >
                <Leaf class="w-16 h-16 text-emerald-400" />
              </div>
            </div>
            <div class="absolute inset-0 p-4 flex flex-col">
              <div
                class="bg-black/60 rounded-lg px-3 py-2 self-start backdrop-blur-sm"
              >
                <div class="text-gray-400 text-xs tracking-wider">
                  {{ $t("scanner.detected") }}
                </div>
                <div class="text-white text-sm font-semibold italic">
                  Oryctes rhinoceros
                </div>
              </div>
              <div class="flex-1 flex items-center justify-center">
                <div
                  class="border-2 border-emerald-400 rounded-sm opacity-80"
                  style="width: 45%; height: 55%"
                ></div>
              </div>
            </div>
          </div>

          <div
            class="md:w-2/5 p-5 flex flex-col gap-4 border-t md:border-t-0 md:border-l border-white/10"
          >
            <div class="bg-white/5 rounded-xl p-4">
              <h3
                class="text-white font-semibold text-sm mb-3 flex items-center gap-2"
              >
                <BarChart2 class="w-4 h-4 text-emerald-400" />
                {{ $t("scanner.confidence") }}
              </h3>
              <div class="mb-3">
                <div class="flex justify-between text-xs text-gray-300 mb-1">
                  <span>{{ $t("scanner.pest") }}</span>
                  <span class="text-emerald-400 font-bold">98.2%</span>
                </div>
                <div class="w-full bg-gray-800 rounded-full h-1.5">
                  <div
                    class="bg-emerald-400 h-1.5 rounded-full"
                    style="width: 98.2%"
                  ></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-xs text-gray-300 mb-1">
                  <span>{{ $t("scanner.nutrisi") }}</span>
                  <span class="text-gray-400">1.8%</span>
                </div>
                <div class="w-full bg-gray-800 rounded-full h-1.5">
                  <div
                    class="bg-gray-600 h-1.5 rounded-full"
                    style="width: 1.8%"
                  ></div>
                </div>
              </div>
            </div>

            <div class="border border-red-900/50 bg-red-950/30 rounded-xl p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="text-amber-400 text-sm font-semibold">{{
                  $t("scanner.warning")
                }}</span>
                <TriangleAlert class="w-4 h-4 text-amber-400" />
              </div>
              <p class="text-gray-400 text-xs leading-relaxed">
                {{ $t("scanner.warningDesc") }}
              </p>
              <a
                href="#"
                class="text-amber-400 text-xs font-semibold mt-2 inline-flex items-center gap-1 hover:text-amber-300 transition"
              >
                {{ $t("scanner.openMap") }} <ArrowRight class="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 border-t border-white/10">
          <div class="p-4 border-r border-white/10">
            <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
              {{ $t("scanner.totalScan") }}
            </div>
            <div class="text-white font-bold text-xl">128,402</div>
          </div>
          <div class="p-4 md:border-r border-white/10">
            <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
              {{ $t("scanner.accuracy") }}
            </div>
            <div class="text-emerald-400 font-bold text-xl">99.1%</div>
          </div>
          <div class="p-4 border-r border-t md:border-t-0 border-white/10">
            <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
              {{ $t("scanner.activeMap") }}
            </div>
            <div class="text-white font-bold text-xl">24 Prov</div>
          </div>
          <div class="p-4 border-t md:border-t-0 border-white/10">
            <div class="text-xs text-gray-500 mb-1 uppercase tracking-wide">
              {{ $t("scanner.copricePrice") }}
            </div>
            <div class="text-amber-400 font-bold text-xl">Rp14.200</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION FITUR -->
    <section data-aos="fade-up" class="max-w-4xl mx-auto px-6 pb-24">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div
          class="rounded-2xl border border-white/10 p-6 hover:border-emerald-700/50 transition group"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <div
            class="w-12 h-12 rounded-2xl bg-emerald-900/50 flex items-center justify-center mb-5 group-hover:bg-emerald-800/50 transition"
          >
            <ScanLine class="w-6 h-6 text-emerald-400" />
          </div>
          <h3 class="text-white font-semibold text-lg mb-2">
            {{ $t("features.scanner") }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t("features.scannerDesc") }}
          </p>
        </div>
        <div
          class="rounded-2xl border border-white/10 p-6 hover:border-emerald-700/50 transition group"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <div
            class="w-12 h-12 rounded-2xl bg-emerald-900/50 flex items-center justify-center mb-5 group-hover:bg-emerald-800/50 transition"
          >
            <TrendingUp class="w-6 h-6 text-emerald-400" />
          </div>
          <h3 class="text-white font-semibold text-lg mb-2">
            {{ $t("features.price") }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t("features.priceDesc") }}
          </p>
        </div>
        <div
          class="rounded-2xl border border-white/10 p-6 hover:border-emerald-700/50 transition group"
          style="background: rgba(255, 255, 255, 0.04)"
        >
          <div
            class="w-12 h-12 rounded-2xl bg-emerald-900/50 flex items-center justify-center mb-5 group-hover:bg-emerald-800/50 transition"
          >
            <MapPin class="w-6 h-6 text-emerald-400" />
          </div>
          <h3 class="text-white font-semibold text-lg mb-2">
            {{ $t("features.warning") }}
          </h3>
          <p class="text-gray-400 text-sm leading-relaxed">
            {{ $t("features.warningDesc") }}
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION TANTANGAN -->
    <section
      id="tantangan"
      class="py-24 px-6"
      style="
        background: linear-gradient(
          180deg,
          transparent 0%,
          rgba(0, 0, 0, 0.3) 100%
        );
      "
    >
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl md:text-5xl font-bold text-white mb-4">
            {{ $t("challenge.title") }}
            <span class="text-amber-400">{{
              $t("challenge.titleHighlight")
            }}</span>
          </h2>
          <p class="text-gray-400 text-base max-w-xl mx-auto">
            {{ $t("challenge.desc") }}
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
              {{ $t("challenge.pest") }}
            </h3>
            <p class="text-gray-400 text-sm leading-relaxed">
              {{ $t("challenge.pestDesc") }}
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
              {{ $t("challenge.price") }}
            </h3>
            <p class="text-gray-400 text-sm leading-relaxed">
              {{ $t("challenge.priceDesc") }}
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
              {{ $t("challenge.regulation") }}
            </h3>
            <p class="text-gray-400 text-sm leading-relaxed">
              {{ $t("challenge.regulationDesc") }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION KEUNGGULAN -->
    <section id="keunggulan" class="py-24 px-6">
      <div class="max-w-4xl mx-auto flex flex-col gap-24">
        <div
          data-aos="fade-up"
          class="flex flex-col md:flex-row items-center gap-12"
        >
          <div class="md:w-1/2">
            <div
              class="text-emerald-400 text-xs font-semibold tracking-widest uppercase mb-3"
            >
              {{ $t("advantage.scannerBadge") }}
            </div>
            <h3 class="text-white text-3xl font-bold mb-4">
              {{ $t("advantage.scannerTitle") }}
            </h3>
            <p class="text-gray-400 text-sm leading-relaxed mb-6">
              {{ $t("advantage.scannerDesc") }}
            </p>
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-2 text-sm text-gray-300">
                <CheckCircle class="w-4 h-4 text-emerald-400 shrink-0" />
                {{ $t("advantage.check1") }}
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-300">
                <CheckCircle class="w-4 h-4 text-emerald-400 shrink-0" />
                {{ $t("advantage.check2") }}
              </div>
            </div>
          </div>
          <div class="md:w-1/2 flex justify-center">
            <div
              class="w-56 rounded-3xl border border-white/10 overflow-hidden"
              style="
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
              "
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
                    {{ $t("scanner.detected") }}
                  </div>
                  <div class="text-white text-sm font-semibold italic">
                    Oryctes rhinoceros
                  </div>
                  <div class="w-full bg-gray-800 rounded-full h-1 mt-2">
                    <div
                      class="bg-emerald-400 h-1 rounded-full"
                      style="width: 98%"
                    ></div>
                  </div>
                </div>

                <div class="bg-white/5 rounded-lg p-3 text-xs text-gray-400">
                  {{ $t("chat.recommendation") }}
                  <span class="text-emerald-400">Sycanus</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div
          data-aos="fade-up"
          class="flex flex-col md:flex-row-reverse items-center gap-12"
        >
          <div class="md:w-1/2">
            <div
              class="text-amber-400 text-xs font-semibold tracking-widest uppercase mb-3"
            >
              {{ $t("advantage.ledgerBadge") }}
            </div>
            <h3 class="text-white text-3xl font-bold mb-4">
              {{ $t("advantage.ledgerTitle") }}
            </h3>
            <p class="text-gray-400 text-sm leading-relaxed mb-6">
              {{ $t("advantage.ledgerDesc") }}
            </p>
            <button
              class="border border-amber-500/50 text-amber-400 hover:bg-amber-500/10 px-5 py-2 rounded-full text-sm transition"
            >
              {{ $t("advantage.ledgerBtn") }}
            </button>
          </div>
          <div class="md:w-1/2 flex justify-center">
            <div
              class="w-full max-w-xs rounded-2xl border border-white/10 p-4"
              style="background: rgba(255, 255, 255, 0.04)"
            >
              <div class="text-xs text-gray-500 mb-3">
                {{ $t("chart.title") }}
              </div>
              <div class="flex items-end gap-2 h-24 mb-2">
                <div
                  class="flex-1 bg-amber-700/60 rounded-t-sm"
                  style="height: 55%"
                ></div>
                <div
                  class="flex-1 bg-amber-600/70 rounded-t-sm"
                  style="height: 70%"
                ></div>
                <div
                  class="flex-1 bg-amber-500/80 rounded-t-sm"
                  style="height: 60%"
                ></div>
                <div
                  class="flex-1 bg-amber-400 rounded-t-sm"
                  style="height: 90%"
                ></div>
                <div
                  class="flex-1 bg-amber-500/80 rounded-t-sm"
                  style="height: 75%"
                ></div>
                <div
                  class="flex-1 bg-amber-600/70 rounded-t-sm"
                  style="height: 65%"
                ></div>
                <div
                  class="flex-1 bg-amber-400 rounded-t-sm"
                  style="height: 85%"
                ></div>
              </div>

              <div class="flex justify-between text-xs text-gray-600">
                <span v-for="day in $t('chart.days').split('|')" :key="day">{{
                  day
                }}</span>
              </div>

              <div class="mt-3 flex justify-between items-center">
                <span class="text-xs text-gray-400">Rp14.200/kg</span>
                <span class="text-xs text-emerald-400 font-semibold"
                  >+4.2%</span
                >
              </div>
            </div>
          </div>
        </div>

        <div
          data-aos="fade-up"
          class="flex flex-col md:flex-row items-center gap-12"
        >
          <div class="md:w-1/2">
            <div
              class="text-blue-400 text-xs font-semibold tracking-widest uppercase mb-3"
            >
              {{ $t("advantage.ragBadge") }}
            </div>
            <h3 class="text-white text-3xl font-bold mb-4">
              {{ $t("advantage.ragTitle") }}
            </h3>
            <p class="text-gray-400 text-sm leading-relaxed mb-6">
              {{ $t("advantage.ragDesc") }}
            </p>

            <div
              class="rounded-xl border border-white/10 px-4 py-3 text-sm text-gray-400 italic"
              style="background: rgba(255, 255, 255, 0.04)"
            >
              {{ $t("chat.quote") }}
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
                {{ $t("chat.userMsg") }}
              </div>
              <div
                class="bg-white/5 rounded-xl rounded-tr-sm px-3 py-2 text-xs text-gray-300 self-end max-w-[85%]"
              >
                {{ $t("chat.aiMsg") }}
                <span class="text-emerald-400">Tetrastichus brontispae</span>
                {{ $t("chat.aiMsgEnd") }}
              </div>
              <div
                class="mt-2 bg-white/5 border border-white/10 rounded-full px-3 py-2 flex items-center gap-2"
              >
                <span class="flex-1 text-xs text-gray-600">{{
                  $t("chat.placeholder")
                }}</span>
                <div
                  class="w-5 h-5 rounded-full bg-emerald-600 flex items-center justify-center"
                >
                  <ArrowRight class="w-3 h-3 text-white" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION ALUR KERJA -->
    <section id="alur" class="py-24 px-6">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-white mb-2">
            {{ $t("flow.title") }}
            <span class="text-amber-400">{{ $t("flow.titleHighlight") }}</span>
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
            <h4 class="text-white font-semibold mb-2">
              {{ $t("flow.step1") }}
            </h4>
            <p class="text-gray-400 text-sm leading-relaxed">
              {{ $t("flow.step1Desc") }}
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
            <h4 class="text-white font-semibold mb-2">
              {{ $t("flow.step2") }}
            </h4>
            <p class="text-gray-400 text-sm leading-relaxed">
              {{ $t("flow.step2Desc") }}
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
            <h4 class="text-white font-semibold mb-2">
              {{ $t("flow.step3") }}
            </h4>
            <p class="text-gray-400 text-sm leading-relaxed">
              {{ $t("flow.step3Desc") }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION FAQ -->
    <section data-aos="fade-up" id="faq" class="py-24 px-6">
      <div class="max-w-2xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-white mb-3">
            {{ $t("faq.title") }}
            <span class="text-amber-400">{{ $t("faq.titleHighlight") }}</span>
          </h2>
          <p class="text-gray-400 text-sm">{{ $t("faq.desc") }}</p>
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
              <span class="text-amber-400 text-sm font-medium">{{
                item.q
              }}</span>
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

    <!-- Video Demo Modal -->
<VideoModal
  :is-open="showVideo"
  video-id="NpEaa2P7qZI"
  @close="showVideo = false"
/>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  ScanLine,
  PlayCircle,
  BarChart2,
  TriangleAlert,
  ArrowRight,
  Leaf,
  TrendingUp,
  MapPin,
  Bug,
  Banknote,
  FileText,
  CheckCircle,
  ChevronDown,
} from "lucide-vue-next";
import AppNavbar from "../components/AppNavbar.vue";
import AppFooter from "../components/AppFooter.vue";

import VideoModal from '../components/VideoModal.vue'
const showVideo = ref(false)

const { t } = useI18n();

const leafImageError = ref(false);
const leafImageLoaded = ref(false);
const activeFaq = ref(null);

// FAQ otomatis ikut bahasa
const faqs = computed(() => [
  { q: t("faq.q1"), a: t("faq.a1") },
  { q: t("faq.q2"), a: t("faq.a2") },
  { q: t("faq.q3"), a: t("faq.a3") },
  { q: t("faq.q4"), a: t("faq.a4") },
]);
</script>
