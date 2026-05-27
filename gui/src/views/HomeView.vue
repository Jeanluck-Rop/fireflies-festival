<template>
  <div class="flex flex-col">
    <HeroSection />
    <HowToSection />
    <CabinVsCamping />
    <DidYouKnow />
    <FinalCTA />
    <FooterSection />
  </div>
</template>

<script setup lang="ts">
import HeroSection from '../components/landing/HeroSection.vue';
import HowToSection from '../components/landing/HowToSection.vue';
import CabinVsCamping from '../components/landing/CabinVsCamping.vue';
import DidYouKnow from '../components/landing/DidYouKnow.vue';
import FinalCTA from '../components/landing/FinalCTA.vue';
import FooterSection from '../components/landing/FooterSection.vue';
</script>
