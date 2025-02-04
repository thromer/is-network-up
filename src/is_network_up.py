from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import time
import socket
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod


class Probe(ABC):
    """Abstract base class for a probe that collects metric data."""

    @abstractmethod
    def probe(self) -> Tuple[bool, Dict[str, str]]:
        """Must be implemented to return (metric value, metadata)."""
        pass


class TCPReachabilityProbe(Probe):
    def __init__(self, targets: List[Tuple[str, int]]):
        """
        Checks if at least one (host, port) pair is reachable via TCP.

        :param targets: List of (host, port) tuples to check.
        """
        self.targets = targets

    def probe(self) -> Tuple[bool, Dict[str, str]]:
        """
        Returns (True, metadata) if any host is reachable, otherwise (False, metadata).
        """
        for host, port in self.targets:
            try:
                with socket.create_connection((host, port), timeout=2):
                    return True, {"reachable_host": host, "reachable_port": str(port)}
            except (socket.timeout, socket.error):
                continue

        return False, {"reachable_host": "none", "reachable_port": "none"}


class MetricReporter:
    def __init__(self, project_id: str, metric_type: str, probe: Probe):
        """
        Reports a binary metric to Google Cloud Monitoring.

        :param project_id: Google Cloud Project ID.
        :param metric_type: Fully qualified metric type (e.g., custom.googleapis.com/binary_status).
        :param probe: A `Probe` instance that provides the metric value.
        """
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{project_id}"
        self.metric_type = metric_type
        self.probe = probe

    def report_metric(self) -> None:
        """Collects data from the probe and sends it to Cloud Monitoring."""
        value, labels = self.probe.probe()

        series = monitoring_v3.TimeSeries()
        series.metric.type = self.metric_type
        series.resource.type = "global"  # Use "global" if not tied to a specific GCP resource
        series.metric.labels.update()  # TODO remove entirely I think (labels)

        point = monitoring_v3.Point()
        point.value.bool_value = value

        timestamp = Timestamp()
        timestamp.FromSeconds(int(time.time()))
        point.interval.end_time = timestamp

        series.points.append(point)

        self.client.create_time_series(name=self.project_name, time_series=[series])
        print(f"Metric reported: {value} with labels {labels}")
