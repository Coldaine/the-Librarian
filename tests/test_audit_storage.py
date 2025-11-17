"""
Tests for GraphAuditStorage - Neo4j-backed audit trail persistence.

Tests cover audit record storage, retrieval, querying, and statistics.
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any

from src.integration.audit_storage import GraphAuditStorage
from src.graph.operations import GraphOperations
from src.graph.schema import NodeLabels


@pytest.fixture
async def audit_storage(graph_ops):
    """Create GraphAuditStorage instance."""
    return GraphAuditStorage(graph_ops)


@pytest.fixture
def sample_audit_record() -> Dict[str, Any]:
    """Create sample audit record."""
    return {
        "id": "audit_test_001",
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "validation",
        "request_id": "req_001",
        "agent_id": "agent_001",
        "target_id": "ARCH-001",
        "target_type": "Architecture",
        "decision": "approved",
        "result": {
            "status": "approved",
            "violations": [],
            "passed": True,
            "confidence": 0.95
        },
        "metadata": {
            "processing_time_ms": 150.5,
            "rule_count": 5,
            "file_path": "/docs/architecture.md"
        }
    }


@pytest.fixture
def sample_validation_record() -> Dict[str, Any]:
    """Create sample validation audit record."""
    return {
        "id": "audit_val_001",
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "validation",
        "request_id": "req_val_001",
        "agent_id": "validator_agent",
        "decision": "revision_required",
        "result": {
            "status": "revision_required",
            "violations": [
                {
                    "code": "DOC-001",
                    "message": "Missing required field: version",
                    "severity": "critical"
                }
            ],
            "passed": False
        },
        "metadata": {
            "processing_time_ms": 85.2
        }
    }


class TestGraphAuditStorage:
    """Tests for GraphAuditStorage class."""

    @pytest.mark.asyncio
    async def test_store_audit_record(self, audit_storage, sample_audit_record, cleanup_test_nodes):
        """Test storing a basic audit record."""
        # When: Store audit record
        audit_id = await audit_storage.store_audit_record(sample_audit_record)

        # Register for cleanup
        cleanup_test_nodes.append(("AuditEvent", audit_id))

        # Then: Record stored successfully
        assert audit_id is not None
        assert isinstance(audit_id, str)

    @pytest.mark.asyncio
    async def test_store_audit_record_with_target(
        self,
        audit_storage,
        sample_audit_record,
        architecture_node_factory,
        cleanup_test_nodes
    ):
        """Test storing audit record with target node relationship."""
        # Given: Target architecture node exists
        arch_node = await architecture_node_factory(
            id="ARCH-001",
            title="Test Architecture",
            version="1.0.0"
        )

        # When: Store audit record with target
        audit_id = await audit_storage.store_audit_record(sample_audit_record)
        cleanup_test_nodes.append(("AuditEvent", audit_id))

        # Then: Audit record created and linked to target
        assert audit_id is not None

        # Verify relationship exists
        cypher = """
        MATCH (audit:AuditEvent {id: $audit_id})-[r:AUDITS]->(target)
        RETURN target.id as target_id, type(r) as rel_type
        """
        results = await audit_storage.graph_ops.query(cypher, {"audit_id": audit_id})

        assert len(results) == 1
        assert results[0]["target_id"] == "ARCH-001"
        assert results[0]["rel_type"] == "AUDITS"

    @pytest.mark.asyncio
    async def test_get_audit_trail(
        self,
        audit_storage,
        architecture_node_factory,
        cleanup_test_nodes
    ):
        """Test retrieving audit trail for a target."""
        # Given: Target node exists
        arch_node = await architecture_node_factory(
            id="ARCH-002",
            title="Test Architecture 2",
            version="1.0.0"
        )

        # And: Multiple audit records for this target
        records = []
        for i in range(3):
            record = {
                "id": f"audit_trail_{i}",
                "timestamp": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
                "event_type": "validation",
                "agent_id": f"agent_{i}",
                "decision": "approved" if i % 2 == 0 else "revision_required",
                "target_id": "ARCH-002",
                "target_type": "Architecture",
                "metadata": {"test": True}
            }
            audit_id = await audit_storage.store_audit_record(record)
            cleanup_test_nodes.append(("AuditEvent", audit_id))
            records.append(record)

        # When: Get audit trail
        trail = await audit_storage.get_audit_trail("ARCH-002", limit=10)

        # Then: All records returned in reverse chronological order
        assert len(trail) == 3

        # Verify order (most recent first)
        timestamps = [datetime.fromisoformat(r["timestamp"]) for r in trail]
        assert timestamps == sorted(timestamps, reverse=True)

        # Verify content
        assert trail[0]["id"] == "audit_trail_0"
        assert trail[0]["decision"] == "approved"
        assert trail[1]["id"] == "audit_trail_1"
        assert trail[2]["id"] == "audit_trail_2"

    @pytest.mark.asyncio
    async def test_get_audit_trail_with_limit(
        self,
        audit_storage,
        architecture_node_factory,
        cleanup_test_nodes
    ):
        """Test audit trail respects limit parameter."""
        # Given: Target with 5 audit records
        arch_node = await architecture_node_factory(
            id="ARCH-003",
            title="Test Architecture 3",
            version="1.0.0"
        )

        for i in range(5):
            record = {
                "id": f"audit_limit_{i}",
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "validation",
                "target_id": "ARCH-003",
                "target_type": "Architecture",
                "decision": "approved",
                "metadata": {}
            }
            audit_id = await audit_storage.store_audit_record(record)
            cleanup_test_nodes.append(("AuditEvent", audit_id))

        # When: Get audit trail with limit=3
        trail = await audit_storage.get_audit_trail("ARCH-003", limit=3)

        # Then: Only 3 records returned
        assert len(trail) == 3

    @pytest.mark.asyncio
    async def test_get_validation_history(
        self,
        audit_storage,
        cleanup_test_nodes
    ):
        """Test retrieving validation event history."""
        # Given: Multiple validation events
        validation_records = []
        for i in range(3):
            record = {
                "id": f"val_history_{i}",
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": "validation",
                "agent_id": "test_agent",
                "decision": "approved" if i % 2 == 0 else "rejected",
                "result": {
                    "status": "approved" if i % 2 == 0 else "rejected",
                    "violations": []
                },
                "metadata": {"index": i}
            }
            audit_id = await audit_storage.store_audit_record(record)
            cleanup_test_nodes.append(("AuditEvent", audit_id))
            validation_records.append(record)

        # When: Get validation history
        history = await audit_storage.get_validation_history(limit=10)

        # Then: All validation events returned
        assert len(history) >= 3  # May have other validation events from other tests

        # Verify our records are in the results
        our_ids = {r["id"] for r in validation_records}
        returned_ids = {r["id"] for r in history}
        assert our_ids.issubset(returned_ids)

    @pytest.mark.asyncio
    async def test_get_validation_history_by_agent(
        self,
        audit_storage,
        cleanup_test_nodes
    ):
        """Test filtering validation history by agent ID."""
        # Given: Validation events from different agents
        for agent in ["agent_A", "agent_B"]:
            for i in range(2):
                record = {
                    "id": f"val_{agent}_{i}",
                    "timestamp": datetime.utcnow().isoformat(),
                    "event_type": "validation",
                    "agent_id": agent,
                    "decision": "approved",
                    "result": {"status": "approved"},
                    "metadata": {}
                }
                audit_id = await audit_storage.store_audit_record(record)
                cleanup_test_nodes.append(("AuditEvent", audit_id))

        # When: Get history for agent_A only
        history = await audit_storage.get_validation_history(agent_id="agent_A", limit=10)

        # Then: Only agent_A events returned
        assert len(history) >= 2
        agent_a_events = [r for r in history if r["agent_id"] == "agent_A"]
        assert len(agent_a_events) >= 2

    @pytest.mark.asyncio
    async def test_get_validation_history_since_timestamp(
        self,
        audit_storage,
        cleanup_test_nodes
    ):
        """Test filtering validation history by timestamp."""
        # Given: Validation events at different times
        cutoff_time = datetime.utcnow()

        # Old event (before cutoff)
        old_record = {
            "id": "val_old",
            "timestamp": (cutoff_time - timedelta(hours=2)).isoformat(),
            "event_type": "validation",
            "agent_id": "test_agent",
            "decision": "approved",
            "result": {"status": "approved"},
            "metadata": {}
        }
        old_audit_id = await audit_storage.store_audit_record(old_record)
        cleanup_test_nodes.append(("AuditEvent", old_audit_id))

        # New event (after cutoff)
        new_record = {
            "id": "val_new",
            "timestamp": (cutoff_time + timedelta(seconds=1)).isoformat(),
            "event_type": "validation",
            "agent_id": "test_agent",
            "decision": "approved",
            "result": {"status": "approved"},
            "metadata": {}
        }
        new_audit_id = await audit_storage.store_audit_record(new_record)
        cleanup_test_nodes.append(("AuditEvent", new_audit_id))

        # When: Get history since cutoff
        history = await audit_storage.get_validation_history(since=cutoff_time, limit=10)

        # Then: Only new events returned
        returned_ids = {r["id"] for r in history}
        assert "val_new" in returned_ids
        assert "val_old" not in returned_ids

    @pytest.mark.asyncio
    async def test_audit_record_metadata_serialization(
        self,
        audit_storage,
        cleanup_test_nodes
    ):
        """Test that complex metadata is properly serialized/deserialized."""
        # Given: Audit record with complex metadata
        record = {
            "id": "audit_meta_test",
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "validation",
            "decision": "approved",
            "metadata": {
                "nested": {
                    "field": "value",
                    "number": 42,
                    "boolean": True,
                    "list": [1, 2, 3]
                },
                "string": "test",
                "float": 3.14
            },
            "result": {
                "violations": [
                    {"code": "TEST-001", "message": "Test violation"}
                ]
            }
        }

        # When: Store and retrieve
        audit_id = await audit_storage.store_audit_record(record)
        cleanup_test_nodes.append(("AuditEvent", audit_id))

        history = await audit_storage.get_validation_history(limit=1)
        retrieved = next((r for r in history if r["id"] == "audit_meta_test"), None)

        # Then: Metadata properly deserialized
        assert retrieved is not None
        assert retrieved["metadata"]["nested"]["field"] == "value"
        assert retrieved["metadata"]["nested"]["number"] == 42
        assert retrieved["metadata"]["nested"]["boolean"] is True
        assert retrieved["metadata"]["nested"]["list"] == [1, 2, 3]
        assert retrieved["result"]["violations"][0]["code"] == "TEST-001"

    @pytest.mark.asyncio
    async def test_empty_audit_trail(self, audit_storage):
        """Test retrieving audit trail for non-existent target."""
        # When: Get audit trail for target that doesn't exist
        trail = await audit_storage.get_audit_trail("NONEXISTENT", limit=10)

        # Then: Empty list returned
        assert trail == []

    @pytest.mark.asyncio
    async def test_validation_history_empty(self, audit_storage):
        """Test validation history with no matching records."""
        # When: Get validation history with agent that doesn't exist
        history = await audit_storage.get_validation_history(
            agent_id="nonexistent_agent_xyz_12345",
            limit=10
        )

        # Then: Empty or no matching records
        matching = [r for r in history if r["agent_id"] == "nonexistent_agent_xyz_12345"]
        assert len(matching) == 0
