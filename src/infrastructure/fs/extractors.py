from bs4 import BeautifulSoup
from docx import Document as DocxReader
from pypdf import PdfReader

####DEBEMOS MEJORARA LOS EXTRACTORES PARA QUE USEN LOGGIN EN LUGAR DE PRINT

# Importamos la interfaz que deben cumplir
from src.core.interfaces import BaseExtractor


class TextExtractor(BaseExtractor):
    """Maneja archivos .txt simples."""

    def get_text(self, file_path: str) -> str | None:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"Error leyendo TXT {file_path}: {e}")
            return None


class PDFExtractor(BaseExtractor):
    """Maneja archivos .pdf usando pypdf."""

    def get_text(self, file_path: str) -> str | None:
        try:
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_parts.append(extracted)
            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error leyendo PDF {file_path}: {e}")
            return None


class DocxExtractor(BaseExtractor):
    """Maneja archivos Word (.docx)."""

    def get_text(self, file_path: str) -> str | None:
        try:
            doc = DocxReader(file_path)
            # Unimos los párrafos con saltos de línea
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"Error leyendo DOCX {file_path}: {e}")
            return None


class HTMLExtractor(BaseExtractor):
    """Maneja archivos Web (.html) limpiando las etiquetas."""

    def get_text(self, file_path: str) -> str | None:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                soup = BeautifulSoup(f, "html.parser")
                # get_text con separator=' ' evita que palabras pegadas de dif etiquetas se unan
                return soup.get_text(separator=" ")
        except Exception as e:
            print(f"Error leyendo HTML {file_path}: {e}")
            return None
