#!/usr/bin/env python

from is_network_up import MetricReporter, TCPReachabilityProbe

if __name__ == "__main__":
    PROJECT_ID = "seventh-torch-825"
    METRIC_TYPE = "custom.googleapis.com/binary_status"

    # Define hosts to check
    probe = TCPReachabilityProbe([("8.8.8.8", 53), ("4.4.4.4", 53)])

    # Create metric reporter
    reporter = MetricReporter(PROJECT_ID, METRIC_TYPE, probe)

    # Report the metric
    reporter.report_metric()
