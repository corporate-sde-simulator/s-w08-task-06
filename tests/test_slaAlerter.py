"""Tests for SLA breach alerting system."""
import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from slaAlerter import SlaAlerter
from breachDetector import BreachDetector

class TestMain:
    def test_basic(self):
        obj = SlaAlerter()
        assert obj.process({"key": "val"}) is not None
    def test_empty(self):
        obj = SlaAlerter()
        assert obj.process(None) is None
    def test_stats(self):
        obj = SlaAlerter()
        obj.process({"x": 1})
        assert obj.get_stats()["processed"] == 1

class TestSupport:
    def test_basic(self):
        obj = BreachDetector()
        assert obj.process({"key": "val"}) is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
