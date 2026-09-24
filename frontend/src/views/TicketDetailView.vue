<template>
  <div>
    <!-- Header -->
    <div class="flex items-center gap-3 mb-4">
      <router-link to="/tickets" class="text-gray-500 hover:text-gray-700 text-xl">
        ←
      </router-link>
      <div>
        <h1 class="text-2xl font-bold">
          <span class="text-gray-400">#{{ ticket?.id }}</span> {{ ticket?.title }}
        </h1>
        <p class="text-sm text-gray-500 mt-0.5">Ticket detail and management</p>
      </div>
    </div>

    <Loader v-if="loading" />

    <div v-else-if="!ticket" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
      <p class="text-5xl mb-3">🎫</p>
      <p class="font-medium text-gray-700">Ticket not found</p>
      <router-link to="/tickets" class="inline-block mt-4 text-blue-600 hover:underline">
        ← Back to Tickets
      </router-link>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-5">
      <!-- Left: Info + Description -->
      <div class="lg:col-span-2 space-y-5">
        <!-- Info card -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-xs text-gray-500 mb-1">Status</p>
              <span :class="statusBadge(ticket.status)" class="px-2.5 py-1 rounded text-xs font-medium inline-block">
                {{ statusIcon(ticket.status) }} {{ ticket.status.replace('_', ' ') }}
              </span>
            </div>
            <div>
              <p class="text-xs text-gray-500 mb-1">Priority</p>
              <span :class="priorityBadge(ticket.priority)" class="px-2.5 py-1 rounded text-xs font-medium inline-block">
                {{ priorityIcon(ticket.priority) }} {{ ticket.priority }}
              </span>
            </div>
            <div>
              <p class="text-xs text-gray-500 mb-1">Created</p>
              <p class="text-sm text-gray-800">{{ timeAgo(ticket.created_at) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 mb-1">Assigned To</p>
              <p class="text-sm text-gray-800">
                {{ ticket.assigned_to ? `User #${ticket.assigned_to}` : 'Unassigned' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-3">Description</h3>
          <p class="text-sm text-gray-700 whitespace-pre-wrap">
            {{ ticket.description || 'No description provided.' }}
          </p>
        </div>

        <!-- Actions -->
        <div v-if="auth.canEdit" class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-3">Actions</h3>

          <!-- Status change -->
          <div class="mb-4">
            <p class="text-xs text-gray-500 mb-2">Change Status:</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="s in statusOptions"
                :key="s.value"
                :disabled="ticket.status === s.value || updating"
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition disabled:opacity-30"
                :class="statusBtnClass(s.value, ticket.status)"
                @click="changeStatus(s.value)"
              >
                {{ s.icon }} {{ s.label }}
              </button>
            </div>
          </div>

          <!-- Assign -->
          <div class="mb-4">
            <p class="text-xs text-gray-500 mb-2">Assign To:</p>
            <div class="flex gap-2">
              <select
                v-model.number="assignTo"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option :value="null">-- Unassigned --</option>
                <option v-for="u in users" :key="u.id" :value="u.id">
                  {{ u.username }} ({{ u.role }})
                </option>
              </select>
              <button
                :disabled="updating"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50"
                @click="assignUser"
              >
                Save
              </button>
            </div>
          </div>

          <!-- Priority change -->
          <div>
            <p class="text-xs text-gray-500 mb-2">Change Priority:</p>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="p in priorityOptions"
                :key="p.value"
                :disabled="ticket.priority === p.value || updating"
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition disabled:opacity-30"
                :class="priorityBtnClass(p.value, ticket.priority)"
                @click="changePriority(p.value)"
              >
                {{ p.icon }} {{ p.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Timeline -->
      <div>
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-4">📜 Timeline</h3>

          <div class="space-y-4">
            <div class="flex gap-3">
              <div class="w-2 h-2 rounded-full bg-blue-500 mt-2 shrink-0"></div>
              <div>
                <p class="text-sm font-medium text-gray-800">Ticket Created</p>
                <p class="text-xs text-gray-500">{{ timeAgo(ticket.created_at) }}</p>
                <p class="text-xs text-gray-500">by User #{{ ticket.created_by || 'system' }}</p>
              </div>
            </div>

            <div v-if="ticket.updated_at && ticket.updated_at !== ticket.created_at" class="flex gap-3">
              <div class="w-2 h-2 rounded-full bg-yellow-500 mt-2 shrink-0"></div>
              <div>
                <p class="text-sm font-medium text-gray-800">Last Updated</p>
                <p class="text-xs text-gray-500">{{ timeAgo(ticket.updated_at) }}</p>
              </div>
            </div>

            <div v-if="ticket.resolved_at" class="flex gap-3">
              <div class="w-2 h-2 rounded-full bg-green-500 mt-2 shrink-0"></div>
              <div>
                <p class="text-sm font-medium text-gray-800">Resolved</p>
                <p class="text-xs text-gray-500">{{ timeAgo(ticket.resolved_at) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ticketsApi } from '@/api/tickets'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import { timeAgo } from '@/composables/useTimeAgo'
import Loader from '@/components/common/Loader.vue'

const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

const ticket = ref(null)
const users = ref([])
const loading = ref(true)
const updating = ref(false)
const assignTo = ref(null)

const statusOptions = [
  { value: 'open', label: 'Open', icon: '⚡' },
  { value: 'in_progress', label: 'In Progress', icon: '🔧' },
  { value: 'resolved', label: 'Resolved', icon: '✅' },
  { value: 'closed', label: 'Closed', icon: '✕' },
]

const priorityOptions = [
  { value: 'low', label: 'Low', icon: '🟢' },
  { value: 'medium', label: 'Medium', icon: '🟡' },
  { value: 'high', label: 'High', icon: '🟠' },
  { value: 'critical', label: 'Critical', icon: '🔴' },
]

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
  return { open: '⚡', in_progress: '🔧', resolved: '✅', closed: '✕' }[s] || '⚪'
}
function statusBadge(s) {
  return {
    open: 'bg-orange-100 text-orange-700',
    in_progress: 'bg-blue-100 text-blue-700',
    resolved: 'bg-green-100 text-green-700',
    closed: 'bg-gray-100 text-gray-700',
  }[s] || 'bg-gray-100 text-gray-700'
}

function statusBtnClass(value, current) {
  if (value === current) return 'bg-gray-300 text-gray-600'
  return {
    open: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
    in_progress: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
    resolved: 'bg-green-100 text-green-700 hover:bg-green-200',
    closed: 'bg-gray-100 text-gray-700 hover:bg-gray-200',
  }[value]
}

function priorityBtnClass(value, current) {
  if (value === current) return 'bg-gray-300 text-gray-600'
  return {
    low: 'bg-green-100 text-green-700 hover:bg-green-200',
    medium: 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200',
    high: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
    critical: 'bg-red-100 text-red-700 hover:bg-red-200',
  }[value]
}

onMounted(loadTicket)

watch(() => route.params.id, loadTicket)

async function loadTicket() {
  loading.value = true
  try {
    const { data } = await ticketsApi.get(route.params.id)
    ticket.value = data
    assignTo.value = data.assigned_to
  } catch (e) {
    toast.error('Failed to load ticket')
    ticket.value = null
  } finally {
    loading.value = false
  }
}

async function changeStatus(status) {
  updating.value = true
  try {
    const { data } = await ticketsApi.update(ticket.value.id, { status })
    ticket.value = data
    toast.success('Status updated')
  } catch (e) {
    toast.error('Update failed')
  } finally {
    updating.value = false
  }
}

async function changePriority(priority) {
  updating.value = true
  try {
    const { data } = await ticketsApi.update(ticket.value.id, { priority })
    ticket.value = data
    toast.success('Priority updated')
  } catch (e) {
    toast.error('Update failed')
  } finally {
    updating.value = false
  }
}

async function assignUser() {
  updating.value = true
  try {
    const { data } = await ticketsApi.update(ticket.value.id, {
      assigned_to: assignTo.value,
    })
    ticket.value = data
    toast.success('Assigned successfully')
  } catch (e) {
    toast.error('Assign failed')
  } finally {
    updating.value = false
  }
}
</script>