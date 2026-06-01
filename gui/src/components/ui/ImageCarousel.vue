<template>
  <div class="card-images" @mouseenter="stop" @mouseleave="start">
    <transition name="fade-img" mode="out-in">
      <img
        v-if="images?.length"
        :key="currentImageIndex"
        :src="images[currentImageIndex].url"
        :alt="alt"
        class="card-img"
      />

      <div v-else class="card-img card-img-placeholder">
        <FireflyLogo :pulse="true" :drift="false" size="w-14 h-14" />
      </div>
    </transition>

    <!-- arrows -->
    <button v-if="images?.length > 1" class="carousel-btn left" @click="prev">
      ‹
    </button>

    <button v-if="images?.length > 1" class="carousel-btn right" @click="next">
      ›
    </button>

    <!-- dots -->
    <div v-if="images?.length > 1" class="carousel-dots">
      <span
        v-for="(_, i) in images"
        :key="i"
        class="dot"
        :class="{ 'dot-active': i === currentImageIndex }"
        @click="goTo(i)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import FireflyLogo from "./FireflyLogo.vue";
import { useCarousel } from "../../composables/useCarousel";

interface ImageItem {
  url: string;
}

const props = defineProps<{
  images?: ImageItem[];
  alt?: string;
}>();

const {
  currentIndex: currentImageIndex,
  next,
  prev,
  goTo,
  start,
  stop,
} = useCarousel(props.images?.length || 0);
</script>

<style scoped>
.card-images {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #0d1a10;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-img-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

/* botones */
.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.45);
  color: white;
  font-size: 18px;
  opacity: 0;
  transition: 0.2s;
}

.card-images:hover .carousel-btn {
  opacity: 1;
}

.carousel-btn.left {
  left: 8px;
}

.carousel-btn.right {
  right: 8px;
}

/* dots */
.carousel-dots {
  position: absolute;
  bottom: 6px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 4px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
}

.dot-active {
  background: var(--color-accent);
}

.dot:hover {
  background: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

/* transition */
.fade-img-enter-active,
.fade-img-leave-active {
  transition: opacity 0.5s ease;
}

.fade-img-enter-from,
.fade-img-leave-to {
  opacity: 0;
}
</style>
