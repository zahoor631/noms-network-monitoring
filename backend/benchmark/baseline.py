"""
Baseline Fixed-Interval Monitoring
====================================
Traditional approach: Ping every device at constant interval.
Declare DOWN after N consecutive failures.
"""
import time
import subprocess
from datetime import datetime
from typing import Optional, Dict, List
import platform


class FixedIntervalMonitor:
    """
    Fixed-interval monitoring engine.
    
    Parameters:
        interval: seconds between probes (default 5)
        failure_threshold: consecutive failures to declare DOWN (default 3)
        timeout: ping timeout in seconds (default 2)
    """
    
    def __init__(
        self,
        interval: int = 5,
        failure_threshold: int = 3,
        timeout: int = 2,
    ):
        self.interval = interval
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.consecutive_failures = 0
        self.current_status = "unknown"
        self.log = []
        self.probe_count = 0
    
    def ping(self, ip: str):
        """
        Send ICMP ping.
        Returns: (success, response_time_ms)
        """
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", str(self.timeout * 1000), ip]
        else:
            cmd = ["ping", "-c", "1", "-W", str(self.timeout), ip]
        
        try:
            start = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 1,
            )
            elapsed_ms = (time.time() - start) * 1000
            
            if result.returncode == 0:
                return True, round(elapsed_ms, 2)
            return False, None
        except Exception:
            return False, None
    
    def probe(self, device_id: str, ip: str) -> Dict:
        """Send one probe and update status."""
        self.probe_count += 1
        timestamp = datetime.now().isoformat()
        
        success, response_ms = self.ping(ip)
        
        alert_generated = False
        status_changed = False
        previous_status = self.current_status
        
        if success:
            self.consecutive_failures = 0
            if self.current_status != "online":
                self.current_status = "online"
                status_changed = True
        else:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.failure_threshold:
                if self.current_status != "offline":
                    self.current_status = "offline"
                    status_changed = True
                    alert_generated = True
        
        entry = {
            "timestamp": timestamp,
            "device_id": device_id,
            "ip": ip,
            "probe_success": success,
            "response_time_ms": response_ms,
            "consecutive_failures": self.consecutive_failures,
            "status": self.current_status,
            "status_changed": status_changed,
            "previous_status": previous_status,
            "alert_generated": alert_generated,
            "probe_count": self.probe_count,
        }
        
        self.log.append(entry)
        return entry
    
    def run(self, device_id: str, ip: str, duration_sec: int) -> List[Dict]:
        """Run monitoring for given duration."""
        start = time.time()
        entries = []
        
        while (time.time() - start) < duration_sec:
            entry = self.probe(device_id, ip)
            entries.append(entry)
            time.sleep(self.interval)
        
        return entries
    
    def get_stats(self) -> Dict:
        """Summary statistics."""
        total = len(self.log)
        successes = sum(1 for e in self.log if e["probe_success"])
        failures = total - successes
        alerts = sum(1 for e in self.log if e["alert_generated"])
        
        return {
            "total_probes": total,
            "successful": successes,
            "failed": failures,
            "success_rate": round(successes / total * 100, 2) if total else 0,
            "alerts": alerts,
            "duration_sec": total * self.interval,
        }