<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Tickets</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          Incident management — tickets create karo, assign karo, resolve karo
        </p>
      </div>
      <button
        v-if="auth.canEdit"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
        @click="openCreate"
      >
        <span>➕</span> Create Ticket
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Total</p>
        <p class="text-2xl font-bold text-gray-800">{{ tickets.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Open</p>
        <p class="text-2xl font-bold text-orange-600">{{ countBy('open') }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">In Progress</p>
        <p class="text-2xl font-bold text-blue-600">{{ countBy('in_progress') }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Resolved</p>
        <p class="text-2xl font-bold text-green-600">{{ countBy('resolved') }}</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-4 flex flex-wrap items-center gap-3">
      <span class="text-sm text-gray-500 font-medium">Filter:</span>
      <button
        v-for="f in statusFilters"
        :key="f.value"
        :class="statusFilter === f.value ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
        class="px-3 py-1.5 rounded-lg text-xs font-medium transition"
        @click="statusFilter = f.value"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Loading -->
    <Loader v-if="loading" />

    <!-- Empty -->
    <div v-else-if="!filteredTickets.length" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
      <p class="text-5xl mb-3">🎫</p>
      <p class="font-medium text-gray-700">No tickets found</p>
      <p class="text-sm text-gray-500 mt-1">
        {{ statusFilter ? 'Filter clear karo ya naya ticket banao' : '"Create Ticket" button se shuru karo' }}
      </p>
    </div>

    <!-- Table -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
            <tr>
              <th class="text-left px-4 py-3 font-medium">#</th>
              <th class="text-left px-4 py-3 font-medium">Title</th>
              <th class="text-left px-4 py-3 font-medium">Priority</th>
              <th class="text-left px-4 py-3 font-medium">Status</th>
              <th class="text-left px-4 py-3 font-medium">Assigned</th>
              <th class="text-left px-4 py-3 font-medium">Created</th>
              <th class="text-right px-4 py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="t in filteredTickets"
              :key="t.id"
              class="border-t border-gray-100 hover:bg-gray-50"
            >
              <td class="px-4 py-3 font-mono text-xs text-gray-500">#{{ t.id }}</td>
              <td class="px-4 py-3">
                <router-link
                  :to="`/tickets/${t.id}`"
                  class="font-medium text-gray-800 hover:text-blue-600"
                >
                  {{ t.title }}
                </router-link>
                <p v-if="t.description" class="text-xs text-gray-500 mt-0.5 truncate max-w-xs">
                  {{ t.description }}
                </p>
              </td>
              <td class="px-4 py-3">
                <span :class="priorityBadge(t.priority)" class="px-2 py-0.5 rounded text-xs font-medium">
                  {{ priorityIcon(t.priority) }} {{ t.priority }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span :class="statusBadge(t.status)" class="px-2 py-0.5 rounded text-xs font-medium">
                  {{ statusIcon(t.status) }} {{ t.status.replace('_', ' ') }}
                </span>
              </td>
              <td class="px-4 py-3 text-gray-600">
                <span v-if="t.assigned_to" class="text-xs">
                  👤 User #{{ t.assigned_to }}
                </span>
                <span v-else class="text-xs text-gray-400">Unassigned</span>
              </td>
              <td class="px-4 py-3 text-gray-500 text-xs">
                {{ timeAgo(t.created_at) }}
              </td>
              <td class="px-4 py-3 text-right">
                <router-link
                  :to="`/tickets/${t.id}`"
                  class="text-blue-600 hover:text-blue-800 text-xs font-medium"
                >
                  View →
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Modal -->
    <BaseModal v-model="showForm" title="Create Ticket">
      <form @submit.prevent="handleCreate" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Title <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.title"
            type="text"
            required
            placeholder="Router not responding"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              v-model="form.priority"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="low">🟢 Low</option>
              <option value="medium">🟡 Medium</option>
              <option value="high">🟠 High</option>
              <option value="critical">🔴 Critical</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Device</label>
            <select
              v-model.number="form.device_id"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option :value="null">-- None --</option>
              <option v-for="d in devices" :key="d.id" :value="d.id">
                {{ d.hostname }}
              </option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            v-model="form.description"
            rows="3"
            placeholder="Details..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          ></textarea>
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-lg">
          {{ error }}
        </div>

        <div class="flex justify-end gap-2 pt-2 border-t border-gray-100">
          <button
            type="button"
            class="px-4 py-2 text-sm bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition"
            @click="showForm = false"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="saving"
            class="px-4 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition disabled:opacity-50"
          >
            {{ saving ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </form>
    </BaseModal>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ticketsApi } from '@/api/tickets'
import { devicesApi } from '@/api/devices'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import { timeAgo } from '@/composables/useTimeAgo'
import BaseModal from '@/components/common/BaseModal.vue'
import Loader from '@/components/common/Loader.vue'

const auth = useAuthStore()
const toast = useToast()

const tickets = ref([])
const devices = ref([])
const loading = ref(true)
const saving = ref(false)
const showForm = ref(false)
const statusFilter = ref('')
const error = ref('')

const form = reactive({
  title: '',
  description: '',
  priority: 'medium',
  device_id: null,
})

const statusFilters = [
  { value: '', label: 'All' },
  { value: 'open', label: '⚡ Open' },
  { value: 'in_progress', label: '🔧 In Progress' },
  { value: 'resolved', label: '✅ Resolved' },
  { value: 'closed', label: '✕ Closed' },
]

const filteredTickets = computed(() => {
  if (!statusFilter.value) return tickets.value
  return tickets.value.filter((t) => t.status === statusFilter.value)
})

function countBy(status) {
  return tickets.value.filter((t) => t.status === status).length
}

function priorityIcon(p) {
  return { low: '🟢', medium: '🟡', high: '🟠', critical: '🔴' }[p] || '⚪'
}

function priorityBadge(p) {
  return {
    low: 'bg-green-100 text-green-700',
    medium: 'bg-yellow-100 text-yellow-700',
    high: 'bg-orange-100 text-orange-700',
    critical: 'bg-red-100 text-red-700',
  }[p] || 'bg-gray-100 text-gray-700'
}

function statusIcon(s) {
  return {
    open: '⚡',
    in_progress: '🔧',
    resolved: '✅',
    closed: '✕',
  }[s] || '⚪'
}

function statusBadge(s) {
  return {
    open: 'bg-orange-100 text-orange-700',
    in_progress: 'bg-blue-100 text-blue-700',
    resolved: 'bg-green-100 text-green-700',
    closed: 'bg-gray-100 text-gray-700',
  }[s] || 'bg-gray-100 text-gray-700'
}

onMounted(async () => {
  await Promise.all([loadTickets(), loadDevices()])
})

async function loadTickets() {
  loading.value = true
  try {
    const { data } = await ticketsApi.list({})
    tickets.value = data
  } catch (e) {
    toast.error('Failed to load tickets')
  } finally {
    loading.value = false
  }
}

async function loadDevices() {
  try {
    const { data } = await devicesApi.list({})
    devices.value = data
  } catch (e) {
    console.error(e)
  }
}

function openCreate() {
  Object.assign(form, { title: '', description: '', priority: 'medium', device_id: null })
  error.value = ''
  showForm.value = true
}

async function handleCreate() {
  error.value = ''
  saving.value = true
  try {
    const payload = { ...form }
    if (!payload.device_id) delete payload.device_id
    if (!payload.description) delete payload.description
    await ticketsApi.create(payload)
    toast.success('Ticket created')
    showForm.value = false
    await loadTickets()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Create failed'
  } finally {
    saving.value = false
  }
}
</script>