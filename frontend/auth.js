export function getToken() {
  return localStorage.getItem('token')
}

export function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch (e) {
    return null
  }
}

export function isTokenValid(token) {
  if (!token) return false
  const payload = parseJwt(token)
  if (!payload) return false
  const now = Math.floor(Date.now() / 1000)
  return payload.exp && payload.exp > now
}

export function getUserRole(token) {
  const payload = parseJwt(token)
  return payload?.role || null
}

export function getUserId(token) {
  const payload = parseJwt(token)
  return payload?.sub
}