"""Health check endpoint."""

from fastapi import APIRouter, HTTPException
import logging

from src.graph.connection import get_connection
from src.processing.embedder import EmbeddingGenerator
from src.api.models import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check system health including Neo4j and Ollama connectivity.

    Returns:
        HealthResponse with status of all services
    """
    # Check Neo4j
    neo4j_healthy = False
    neo4j_details = {}

    try:
        conn = get_connection()
        health_data = await conn.health_check()
        neo4j_healthy = health_data.get("connected", False)
        neo4j_details = health_data
        logger.info(f"Neo4j health check: {neo4j_healthy}")
    except Exception as e:
        logger.error(f"Neo4j health check failed: {e}")
        neo4j_details = {"error": str(e)}

    # Check Ollama
    ollama_healthy = False
    ollama_details = {}

    try:
        embedder = EmbeddingGenerator()
        ollama_healthy = embedder.check_connection()
        if ollama_healthy:
            model_available = embedder.check_model_available()
            ollama_details = {
                "connection": True,
                "model_available": model_available,
                "model": embedder.model_name
            }
        else:
            ollama_details = {"connection": False}
        logger.info(f"Ollama health check: {ollama_healthy}")
    except Exception as e:
        logger.error(f"Ollama health check failed: {e}")
        ollama_details = {"error": str(e)}

    # Determine overall status
    status = "healthy" if (neo4j_healthy and ollama_healthy) else "degraded"

    return HealthResponse(
        status=status,
        neo4j=neo4j_healthy,
        ollama=ollama_healthy,
        version="0.1.0",
        details={
            "neo4j": neo4j_details,
            "ollama": ollama_details
        }
    )
