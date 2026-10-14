\# Research Question



\## Main Question

Can an adaptive polling algorithm reduce the mean detection delay and 

false-positive alert rate for network device failures compared to 

traditional fixed-interval monitoring, while maintaining monitoring 

overhead within acceptable bounds?



\## Sub-Questions

1\. \*\*Detection Delay:\*\* How quickly can the system declare a device DOWN after actual failure onset?

2\. \*\*False Alarms:\*\* How many alerts are generated when the device is actually UP?

3\. \*\*Monitoring Overhead:\*\* How many total probes are sent per device per minute?



\## Scope

\- Target: Small-medium networks (10-500 devices)

\- Protocol: ICMP ping-based monitoring

\- Environment: Simulated testbed + real devices



\## Out of Scope

\- SNMP-based monitoring (future work)

\- Multi-vendor device compatibility

\- Production-scale deployment (>1000 devices)



\## Acceptance Criteria (Initial)

\- Detection delay: Mean should not increase by more than 2 seconds compared to baseline

\- False alarms: Reduce by at least 30%

\- Monitoring overhead: Reduce by at least 20%

\- Recovery detection: Must detect device recovery within 10 seconds

