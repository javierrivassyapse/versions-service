Metrics & Telemetry
===================

The service has a simple context manager in :function:`versions_service.metrics.measure`
that allows any block of code to be wrapped and executed.

The context manager will measure runtime and counts for calls, successes, and
errors (categorized by exception type) and reports them to statsd.

.. autofunction:: versions_service.metrics.measure
