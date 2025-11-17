"""
Tests for API middleware - TimingMiddleware and JSONLoggingMiddleware.

Tests cover request timing, response headers, and structured logging.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.middleware import TimingMiddleware, JSONLoggingMiddleware


@pytest.fixture
def app():
    """Create FastAPI app for testing."""
    app = FastAPI()

    @app.get("/test")
    async def test_endpoint():
        return {"message": "test"}

    @app.get("/slow")
    async def slow_endpoint():
        import time
        time.sleep(0.05)  # 50ms
        return {"message": "slow"}

    return app


class TestTimingMiddleware:
    """Tests for TimingMiddleware."""

    def test_adds_timing_header(self, app):
        """Test that X-Process-Time header is added to responses."""
        # Given: App with timing middleware
        app.add_middleware(TimingMiddleware)
        client = TestClient(app)

        # When: Make request
        response = client.get("/test")

        # Then: Response includes timing header
        assert "X-Process-Time" in response.headers
        assert "ms" in response.headers["X-Process-Time"]

    def test_timing_header_format(self, app):
        """Test that timing header is formatted correctly."""
        # Given: App with timing middleware
        app.add_middleware(TimingMiddleware)
        client = TestClient(app)

        # When: Make request
        response = client.get("/test")

        # Then: Timing header has correct format (e.g., "1.23ms")
        timing = response.headers["X-Process-Time"]
        assert timing.endswith("ms")

        # Extract number
        timing_value = float(timing.replace("ms", ""))
        assert timing_value >= 0

    def test_timing_different_endpoints(self, app):
        """Test timing works for different endpoints."""
        # Given: App with timing middleware
        app.add_middleware(TimingMiddleware)
        client = TestClient(app)

        # When: Make requests to different endpoints
        response1 = client.get("/test")
        response2 = client.get("/slow")

        # Then: Both have timing headers
        assert "X-Process-Time" in response1.headers
        assert "X-Process-Time" in response2.headers

    def test_preserves_response_body(self, app):
        """Test that middleware doesn't modify response body."""
        # Given: App with timing middleware
        app.add_middleware(TimingMiddleware)
        client = TestClient(app)

        # When: Make request
        response = client.get("/test")

        # Then: Response body unchanged
        assert response.json() == {"message": "test"}


class TestJSONLoggingMiddleware:
    """Tests for JSONLoggingMiddleware."""

    @patch('src.api.middleware.logger')
    def test_logs_successful_request(self, mock_logger, app):
        """Test logging of successful requests."""
        # Given: App with JSON logging middleware
        app.add_middleware(JSONLoggingMiddleware)
        client = TestClient(app)

        # When: Make successful request
        response = client.get("/test")

        # Then: Request logged
        assert mock_logger.info.called or mock_logger.debug.called

    def test_middleware_doesnt_modify_response(self, app):
        """Test that logging middleware doesn't modify response."""
        # Given: App with JSON logging middleware
        app.add_middleware(JSONLoggingMiddleware)
        client = TestClient(app)

        # When: Make request
        response = client.get("/test")

        # Then: Response unchanged
        assert response.json() == {"message": "test"}
        assert response.status_code == 200


class TestMiddlewareIntegration:
    """Tests for both middleware working together."""

    @patch('src.api.middleware.logger')
    def test_both_middleware_together(self, mock_logger, app):
        """Test both middleware can work together."""
        # Given: App with both middleware
        app.add_middleware(TimingMiddleware)
        app.add_middleware(JSONLoggingMiddleware)
        client = TestClient(app)

        # When: Make request
        response = client.get("/test")

        # Then: Timing header added
        assert "X-Process-Time" in response.headers

        # And: Response intact
        assert response.json() == {"message": "test"}
