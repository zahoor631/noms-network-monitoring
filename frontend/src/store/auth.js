import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('token') || null,
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    role: (state) => state.user?.role,
    isAdmin: (state) => state.user?.role === 'admin',
    isEngineer: (state) => state.user?.role === 'engineer',
    canEdit: (state) =>
      state.user?.role === 'admin' || state.user?.role === 'engineer',
  },

  actions: {
    async login(username, password) {
      this.loading = true
      try {
        const { data } = await authApi.login(username, password)
        this.token = data.access_token
        this.user = data.user
        localStorage.setItem('token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        return data
      } finally {
        this.loading = false
      }
    },

    async fetchMe() {
      const { data } = await authApi.me()
      this.user = data
      localStorage.setItem('user', JSON.stringify(data))
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },
})