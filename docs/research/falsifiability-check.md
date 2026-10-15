\# Falsifiability \& Scope Check



\## What is Falsifiability?

A hypothesis is falsifiable if there exists an observation that could prove 

it wrong.



\## H1: Overhead Reduction

\*\*Statement:\*\* Adaptive reduces probes by ≥ 20% without increasing median 

detection delay by > 2 sec.



\*\*Falsify if:\*\* Probe reduction < 20%, OR delay increase > 2 sec.



\*\*Falsifiable?\*\* ✅ YES



\## H2: False Alarm Reduction

\*\*Statement:\*\* Adaptive+confirmation reduces false alarms by ≥ 30%.



\*\*Falsify if:\*\* Reduction < 30%.



\*\*Falsifiable?\*\* ✅ YES



\## H3: Trade-off

\*\*Statement:\*\* Adaptive+confirmation has ≤ 5 sec higher delay but ≥ 40% 

fewer false alarms than pure adaptive.



\*\*Falsify if:\*\* Delay diff > 5 sec, OR false alarm reduction < 40%.



\*\*Falsifiable?\*\* ✅ YES



\## What Would Make Us Wrong?



\### Scenario A: Adaptive Doesn't Help

Same overhead, no false alarm reduction.

\*\*Action:\*\* Report honestly — valid negative finding.



\### Scenario B: Confirmation Hurts

>10 sec delay, no false alarm reduction.

\*\*Action:\*\* Report — confirmation not useful for ICMP.



\### Scenario C: Mixed Results

Works for some scenarios, not others.

\*\*Action:\*\* Report scenario-dependent results.



\## Scope



\*\*We claim:\*\*

\- ✅ Comparison on 6 scenarios

\- ✅ Simulated testbed metrics

\- ✅ Reproducible benchmark



\*\*We don't claim:\*\*

\- ❌ "Always better"

\- ❌ "Works on all networks"

\- ❌ "Production-ready"



\## Limitations (Honest)



1\. Simulated testbed

2\. ICMP only

3\. Single host

4\. ≤500 devices

5\. 6 scenarios only

6\. Static thresholds

7\. 10 repetitions



\## Ethics



1\. No fabrication

2\. No cherry-picking

3\. Honest interpretation

4\. Reproducible

5\. Open source



\## Next: Day 6 — Implementation Start

