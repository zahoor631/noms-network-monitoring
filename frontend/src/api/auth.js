import api from './axios'

export const authApi = {
  login: (username, password) => {
    const form = new URLSearchParams()
    form.append('username', username)
    form.append('password', password)
    return api.post('/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },
  me: () => api.get('/auth/me'),

  // Forgot password
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  verifyResetCode: (email, code) =>
    api.post('/auth/verify-reset-code', { email, code }),
  resetPassword: (email, code, newPassword) =>
    api.post('/auth/reset-password', {
      email,
      code,
      new_password: newPassword,
    }),
}