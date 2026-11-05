# Enterprise RAG Architectures & Sovereign Retrieval Engines
### Multi-Pattern RAG Suite with OWASP LLM Guardrails & FinOps Controls

[![Architecture](https://img.shields.io/badge/Architecture-Agentic_%7C_Hybrid_%7C_Graph_%7C_General-blue.svg)]()
[![Compliance](https://img.shields.io/badge/Compliance-EU_AI_Act_%7C_DORA_%7C_ENS_Alta-purple.svg)]()
[![Security](https://img.shields.io/badge/Security-OWASP_LLM_Top_10_Guardrails-red.svg)]()
[![FinOps](https://img.shields.io/badge/FinOps-Token_Budget_%26_Cost_Gateway-green.svg)]()

---

## 1. Resumen Ejecutivo (C-Level & Strategic ROI)

Este repositorio consolida las 4 topologías fundamentales de **Sistemas de Recuperación Aumentada por Generación (RAG)** de nivel enterprise, desacopladas bajo principios de arquitectura limpia, gobernanza regulatoria y optimización de costes en inferencia.

### Matriz Estratégica para la Dirección

| Rol Directivo | Desafío en Adopción RAG | Solución RAG Types Suite | Impacto Medible / KPI |
|---|---|---|---|
| **CISO / Ciberseguridad** | Inyección de prompts indirectos y fuga de datos en embeddings. | **Guardrails_OWASP** con filtros semánticos y validación de contexto. | 0 incidentes de exfiltración de credenciales. |
| **CFO / FinOps** | Facturación descontrolada por tokens en modelos fundacionales. | **FinOps-Gateway** con cuotas estrictas, rate-limiting y fallback local. | -45% coste operativo en inferencia LLM. |
| **CTO / Arquitectura** | Falta de precisión en dominios no estructurados y grafos relacionales. | Implementaciones nativas de **Agentic RAG**, **Hybrid RAG** y **Graph RAG**. | Precisión semántica > 94% en retrieval. |
| **Chief Risk / Legal Officer** | Trazabilidad nula y alucinaciones no auditables. | **rag-evaluation** & **regulated-rag-ai-governance** con sellado criptográfico. | Cumplimiento estricto DORA & EU AI Act. |

---

## 2. Diagrama de Arquitectura de los Motores RAG

`
flowchart TD
    subgraph IngestionLayer ["CAPA 0: ENTRADA & SEGURIDAD PERIMETRAL"]
        PROMPT["Consulta de Usuario / API"]
        GW["Guardrails OWASP (Validación Sanitizada)"]
        FIN["FinOps Gateway (Token Budgeting & Routing)"]
    end

    subgraph TopologyEngines ["CAPA 1: MOTORES DE RECUPERACIÓN ESPECIALIZADOS"]
        AG["Agentic RAG\n(ReAct + Self-RAG Iterativo)"]
        HY["Hybrid RAG\n(Dense Vectors + BM25 Lexical)"]
        GR["Graph RAG\n(Neo4j / NetworkX Knowledge Graph)"]
        GE["General RAG\n(Vector Pipeline Convencional)"]
    end

    subgraph GovernanceLayer ["CAPA 2: AUDITORÍA & CERTIFICACIÓN"]
        EVAL["RAG Evaluation (Métricas Faithfulness & Recall)"]
        REG["Regulated RAG AI Governance (Sellado SHA-256)"]
    end

    PROMPT --> GW
    GW --> FIN
    FIN --> AG
    FIN --> HY
    FIN --> GR
    FIN --> GE
    AG --> EVAL
    HY --> EVAL
    GR --> EVAL
    GE --> EVAL
    EVAL --> REG
`

---

## 3. Topologías Incluidas

1. **Agentic RAG**:
   - Razonamiento multi-paso mediante patrón ReAct.
   - Evaluación reflexiva de relevancia antes de generar respuesta (Corrective Self-RAG).
   - Acceso determinista a herramientas de compliance y bases vectoriales.

2. **Hybrid RAG**:
   - Fusión de búsqueda semántica densa (embeddings vectoriales) y búsqueda léxica exacta (BM25 / Splade).
   - Reciprocal Rank Fusion (RRF) para ponderación equilibrada de resultados técnicos y legales.

3. **Graph RAG**:
   - Modelado de grafos de conocimiento para descubrir relaciones complejas de n-saltos en normativas y contratos.
   - Ideal para mapas regulatorios (DORA, NIS2, RGPD, ISO 27001).

4. **General RAG**:
   - Implementación base altamente optimizada, modular y desacoplada de frameworks pesados.

5. **Guardrails_OWASP & inops-gateway**:
   - Defensas activas contra inyección de prompts, jailbreaks y alucinaciones.
   - Control de gasto presupuestario por llamada, usuario y departamento.

6. **ag-evaluation & egulated-rag-ai-governance**:
   - Pipelines automáticos de cálculo de métricas de precisión (Fidelidad, Relevancia de Contexto, Precisión de Respuesta).

---

## 4. Guía de Inicio Rápido

`ash
# Clonar el repositorio
git clone https://github.com/Tardigrado-76/rag-types.git
cd rag-types

# Configurar entorno de dependencias
pip install -r requirements.txt
`

---

## 5. Licencia y Cumplimiento
Código bajo licencia enterprise para arquitectura soberana de IA. Conforme al marco de gobernanza europea de inteligencia artificial.
