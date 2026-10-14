\# Test Scenarios



\## Scenario S1: Stable Network (Baseline)

\*\*Ground Truth:\*\* Device always reachable

\*\*Duration:\*\* 10 minutes

\*\*Test:\*\* False alarm rate

\*\*Expected:\*\* Zero false alarms

\*\*Parameters:\*\*

\- Latency: 20-30 ms

\- Packet loss: 0%

\- Device status: Always UP



\---



\## Scenario S2: Temporary Packet Loss (Flapping)

\*\*Ground Truth:\*\* 1-2 consecutive pings lost, then recovers

\*\*Duration:\*\* 10 minutes

\*\*Test:\*\* Flapping resistance

\*\*Parameters:\*\*

\- Latency: 20-30 ms

\- Packet loss: Random bursts of 1-2 packets

\- Frequency: Every 2-3 minutes



\---



\## Scenario S3: Short Outage (10 seconds)

\*\*Ground Truth:\*\* Device DOWN for exactly 10 seconds

\*\*Duration:\*\* 5 minutes

\*\*Test:\*\* Detection delay (short outages)

\*\*Parameters:\*\*

\- Downtime: 10 seconds

\- Recovery: Automatic

\- Frequency: Once per test



\---



\## Scenario S4: Sustained Outage (60 seconds)

\*\*Ground Truth:\*\* Device DOWN for 60 seconds

\*\*Duration:\*\* 5 minutes

\*\*Test:\*\* Sustained failure detection

\*\*Parameters:\*\*

\- Downtime: 60 seconds

\- Recovery: Automatic

\- Frequency: Once per test



\---



\## Scenario S5: Latency Spike

\*\*Ground Truth:\*\* Device UP but latency increases 20ms → 500ms

\*\*Duration:\*\* 5 minutes

\*\*Test:\*\* Latency spike handling

\*\*Parameters:\*\*

\- Baseline latency: 20 ms

\- Spike latency: 500 ms

\- Duration: 2 minutes of spike



\---



\## Scenario S6: Device Down → Up (Recovery)

\*\*Ground Truth:\*\* Device DOWN for 30s, then recovers

\*\*Duration:\*\* 5 minutes

\*\*Test:\*\* Recovery detection

\*\*Parameters:\*\*

\- Downtime: 30 seconds

\- Recovery: Automatic

\- Detection window: 10 seconds after recovery



\---



\## Test Execution Plan



Each scenario runs 10 times:

\- \*\*Total runs:\*\* 6 scenarios × 10 repetitions = 60 test runs

\- \*\*Total time:\*\* \~30 hours of experiments

\- \*\*Data collected:\*\* Raw CSV logs per run



\## Ground Truth Logging



Each scenario has a separate ground truth file:

\- `s1\_ground\_truth.csv` — device always UP

\- `s2\_ground\_truth.csv` — transient packet loss events

\- ... etc.



\*\*Ground truth vs Monitoring output\*\* compare karenge.

