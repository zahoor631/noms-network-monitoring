import api from './axios'

export const usersApi = {
  list: () => api.get('/users/'),
  get: (id) => api.get(`/users/${id}`),
  create: (payload) => api.post('/users/', payload),
  update: (id, payload) => api.patch(`/users/${id}`, payload),
  remove: (id) => api.delete(`/users/${id}`),

  // Current user
  updateMe: (payload) => api.patch('/users/me', payload),
  uploadAvatar: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/users/me/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  deleteAvatar: () => api.delete('/users/me/avatar'),

  // Admin actions
  adminResetPassword: (userId, newPassword) =>
    api.post(`/users/${userId}/reset-password`, { new_password: newPassword }),
  adminUploadAvatar: (userId, file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/users/${userId}/avatar`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}