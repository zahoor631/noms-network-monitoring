<template>
  <footer class="bg-white border-t border-gray-200 px-6 py-2 text-xs text-gray-500 text-center">
    © {{ year }} NOMS — Network Operations & Monitoring System
  </footer>
</template>

<script setup>
const year = new Date().getFullYear()
</script>