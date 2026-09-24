import api from './axios'

export const ticketsApi = {
  list: (params) => api.get('/tickets/', { params }),
  get: (id) => api.get(`/tickets/${id}`),
  create: (payload) => api.post('/tickets/', payload),
  update: (id, payload) => api.patch(`/tickets/${id}`, payload),
}