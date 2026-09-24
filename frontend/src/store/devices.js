import { defineStore } from 'pinia'
import { devicesApi } from '@/api/devices'

export const useDevicesStore = defineStore('devices', {
  state: () => ({
    devices: [],
    stats: { total: 0, online: 0, offline: 0, unknown: 0 },
    loading: false,
    filters: { device_type: '', status: '', search: '' },
  }),

  getters: {
    filteredDevices: (state) => state.devices,
    hasDevices: (state) => state.devices.length > 0,
  },

  actions: {
    async fetchAll() {
      this.loading = true
      try {
        const params = {}
        Object.entries(this.filters).forEach(([k, v]) => {
          if (v !== '' && v !== null && v !== undefined) params[k] = v
        })
        const { data } = await devicesApi.list(params)
        this.devices = data
      } catch (e) {
        console.error('Failed to fetch devices:', e)
        throw e
      } finally {
        this.loading = false
      }
    },

    async fetchStats() {
      try {
        const { data } = await devicesApi.stats()
        this.stats = data
      } catch (e) {
        console.error('Failed to fetch stats:', e)
      }
    },

    async create(payload) {
      const { data } = await devicesApi.create(payload)
      this.devices.unshift(data)
      await this.fetchStats()
      return data
    },

    async update(id, payload) {
      const { data } = await devicesApi.update(id, payload)
      const idx = this.devices.findIndex((d) => d.id === id)
      if (idx !== -1) this.devices[idx] = data
      return data
    },

    async remove(id) {
      await devicesApi.remove(id)
      this.devices = this.devices.filter((d) => d.id !== id)
      await this.fetchStats()
    },

    setFilter(key, value) {
      this.filters[key] = value
    },

    resetFilters() {
      this.filters = { device_type: '', status: '', search: '' }
    },
  },
})