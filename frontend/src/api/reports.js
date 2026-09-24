import api from './axios'

export const reportsApi = {
  uptime: (days = 1) => api.get('/reports/uptime', { params: { days } }),
  incidents: () => api.get('/reports/incidents'),
  dashboard: () => api.get('/reports/dashboard'),
}