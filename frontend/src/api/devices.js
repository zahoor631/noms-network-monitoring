import api from './axios'

export const devicesApi = {
  list: (params) => api.get('/devices/', { params }),
  stats: () => api.get('/devices/stats'),
  get: (id) => api.get(`/devices/${id}`),
  create: (payload) => api.post('/devices/', payload),
  update: (id, payload) => api.patch(`/devices/${id}`, payload),
  remove: (id) => api.delete(`/devices/${id}`),
}