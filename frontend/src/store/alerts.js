import { defineStore } from 'pinia'
import { alertsApi } from '@/api/alerts'

export const useAlertsStore = defineStore('alerts', {
  state: () => ({
    alerts: [],
    loading: false,
  }),
  actions: {
    async fetchAll() {
      this.loading = true
      try {
        const { data } = await alertsApi.list()
        this.alerts = data
      } finally {
        this.loading = false
      }
    },
    async resolve(id) {
      const { data } = await alertsApi.resolve(id)
      const idx = this.alerts.findIndex((a) => a.id === id)
      if (idx !== -1) this.alerts[idx] = data
    },
  },
})