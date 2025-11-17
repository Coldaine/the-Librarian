"""
Tests for MetricsCollector - Application metrics collection.

Tests cover request tracking, validation metrics, ingestion metrics,
and metrics aggregation.
"""

import pytest
import time
from src.api.metrics import MetricsCollector


@pytest.fixture
def metrics():
    """Create fresh MetricsCollector instance."""
    return MetricsCollector()


class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    def test_initialization(self, metrics):
        """Test MetricsCollector initializes correctly."""
        # Then: All counters initialized
        assert len(metrics.request_count) == 0
        assert len(metrics.request_duration) == 0
        assert len(metrics.validation_results) == 0
        assert len(metrics.document_ingestions) == 0
        assert metrics.start_time > 0

    def test_record_request(self, metrics):
        """Test recording API request metrics."""
        # When: Record a request
        metrics.record_request("GET", "/health", 25.5, 200)

        # Then: Request count incremented
        assert metrics.request_count["GET:/health:200"] == 1

        # And: Duration recorded
        assert "GET:/health" in metrics.request_duration
        assert metrics.request_duration["GET:/health"] == [25.5]

    def test_record_multiple_requests_same_endpoint(self, metrics):
        """Test recording multiple requests to same endpoint."""
        # When: Record multiple requests
        metrics.record_request("GET", "/health", 10.0, 200)
        metrics.record_request("GET", "/health", 15.0, 200)
        metrics.record_request("GET", "/health", 20.0, 200)

        # Then: Count aggregated
        assert metrics.request_count["GET:/health:200"] == 3

        # And: All durations recorded
        assert len(metrics.request_duration["GET:/health"]) == 3
        assert metrics.request_duration["GET:/health"] == [10.0, 15.0, 20.0]

    def test_record_requests_different_status_codes(self, metrics):
        """Test recording requests with different status codes."""
        # When: Record requests with different statuses
        metrics.record_request("POST", "/validate", 50.0, 200)
        metrics.record_request("POST", "/validate", 45.0, 400)
        metrics.record_request("POST", "/validate", 55.0, 500)

        # Then: Each status tracked separately
        assert metrics.request_count["POST:/validate:200"] == 1
        assert metrics.request_count["POST:/validate:400"] == 1
        assert metrics.request_count["POST:/validate:500"] == 1

        # And: Durations combined for endpoint
        assert len(metrics.request_duration["POST:/validate"]) == 3

    def test_record_validation(self, metrics):
        """Test recording validation results."""
        # When: Record validations
        metrics.record_validation("approved")
        metrics.record_validation("approved")
        metrics.record_validation("revision_required")

        # Then: Results counted
        assert metrics.validation_results["approved"] == 2
        assert metrics.validation_results["revision_required"] == 1

    def test_record_ingestion(self, metrics):
        """Test recording document ingestions."""
        # When: Record successful ingestions
        metrics.record_ingestion("architecture", success=True)
        metrics.record_ingestion("architecture", success=True)
        metrics.record_ingestion("design", success=True)

        # Then: Ingestions counted
        assert metrics.document_ingestions["architecture:success"] == 2
        assert metrics.document_ingestions["design:success"] == 1

    def test_record_failed_ingestion(self, metrics):
        """Test recording failed ingestions."""
        # When: Record failed ingestions
        metrics.record_ingestion("architecture", success=False)
        metrics.record_ingestion("design", success=False)

        # Then: Failures counted separately
        assert metrics.document_ingestions["architecture:failure"] == 1
        assert metrics.document_ingestions["design:failure"] == 1

    def test_get_metrics_basic(self, metrics):
        """Test getting basic metrics snapshot."""
        # Given: Some recorded metrics
        metrics.record_request("GET", "/health", 10.0, 200)
        metrics.record_validation("approved")
        metrics.record_ingestion("architecture", success=True)

        # When: Get metrics
        snapshot = metrics.get_metrics()

        # Then: All metrics present
        assert "uptime_seconds" in snapshot
        assert "requests" in snapshot
        assert "validations" in snapshot
        assert "ingestions" in snapshot

        # And: Nested structure correct
        assert snapshot["requests"]["by_endpoint"]["GET:/health:200"] == 1
        assert snapshot["validations"]["by_status"]["approved"] == 1
        assert snapshot["ingestions"]["by_type"]["architecture:success"] == 1

    def test_get_metrics_uptime(self, metrics):
        """Test uptime tracking in metrics."""
        # Given: Some time has passed
        time.sleep(0.1)  # 100ms

        # When: Get metrics
        snapshot = metrics.get_metrics()

        # Then: Uptime is positive
        assert snapshot["uptime_seconds"] > 0
        assert snapshot["uptime_seconds"] >= 0.1

    def test_average_duration_calculation(self, metrics):
        """Test average request duration calculation."""
        # Given: Multiple requests with known durations
        metrics.record_request("GET", "/search", 100.0, 200)
        metrics.record_request("GET", "/search", 200.0, 200)
        metrics.record_request("GET", "/search", 300.0, 200)

        # When: Get metrics
        snapshot = metrics.get_metrics()

        # Then: Average calculated correctly
        avg = snapshot["requests"]["avg_duration_ms"]["GET:/search"]
        assert avg == 200.0  # (100 + 200 + 300) / 3

    def test_average_duration_multiple_endpoints(self, metrics):
        """Test average duration for multiple endpoints."""
        # Given: Different endpoints with different durations
        metrics.record_request("GET", "/health", 5.0, 200)
        metrics.record_request("GET", "/health", 15.0, 200)

        metrics.record_request("POST", "/validate", 100.0, 200)
        metrics.record_request("POST", "/validate", 200.0, 200)

        # When: Get metrics
        snapshot = metrics.get_metrics()

        # Then: Each endpoint averaged separately
        assert snapshot["requests"]["avg_duration_ms"]["GET:/health"] == 10.0
        assert snapshot["requests"]["avg_duration_ms"]["POST:/validate"] == 150.0

    def test_average_duration_no_requests(self, metrics):
        """Test average duration when no requests recorded."""
        # When: Get metrics with no requests
        snapshot = metrics.get_metrics()

        # Then: avg_duration_ms is empty dict
        assert snapshot["requests"]["avg_duration_ms"] == {}

    def test_metrics_independence(self):
        """Test that multiple MetricsCollector instances are independent."""
        # Given: Two separate collectors
        collector1 = MetricsCollector()
        collector2 = MetricsCollector()

        # When: Record to first collector
        collector1.record_request("GET", "/health", 10.0, 200)
        collector1.record_validation("approved")

        # Then: Second collector unaffected
        assert len(collector2.request_count) == 0
        assert len(collector2.validation_results) == 0

    def test_comprehensive_metrics_snapshot(self, metrics):
        """Test comprehensive metrics collection scenario."""
        # Given: Realistic usage pattern
        # API requests
        for i in range(10):
            metrics.record_request("GET", "/health", 5.0 + i, 200)
        for i in range(3):
            metrics.record_request("POST", "/validate", 100.0 + i * 10, 200)
        metrics.record_request("POST", "/validate", 150.0, 400)

        # Validations
        for _ in range(7):
            metrics.record_validation("approved")
        for _ in range(2):
            metrics.record_validation("revision_required")
        metrics.record_validation("rejected")

        # Ingestions
        for _ in range(5):
            metrics.record_ingestion("architecture", success=True)
        for _ in range(3):
            metrics.record_ingestion("design", success=True)
        metrics.record_ingestion("architecture", success=False)

        # When: Get comprehensive snapshot
        snapshot = metrics.get_metrics()

        # Then: All metrics accurately captured
        # Requests
        assert snapshot["requests"]["by_endpoint"]["GET:/health:200"] == 10
        assert snapshot["requests"]["by_endpoint"]["POST:/validate:200"] == 3
        assert snapshot["requests"]["by_endpoint"]["POST:/validate:400"] == 1

        # Durations
        assert snapshot["requests"]["avg_duration_ms"]["GET:/health"] == 9.5  # (5+6+...+14) / 10
        expected_validate_avg = (100 + 110 + 120 + 150) / 4
        assert snapshot["requests"]["avg_duration_ms"]["POST:/validate"] == expected_validate_avg

        # Validations
        assert snapshot["validations"]["by_status"]["approved"] == 7
        assert snapshot["validations"]["by_status"]["revision_required"] == 2
        assert snapshot["validations"]["by_status"]["rejected"] == 1

        # Ingestions
        assert snapshot["ingestions"]["by_type"]["architecture:success"] == 5
        assert snapshot["ingestions"]["by_type"]["design:success"] == 3
        assert snapshot["ingestions"]["by_type"]["architecture:failure"] == 1

    def test_edge_case_zero_duration(self, metrics):
        """Test handling of zero duration requests."""
        # When: Record request with 0ms duration
        metrics.record_request("GET", "/instant", 0.0, 200)

        # Then: Recorded correctly
        snapshot = metrics.get_metrics()
        assert snapshot["requests"]["avg_duration_ms"]["GET:/instant"] == 0.0

    def test_edge_case_very_large_duration(self, metrics):
        """Test handling of very large durations."""
        # When: Record request with very large duration
        metrics.record_request("GET", "/slow", 99999.99, 200)

        # Then: Recorded correctly
        snapshot = metrics.get_metrics()
        assert snapshot["requests"]["avg_duration_ms"]["GET:/slow"] == 99999.99

    def test_special_characters_in_path(self, metrics):
        """Test handling of special characters in request paths."""
        # When: Record requests with special characters
        metrics.record_request("GET", "/search?q=test&limit=10", 50.0, 200)
        metrics.record_request("POST", "/docs/ARCH-001", 75.0, 201)

        # Then: Recorded correctly
        snapshot = metrics.get_metrics()
        assert snapshot["requests"]["by_endpoint"]["GET:/search?q=test&limit=10:200"] == 1
        assert snapshot["requests"]["by_endpoint"]["POST:/docs/ARCH-001:201"] == 1
