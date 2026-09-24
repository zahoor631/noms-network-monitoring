import { defineStore } from 'pinia'
import { ipamApi } from '@/api/ipam'

export const useIpamStore = defineStore('ipam', {
  state: () => ({
    subnets: [],
    ips: [],
    loading: false,
  }),
  actions: {
    async fetchSubnets() {
      this.loading = true
      try {
        const { data } = await ipamApi.listSubnets()
        this.subnets = data
      } finally {
        this.loading = false
      }
    },
    async createSubnet(payload) {
      const { data } = await ipamApi.createSubnet(payload)
      this.subnets.unshift(data)
      return data
    },
    async fetchIPs(subnetId = null) {
      const { data } = subnetId
        ? await ipamApi.listSubnetIps(subnetId)
        : await ipamApi.listIps()
      this.ips = data
    },
  },
})