from typing import Any, cast

from whoosh.highlight import ContextFragmenter
from whoosh.qparser import OrGroup, QueryParser

from src.core.interfaces import IIndexReader
from src.core.models import ExpandedQuery, SearchResult
from src.infrastructure.search_engine.adapter import WhooshAdapter


class WhooshReader(IIndexReader):
    """
    Implementación de lectura/búsqueda usando Whoosh.
    """

    def __init__(self, adapter: WhooshAdapter):
        self.adapter = adapter
        self.ix = adapter.get_index()

    def search(self, query: ExpandedQuery) -> list[SearchResult]:
        results_list: list[SearchResult] = []

        query_str = query.to_boolean_query()

        with self.ix.searcher() as searcher:
            # type: ignore -> Ignoramos el error de OrGroup vs AndGroup
            parser = QueryParser("content", self.ix.schema, group=OrGroup) # type: ignore

            try:
                parsed_query = parser.parse(query_str)
                hits = searcher.search(parsed_query, limit=20)
                hits.fragmenter = ContextFragmenter(maxchars=200, surround=40)

                for hit in hits:
                    snippet = (
                        hit.highlights("content")
                        or cast(str, hit.get("content", ""))[:200]
                    )

                    
                    # Forzamos la conversión a float para calmar al linter.
                    raw_score = hit.score
                    safe_score: float = (
                        float(raw_score) if raw_score is not None else 0.0
                    )

                    result = SearchResult(
                        title=cast(str, hit.get("title", "Sin título")),
                        path=cast(str, hit.get("path", "")),
                        score=safe_score,
                        snippet=snippet,
                    )
                    results_list.append(result)

            except Exception as e:
                print(f"Error durante la búsqueda: {e}")
                return []

        return results_list
