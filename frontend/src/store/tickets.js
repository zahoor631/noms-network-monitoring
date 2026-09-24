import { defineStore } from 'pinia'
import { ticketsApi } from '@/api/tickets'

export const useTicketsStore = defineStore('tickets', {
  state: () => ({
    tickets: [],
    loading: false,
  }),
  actions: {
    async fetchAll() {
      this.loading = true
      try {
        const { data } = await ticketsApi.list()
        this.tickets = data
      } finally {
        this.loading = false
      }
    },
    async create(payload) {
      const { data } = await ticketsApi.create(payload)
      this.tickets.unshift(data)
      return data
    },
    async update(id, payload) {
      const { data } = await ticketsApi.update(id, payload)
      const idx = this.tickets.findIndex((t) => t.id === id)
      if (idx !== -1) this.tickets[idx] = data
      return data
    },
  },
})