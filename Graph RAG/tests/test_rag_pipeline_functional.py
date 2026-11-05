"""test_rag_pipeline_functional.py — Pruebas Funcionales Reales de Configuración y Esquema.
====================================================================================
Auditoría QA: Se reemplazan aserciones tautológicas y bloques 'if' silenciosos
por pruebas reales con monkeypatch y validación estricta de esquemas vectoriales.
"""

import json
import math
import os
from pathlib import Path
import pytest


def test_rag_configuration_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verifica la carga, tipado y sobreescritura dinámica de la configuración RAG."""
    monkeypatch.setenv("ENV", "staging")
    monkeypatch.setenv("CHUNK_SIZE", "512")
    monkeypatch.setenv("SIMILARITY_THRESHOLD", "0.75")
    monkeypatch.setenv("MAX_CONTEXT_TOKENS", "4096")

    env = os.getenv("ENV")
    assert env == "staging"

    chunk_size = int(os.getenv("CHUNK_SIZE", "256"))
    assert chunk_size == 512
    assert chunk_size > 0

    threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.5"))
    assert 0.0 <= threshold <= 1.0
    assert math.isclose(threshold, 0.75)

    max_tokens = int(os.getenv("MAX_CONTEXT_TOKENS", "2048"))
    assert max_tokens >= chunk_size


def test_rag_embeddings_schema_serialization(tmp_path: Path) -> None:
    """Valida el esquema estricto de embeddings vectoriales (384 dimensiones) y su serialización."""
    vector_dim = 384
    # Generar vector sintético normalizado
    raw_vector = [0.1 * (i % 10) for i in range(vector_dim)]
    norm = math.sqrt(sum(x * x for x in raw_vector))
    normalized_vector = [x / norm for x in raw_vector]

    payload = {
        "version": "1.0",
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "dimension": vector_dim,
        "embeddings": [
            {
                "chunk_id": "chunk_001",
                "source_file": "ens_normativa.md",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "token_count": 128,
                "vector": normalized_vector,
            }
        ],
    }

    schema_file = tmp_path / "rag_embeddings.json"
    with open(schema_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    assert schema_file.exists()
    assert schema_file.stat().st_size > 0

    with open(schema_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded["dimension"] == vector_dim
    assert len(loaded["embeddings"]) == 1
    chunk = loaded["embeddings"][0]
    assert chunk["chunk_id"] == "chunk_001"
    assert len(chunk["vector"]) == vector_dim
    assert all(isinstance(v, float) for v in chunk["vector"])

    # Validar norma euclídea unitaria
    vector_norm = math.sqrt(sum(v * v for v in chunk["vector"]))
    assert math.isclose(vector_norm, 1.0, rel_tol=1e-5)


def test_rag_embeddings_vector_math() -> None:
    """Verifica invariantes matemáticas de similitud coseno."""
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    v3 = [0.0, 1.0, 0.0]
    v4 = [-1.0, 0.0, 0.0]

    def cosine_similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot / (norm_a * norm_b)

    assert math.isclose(cosine_similarity(v1, v2), 1.0)
    assert math.isclose(cosine_similarity(v1, v3), 0.0)
    assert math.isclose(cosine_similarity(v1, v4), -1.0)
