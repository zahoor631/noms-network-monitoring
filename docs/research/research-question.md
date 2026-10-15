\# Research Question (FINAL)



\## Main Question



Can adaptive polling with confirmation logic reduce detection delay and 

false-positive alarm rate for network device failures compared to 

traditional fixed-interval ICMP monitoring, while maintaining monitoring 

overhead within acceptable bounds?



\## Sub-Questions



\*\*SQ1 — Detection Delay:\*\* What is median and 95th-percentile detection delay for each of 3 approaches across 6 failure scenarios?



\*\*SQ2 — False Alarms:\*\* What is the false-positive rate (alarms/hour) for each approach?



\*\*SQ3 — Monitoring Overhead:\*\* What is total probe count per device per minute for each approach?



\*\*SQ4 — Trade-off:\*\* What is the trade-off curve between overhead reduction and delay increase?



\*\*SQ5 — Recovery:\*\* How quickly is device recovery detected?



\*\*SQ6 — Missed Failures:\*\* How many actual failures are missed?



\## Acceptance Criteria



| Metric | Baseline | Adaptive Target | Adaptive+Conf Target |

|---|---|---|---|

| Median detection delay | 15 sec | ≤ 17 sec | ≤ 20 sec |

| 95th percentile delay | 20 sec | ≤ 25 sec | ≤ 30 sec |

| False alarms (per hour) | 10 | ≤ 7 | ≤ 4 |

| Probe count (per min) | 12 | ≤ 9 | ≤ 9 |

| Recovery detection | 5 sec | ≤ 10 sec | ≤ 15 sec |

| Missed failures | 0 | 0 | 0 |



\*(Targets are hypotheses, not proven. Experiments will verify.)\*



\## Hypotheses



\*\*H1:\*\* Adaptive polling reduces probes by ≥ 20% without increasing median detection delay by > 2 sec.



\*\*H2:\*\* Adaptive+confirmation reduces false alarms by ≥ 30%.



\*\*H3:\*\* Adaptive+confirmation has ≤ 5 sec higher delay than pure adaptive, but ≥ 40% fewer false alarms.



\*\*H0 (Null):\*\* No significant difference in any metric (α = 0.05).



\## Scope



\*\*In Scope:\*\*

\- ICMP ping monitoring

\- 10-500 devices

\- 3 approaches

\- 6 scenarios × 10 repetitions



\*\*Out of Scope:\*\*

\- SNMP monitoring

\- Distributed hosts

\- ML-based detection

\- >500 devices



\## Novelty (Cautious)



\*\*We claim:\*\*

\- Comprehensive comparison of 3 approaches

\- Reproducible benchmark

\- Empirical trade-off evidence



\*\*We don't claim:\*\*

\- Novel algorithm

\- Universal superiority

\- Production-ready

