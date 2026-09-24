<template>
  <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
    <h2 class="text-lg font-semibold text-gray-800">
      {{ currentTitle }}
    </h2>
    <div class="flex items-center gap-4">
      <!-- Avatar + User Info -->
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-full overflow-hidden bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm border-2 border-white shadow">
          <img
            v-if="auth.user?.avatar_url"
            :src="auth.user.avatar_url"
            alt="Avatar"
            class="w-full h-full object-cover"
          />
          <span v-else>{{ auth.user?.username?.charAt(0).toUpperCase() }}</span>
        </div>
        <div class="text-sm text-gray-600">
          <span class="font-medium">{{ auth.user?.username }}</span>
          <span class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded">
            {{ auth.user?.role }}
          </span>
        </div>
      </div>
      <button
        @click="logout"
        class="text-sm text-red-600 hover:text-red-800 font-medium"
      >
        Logout
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const currentTitle = computed(() => {
  return route.name ? String(route.name) : 'Dashboard'
})

function logout() {
  auth.logout()
  router.push('/login')
}
</script>