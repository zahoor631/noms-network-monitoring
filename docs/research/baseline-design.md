\# Baseline Monitoring Design (Fixed-Interval)



\## Overview

Fixed-interval monitoring is the \*\*simplest\*\* approach — poll every device 

at a constant interval. This is our baseline for comparison.



\## Algorithm



```python

def monitor\_fixed\_interval(device, interval=5, failures\_threshold=3):

&#x20;   consecutive\_failures = 0

&#x20;   

&#x20;   while True:

&#x20;       # Ping device

&#x20;       success = ping(device.ip, timeout=2)

&#x20;       

&#x20;       if success:

&#x20;           # Device UP

&#x20;           consecutive\_failures = 0

&#x20;           device.status = "online"

&#x20;       else:

&#x20;           # Probe failed

&#x20;           consecutive\_failures += 1

&#x20;           if consecutive\_failures >= failures\_threshold:

&#x20;               device.status = "offline"

&#x20;               generate\_alert(device)

&#x20;       

&#x20;       # Wait fixed interval

&#x20;       sleep(interval)

