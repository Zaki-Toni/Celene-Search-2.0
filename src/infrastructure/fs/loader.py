import os

from src.core.interfaces import BaseExtractor
from src.core.models import Document

####DEBEMOS USAR LOGGIN EN LUGAR DE PRINT

from src.infrastructure.fs.extractors import (
    DocxExtractor,
    HTMLExtractor,
    PDFExtractor,
    TextExtractor,
)


class FileDocumentLoader:
    """
    Se encarga de escanear un directorio y convertir archivos físicos
    en objetos 'Document'.
    """

    def __init__(self, source_dir: str):
        self.source_dir = source_dir

        # Mapeo: Extensión -> Estrategia de extracción
        # Usamos tipado moderno dict[str, BaseExtractor]
        self._extractors: dict[str, BaseExtractor] = {
            ".txt": TextExtractor(),
            ".pdf": PDFExtractor(),
            ".docx": DocxExtractor(),
            ".html": HTMLExtractor(),
            ".htm": HTMLExtractor(),
        }

    def load_all(self) -> list[Document]:
        """
        Recorre la carpeta configurada y devuelve una lista de documentos procesados.
        """
        if not os.path.exists(self.source_dir):
            print(f"Advertencia: El directorio {self.source_dir} no existe.")
            return []

        documents: list[Document] = []

        print(f"Escaneando directorio: {self.source_dir} ...")

        for filename in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, filename)

            # Saltamos carpetas, solo archivos
            if not os.path.isfile(file_path):
                continue

            # Obtener extensión (ej: '.pdf') en minúsculas
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            # Verificar si tenemos un extractor para esa extensión
            if ext in self._extractors:
                extractor = self._extractors[ext]

                # Usamos el extractor
                content = extractor.get_text(file_path)

                if content:
                    doc = Document(
                        title=filename,
                        content=content,
                        path=file_path,
                        metadata={"type": ext},
                    )
                    documents.append(doc)
                    print(f"✅ Cargado: {filename}")
                else:
                    print(f"⚠️  Archivo vacío o corrupto: {filename}")
            else:
                # Cositas para hacer luego
                # Avisar de archivos ignorados
                # print(f"Ignorando formato no soportado: {filename}")
                pass

        return documents
