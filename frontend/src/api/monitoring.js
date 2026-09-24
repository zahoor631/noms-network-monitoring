import api from './axios'

export const monitoringApi = {
  pingNow: (deviceId) => api.post(`/monitoring/ping/${deviceId}`),
  pingAll: () => api.post('/monitoring/ping-all'),
  metrics: (deviceId, limit = 100) =>
    api.get(`/monitoring/metrics/${deviceId}`, { params: { limit } }),
}