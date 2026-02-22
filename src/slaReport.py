"""
SLA Report — generates SLA compliance reports.

Author: Ravi Krishnan (SRE team)
Last Modified: 2026-03-25
"""

from typing import Dict, List, Optional
from collections import defaultdict


class SLAReport:
    """Generates SLA compliance and breach reports."""

    def __init__(self, alert_manager):
        self.alert_manager = alert_manager

    def generate_summary(self) -> Dict:
        """Generate a summary of SLA compliance."""
        alerts = self.alert_manager.get_alerts()
        stats = self.alert_manager.get_stats()

        by_service = defaultdict(list)
        by_metric = defaultdict(list)

        for alert in alerts:
            by_service[alert['service']].append(alert)
            by_metric[alert['metric']].append(alert)

        return {
            'total_checks': stats['checks'],
            'total_breaches': stats['breaches'],
            'alerts_sent': stats['alerts_sent'],
            'deduplicated': stats['deduplicated'],
            'breach_rate': round(stats['breaches'] / max(stats['checks'], 1) * 100, 2),
            'services_affected': list(by_service.keys()),
            'metrics_breached': list(by_metric.keys()),
            'worst_service': max(by_service.keys(), key=lambda s: len(by_service[s])) if by_service else None,
        }

    def get_service_report(self, service: str) -> Dict:
        """Get detailed SLA report for a specific service."""
        alerts = self.alert_manager.get_alerts(service)
        return {
            'service': service,
            'total_breaches': len(alerts),
            'breaches': alerts,
        }
