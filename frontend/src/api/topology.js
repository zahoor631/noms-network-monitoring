import api from './axios'

export const topologyApi = {
  get: () => api.get('/topology/'),
  autoDiscover: () => api.get('/topology/auto-discover'),
}