<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Users</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          User management — roles aur permissions (admin only)
        </p>
      </div>
      <button
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
        @click="openCreate"
      >
        <span>➕</span> Create User
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Total Users</p>
        <p class="text-2xl font-bold text-blue-600">{{ users.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Active</p>
        <p class="text-2xl font-bold text-green-600">{{ activeCount }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Admins</p>
        <p class="text-2xl font-bold text-red-600">{{ countBy('admin') }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Engineers</p>
        <p class="text-2xl font-bold text-orange-600">{{ countBy('engineer') }}</p>
      </div>
    </div>

    <!-- Loading -->
    <Loader v-if="loading" />

    <!-- Table -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
              <th class="text-left px-4 py-3 font-medium">User</th>
              <th class="text-left px-4 py-3 font-medium">Email</th>
              <th class="text-left px-4 py-3 font-medium">Role</th>
              <th class="text-left px-4 py-3 font-medium">Status</th>
              <th class="text-left px-4 py-3 font-medium">Created</th>
              <th class="text-right px-4 py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!users.length">
              <td colspan="6" class="text-center py-12 text-gray-400">
                <p class="text-4xl mb-2">👥</p>
                <p class="font-medium">No users yet</p>
              </td>
            </tr>
            <tr
              v-for="u in users"
              :key="u.id"
              class="border-t border-gray-100 hover:bg-gray-50"
            >
              <td class="px-4 py-3">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full overflow-hidden bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm shrink-0">
                    <img
                      v-if="u.avatar_url"
                      :src="u.avatar_url"
                      alt="Avatar"
                      class="w-full h-full object-cover"
                    />
                    <span v-else>{{ u.username.charAt(0).toUpperCase() }}</span>
                  </div>
                  <div>
                    <p class="font-medium text-gray-800">{{ u.username }}</p>
                    <p v-if="u.full_name" class="text-xs text-gray-500">{{ u.full_name }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3 text-gray-600 text-xs">{{ u.email }}</td>
              <td class="px-4 py-3">
                <span :class="roleBadge(u.role)" class="px-2 py-0.5 rounded text-xs font-medium">
                  {{ roleIcon(u.role) }} {{ u.role }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span
                  v-if="u.is_active"
                  class="px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-700"
                >
                  ● Active
                </span>
                <span
                  v-else
                  class="px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600"
                >
                  ○ Inactive
                </span>
              </td>
              <td class="px-4 py-3 text-gray-500 text-xs">
                {{ formatDate(u.created_at) }}
              </td>
              <td class="px-4 py-3 text-right whitespace-nowrap">
                <button
                  class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-3"
                  @click="openEdit(u)"
                >
                  ✏️ Edit
                </button>
                <button
                  class="text-orange-600 hover:text-orange-800 text-xs font-medium mr-3"
                  @click="openPasswordReset(u)"
                >
                  🔑 Password
                </button>
                <button
                  class="text-purple-600 hover:text-purple-800 text-xs font-medium mr-3"
                  @click="openAvatarUpload(u)"
                >
                  🖼️ Avatar
                </button>
                <button
                  v-if="u.username !== 'admin'"
                  class="text-red-600 hover:text-red-800 text-xs font-medium"
                  @click="confirmDelete(u)"
                >
                  🗑️ Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <BaseModal
      v-model="showForm"
      :title="editing ? 'Edit User' : 'Create User'"
    >
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Username <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.username"
            type="text"
            required
            :disabled="!!editing"
            placeholder="john_doe"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Email <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.email"
            type="email"
            required
            placeholder="john@noms.com"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
          <input
            v-model="form.full_name"
            type="text"
            placeholder="John Doe"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div v-if="!editing">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Password <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.password"
            type="password"
            required
            minlength="6"
            placeholder="••••••"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Role <span class="text-red-500">*</span>
          </label>
          <select
            v-model="form.role"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="admin">🔴 Admin — Full access</option>
            <option value="engineer">🟠 Engineer — Manage devices</option>
            <option value="noc">🟡 NOC Operator — Monitor & tickets</option>
            <option value="viewer">⚪ Viewer — Read-only</option>
          </select>
        </div>

        <div v-if="editing">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              v-model="form.is_active"
              type="checkbox"
              class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
            />
            <span class="text-sm text-gray-700">Active (user can login)</span>
          </label>
        </div>

        <div
          v-if="error"
          class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg"
        >
          {{ error }}
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
          <button
            type="button"
            class="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition"
            @click="closeForm"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition disabled:opacity-50"
          >
            {{ saving ? 'Saving...' : editing ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </BaseModal>

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-model="showDelete"
      title="Delete User"
      :message="`Kya aap '${deleting?.username}' ko delete karna chahte ho? Ye action undo nahi hoga.`"
      @confirm="handleDelete"
    />

    <!-- Admin: Reset Password Modal -->
    <BaseModal v-model="showPasswordReset" title="🔑 Reset User Password">
      <div class="space-y-4">
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm">
          <p class="font-medium text-blue-800">User: {{ resettingUser?.username }}</p>
          <p class="text-blue-600 text-xs mt-1">{{ resettingUser?.email }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            New Password <span class="text-red-500">*</span>
          </label>
          <div class="flex gap-2">
            <input
              v-model="newPassword"
              type="text"
              placeholder="Minimum 6 characters"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
            />
            <button
              type="button"
              class="px-3 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-xs"
              @click="generateRandomPassword"
            >
              🎲 Random
            </button>
          </div>
          <p class="text-xs text-gray-400 mt-1">
            ⚠️ Ye password user ko bata dena (ya email kar dena)
          </p>
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
          <button
            type="button"
            class="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg font-medium"
            @click="showPasswordReset = false"
          >
            Cancel
          </button>
          <button
            type="button"
            :disabled="resettingPassword"
            class="px-4 py-2 text-sm bg-orange-600 hover:bg-orange-700 text-white rounded-lg font-medium disabled:opacity-50"
            @click="handleAdminPasswordReset"
          >
            {{ resettingPassword ? 'Resetting...' : 'Reset Password' }}
          </button>
        </div>
      </div>
    </BaseModal>

    <!-- Admin: Upload Avatar Modal -->
    <BaseModal v-model="showAvatarUpload" title="🖼️ Change User Avatar">
      <div class="space-y-4">
        <div class="bg-purple-50 border border-purple-200 rounded-lg p-3 text-sm">
          <p class="font-medium text-purple-800">User: {{ resettingUser?.username }}</p>
          <p class="text-purple-600 text-xs mt-1">{{ resettingUser?.email }}</p>
        </div>

        <!-- Preview current -->
        <div v-if="resettingUser?.avatar_url" class="flex justify-center">
          <div class="w-24 h-24 rounded-full overflow-hidden bg-gray-100 border-4 border-white shadow-lg">
            <img :src="resettingUser.avatar_url" alt="Current" class="w-full h-full object-cover" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Select New Image</label>
          <input
            type="file"
            accept="image/*"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm"
            @change="handleAdminAvatarUpload"
          />
          <p class="text-xs text-gray-400 mt-1">Max 5MB · JPG, PNG, GIF, WebP</p>
        </div>

        <div v-if="uploadingAvatar" class="text-center text-sm text-blue-600">
          ⏳ Uploading...
        </div>
      </div>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { usersApi } from '@/api/users'
import { useToast } from '@/composables/useToast'
import { formatDate } from '@/utils/formatters'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import Loader from '@/components/common/Loader.vue'

const toast = useToast()

const users = ref([])
const loading = ref(true)
const saving = ref(false)
const showForm = ref(false)
const showDelete = ref(false)
const editing = ref(null)
const deleting = ref(null)
const error = ref('')

// Admin password reset
const showPasswordReset = ref(false)
const resettingUser = ref(null)
const newPassword = ref('')
const resettingPassword = ref(false)

// Admin avatar upload
const showAvatarUpload = ref(false)
const uploadingAvatar = ref(false)

const form = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
  role: 'viewer',
  is_active: true,
})

const activeCount = computed(() => users.value.filter((u) => u.is_active).length)

function countBy(role) {
  return users.value.filter((u) => u.role === role).length
}

function roleIcon(role) {
  return { admin: '🔴', engineer: '🟠', noc: '🟡', viewer: '⚪' }[role] || '⚪'
}

function roleBadge(role) {
  return {
    admin: 'bg-red-100 text-red-700',
    engineer: 'bg-orange-100 text-orange-700',
    noc: 'bg-yellow-100 text-yellow-700',
    viewer: 'bg-gray-100 text-gray-700',
  }[role] || 'bg-gray-100 text-gray-700'
}

onMounted(loadUsers)

async function loadUsers() {
  loading.value = true
  try {
    const { data } = await usersApi.list()
    users.value = data
  } catch (e) {
    toast.error('Failed to load users')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editing.value = null
  Object.assign(form, {
    username: '',
    email: '',
    full_name: '',
    password: '',
    role: 'viewer',
    is_active: true,
  })
  error.value = ''
  showForm.value = true
}

function openEdit(user) {
  editing.value = user
  Object.assign(form, {
    username: user.username,
    email: user.email,
    full_name: user.full_name || '',
    password: '',
    role: user.role,
    is_active: user.is_active,
  })
  error.value = ''
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editing.value = null
  error.value = ''
}

async function handleSubmit() {
  error.value = ''
  saving.value = true
  try {
    if (editing.value) {
      const payload = {
        email: form.email,
        full_name: form.full_name || null,
        role: form.role,
        is_active: form.is_active,
      }
      await usersApi.update(editing.value.id, payload)
      toast.success('User updated')
    } else {
      await usersApi.create({
        username: form.username,
        email: form.email,
        full_name: form.full_name || null,
        password: form.password,
        role: form.role,
      })
      toast.success('User created')
    }
    closeForm()
    await loadUsers()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Save failed'
  } finally {
    saving.value = false
  }
}

function confirmDelete(user) {
  deleting.value = user
  showDelete.value = true
}

async function handleDelete() {
  if (!deleting.value) return
  try {
    await usersApi.remove(deleting.value.id)
    toast.success('User deleted')
    await loadUsers()
  } catch (e) {
    toast.error('Delete failed: ' + (e.response?.data?.detail || e.message))
  } finally {
    deleting.value = null
    showDelete.value = false
  }
}

// ───── ADMIN: RESET PASSWORD ─────

function openPasswordReset(user) {
  resettingUser.value = user
  newPassword.value = ''
  showPasswordReset.value = true
}

function generateRandomPassword() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'
  let pwd = ''
  for (let i = 0; i < 10; i++) {
    pwd += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  newPassword.value = pwd
}

async function handleAdminPasswordReset() {
  if (newPassword.value.length < 6) {
    toast.error('Password must be at least 6 characters')
    return
  }
  resettingPassword.value = true
  try {
    await usersApi.adminResetPassword(resettingUser.value.id, newPassword.value)
    toast.success(`Password reset for ${resettingUser.value.username}`)
    // Show the password for admin to note
    setTimeout(() => {
      toast.info(`New password: ${newPassword.value}`)
    }, 500)
    showPasswordReset.value = false
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Failed to reset password')
  } finally {
    resettingPassword.value = false
  }
}

// ───── ADMIN: UPLOAD AVATAR ─────

function openAvatarUpload(user) {
  resettingUser.value = user
  showAvatarUpload.value = true
}

async function handleAdminAvatarUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return

  if (file.size > 5 * 1024 * 1024) {
    toast.error('File too large. Max 5MB.')
    return
  }

  uploadingAvatar.value = true
  try {
    await usersApi.adminUploadAvatar(resettingUser.value.id, file)
    toast.success(`Avatar updated for ${resettingUser.value.username}`)
    showAvatarUpload.value = false
    await loadUsers()
  } catch (e) {
    toast.error(e.response?.data?.detail || 'Upload failed')
  } finally {
    uploadingAvatar.value = false
    event.target.value = ''
  }
}
</script>