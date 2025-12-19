import sys
import os
import time

# --- CONFIGURACIÓN DE RUTAS ---
# Añadimos el directorio actual al path para importar los módulos 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- IMPORTACIONES DE LA ARQUITECTURA ---
from src.infrastructure.fs.loader import FileDocumentLoader
from src.infrastructure.search_engine.adapter import WhooshAdapter
from src.infrastructure.search_engine.writer import WhooshWriter
from src.services.indexing_service import IndexingService

# --- CONFIGURACIÓN DE DIRECTORIOS ---
# Aquí es donde debes poner tus PDFs, DOCX, TXT
DOCS_DIR = os.path.join(current_dir, 'data', 'documents')
# Aquí se guardará la base de datos
INDEX_DIR = os.path.join(current_dir, 'data', 'index_storage')

def main():
    print("============================================================")
    print("🚀 HERRAMIENTA DE INDEXACIÓN MASIVA (ARCHIVOS REALES)")
    print("============================================================")

    # 1. Validación de directorios
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"⚠️  El directorio de documentos no existía.")
        print(f"📂 Se ha creado: {DOCS_DIR}")
        print("👉 Por favor, coloca tus archivos reales (.pdf, .docx, .txt) ahí y vuelve a ejecutar.")
        return

    # Comprobamos si hay archivos
    files = [f for f in os.listdir(DOCS_DIR) if os.path.isfile(os.path.join(DOCS_DIR, f))]
    if not files:
        print(f"⚠️  La carpeta {DOCS_DIR} está vacía.")
        print("👉 Añade algunos archivos PDF, Word o TXT para probar los extractores.")
        return

    print(f"📂 Directorio de origen: {DOCS_DIR}")
    print(f"📄 Archivos detectados: {len(files)}")
    print("-" * 60)

    # 2. Inicialización de Componentes (Infraestructura)
    print("⚙️  Inicializando componentes...")
    
    # Adaptador de base de datos
    adapter = WhooshAdapter(INDEX_DIR)
    
    # IMPORTANTE: Reiniciamos el índice para borrar datos antiguos (como los del seed_index)
    # y tener una base de datos limpia con solo los archivos reales.
    adapter.reset_index() 
    print("🧹 Índice anterior eliminado (Reset completo).")

    writer = WhooshWriter(adapter)
    loader = FileDocumentLoader(DOCS_DIR)

    # 3. Inicialización del Servicio (Capa de Aplicación)
    # Inyectamos las dependencias
    indexing_service = IndexingService(writer, loader)

    # 4. Ejecución
    print("\n▶️  Iniciando proceso de Ingesta e Indexación...")
    start_time = time.time()
    
    # Aquí ocurre la magia: Loader -> Extractors -> Writer -> Disk
    count = indexing_service.run_indexing()
    
    end_time = time.time()
    duration = end_time - start_time

    # 5. Resumen
    print("-" * 60)
    print(f"✅ Proceso finalizado en {duration:.2f} segundos.")
    print(f"📚 Total documentos indexados: {count}")
    print(f"🗄️  Base de datos guardada en: {INDEX_DIR}")
    print("============================================================")
    print("💡 AHORA: Ejecuta 'python run_server.py' para buscar en tus archivos.")

if __name__ == "__main__":
    main()