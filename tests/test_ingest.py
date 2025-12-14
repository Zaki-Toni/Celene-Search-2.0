import os
import sys

# --- BLOQUE DE CONFIGURACIÓN DE RUTAS ---
# 1. Obtenemos la ruta absoluta de este archivo (tests/test_ingest.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Obtenemos la raíz del proyecto (una carpeta arriba de tests)
project_root = os.path.dirname(current_dir)

# 3. Agregamos la raíz al "Path" de Python para poder importar 'src'
sys.path.append(project_root)

# --- AHORA SÍ PODEMOS IMPORTAR EL CÓDIGO DEL PROYECTO ---
from src.infrastructure.fs.loader import FileDocumentLoader

# Definimos dónde están los documentos de prueba (relativo a la raíz del proyecto)
DOCS_DIR = os.path.join(project_root, "data", "documents")


def main():
    print(f"--- Probando Ingesta desde: {DOCS_DIR} ---")

    # Verificamos que la carpeta exista antes de empezar
    if not os.path.exists(DOCS_DIR):
        # Creamos la carpeta si no existe para evitar errores
        os.makedirs(DOCS_DIR, exist_ok=True)
        print(f"⚠️ La carpeta {DOCS_DIR} no existía. Se ha creado vacía.")
        print("Por favor, pon algunos archivos (.txt, .pdf) ahí y vuelve a ejecutar.")
        return

    # 1. Instanciar el Loader
    loader = FileDocumentLoader(DOCS_DIR)

    # 2. Cargar
    docs = loader.load_all()

    # 3. Mostrar resultados
    print(f"\n✅ Total documentos cargados: {len(docs)}")

    if len(docs) == 0:
        print("⚠️ No se encontraron archivos soportados en la carpeta.")

    for doc in docs:
        print("-" * 40)
        print(f"📂 Archivo: {doc.title}")
        print(f"📍 Ruta: {doc.path}")
        print(f"📝 Tipo detectado: {doc.metadata.get('type', 'desconocido')}")
        # Mostramos solo los primeros 100 caracteres sin saltos de línea para que se vea limpio
        preview = doc.content[:100].replace("\n", " ")
        print(f"👀 Contenido: {preview}...")


if __name__ == "__main__":
    main()
