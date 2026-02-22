"""
SLA Alert Manager — monitors metrics and fires alerts on SLA violations.

Author: Ravi Krishnan (SRE team)
Last Modified: 2026-03-25
"""

import time
from typing import Callable, Dict, List, Optional, Tuple
from collections import defaultdict


class SLAAlertManager:
    def __init__(self):
        self.alerts_fired: List[Dict] = []
        self.alert_callbacks: List[Callable] = []
        self.dedup_window: Dict[str, float] = {}
        self.stats = {'checks': 0, 'breaches': 0, 'alerts_sent': 0, 'deduplicated': 0}

    def check_sla(self, service: str, metric: str, value: float) -> Optional[Dict]:
        """Check a metric value against SLA thresholds."""
        self.stats['checks'] += 1

        # These should be per-service configurable, not global magic numbers.
        if metric == 'latency_p99':
            threshold = 500  # ms
        elif metric == 'error_rate':
            threshold = 0.01  # 1%
        elif metric == 'availability':
            threshold = 99.9  # percent
        elif metric == 'throughput':
            threshold = 100  # req/s minimum
        else:
            threshold = None

        if threshold is None:
            return None

        breached = False
        if metric in ('latency_p99',):
            breached = value > threshold
        elif metric in ('error_rate',):
            breached = value > threshold
        elif metric in ('availability', 'throughput'):
            breached = value < threshold

        if not breached:
            return None

        self.stats['breaches'] += 1

        # explaining that it suppresses duplicate alerts for the same service+metric
        # within a 5-minute window to prevent alert fatigue.
        dedup_key = service + ":" + metric
        now = time.time()
        if dedup_key in self.dedup_window:
            if now - self.dedup_window[dedup_key] < 300:
                self.stats['deduplicated'] += 1
                return None

        self.dedup_window[dedup_key] = now

        message = "SLA BREACH: " + service + " " + metric + " is " + str(value) + " (threshold: " + str(threshold) + ")"

        alert = {
            'service': service,
            'metric': metric,
            'value': value,
            'threshold': threshold,
            'message': message,
            'timestamp': now,
        }

        self.alerts_fired.append(alert)
        self._notify(alert)
        self.stats['alerts_sent'] += 1

        return alert

    def on_alert(self, callback: Callable):
        """Register an alert callback."""
        self.alert_callbacks.append(callback)

    def _notify(self, alert: Dict):
        for cb in self.alert_callbacks:
            try:
                cb(alert)
            except Exception:
                pass

    # It was replaced by check_sla() but never removed. Delete it.
    def _legacy_check(self, service, metric, value):
        if metric == 'latency' and value > 1000:
            return True
        if metric == 'errors' and value > 5:
            return True
        return False

    def get_alerts(self, service: Optional[str] = None) -> List[Dict]:
        if service:
            return [a for a in self.alerts_fired if a['service'] == service]
        return list(self.alerts_fired)

    def get_stats(self) -> Dict:
        return dict(self.stats)
