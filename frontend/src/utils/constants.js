export const DEVICE_TYPES = [
  { value: 'router', label: 'Router', icon: '📡' },
  { value: 'switch', label: 'Switch', icon: '🔀' },
  { value: 'server', label: 'Server', icon: '🖥️' },
  { value: 'firewall', label: 'Firewall', icon: '🛡️' },
  { value: 'access_point', label: 'Access Point', icon: '📶' },
  { value: 'pc', label: 'PC', icon: '💻' },
]

export const DEVICE_STATUS = [
  { value: 'online', label: 'Online' },
  { value: 'offline', label: 'Offline' },
  { value: 'unknown', label: 'Unknown' },
]

export const TICKET_PRIORITIES = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'critical', label: 'Critical' },
]

export const TICKET_STATUSES = [
  { value: 'open', label: 'Open' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'resolved', label: 'Resolved' },
  { value: 'closed', label: 'Closed' },
]

export const ALERT_SEVERITIES = [
  { value: 'info', label: 'Info' },
  { value: 'warning', label: 'Warning' },
  { value: 'critical', label: 'Critical' },
]

export function getDeviceTypeLabel(value) {
  return DEVICE_TYPES.find((t) => t.value === value)?.label || value
}

export function getDeviceTypeIcon(value) {
  return DEVICE_TYPES.find((t) => t.value === value)?.icon || '📦'
}