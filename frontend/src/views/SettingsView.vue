<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Settings</h1>
      <p class="text-sm text-gray-500 mt-0.5">
        Application aur system settings — profile, monitoring, danger zone
      </p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      <!-- Profile Card -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3 mb-4">
          <span class="text-2xl">👤</span>
          <h3 class="font-semibold text-gray-800">Profile</h3>
        </div>

        <div class="flex items-center gap-4 mb-4">
          <div class="relative group">
            <div class="w-20 h-20 rounded-full overflow-hidden bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-3xl border-4 border-white shadow-lg">
              <img
                v-if="auth.user?.avatar_url"
                :src="auth.user.avatar_url"
                alt="Avatar"
                class="w-full h-full object-cover"
              />
              <span v-else>{{ auth.user?.username?.charAt(0).toUpperCase() }}</span>
            </div>
            <label class="absolute inset-0 rounded-full bg-black/50 text-white opacity-0 group-hover:opacity-100 flex items-center justify-center cursor-pointer transition">
              <span class="text-2xl">📷</span>
              <input type="file" accept="image/*" class="hidden" @change="handleAvatarUpload" />
            </label>
          </div>

          <div class="flex-1">
            <p class="font-semibold text-gray-800">{{ auth.user?.username }}</p>
            <p class="text-sm text-gray-500">{{ auth.user?.email }}</p>
            <span :class="roleBadge(auth.user?.role)" class="inline-block mt-1 px-2 py-0.5 rounded text-xs font-medium">
              {{ auth.user?.role }}
            </span>
            <div class="flex items-center gap-3 mt-2 flex-wrap">
              <label class="text-xs text-blue-600 hover:text-blue-800 font-medium cursor-pointer">
                📷 {{ auth.user?.avatar_url ? 'Change' : 'Upload' }}
                <input type="file" accept="image/*" class="hidden" @change="handleAvatarUpload" />
              </label>
              <button v-if="auth.user?.avatar_url" class="text-xs text-red-600 hover:text-red-800 font-medium" @click="handleAvatarDelete">
                🗑️ Remove
              </button>
              <button class="text-xs text-blue-600 hover:text-blue-800 font-medium" @click="openEditProfile">
                ✏️ Edit Profile
              </button>
            </div>
            <p v-if="uploading" class="text-xs text-blue-600 mt-1">⏳ Uploading...</p>
          </div>
        </div>

        <div class="space-y-2 text-sm border-t border-gray-100 pt-4">
          <div class="flex justify-between">
            <span class="text-gray-500">User ID</span>
            <span class="font-mono text-xs">#{{ auth.user?.id }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Full Name</span>
            <span>{{ auth.user?.full_name || '—' }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Status</span>
            <span :class="auth.user?.is_active ? 'text-green-600' : 'text-red-600'">
              {{ auth.user?.is_active ? '● Active' : '○ Inactive' }}
            </span>
          </div>
        </div>
      </div>

      <!-- System Info Card -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
        <div class="flex items-center gap-3 mb-4">
          <span class="text-2xl">⚙️</span>
          <h3 class="font-semibold text-gray-800">System Information</h3>
        </div>
        <div class="space-y-3 text-sm">
          <div class="flex justify-between"><span class="text-gray-500">Application</span><span class="font-medium">NOMS</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Version</span><span class="font-mono text-xs">0.1.0</span></div>
          <div class="flex justify-between"><span class="text-gray-500">Backend API</span><span class="font-mono text-xs">{{ apiUrl }}</span></div>
          <div class="flex justify-between items-center">
            <span class="text-gray-500">Backend Status</span>
            <span :class="health === 'ok' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'" class="px-2 py-0.5 rounded text-xs font-medium">
              {{ health === 'ok' ? '● Running' : '● Down' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal -->
    <BaseModal v-model="showEditProfile" title="Edit Profile">
      <form @submit.prevent="handleUpdateProfile" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
          <input :value="auth.user?.username" disabled class="w-full px-3 py-2 border border-gray-300 rounded-lg bg-gray-100" />
          <p class="text-xs text-gray-400 mt-1">Username change nahi ho sakta</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email <span class="text-red-500">*</span></label>
          <input v-model="editForm.email" type="email" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <p class="text-xs text-gray-400 mt-1">Forgot password ke liye ye email use hoga</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
          <input v-model="editForm.full_name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div v-if="profileError" class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg">
          {{ profileError }}
        </div>
        <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
          <button type="button" class="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg font-medium" @click="showEditProfile = false">Cancel</button>
          <button type="submit" :disabled="savingProfile" class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium disabled:opacity-50">
            {{ savingProfile ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </form>
    </BaseModal>

    <div class="mt-6 text-center text-xs text-gray-400">
      NOMS — Network Operations & Monitoring System · v0.1.0 · © {{ year }}
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { usersApi } from '@/api/users'
import { useToast } from '@/composables/useToast'
import BaseModal from '@/components/common/BaseModal.vue'

const auth = useAuthStore()
const toast = useToast()

const health = ref('ok')
const uploading = ref(false)
const apiUrl = import.meta.env.VITE_API_BASE_URL || '/api'
const year = new Date().getFullYear()

// Edit profile
const showEditProfile = ref(false)
const savingProfile = ref(false)
const profileError = ref('')
const editForm = reactive({ email: '', full_name: '' })

onMounted(checkHealth)

function roleBadge(role) {
  return {
    admin: 'bg-red-100 text-red-700',
    engineer: 'bg-orange-100 text-orange-700',
    noc: 'bg-yellow-100 text-yellow-700',
    viewer: 'bg-gray-100 text-gray-700',
  }[role] || 'bg-gray-100 text-gray-700'
}

async function checkHealth() {
  try {
    const res = await fetch('/api/health')
    health.value = res.ok ? 'ok' : 'error'
  } catch {
    health.value = 'error'
  }
}

function openEditProfile() {
  editForm.email = auth.user?.email || ''
  editForm.full_name = auth.user?.full_name || ''
  profileError.value = ''
  showEditProfile.value = true
}

async function handleUpdateProfile() {
  savingProfile.value = true
  profileError.value = ''
  try {
    const { data } = await usersApi.updateMe({
      email: editForm.email,
      full_name: editForm.full_name,
    })
    auth.user = { ...auth.user, email: data.email, full_name: data.full_name }
    localStorage.setItem('user', JSON.stringify(auth.user))
    toast.success('Profile updated')
    showEditProfile.value = false
  } catch (e) {
    profileError.value = e.response?.data?.detail || 'Update failed'
  } finally {
    savingProfile.value = false
  }
}

async function handleAvatarUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) {
    toast.error('File too large. Max 5MB.')
    return
  }
  uploading.value = true
  try {
    const { data } = await usersApi.uploadAvatar(file)
    auth.user = { ...auth.user, avatar_url: data.avatar_url }
    localStorage.setItem('user', JSON.stringify(auth.user))
    toast.success('Photo uploaded!')
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Upload failed')
  } finally {
    uploading.value = false
    event.target.value = ''
  }
}

async function handleAvatarDelete() {
  if (!confirm('Remove profile photo?')) return
  try {
    await usersApi.deleteAvatar()
    auth.user = { ...auth.user, avatar_url: null }
    localStorage.setItem('user', JSON.stringify(auth.user))
    toast.success('Photo removed')
  } catch {
    toast.error('Delete failed')
  }
}
</script>