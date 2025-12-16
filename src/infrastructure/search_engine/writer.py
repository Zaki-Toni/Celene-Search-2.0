from src.core.interfaces import IIndexWriter
from src.core.models import Document
from src.infrastructure.search_engine.adapter import WhooshAdapter

###CAMBIAR DEBUG A LOGGIN

class WhooshWriter(IIndexWriter):
    """
    Implementación de escritura usando Whoosh.
    """

    def __init__(self, adapter: WhooshAdapter):
        self.adapter = adapter
        self.ix = adapter.get_index()
        self._writer = self.ix.writer()

    def add_documents(self, docs: list[Document]) -> None:
        """
        Añade una lista de documentos al buffer de escritura.
        """
        for doc in docs:
            try:
                self._writer.add_document(
                    title=doc.title, content=doc.content, path=doc.path
                )
            except Exception as e:
                print(f"Error indexando {doc.title}: {e}")

    def commit(self) -> None:
        """
        Guarda los cambios físicamente en el disco.
        """
        try:
            self._writer.commit()
            self._writer = self.ix.writer()
        except Exception as e:
            print(f"Error en commit: {e}")
            self._writer.cancel()
