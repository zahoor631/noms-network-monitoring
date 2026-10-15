\# Problem Statement



\## Background



Network Operations Centers (NOCs) monitor hundreds to thousands of network 

devices (routers, switches, servers) to detect failures and minimize downtime. 

Traditional monitoring uses \*\*fixed-interval polling\*\* — pinging every device 

at a constant interval (e.g., every 5 or 60 seconds).



\## The Problem



Fixed-interval polling faces a \*\*fundamental trade-off\*\*:



\### High-Frequency Polling (e.g., 5 seconds)

\- ✅ \*\*Fast detection\*\* — Device failure detected in \~15 seconds

\- ✅ \*\*Good for critical devices\*\*

\- ❌ \*\*High overhead\*\* — 12 probes per device per minute

\- ❌ \*\*False alarms\*\* — Transient packet loss causes alerts

\- ❌ \*\*Scales poorly\*\* — 500 devices × 12 probes = 6000 probes/minute



\### Low-Frequency Polling (e.g., 60 seconds)

\- ✅ \*\*Low overhead\*\* — 1 probe per device per minute

\- ✅ \*\*Good for non-critical devices\*\*

\- ❌ \*\*Slow detection\*\* — Device failure detected in \~3 minutes

\- ❌ \*\*SLA violations\*\* — Customers notice before NOC does



\## The Research Question



\*\*Can adaptive polling with confirmation logic reduce detection delay AND 

false alarm rate, while keeping monitoring overhead acceptable?\*\*



Specifically:

\- Can we achieve \*\*fast detection\*\* (like high-frequency polling) with \*\*low overhead\*\* (like low-frequency polling)?

\- Can we reduce \*\*false alarms\*\* by using \*\*confirmation logic\*\*?

\- What are the \*\*trade-offs\*\* between overhead, delay, and accuracy?



\## Why It Matters



1\. \*\*Cost Reduction\*\* — Fewer probes = less network traffic + less CPU usage

2\. \*\*Better SLA\*\* — Faster detection = fewer customer complaints

3\. \*\*Fewer False Alarms\*\* — NOC engineers trust alerts more

4\. \*\*Scalability\*\* — Support more devices with same infrastructure



\## Our Approach



We propose to compare \*\*three monitoring approaches\*\* on a \*\*reproducible benchmark\*\*:



1\. \*\*Baseline:\*\* Fixed-interval polling (5 seconds, 3 failures = DOWN)

2\. \*\*Adaptive:\*\* Dynamic polling (5-30 seconds based on device health)

3\. \*\*Adaptive + Confirmation:\*\* Adaptive + cooldown + confirmation logic



\*\*Evaluation:\*\* 6 scenarios × 10 repetitions = 60 test runs



\*\*Metrics:\*\* Detection delay (median, p95), false alarms, missed failures, 

monitoring overhead (probes/device/minute)



\## Expected Contributions



1\. \*\*Comprehensive comparison\*\* of 3 approaches

2\. \*\*Reproducible benchmark\*\* with ground-truth data

3\. \*\*Trade-off analysis\*\* (overhead vs delay)

4\. \*\*Practical guidance\*\* for NOC engineers

5\. \*\*Research paper draft\*\* for publication



\## Scope



\- \*\*In scope:\*\* ICMP-based monitoring, 10-500 devices, small-medium networks

\- \*\*Out of scope:\*\* SNMP, distributed systems, enterprise (>1000 devices), mobile devices



\## Limitations



1\. \*\*Simulated testbed\*\* — Not tested on real production network

2\. \*\*ICMP only\*\* — No SNMP polling

3\. \*\*Single monitoring host\*\* — No distributed monitoring

4\. \*\*English/Urdu reports only\*\* — No multi-language support



\## Timeline



\*\*Day 1-5:\*\* Research foundation  

\*\*Day 6-10:\*\* Testbed design  

\*\*Day 11-16:\*\* Algorithm implementation  

\*\*Day 17-22:\*\* Experiments  

\*\*Day 23-26:\*\* Analysis  

\*\*Day 27-30:\*\* Research paper



\## References



1\. Chandra, T., \& Toueg, S. (1996). Unreliable Failure Detectors for Reliable Distributed Systems.

2\. Prometheus Team. (2023). Alerting Best Practices.

3\. \[Additional references from literature matrix]

