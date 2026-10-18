<template>
  <div
    class="min-h-screen"
    style="background: radial-gradient(ellipse at top, #1a4a2e 0%, #0d2818 40%, #061510 100%)"
  >
    <AppNavbar />

    <HeroSection @open-demo="showVideo = true" />
    <ScannerPreview />
    <FeaturesSection />
    <ChallengeSection />
    <AdvantageSection />
    <FlowSection />
    <FaqSection />

    <!-- Video Demo Modal -->
    <VideoModal :is-open="showVideo" video-id="NpEaa2P7qZI" @close="showVideo = false" />
    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppNavbar from '../components/AppNavbar.vue'
import AppFooter from '../components/AppFooter.vue'
import VideoModal from '../components/VideoModal.vue'
import HeroSection from '../components/home/HeroSection.vue'
import ScannerPreview from '../components/home/ScannerPreview.vue'
import FeaturesSection from '../components/home/FeaturesSection.vue'
import ChallengeSection from '../components/home/ChallengeSection.vue'
import AdvantageSection from '../components/home/AdvantageSection.vue'
import FlowSection from '../components/home/FlowSection.vue'
import FaqSection from '../components/home/FaqSection.vue'

const showVideo = ref(false)
</script>
