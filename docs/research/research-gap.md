\# Research Gap Analysis



\## What is Already Known



\### 1. Fixed-Interval Monitoring (Traditional)

\- \*\*Approach:\*\* Ping every N seconds (e.g., 5s or 60s)

\- \*\*Down detection:\*\* M consecutive failures (e.g., 3)

\- \*\*Recovery detection:\*\* 1 success

\- \*\*Pros:\*\* Simple, predictable

\- \*\*Cons:\*\* High overhead, fixed delay, false alarms during transient loss



\### 2. Adaptive Polling (Modern)

\- \*\*Approach:\*\* Adjust polling interval based on device health

\- \*\*Down detection:\*\* Variable threshold

\- \*\*Pros:\*\* Lower overhead

\- \*\*Cons:\*\* Complex, still false alarms



\### 3. Confirmation Logic (Industry)

\- \*\*Approach:\*\* Multiple confirmations before declaring DOWN/UP

\- \*\*Down detection:\*\* Consecutive failures + cooldown

\- \*\*Pros:\*\* Fewer false alarms

\- \*\*Cons:\*\* Higher detection delay



\### 4. Prometheus Alerting (Industry Standard)

\- \*\*Approach:\*\* Alert rules + grouping + cooldown

\- \*\*Focus:\*\* Reduce alert noise, not failure detection

\- \*\*Reference:\*\* https://prometheus.io/docs/practices/alerting/



\---



\## What is NOT Known (Research Gaps)



\### Gap 1: Comprehensive Comparison

\*\*Missing:\*\* Head-to-head comparison of all 3 approaches on the same dataset



\*\*Why important:\*\* Without this, engineers don't know which approach to choose



\*\*Our contribution:\*\* Benchmark all 3 on identical 6 scenarios × 10 repetitions



\---



\### Gap 2: Detection Delay Distribution

\*\*Missing:\*\* Most papers report only mean delay, not distribution



\*\*Why important:\*\* 95th percentile matters more than mean for SLA



\*\*Our contribution:\*\* Report median, 95th percentile, and max delay



\---



\### Gap 3: Confirmation Logic for ICMP

\*\*Missing:\*\* Confirmation logic rarely applied to ICMP-based monitoring



\*\*Why important:\*\* Transient packet loss causes many false alarms



\*\*Our contribution:\*\* Implement adaptive + confirmation and measure false alarm reduction



\---



\### Gap 4: Reproducible Benchmark

\*\*Missing:\*\* No standard benchmark dataset for monitoring algorithms



\*\*Why important:\*\* Research is not reproducible



\*\*Our contribution:\*\* Provide reproducible testbed with ground-truth logs



\---



\### Gap 5: Monitoring Overhead vs Accuracy Trade-off

\*\*Missing:\*\* No clear guidance on acceptable trade-off



\*\*Why important:\*\* Engineers need to know: "How many probes can I reduce?"



\*\*Our contribution:\*\* Map trade-off curve (overhead reduction vs delay increase)



\---



\## Research Gap Summary



\*\*Our research fills 5 gaps:\*\*



1\. ✅ \*\*Comprehensive comparison\*\* — All 3 approaches on same data

2\. ✅ \*\*Distribution metrics\*\* — Median, 95th percentile

3\. ✅ \*\*Confirmation logic\*\* — Applied to ICMP monitoring

4\. ✅ \*\*Reproducible benchmark\*\* — Open-source testbed

5\. ✅ \*\*Trade-off analysis\*\* — Overhead vs accuracy



\*\*Novelty:\*\* Combine adaptive polling + confirmation logic for ICMP-based monitoring and provide comprehensive reproducible benchmark.



\*\*Not claimed:\*\* Not claiming novel algorithm — we're claiming \*\*novel application + comprehensive evaluation\*\*.

