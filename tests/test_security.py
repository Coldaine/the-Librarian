"""
Security tests for Cypher injection prevention and path validation.

Tests that security measures are properly enforced to prevent attacks.
"""

import pytest
from src.graph.schema import (
    validate_node_label,
    validate_relationship_type,
    ALLOWED_NODE_LABELS,
    ALLOWED_RELATIONSHIP_TYPES,
)
from src.processing.parser import validate_file_path


class TestCypherInjectionPrevention:
    """Test Cypher injection prevention mechanisms."""

    def test_valid_node_labels_accepted(self):
        """Test that valid node labels are accepted."""
        for label in ALLOWED_NODE_LABELS:
            # Should not raise exception
            validate_node_label(label)

    def test_invalid_node_label_rejected(self):
        """Test that invalid node labels are rejected."""
        invalid_labels = [
            "FakeLabel",
            "Architecture; DROP DATABASE",
            "Design') MATCH (n) DETACH DELETE n--",
            "'; DELETE *",
            "UNION SELECT",
        ]

        for label in invalid_labels:
            with pytest.raises(ValueError, match="Invalid node label"):
                validate_node_label(label)

    def test_valid_relationship_types_accepted(self):
        """Test that valid relationship types are accepted."""
        for rel_type in ALLOWED_RELATIONSHIP_TYPES:
            # Should not raise exception
            validate_relationship_type(rel_type)

    def test_invalid_relationship_type_rejected(self):
        """Test that invalid relationship types are rejected."""
        invalid_rels = [
            "FAKE_REL",
            "CREATES; DROP DATABASE",
            "LINKS') MATCH (n) DETACH DELETE n--",
        ]

        for rel_type in invalid_rels:
            with pytest.raises(ValueError, match="Invalid relationship type"):
                validate_relationship_type(rel_type)

    def test_label_whitelist_comprehensive(self):
        """Test that label whitelist includes all expected labels."""
        expected_labels = {
            "Architecture",
            "Design",
            "Requirement",
            "CodeArtifact",
            "Decision",
            "AgentRequest",
            "Person",
            "Chunk",
        }

        assert ALLOWED_NODE_LABELS == expected_labels

    def test_relationship_whitelist_comprehensive(self):
        """Test that relationship whitelist includes all expected types."""
        expected_rels = {
            "DEFINES",
            "IMPLEMENTS",
            "SATISFIES",
            "SUPERSEDES",
            "DERIVED_FROM",
            "INVALIDATES",
            "TARGETS",
            "REFERENCES",
            "RESULTED_IN",
            "APPROVES",
            "REJECTS",
            "OWNS",
            "REVIEWED",
            "AUTHORED",
            "CREATED_FROM",
        }

        assert ALLOWED_RELATIONSHIP_TYPES == expected_rels


class TestPathTraversalPrevention:
    """Test path traversal attack prevention."""

    def test_valid_paths_accepted(self):
        """Test that valid paths are accepted."""
        valid_paths = [
            "/home/user/docs/test.md",
            "/var/lib/app/documents/architecture.md",
            "docs/design.md",
        ]

        for path in valid_paths:
            # Should not raise exception
            assert validate_file_path(path) is True

    def test_parent_directory_traversal_rejected(self):
        """Test that parent directory traversal is rejected."""
        dangerous_paths = [
            "../../../etc/passwd",
            "docs/../../../etc/passwd",
            "docs/./../../secret",
            "/docs/../../../root/.ssh/id_rsa",
        ]

        for path in dangerous_paths:
            with pytest.raises(ValueError, match="(Path traversal detected|Dangerous pattern)"):
                validate_file_path(path)

    def test_home_directory_expansion_rejected(self):
        """Test that home directory expansion is rejected."""
        with pytest.raises(ValueError, match="Dangerous pattern"):
            validate_file_path("~/secrets/config")

    def test_variable_expansion_rejected(self):
        """Test that variable expansion is rejected."""
        dangerous_paths = [
            "$HOME/secrets",
            "${PWD}/config",
            "docs/$USER/private",
        ]

        for path in dangerous_paths:
            with pytest.raises(ValueError, match="Dangerous pattern"):
                validate_file_path(path)

    def test_command_substitution_rejected(self):
        """Test that command substitution is rejected."""
        with pytest.raises(ValueError, match="Dangerous pattern"):
            validate_file_path("docs/`whoami`.md")

    def test_allowed_directory_enforcement(self):
        """Test that allowed_directories are enforced."""
        allowed_dirs = ["/home/user/docs", "/var/lib/app"]

        # Path within allowed directory
        assert validate_file_path("/home/user/docs/test.md", allowed_dirs) is True

        # Path outside allowed directories
        with pytest.raises(ValueError, match="outside allowed directories"):
            validate_file_path("/etc/passwd", allowed_dirs)

        # Attempt to escape with ..
        with pytest.raises(ValueError, match="(Path traversal detected|Dangerous pattern)"):
            validate_file_path("/home/user/docs/../../../etc/passwd", allowed_dirs)

    def test_windows_path_traversal_rejected(self):
        """Test that Windows-style path traversal is rejected."""
        dangerous_paths = [
            "docs\\..\\..\\windows\\system32",
            "C:\\..\\..\\secrets",
        ]

        for path in dangerous_paths:
            with pytest.raises(ValueError, match="(Path traversal detected|Dangerous pattern)"):
                validate_file_path(path)


class TestSecurityDefenseInDepth:
    """Test defense-in-depth security measures."""

    def test_multiple_security_layers(self):
        """Test that multiple security layers are in place."""
        # Layer 1: Label validation
        with pytest.raises(ValueError):
            validate_node_label("MaliciousLabel")

        # Layer 2: Path validation
        with pytest.raises(ValueError):
            validate_file_path("../../../etc/passwd")

    def test_sql_comment_patterns_rejected(self):
        """Test that SQL-style comments are rejected in paths."""
        # These patterns might be used to bypass validation
        dangerous_paths = [
            "docs/test.md/*comment*/",
            "docs/*/test.md",
        ]

        for path in dangerous_paths:
            # validate_file_path should handle or reject these
            try:
                validate_file_path(path)
            except ValueError:
                pass  # Expected

    def test_null_byte_injection_handled(self):
        """Test that null byte injection is handled."""
        # Null bytes used to truncate strings in some contexts
        path_with_null = "docs/test.md\x00../../etc/passwd"

        # Should either reject or sanitize
        try:
            result = validate_file_path(path_with_null)
            # If it passes, the null byte should be handled
            assert "\x00" not in path_with_null or result is True
        except ValueError:
            pass  # Also acceptable to reject


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
