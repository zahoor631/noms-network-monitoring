import api from './axios'

export const alertsApi = {
  list: (params) => api.get('/alerts/', { params }),
  create: (payload) => api.post('/alerts/', payload),
  resolve: (id) => api.post(`/alerts/${id}/resolve`),
}