<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="wrapper">
    <header>
      <div class="relative mx-auto">
        <div class="row items-center">
          <div class="w-full">
            <div class="flex items-center justify-between p-4 text-gray-800">
              <router-link to="/" class="text-xl hover:text-blue-700">Retina DeepAI</router-link>
            </div>
          </div>
        </div>
      </div>
    </header>

    <section class="border-solid border-t-2 border-gray-200">
      <router-view />
    </section>

    <footer>
    </footer>
  </div>
</template>

<style scoped>
.wrapper {
  min-height: 100vh;
}
</style>
