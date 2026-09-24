import api from './axios'

export const ipamApi = {
  // Subnets
  listSubnets: () => api.get('/ipam/subnets'),
  createSubnet: (payload) => api.post('/ipam/subnets', payload),
  updateSubnet: (id, payload) => api.patch(`/ipam/subnets/${id}`, payload),
  deleteSubnet: (id) => api.delete(`/ipam/subnets/${id}`),
  generateIps: (id) => api.post(`/ipam/subnets/${id}/generate-ips`),

  // IPs
  listIps: () => api.get('/ipam/ips'),
  listSubnetIps: (subnetId) => api.get(`/ipam/subnets/${subnetId}/ips`),
  updateIp: (id, payload) => api.patch(`/ipam/ips/${id}`, payload),

  // Calculator
  calculate: (ip, cidr) =>
    api.post('/ipam/subnet-calculator', { ip, cidr }),
}