from langchain.chains.query_constructor.schema import AttributeInfo

metadata_field_info = [
    AttributeInfo(
        name="case_id",
        description=(
            "- Identificador único do caso (ex.: 'case001', 'case002', 'case003').\n"
            "- SEMPRE use este filtro quando o usuário mencionar explicitamente um caso.\n"
            "- Nunca misture documentos de casos diferentes."
        ),
        type="string",
    ),
    AttributeInfo(
        name="document_type",
        description=(
            "- Tipo do documento pericial.\n"
            "- Valores possíveis:\n"
            "  'autopsy', 'police_report', 'medical_history', 'toxicology_report'.\n"
            "- Use este filtro sempre que a pergunta indicar um tipo específico de documento."
        ),
        type="string",
    ),
    AttributeInfo(
        name="document_date",
        description=(
            "- Data do documento no formato 'YYYY-MM-DD' (string).\n"
            "- Você PODE usar operadores de comparação (lt, gt, lte, gte) e igualdade (eq).\n"
            "- Se o usuário disser 'antes de AAAA', use 'lt' considerando 'AAAA-01-01' como limite.\n"
            "- Se o usuário disser 'depois de AAAA', use 'gt' considerando 'AAAA-12-31' como limite."
        ),
        type="string",
    ),
    AttributeInfo(
        name="pdf_name",
        description=(
            "- Nome do arquivo PDF de origem.\n"
            "- Exemplos: 'autopsy.pdf', 'police_report.pdf', 'medical_history.pdf', 'toxicology_report.pdf'."
        ),
        type="string",
    ),
    AttributeInfo(
        name="section",
        description=(
            "- Seção interna do documento pericial.\n"
            "- Exemplos:\n"
            "  'external_examination', 'internal_examination', 'cause_of_death', 'manner_of_death',\n"
            "  'scene_description', 'witness_statement', 'suspect_info',\n"
            "  'chronic_conditions', 'medications', 'recent_events',\n"
            "  'toxicology_results'."
        ),
        type="string",
    ),
    AttributeInfo(
        name="chunk_index",
        description="Índice numérico do chunk dentro do documento.",
        type="integer",
    ),
    AttributeInfo(
        name="confidence_level",
        description="Nível de confiabilidade do trecho: 'high', 'medium' ou 'low'.",
        type="string",
    ),
]

document_content_description = """
Coleção de trechos (chunks) de documentos médico-legais organizados por caso pericial (case_id),
incluindo laudos de necropsia (autopsy), relatórios policiais (police_report),
histórico médico (medical_history) e exames toxicológicos (toxicology_report).

Cada trecho contém metadados como:
- Identificação do caso (case_id)
- Tipo de documento (document_type)
- Data do documento (document_date)
- Nome do arquivo PDF de origem (pdf_name)
- Seção interna do documento (section)
- Índice do chunk no documento (chunk_index)
- Nível de confiabilidade (confidence_level)

O sistema NUNCA deve misturar documentos de casos diferentes.
"""
