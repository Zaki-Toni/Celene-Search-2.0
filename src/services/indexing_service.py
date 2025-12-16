from src.core.interfaces import IIndexWriter
from src.infrastructure.fs.loader import FileDocumentLoader

class IndexingService:
    """
    Coordina la ingesta y guardado de documentos.
    """
    def __init__(self, writer: IIndexWriter, loader: FileDocumentLoader):
        self.writer = writer
        self.loader = loader

    def run_indexing(self) -> int:
        """
        Ejecuta el proceso completo. Retorna el número de docs indexados.
        """
        # 1. Cargar documentos
        print("Cargando documentos del disco...")
        docs = self.loader.load_all()
        
        if not docs:
            print("No se encontraron documentos.")
            return 0
            
        # 2. Guardar en índice
        print(f"Indexando {len(docs)} archivos...")
        self.writer.add_documents(docs)
        
        # 3. Confirmar cambios
        self.writer.commit()
        print("Cambios guardados correctamente.")
        
        return len(docs)