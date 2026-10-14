\# Comparison: Fixed vs Adaptive vs Adaptive+Confirmation



| Aspect | A: Fixed Interval | B: Adaptive Polling | C: Adaptive + Confirmation |

|---|---|---|---|

| \*\*Polling Interval\*\* | Always 5 seconds | Dynamic: 5-30 seconds | Dynamic: 5-30 seconds |

| \*\*When device stable\*\* | 5 sec (high overhead) | 30 sec (low overhead) | 30 sec (low overhead) |

| \*\*When latency spike\*\* | 5 sec (delayed detection) | 5 sec (fast detection) | 5 sec (fast detection) |

| \*\*DOWN declaration\*\* | 3 consecutive failures | 3 consecutive failures | 3 failures + cooldown |

| \*\*RECOVERY detection\*\* | 1 successful ping | 1 successful ping | 2 consecutive successes |

| \*\*Alert cooldown\*\* | None | None | 60 seconds |

| \*\*False alarms (transient)\*\* | High | Medium | Low |

| \*\*Detection delay\*\* | Fixed (3 × 5 = 15 sec) | Variable (5-15 sec) | Variable (5-20 sec) |

| \*\*Monitoring overhead\*\* | High | Low | Low |

| \*\*Complexity\*\* | Simple | Medium | High |

| \*\*Best for\*\* | Small networks | Medium networks | Enterprise NOC |



\## Reference

\- Prometheus Alerting Best Practices: https://prometheus.io/docs/practices/alerting/

\- Cisco Network Monitoring Guidelines

\- IEEE 802.3 Ethernet Standards

