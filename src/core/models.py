from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """
    Representa un archivo procesado listo para ser indexado.
    """

    title: str
    content: str
    path: str
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
    expanded_terms: list[str]

    def to_boolean_query(self) -> str:
        """
        Genera una consulta booleana utilizando los términos expandidos.

        Procesa la lista `expanded_terms` para crear una única cadena de búsqueda
        donde todos los términos están unidos por el operador lógico OR. Cada término
        se encierra entre comillas dobles para forzar una coincidencia de frase exacta
        (o palabra exacta, dependiendo de la configuración del analizador).

        Si `expanded_terms` está vacío o solo contiene cadenas vacías después de la limpieza,
        devuelve el valor de `original_text`.

        Returns:
            str: La cadena de consulta booleana lista para ser usada por un motor
                 como Whoosh (ej: '"término1" OR "término2"').
        """
        clean_terms = [t.replace('"', "") for t in self.expanded_terms if t.strip()]

        if not clean_terms:
            return self.original_text

        return " OR ".join(f'"{term}"' for term in clean_terms)
