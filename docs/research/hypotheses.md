\# Research Hypotheses



\## H1: Monitoring Overhead Reduction

\*\*Hypothesis:\*\* Adaptive polling will reduce total monitoring probes by at least 20% compared to fixed-interval polling, without increasing the median detection delay by more than 2 seconds.



\*\*Metric:\*\* 

\- Probe count reduction (%)

\- Median detection delay (seconds)



\*\*Acceptance Criteria:\*\*

\- Probe count: ≥ 20% reduction

\- Detection delay: ≤ 2 sec increase



\*\*Test Scenario:\*\* S1 (stable device) + S5 (latency spike)



\---



\## H2: False Alarm Reduction

\*\*Hypothesis:\*\* Adaptive polling with confirmation logic will reduce false alarms by at least 30% compared to fixed-interval polling in scenarios with transient packet loss.



\*\*Metric:\*\*

\- False positive rate (alarms/hour)



\*\*Acceptance Criteria:\*\*

\- False alarms: ≥ 30% reduction



\*\*Test Scenario:\*\* S2 (temporary packet loss)



\---



\## H3: Detection Delay Trade-off

\*\*Hypothesis:\*\* Adaptive+Confirmation will have a slightly higher detection delay (up to 5 seconds) than pure adaptive polling, but will produce significantly fewer false alarms in high-latency environments.



\*\*Metric:\*\*

\- Detection delay (median + 95th percentile)

\- False alarms count

\- Missed failures count



\*\*Acceptance Criteria:\*\*

\- Detection delay: ≤ 5 sec increase

\- False alarms: ≥ 40% reduction

\- Missed failures: No increase



\*\*Test Scenario:\*\* S2 + S3 + S5



\---



\## Null Hypotheses (For Statistical Testing)



\- \*\*H0-1:\*\* No significant difference in probe count between adaptive and fixed (α = 0.05)

\- \*\*H0-2:\*\* No significant difference in false alarm rate (α = 0.05)

\- \*\*H0-3:\*\* No significant difference in detection delay (α = 0.05)

