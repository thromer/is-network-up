"""Tests by ChatGPT"""
import socket
import unittest
from unittest.mock import patch, MagicMock
from is_network_up import Probe, TCPReachabilityProbe

class TestTCPReachabilityProbe(unittest.TestCase):
    @patch("socket.create_connection")
    def test_probe_success(self, mock_create_connection):
        """Test when at least one target is reachable."""
        mock_create_connection.return_value = True  # Simulate successful connection

        probe = TCPReachabilityProbe([("8.8.8.8", 53), ("example.com", 443)])
        status, labels = probe.probe()

        self.assertTrue(status)
        self.assertIn("reachable_host", labels)
        self.assertNotEqual(labels["reachable_host"], "none")

    @patch("socket.create_connection", side_effect=socket.error)
    def test_probe_failure(self, mock_create_connection):
        """Test when all targets are unreachable."""
        probe = TCPReachabilityProbe([("invalid.host", 9999)])
        status, labels = probe.probe()

        self.assertFalse(status)
        self.assertEqual(labels["reachable_host"], "none")


class TestMetricReporter(unittest.TestCase):
    @patch("google.cloud.monitoring_v3.MetricServiceClient")
    def test_report_metric(self, mock_metric_client):
        """Test that MetricReporter correctly calls the Cloud Monitoring API."""
        mock_client_instance = MagicMock()
        mock_metric_client.return_value = mock_client_instance

        class MockProbe(Probe):
            def probe(self) -> Tuple[bool, Dict[str, str]]:
                return True, {"test_label": "value"}

        reporter = MetricReporter("test-project", "custom.googleapis.com/test_metric", MockProbe())
        reporter.report_metric()

        mock_client_instance.create_time_series.assert_called_once()
