import os
import shutil

from whoosh.analysis import StandardAnalyzer
from whoosh.fields import ID, TEXT, Schema
from whoosh.index import Index, create_in, exists_in, open_dir


class WhooshAdapter:
    """
    Gestiona el acceso físico al índice de Whoosh.
    Encapsula la configuración del Schema y la creación del directorio.
    """

    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        # Definimos el esquema de la base de datos:
        # - title: Texto indexable y almacenado.
        # - content: Texto indexable y almacenado. Analizador Estándar.
        # - path: ID único, almacenado pero no analizado.
        self.schema = Schema(
            title=TEXT(stored=True),
            content=TEXT(stored=True, analyzer=StandardAnalyzer()),
            path=ID(stored=True, unique=True),
        )

    def get_index(self) -> Index:
        """
        Devuelve el objeto índice. Si no existe, lo crea.
        """
        if not os.path.exists(self.index_dir):
            os.makedirs(self.index_dir)
            return create_in(self.index_dir, self.schema)

        if exists_in(self.index_dir):
            return open_dir(self.index_dir)
        else:
            return create_in(self.index_dir, self.schema)

    def reset_index(self):
        """
        Borra y recrea el índice (útil para re-indexar desde cero).
        """
        if os.path.exists(self.index_dir):
            shutil.rmtree(self.index_dir)
        os.makedirs(self.index_dir)
        create_in(self.index_dir, self.schema)
