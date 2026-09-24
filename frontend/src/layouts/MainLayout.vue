<template>
  <div class="flex h-screen bg-gray-100">
    <AppSidebar />
    <div class="flex-1 flex flex-col overflow-hidden">
      <AppTopbar />
      <main class="flex-1 overflow-y-auto p-6">
        <router-view />
      </main>
      <AppFooter />
    </div>
  </div>
</template>

<script setup>
import AppSidebar from '@/components/common/AppSidebar.vue'
import AppTopbar from '@/components/common/AppTopbar.vue'
import AppFooter from '@/components/common/AppFooter.vue'
</script>