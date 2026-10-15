"""
Adaptive + Confirmation Monitor
================================
Adaptive polling + confirmation + cooldown logic.
"""
import time
import subprocess
from datetime import datetime
from typing import Optional, Dict, List
import platform


class AdaptiveConfirmationMonitor:
    def __init__(
        self,
        min_interval: int = 5,
        max_interval: int = 30,
        failure_threshold: int = 3,
        recovery_threshold: int = 2,
        alert_cooldown_sec: int = 60,
        timeout: int = 2,
        latency_threshold: float = 100.0,
    ):
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.failure_threshold = failure_threshold
        self.recovery_threshold = recovery_threshold
        self.alert_cooldown_sec = alert_cooldown_sec
        self.timeout = timeout
        self.latency_threshold = latency_threshold
        
        self.current_interval = max_interval
        self.consecutive_failures = 0
        self.consecutive_successes = 0
        self.current_status = "unknown"
        self.last_alert_time = None
        self.log = []
        self.probe_count = 0
        self.suppressed_alerts = 0
    
    def ping(self, ip: str):
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "1", "-w", str(self.timeout * 1000), ip]
        else:
            cmd = ["ping", "-c", "1", "-W", str(self.timeout), ip]
        
        try:
            start = time.time()
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=self.timeout + 1,
            )
            elapsed_ms = (time.time() - start) * 1000
            
            if result.returncode == 0:
                return True, round(elapsed_ms, 2)
            return False, None
        except Exception:
            return False, None
    
    def can_send_alert(self) -> bool:
        if self.last_alert_time is None:
            return True
        elapsed = (datetime.now() - self.last_alert_time).total_seconds()
        return elapsed >= self.alert_cooldown_sec
    
    def calculate_next_interval(self, success: bool, response_ms: Optional[float]):
        if not success:
            return self.min_interval
        if response_ms and response_ms > self.latency_threshold:
            return self.min_interval
        return min(self.current_interval + 5, self.max_interval)
    
    def probe(self, device_id: str, ip: str) -> Dict:
        self.probe_count += 1
        timestamp = datetime.now().isoformat()
        
        success, response_ms = self.ping(ip)
        
        alert_generated = False
        alert_suppressed = False
        status_changed = False
        previous_status = self.current_status
        previous_interval = self.current_interval
        
        if success:
            self.consecutive_failures = 0
            self.consecutive_successes += 1
            if self.consecutive_successes >= self.recovery_threshold:
                if self.current_status != "online":
                    self.current_status = "online"
                    status_changed = True
        else:
            self.consecutive_failures += 1
            self.consecutive_successes = 0
            if self.consecutive_failures >= self.failure_threshold:
                if self.current_status != "offline":
                    self.current_status = "offline"
                    status_changed = True
                    if self.can_send_alert():
                        alert_generated = True
                        self.last_alert_time = datetime.now()
                    else:
                        alert_suppressed = True
                        self.suppressed_alerts += 1
        
        self.current_interval = self.calculate_next_interval(success, response_ms)
        
        entry = {
            "timestamp": timestamp,
            "device_id": device_id,
            "ip": ip,
            "probe_success": success,
            "response_time_ms": response_ms,
            "consecutive_failures": self.consecutive_failures,
            "consecutive_successes": self.consecutive_successes,
            "status": self.current_status,
            "status_changed": status_changed,
            "previous_status": previous_status,
            "alert_generated": alert_generated,
            "alert_suppressed": alert_suppressed,
            "probe_count": self.probe_count,
            "interval_used": previous_interval,
            "next_interval": self.current_interval,
        }
        
        self.log.append(entry)
        return entry
    
    def run(self, device_id: str, ip: str, duration_sec: int) -> List[Dict]:
        start = time.time()
        entries = []
        while (time.time() - start) < duration_sec:
            entry = self.probe(device_id, ip)
            entries.append(entry)
            time.sleep(self.current_interval)
        return entries
    
    def get_stats(self) -> Dict:
        total = len(self.log)
        successes = sum(1 for e in self.log if e["probe_success"])
        failures = total - successes
        alerts = sum(1 for e in self.log if e["alert_generated"])
        avg_interval = sum(e["interval_used"] for e in self.log) / total if total else 0
        
        return {
            "total_probes": total,
            "successful": successes,
            "failed": failures,
            "success_rate": round(successes / total * 100, 2) if total else 0,
            "alerts": alerts,
            "alerts_suppressed": self.suppressed_alerts,
            "avg_interval_sec": round(avg_interval, 2),
            "duration_sec": sum(e["interval_used"] for e in self.log),
        }