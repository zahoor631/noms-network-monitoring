<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">Devices</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          Network devices manage karo — routers, switches, servers, etc.
        </p>
      </div>
      <button
        v-if="auth.canEdit"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
        @click="openCreate"
      >
        <span>➕</span> Add Device
      </button>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      <StatCard title="Total" :value="stats.total" color="blue" icon="🖥️" />
      <StatCard title="Online" :value="stats.online" color="green" icon="🟢" />
      <StatCard title="Offline" :value="stats.offline" color="red" icon="🔴" />
      <StatCard title="Unknown" :value="stats.unknown" color="gray" icon="❓" />
    </div>

    <DeviceFilter
      :filters="store.filters"
      @update:search="onFilter('search', $event)"
      @update:type="onFilter('device_type', $event)"
      @update:status="onFilter('status', $event)"
      @reset="onResetFilters"
    />

    <Loader v-if="store.loading" />

    <DeviceTable
      v-else
      :devices="store.devices"
      :has-filters="hasFilters"
      @edit="openEdit"
      @delete="openDelete"
    />

    <BaseModal
      v-model="showForm"
      :title="editing ? 'Edit Device' : 'Add New Device'"
    >
      <DeviceForm
        ref="formRef"
        :initial="editing"
        :submit-label="editing ? 'Update' : 'Create'"
        @submit="handleSubmit"
        @cancel="closeForm"
      />
    </BaseModal>

    <ConfirmDialog
      v-model="showDelete"
      title="Delete Device"
      :message="`Kya aap '${deleting?.hostname}' ko delete karna chahte ho?`"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useDevicesStore } from '@/store/devices'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import StatCard from '@/components/dashboard/StatCard.vue'
import DeviceFilter from '@/components/devices/DeviceFilter.vue'
import DeviceTable from '@/components/devices/DeviceTable.vue'
import DeviceForm from '@/components/devices/DeviceForm.vue'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import Loader from '@/components/common/Loader.vue'

const store = useDevicesStore()
const auth = useAuthStore()
const toast = useToast()

// ✅ Reactive stats — use storeToRefs directly
const stats = computed(() => store.stats)

const showForm = ref(false)
const showDelete = ref(false)
const editing = ref(null)
const deleting = ref(null)
const formRef = ref(null)

const hasFilters = computed(
  () => store.filters.search || store.filters.device_type || store.filters.status
)

onMounted(async () => {
  await Promise.all([store.fetchAll(), store.fetchStats()])
})

// Watch filters (debounced)
let timer = null
watch(
  () => ({ ...store.filters }),
  () => {
    clearTimeout(timer)
    timer = setTimeout(() => store.fetchAll(), 300)
  },
  { deep: true }
)

function onFilter(key, value) {
  store.setFilter(key, value)
}

function onResetFilters() {
  store.resetFilters()
  store.fetchAll()
}

function openCreate() {
  editing.value = null
  showForm.value = true
}

function openEdit(device) {
  editing.value = { ...device }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editing.value = null
}

async function handleSubmit(payload) {
  try {
    if (editing.value) {
      await store.update(editing.value.id, payload)
      toast.success('Device updated successfully')
    } else {
      await store.create(payload)
      toast.success('Device created successfully')
    }
    // ✅ Refresh stats after create/update
    await store.fetchStats()
    closeForm()
  } catch (e) {
    const msg = e.response?.data?.detail || e.message || 'Save failed'
    formRef.value?.setError(msg)
  }
}

function openDelete(device) {
  deleting.value = device
  showDelete.value = true
}

async function handleDelete() {
  if (!deleting.value) return
  try {
    await store.remove(deleting.value.id)
    toast.success('Device deleted')
    // ✅ Refresh stats after delete
    await store.fetchStats()
  } catch (e) {
    toast.error('Delete failed: ' + (e.response?.data?.detail || e.message))
  } finally {
    deleting.value = null
    showDelete.value = false
  }
}
</script>