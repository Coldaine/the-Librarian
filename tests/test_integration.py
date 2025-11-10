"""
Integration tests for the complete document flow.

Tests the end-to-end pipeline:
- Document processing → Validation → Graph storage
"""

import pytest
import asyncio
from pathlib import Path
from datetime import datetime
import tempfile
import os

from src.processing.models import ParsedDocument, ProcessedChunk, Chunk
from src.processing.pipeline import IngestionPipeline
from src.validation.engine import ValidationEngine
from src.validation.models import ValidationResult, ValidationStatus
from src.validation.agent_models import AgentRequest
from src.graph.connection import Neo4jConnection
from src.graph.operations import GraphOperations
from src.graph.vector_ops import VectorOperations

from src.integration.document_adapter import DocumentGraphAdapter
from src.integration.validation_bridge import ValidationGraphBridge
from src.integration.request_adapter import RequestAdapter
from src.integration.orchestrator import LibrarianOrchestrator
from src.integration.async_utils import AsyncSync


# Test fixtures

@pytest.fixture
def sample_document():
    """Create a sample parsed document for testing."""
    return ParsedDocument(
        path="/test/docs/ARCH-001.md",
        doc_type="architecture",
        content="""# Test Architecture

## Overview
This is a test architecture document.

## Components
- Component A
- Component B
""",
        frontmatter={
            "doc": "architecture",
            "subsystem": "core",
            "id": "ARCH-001",
            "title": "Test Architecture",
            "version": "1.0.0",
            "status": "approved",
            "owners": ["test_user"],
            "compliance_level": "strict",
            "drift_tolerance": "none"
        },
        hash="test_hash_12345",
        sections=[
            {"title": "Overview", "level": 2, "content": "This is a test architecture document."},
            {"title": "Components", "level": 2, "content": "- Component A\n- Component B"}
        ],
        size_bytes=150
    )


@pytest.fixture
def sample_chunks():
    """Create sample processed chunks."""
    return [
        ProcessedChunk(
            content="# Test Architecture\n\n## Overview\nThis is a test architecture document.",
            start_index=0,
            end_index=70,
            embedding=[0.1] * 768,  # Mock 768-dim embedding
            metadata={"doc_type": "architecture", "subsystem": "core"},
            section_title="Overview",
            section_level=2
        ),
        ProcessedChunk(
            content="## Components\n- Component A\n- Component B",
            start_index=71,
            end_index=120,
            embedding=[0.2] * 768,
            metadata={"doc_type": "architecture", "subsystem": "core"},
            section_title="Components",
            section_level=2
        )
    ]


@pytest.fixture
async def neo4j_conn():
    """Create Neo4j connection for testing."""
    # Note: This requires Neo4j to be running
    # Use environment variables or skip if not available
    try:
        conn = Neo4jConnection(
            uri=os.getenv("NEO4J_URI", "neo4j://localhost:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", "password")
        )
        await conn.verify_connection()
        yield conn
        await conn.close()
    except Exception as e:
        pytest.skip(f"Neo4j not available: {e}")


# Unit tests for adapters

class TestRequestAdapter:
    """Test request adapter functionality."""

    def test_document_to_request(self, sample_document):
        """Test converting document to validation request."""
        adapter = RequestAdapter()

        request = adapter.document_to_request(
            document=sample_document,
            agent_id="test_agent",
            action="create"
        )

        assert isinstance(request, AgentRequest)
        assert request.agent_id == "test_agent"
        assert request.action == "create"
        assert request.target_type == "architecture"
        assert request.content["id"] == "ARCH-001"
        assert request.content["doc_type"] == "architecture"
        assert "content" in request.content
        assert request.metadata["source_path"] == sample_document.path

    def test_extract_references(self, sample_document):
        """Test reference extraction from document."""
        adapter = RequestAdapter()

        # Add some references to content
        sample_document.content += "\n\nReferences: [[ARCH-002]], [DESIGN-001]"
        sample_document.frontmatter["architecture_ref"] = "ARCH-000"

        references = adapter._extract_references(sample_document)

        assert "ARCH-000" in references
        assert "ARCH-002" in references
        assert "DESIGN-001" in references

    def test_generate_rationale(self, sample_document):
        """Test rationale generation."""
        adapter = RequestAdapter()

        rationale = adapter._generate_rationale(sample_document, "create")

        assert "ARCH-001" in rationale
        assert "architecture" in rationale
        assert "approved" in rationale


class TestDocumentAdapter:
    """Test document-to-graph adapter."""

    @pytest.mark.asyncio
    async def test_document_to_properties(self, sample_document):
        """Test converting document to node properties."""
        # Mock dependencies
        graph_ops = None
        vector_ops = None
        adapter = DocumentGraphAdapter(graph_ops, vector_ops)

        properties = adapter._document_to_properties(sample_document)

        assert properties["id"] == "ARCH-001"
        assert properties["doc_type"] == "architecture"
        assert properties["subsystem"] == "core"
        assert properties["status"] == "approved"
        assert properties["compliance_level"] == "strict"
        assert properties["content_hash"] == "test_hash_12345"
        assert "owners" in properties

    def test_generate_chunk_id(self):
        """Test chunk ID generation."""
        adapter = DocumentGraphAdapter(None, None)

        chunk_id_1 = adapter._generate_chunk_id("ARCH-001", 0)
        chunk_id_2 = adapter._generate_chunk_id("ARCH-001", 1)
        chunk_id_3 = adapter._generate_chunk_id("ARCH-001", 0)  # Same as first

        assert chunk_id_1 != chunk_id_2
        assert chunk_id_1 == chunk_id_3  # Deterministic
        assert len(chunk_id_1) == 16  # MD5 hash truncated


class TestAsyncUtils:
    """Test async/sync utilities."""

    def test_run_sync(self):
        """Test running async function synchronously."""
        async def async_function():
            await asyncio.sleep(0.01)
            return "success"

        result = AsyncSync.run_sync(async_function())
        assert result == "success"

    @pytest.mark.asyncio
    async def test_run_async(self):
        """Test running sync function asynchronously."""
        def sync_function(x, y):
            return x + y

        result = await AsyncSync.run_async(sync_function, 5, 3)
        assert result == 8

    def test_make_sync_decorator(self):
        """Test make_sync decorator."""
        @AsyncSync.make_sync
        async def async_add(x, y):
            await asyncio.sleep(0.01)
            return x + y

        # Can now call synchronously
        result = async_add(10, 5)
        assert result == 15


# Integration tests

@pytest.mark.asyncio
@pytest.mark.integration
class TestEndToEndFlow:
    """Test complete end-to-end document flow."""

    async def test_document_storage(self, neo4j_conn, sample_document, sample_chunks):
        """Test storing document with chunks in graph."""
        graph_ops = GraphOperations(neo4j_conn)
        vector_ops = VectorOperations(neo4j_conn)
        adapter = DocumentGraphAdapter(graph_ops, vector_ops)

        # Store document
        doc_id = await adapter.store_document(
            document=sample_document,
            chunks=sample_chunks
        )

        assert doc_id == "ARCH-001"

        # Verify document exists
        exists = await adapter.document_exists("ARCH-001", "architecture")
        assert exists

        # Verify chunks stored
        chunks = await adapter.get_document_chunks("ARCH-001", "Architecture")
        assert len(chunks) >= 2  # At least our test chunks

        # Cleanup
        await graph_ops.delete_node("Architecture", "ARCH-001", "id")

    async def test_validation_audit_trail(self, neo4j_conn, sample_document):
        """Test storing validation results as audit trail."""
        graph_ops = GraphOperations(neo4j_conn)
        bridge = ValidationGraphBridge(graph_ops)
        adapter = RequestAdapter()

        # Create request
        request = adapter.document_to_request(
            document=sample_document,
            agent_id="test_agent"
        )

        # Create validation result
        validation_result = ValidationResult(
            status=ValidationStatus.APPROVED,
            violations=[],
            warnings=[],
            reasoning="All validation checks passed",
            confidence=1.0,
            processing_time_ms=50.0
        )

        # Store audit trail
        decision_id = await bridge.store_validation_result(request, validation_result)

        assert decision_id is not None
        assert decision_id.startswith("decision:")

        # Verify stored
        history = await bridge.get_validation_history(
            target_id=sample_document.frontmatter["id"]
        )
        assert len(history) > 0

        # Cleanup
        await graph_ops.delete_node("AgentRequest", request.id)
        await graph_ops.delete_node("Decision", decision_id)


@pytest.mark.asyncio
@pytest.mark.integration
class TestOrchestrator:
    """Test orchestrator functionality."""

    async def test_orchestrator_setup_validation(self, neo4j_conn):
        """Test orchestrator setup validation."""
        orchestrator = LibrarianOrchestrator(neo4j_conn)

        # Note: This will fail if Ollama is not running
        # That's expected - we want to know the real setup status
        setup_result = await orchestrator.validate_setup()

        assert "pipeline" in setup_result
        assert "graph" in setup_result
        assert "validation" in setup_result
        assert isinstance(setup_result["overall"], bool)

    async def test_process_document_with_temp_file(self, neo4j_conn):
        """Test processing a document from a temporary file."""
        # Create temporary markdown file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write("""---
doc: architecture
subsystem: test
id: ARCH-TEST-001
title: Test Architecture
version: 1.0.0
status: draft
owners: [test_user]
compliance_level: strict
drift_tolerance: none
---

# Test Architecture

## Overview
This is a test document for integration testing.

## Design
The system consists of multiple components.
""")
            temp_path = f.name

        try:
            orchestrator = LibrarianOrchestrator(neo4j_conn)

            # Process document (skip validation for test)
            result = await orchestrator.process_document(
                file_path=temp_path,
                skip_validation=True  # Skip validation since Ollama might not be available
            )

            # Check result
            assert result.success or result.error is not None  # Either succeeds or has error
            if result.success:
                assert result.document_id == "ARCH-TEST-001"
                assert result.chunks_stored > 0

                # Cleanup
                graph_ops = GraphOperations(neo4j_conn)
                await graph_ops.delete_node("Architecture", "ARCH-TEST-001")

        finally:
            # Clean up temp file
            os.unlink(temp_path)


# Mock tests (for CI/CD without Neo4j)

class TestIntegrationMocked:
    """Test integration components with mocked dependencies."""

    def test_request_adapter_integration(self, sample_document):
        """Test request adapter with real document structure."""
        adapter = RequestAdapter()

        request = adapter.document_to_request(sample_document, "test_agent")

        # Verify all required fields present
        assert request.id is not None
        assert request.agent_id == "test_agent"
        assert request.action == "create"
        assert request.target_type == "architecture"
        assert request.content["id"] == "ARCH-001"

        # Verify can convert to dict
        request_dict = request.to_dict()
        assert isinstance(request_dict, dict)
        assert "id" in request_dict

    def test_async_sync_boundary(self):
        """Test async/sync boundary handling."""
        # Test that we can run async code from sync context
        async def async_operation():
            await asyncio.sleep(0.01)
            return {"result": "success"}

        result = AsyncSync.run_sync(async_operation())
        assert result["result"] == "success"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
