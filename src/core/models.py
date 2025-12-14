from dataclasses import dataclass, field
from typing import Any  # 'Any' es el único que aún requiere importación


@dataclass
class Document:
    """
    Representa un archivo procesado listo para ser indexado.
    """

    title: str
    content: str
    path: str
    # Uso de dict[] nativo
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchResult:
    """
    Representa un documento encontrado en la búsqueda.
    """

    title: str
    path: str
    score: float
    snippet: str = ""


@dataclass
class ExpandedQuery:
    """
    Representa la consulta del usuario enriquecida con NLP.
    """

    original_text: str
    # Uso de list[] nativo
    expanded_terms: list[str]

    def to_boolean_query(self) -> str:
        """
        Convierte la lista de términos en un string OR para Whoosh.
        """
        clean_terms = [t.replace('"', "") for t in self.expanded_terms if t.strip()]

        if not clean_terms:
            return self.original_text

        return " OR ".join(f'"{term}"' for term in clean_terms)
