export function authGuard(to, from, next) {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  // Public routes
  if (to.meta.public) {
    // If logged in and going to login, redirect home
    if (to.path === '/login' && token) {
      return next('/')
    }
    return next()
  }

  // Auth required
  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  // Role check
  if (to.meta.roles && user && !to.meta.roles.includes(user.role)) {
    return next('/')
  }

  next()
}