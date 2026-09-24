<template>
  <div>
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold">IPAM</h1>
        <p class="text-sm text-gray-500 mt-0.5">
          IP Address Management — subnets, IP allocation aur calculator
        </p>
      </div>
      <button
        v-if="auth.canEdit"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition flex items-center gap-2"
        @click="openSubnetForm()"
      >
        <span>➕</span> Add Subnet
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Total Subnets</p>
        <p class="text-2xl font-bold text-blue-600">{{ subnets.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Total IPs</p>
        <p class="text-2xl font-bold text-gray-800">{{ totalIps }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Used IPs</p>
        <p class="text-2xl font-bold text-red-600">{{ usedIps }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <p class="text-xs text-gray-500">Available</p>
        <p class="text-2xl font-bold text-green-600">{{ availableIps }}</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
      <!-- Subnets List -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-5">
          <h3 class="font-semibold text-gray-800 mb-4">Subnets</h3>

          <div v-if="loading" class="text-center py-8">
            <Loader />
          </div>

          <div v-else-if="!subnets.length" class="text-center py-12 text-gray-400">
            <p class="text-4xl mb-2">🌐</p>
            <p class="font-medium">No subnets yet</p>
            <p class="text-xs mt-1">"Add Subnet" button se shuru karo</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
                <tr>
                  <th class="text-left px-3 py-2 font-medium">Network</th>
                  <th class="text-left px-3 py-2 font-medium">Gateway</th>
                  <th class="text-left px-3 py-2 font-medium">VLAN</th>
                  <th class="text-left px-3 py-2 font-medium">Description</th>
                  <th class="text-right px-3 py-2 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="s in subnets"
                  :key="s.id"
                  class="border-t border-gray-100 hover:bg-gray-50"
                >
                  <td class="px-3 py-2 font-mono text-xs font-medium text-gray-800">
                    {{ s.network }}/{{ s.cidr }}
                  </td>
                  <td class="px-3 py-2 font-mono text-xs text-gray-600">
                    {{ s.gateway || '—' }}
                  </td>
                  <td class="px-3 py-2 text-gray-600">
                    <span v-if="s.vlan" class="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs">
                      {{ s.vlan }}
                    </span>
                    <span v-else>—</span>
                  </td>
                  <td class="px-3 py-2 text-gray-600 text-xs">
                    {{ s.description || '—' }}
                  </td>
                  <td class="px-3 py-2 text-right whitespace-nowrap">
                    <button
                      class="text-green-600 hover:text-green-800 text-xs font-medium mr-2"
                      @click="generateIps(s)"
                    >
                      ⚡ Generate
                    </button>
                    <button
                      class="text-blue-600 hover:text-blue-800 text-xs font-medium mr-2"
                      @click="openSubnetForm(s)"
                    >
                      ✏️
                    </button>
                    <button
                      class="text-red-600 hover:text-red-800 text-xs font-medium"
                      @click="confirmDelete(s)"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Subnet Calculator -->
      <div>
        <SubnetCalculator />
      </div>
    </div>

    <!-- Subnet Form Modal -->
    <BaseModal
      v-model="showSubnetForm"
      :title="editingSubnet ? 'Edit Subnet' : 'Add Subnet'"
    >
      <SubnetForm
        ref="formRef"
        :initial="editingSubnet"
        :submit-label="editingSubnet ? 'Update' : 'Create'"
        @submit="handleSubnetSubmit"
        @cancel="closeSubnetForm"
      />
    </BaseModal>

    <!-- Delete Confirm -->
    <ConfirmDialog
      v-model="showDelete"
      title="Delete Subnet"
      :message="`Kya aap '${deletingSubnet?.network}/${deletingSubnet?.cidr}' delete karna chahte ho? Iske saare IPs bhi delete ho jayenge.`"
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ipamApi } from '@/api/ipam'
import { useAuthStore } from '@/store/auth'
import { useToast } from '@/composables/useToast'
import BaseModal from '@/components/common/BaseModal.vue'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import Loader from '@/components/common/Loader.vue'
import SubnetForm from '@/components/ipam/SubnetForm.vue'
import SubnetCalculator from '@/components/ipam/SubnetCalculator.vue'

const auth = useAuthStore()
const toast = useToast()

const subnets = ref([])
const allIps = ref([])
const loading = ref(false)
const showSubnetForm = ref(false)
const showDelete = ref(false)
const editingSubnet = ref(null)
const deletingSubnet = ref(null)
const formRef = ref(null)

const totalIps = computed(() => allIps.value.length)
const usedIps = computed(() => allIps.value.filter((i) => i.status === 'used').length)
const availableIps = computed(
  () => allIps.value.filter((i) => i.status === 'available').length
)

onMounted(async () => {
  await Promise.all([loadSubnets(), loadIps()])
})

async function loadSubnets() {
  loading.value = true
  try {
    const { data } = await ipamApi.listSubnets()
    subnets.value = data
  } catch (e) {
    toast.error('Failed to load subnets')
  } finally {
    loading.value = false
  }
}

async function loadIps() {
  try {
    const { data } = await ipamApi.listIps()
    allIps.value = data
  } catch (e) {
    console.error(e)
  }
}

function openSubnetForm(subnet = null) {
  editingSubnet.value = subnet ? { ...subnet } : null
  showSubnetForm.value = true
}

function closeSubnetForm() {
  showSubnetForm.value = false
  editingSubnet.value = null
}

async function handleSubnetSubmit(payload) {
  try {
    if (editingSubnet.value) {
      await ipamApi.updateSubnet(editingSubnet.value.id, payload)
      toast.success('Subnet updated')
    } else {
      await ipamApi.createSubnet(payload)
      toast.success('Subnet created')
    }
    closeSubnetForm()
    await loadSubnets()
  } catch (e) {
    const msg = e.response?.data?.detail || 'Save failed'
    formRef.value?.setError(msg)
  }
}

async function generateIps(subnet) {
  try {
    const { data } = await ipamApi.generateIps(subnet.id)
    toast.success(`Generated ${data.generated} IPs for ${subnet.network}/${subnet.cidr}`)
    await loadIps()
  } catch (e) {
    toast.error('Generate failed: ' + (e.response?.data?.detail || e.message))
  }
}

function confirmDelete(subnet) {
  deletingSubnet.value = subnet
  showDelete.value = true
}

async function handleDelete() {
  if (!deletingSubnet.value) return
  try {
    await ipamApi.deleteSubnet(deletingSubnet.value.id)
    toast.success('Subnet deleted')
    await Promise.all([loadSubnets(), loadIps()])
  } catch (e) {
    toast.error('Delete failed')
  } finally {
    deletingSubnet.value = null
    showDelete.value = false
  }
}
</script>