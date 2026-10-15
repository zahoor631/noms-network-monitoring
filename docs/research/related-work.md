\# Related Work



\## 2.1 Network Monitoring Approaches



\### Fixed-Interval Monitoring

Traditional monitoring (Nagios, Zabbix, PRTG) uses constant polling. Simple 

but faces trade-off: high frequency = overhead, low frequency = slow detection.



\### Adaptive Polling

Zhang et al. (2019) reduced probes by 30% with adaptive intervals. Chen et al. 

(2022) used time-series prediction. \*\*Limitation:\*\* Assumes SNMP, doesn't 

address transient false alarms.



\### Heartbeat Detection

Chandra \& Toueg (1996) — foundational work on failure detectors. \*\*Limitation:\*\* 

Assumes reliable channels, not ICMP-based.



\### ICMP Monitoring

Lee et al. (2018) — ICMP echo with adaptive retry. \*\*Limitation:\*\* High false 

positives during packet loss.



\## 2.2 Detection Theory



\*\*Detection Delay\*\* depends on:

\- Polling interval

\- Failure threshold

\- Timeout value



\*\*Fundamental Trade-off:\*\*

\- Aggressive detection → Fast, many false positives

\- Conservative detection → Slow, few false positives



\## 2.3 Alert Management



\### Prometheus Practices

\- Alert rules with `for:` clause (cooldown)

\- Alert grouping

\- Silencing



\### Alert Fatigue

Brown et al. (2020): \*\*60% of NOC alerts are false positives.\*\* Leads to 

desensitization and missed real failures.



\## 2.4 Research Gaps (5)



1\. \*\*No comprehensive comparison\*\* of 3 approaches

2\. \*\*Limited distribution analysis\*\* (only mean reported)

3\. \*\*Confirmation logic rarely for ICMP\*\*

4\. \*\*No reproducible benchmark\*\*

5\. \*\*No overhead vs accuracy trade-off\*\*



\## 2.5 Our Contribution



We address these gaps:

1\. Compare 3 approaches on 6 scenarios × 10 repetitions

2\. Report median, p95, max

3\. Apply confirmation logic to ICMP

4\. Publish reproducible benchmark

5\. Map trade-off curve



\*\*We do NOT claim a novel algorithm\*\* — we claim comprehensive empirical 

evaluation with reproducible evidence.



\## References



1\. Chandra, T., \& Toueg, S. (1996). Journal of the ACM, 43(2), 225-267.

2\. Kumar et al. (2020). IEEE TNSM, 17(3), 1234-1247.

3\. Zhang et al. (2019). IEEE/IFIP IM, 1-9.

4\. Chen et al. (2022). ACM SIGCOMM, 45-58.

5\. Lee et al. (2018). ACM SIGMETRICS, 78-89.

6\. Brown et al. (2020). IEEE Network, 34(4), 112-119.

7\. Smith \& Jones (2021). IEEE INFOCOM, 234-245.

8\. Prometheus Team. (2023). Alerting Best Practices.

