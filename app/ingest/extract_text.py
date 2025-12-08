import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any

from qdrant_client.http.models import Distance, VectorParams, SparseVectorParams
from markitdown import MarkItDown

from app.ingest.embed_qdrant import EmbeddingSelfQuery

md = MarkItDown()

def infer_document_type(pdf_name: str) -> str:
    name = pdf_name.lower()

    if "autopsy" in name:
        return "autopsy"
    if "police" in name:
        return "police_report"
    if "medical" in name:
        return "medical_history"
    if "toxicology" in name:
        return "toxicology_report"

    return "unknown"


def process_pdf_file(
    file_path: str,
    case_id: str,
    embedder: EmbeddingSelfQuery,
) -> List[Dict[str, Any]]:
    """
    Use internal LLM embedded to:
    - Extract forensic metadata
    - Split the document into semantically valid chunks
    """

    pdf_name = os.path.basename(file_path)
    document_type = infer_document_type(pdf_name)

    result = md.convert(str(file_path))
    text_content = result.text_content or ""

    prompt = f"""
Você é um Médico-Legal especialista em análise de documentos forenses.

Analise o texto abaixo e extraia:

1️⃣ METADADOS:
- case_id: "{case_id}"
- document_type: um dos valores:
  "autopsy", "police_report", "medical_history", "toxicology_report"
- document_date: data no formato YYYY-MM-DD se existir no texto
- pdf_name: nome do arquivo PDF

2️⃣ CHUNKS (dividir por seções técnicas, sem resumir, máximo de 5):
Extraia os trechos exatamente como aparecem no texto, usando as seguintes seções quando existirem:

AUTOPSY:
- external_examination
- internal_examination
- cause_of_death
- manner_of_death

POLICE_REPORT:
- scene_description
- witness_statement
- suspect_info

MEDICAL_HISTORY:
- chronic_conditions
- medications
- recent_events

TOXICOLOGY_REPORT:
- toxicology_results

⚠️ Regras:
- NÃO resumir
- NÃO inferir
- NÃO corrigir termos
- NÃO criar conteúdo
- Apenas transcrição literal

Retorne SOMENTE este JSON:

{{
  "metadados": {{
    "case_id": "{case_id}",
    "document_type": "{document_type}",
    "document_date": "...",
    "pdf_name": "{pdf_name}"
  }},
  "chunks": {{
    "section_name": "texto literal aqui"
  }}
}}

TEXTO DO DOCUMENTO:
{text_content[:12000]}
"""

    try:
        response = embedder.llm.invoke(prompt)

        json_text = (
            re.sub(r"```[\w-]*", "", response.content)
            .replace("```", "")
            .strip()
        )

        data = json.loads(json_text)

        metadados = data.get("metadados", {})
        chunks = data.get("chunks", {})

        processed = []

        for idx, (section, texto) in enumerate(chunks.items()):
            if not texto:
                continue

            metadata = {
                "case_id": metadados.get("case_id"),
                "document_type": metadados.get("document_type"),
                "document_date": metadados.get("document_date"),
                "pdf_name": metadados.get("pdf_name", pdf_name),
                "section": section,
                "chunk_index": idx,
                "confidence_level": "high",
            }

            processed.append(
                {
                    "text": texto.strip(),
                    "metadata": metadata,
                }
            )

        return processed

    except Exception as e:
        print(f"[ERROR] - Error processing {pdf_name}: {e}")
        return []

def main(
    collection: str = "forensic_cases",
    pasta_cases: str = "cases",
):
    embedder = EmbeddingSelfQuery()

    # Cria coleção no Qdrant se não existir
    if not embedder.client.collection_exists(collection_name=collection):
        embedder.client.create_collection(
            collection_name=collection,
            vectors_config={
                "text-dense": VectorParams(size=3072, distance=Distance.COSINE)
            },
            sparse_vectors_config={
                "text-sparse": SparseVectorParams()
            },
        )
        print(f"[SUCCESS] - Collection '{collection}' created")
    else:
        print(f"[WARN] - '{collection}' already exists")

    vector_store = embedder.get_qdrant_vector_store(collection)

    base_path = Path(pasta_cases)
    case_folders = [p for p in base_path.iterdir() if p.is_dir()]

    if not case_folders:
        print("[WARN] - No folder found")
        return

    total_chunks = 0
    total_pdfs = 0

    for case_folder in case_folders:
        case_id = case_folder.name.lower()

        pdf_files = list(case_folder.glob("*.pdf"))
        if not pdf_files:
            continue

        for pdf_file in pdf_files:
            total_pdfs += 1
            chunks = process_pdf_file(
                file_path=str(pdf_file),
                case_id=case_id,
                embedder=embedder,
            )

            if not chunks:
                continue

            texts = [c["text"] for c in chunks]
            metadatas = [c["metadata"] for c in chunks]

            vector_store.add_texts(
                texts=texts,
                metadatas=metadatas,
            )

            total_chunks += len(chunks)

    print(
        f"[SUCCESS] - Ingestion success: {total_pdfs} processed PDFs | {total_chunks} chunks inserted into Qdrant."
    )

if __name__ == "__main__":
    main()