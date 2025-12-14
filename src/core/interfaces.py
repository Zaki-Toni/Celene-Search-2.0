import abc
from typing import Any

from src.core.models import Document, ExpandedQuery, SearchResult


class IIndexWriter(abc.ABC):
    """Contrato para escribir documentos en el índice."""

    @abc.abstractmethod
    def add_documents(self, docs: list[Document]) -> None:
        pass

    @abc.abstractmethod
    def commit(self) -> None:
        pass


class IIndexReader(abc.ABC):
    """Contrato para buscar en el índice."""

    @abc.abstractmethod
    def search(self, query: ExpandedQuery) -> list[SearchResult]:
        pass


class INLPComponent(abc.ABC):
    """Contrato para un paso del pipeline de procesamiento de lenguaje."""

    @abc.abstractmethod
    def process(self, data: Any) -> Any:
        pass


class BaseExtractor(abc.ABC):
    """Contrato para extraer texto de diferentes formatos de archivo."""

    @abc.abstractmethod
    def get_text(self, file_path: str) -> str | None:
        """
        Retorna el texto extraído o None si falló la extracción.
        Uso de sintaxis moderna 'str | None' en lugar de 'Optional[str]'.
        """
        pass
