from src.core.interfaces import IIndexReader
from src.core.models import SearchResult
from src.domain_nlp.pipeline import NLPPipeline

class SearchService:
    """
    Coordina el proceso de búsqueda
    """
    def __init__(self, reader: IIndexReader, nlp: NLPPipeline):
        self.reader = reader
        self.nlp = nlp

    def execute_search(self, raw_query: str) -> list[SearchResult]:
        if not raw_query.strip():
            return []

        # 1. Expandir la consulta con NLP (Sinónimos, correcciones, etc.)
        expanded_query = self.nlp.process(raw_query)
        
        print(f"DEBUG - Original: '{expanded_query.original_text}'")
        print(f"DEBUG - Expandida: {expanded_query.to_boolean_query()}")

        # 2. Ejecutar la búsqueda en el índice
        results = self.reader.search(expanded_query)
        
        return results