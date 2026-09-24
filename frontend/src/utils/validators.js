export function isValidIP(ip) {
  const re = /^(\d{1,3}\.){3}\d{1,3}$/
  if (!re.test(ip)) return false
  return ip.split('.').every((n) => Number(n) >= 0 && Number(n) <= 255)
}

export function isValidMAC(mac) {
  return /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/.test(mac)
}