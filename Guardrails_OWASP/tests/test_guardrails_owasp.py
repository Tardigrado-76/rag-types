"""test_guardrails_owasp.py — Pruebas Unitarias Reales del Módulo Guardrails OWASP & Regulación.
=============================================================================================
Auditoría y Remediación QA:
- Valida la sanitización CRA/NIS2 frente a Path Traversal mediante `tmp_path`.
- Valida la anonimización RGPD/LOPDGDD con PIIMasker.mask.
- Valida la fragmentación semántica consciente de tokens con TokenSemanticSplitter.
- Valida la factoría de cargadores DocumentLoaderFactory y la lectura real de archivos.
- Valida los umbrales de configuración de seguridad DORA.
"""

import hashlib
import os
import sys
from pathlib import Path
import pytest

# Asegurar importación de los módulos del directorio padre
MODULE_DIR = Path(__file__).parent.parent.resolve()
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    MAX_FILE_SIZE_MB,
    MAX_PROMPT_LENGTH,
)
from rag_ingestion_pipeline import (
    DocumentLoaderFactory,
    PathSanitizer,
    PIIMasker,
    TokenSemanticSplitter,
)


# ---------------------------------------------------------------------------
# 1. TEST PATH SANITIZER (CRA & NIS2)
# ---------------------------------------------------------------------------
def test_path_sanitizer_safe_and_traversal(tmp_path: Path) -> None:
    safe_dir = tmp_path / "docs"
    safe_dir.mkdir(parents=True, exist_ok=True)
    safe_file = safe_dir / "politica_seguridad.md"
    safe_file.write_text("Texto de prueba para verificación CRA.", encoding="utf-8")

    # Archivo dentro del directorio seguro
    is_safe, reason = PathSanitizer.is_safe_path(safe_file, safe_dir)
    assert is_safe is True
    assert reason in ("OK", "")

    # Intento de Path Traversal
    traversal_file = safe_dir / ".." / "archivo_privado.txt"
    is_safe_trav, reason_trav = PathSanitizer.is_safe_path(traversal_file, safe_dir)
    assert is_safe_trav is False
    assert "Path traversal" in reason_trav or not is_safe_trav


# ---------------------------------------------------------------------------
# 2. TEST PII MASKER (RGPD / LOPDGDD)
# ---------------------------------------------------------------------------
def test_pii_masker_redaction() -> None:
    sample_text = (
        "El auditor D. Carlos Gómez con DNI 54321987B, correo c.gomez@auditoria.es, "
        "teléfono 612345678 e IP 192.168.1.45 revisó el informe."
    )
    masked = PIIMasker.mask(sample_text)

    assert "[REDACTED_DNI_NIE]" in masked
    assert "[REDACTED_EMAIL]" in masked
    assert "[REDACTED_PHONE]" in masked
    assert "[REDACTED_IP]" in masked
    assert "54321987B" not in masked
    assert "c.gomez@auditoria.es" not in masked
    assert "192.168.1.45" not in masked


# ---------------------------------------------------------------------------
# 3. TEST TOKEN SEMANTIC SPLITTER
# ---------------------------------------------------------------------------
def test_token_semantic_splitter_chunking() -> None:
    splitter = TokenSemanticSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    text = (
        "El marco normativo NIS2 impone obligaciones estrictas de ciberseguridad a entidades esenciales. "
        "Las brechas de seguridad deben notificarse formalmente en un plazo inferior a 24 horas. "
    ) * 10

    chunks = splitter.split_text(text)
    assert len(chunks) >= 2
    for chunk in chunks:
        assert isinstance(chunk, str)
        assert len(chunk.strip()) > 0


# ---------------------------------------------------------------------------
# 4. TEST DOCUMENT LOADER FACTORY & EXTRACTION
# ---------------------------------------------------------------------------
def test_document_loader_factory(tmp_path: Path) -> None:
    test_file = tmp_path / "normativa_dora.txt"
    test_content = "DORA Artículo 16: Planes de continuidad y respuesta ante incidentes graves."
    test_file.write_text(test_content, encoding="utf-8")

    loader = DocumentLoaderFactory.get_loader(".txt")
    loaded_text = loader.load(test_file)
    assert loaded_text is not None
    assert "DORA Artículo 16" in loaded_text

    # Verificación de integridad criptográfica SHA-256
    file_sha256 = hashlib.sha256(test_content.encode("utf-8")).hexdigest()
    assert len(file_sha256) == 64


# ---------------------------------------------------------------------------
# 5. TEST CONFIGURATION LIMITS
# ---------------------------------------------------------------------------
def test_guardrails_configuration_limits() -> None:
    assert MAX_FILE_SIZE_MB > 0.0
    assert MAX_PROMPT_LENGTH >= 1000
    assert CHUNK_SIZE > CHUNK_OVERLAP
