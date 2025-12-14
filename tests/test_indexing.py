import os
import shutil
import sys

# --- CONFIGURACIÓN DE RUTAS ---
# Truco para importar módulos desde 'src' estando en 'tests'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# --- IMPORTACIONES ---
from src.core.models import ExpandedQuery
from src.infrastructure.fs.loader import FileDocumentLoader
from src.infrastructure.search_engine.adapter import WhooshAdapter
from src.infrastructure.search_engine.reader import WhooshReader
from src.infrastructure.search_engine.writer import WhooshWriter

# Definimos carpetas de prueba
DOCS_DIR = os.path.join(project_root, "data", "documents")
# Usamos una carpeta de índice separada para no romper la real si existiera
TEST_INDEX_DIR = os.path.join(project_root, "data", "test_index_storage")


def main():
    print("--- 🧪 INICIO TEST INTEGRAL: INGESTA + INDEXACIÓN + BÚSQUEDA ---")

    # 1. Limpieza previa: Borrar índice de pruebas anterior
    if os.path.exists(TEST_INDEX_DIR):
        print(f"🧹 Limpiando índice de pruebas anterior en {TEST_INDEX_DIR}...")
        shutil.rmtree(TEST_INDEX_DIR)

    # 2. Inicialización de componentes (Infraestructura)
    adapter = WhooshAdapter(TEST_INDEX_DIR)
    writer = WhooshWriter(adapter)
    loader = FileDocumentLoader(DOCS_DIR)

    # 3. Cargar documentos del disco
    print(f"\n1. 📂 Leyendo documentos desde: {DOCS_DIR}")
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(
            "⚠️  La carpeta no existía. Se ha creado. Por favor añade archivos y repite."
        )
        return

    docs = loader.load_all()
    if not docs:
        print("❌ No se encontraron documentos válidos (.txt, .pdf, .docx). Abortando.")
        return

    # 4. Indexación (Escritura)
    print(f"\n2. 💾 Indexando {len(docs)} documentos...")
    writer.add_documents(docs)
    writer.commit()  # ¡Importante! Sin commit no se guarda nada.
    print("✅ Indexación completada exitosamente.")

    # 5. Búsqueda (Lectura)
    print("\n3. 🔍 Prueba de Búsqueda")
    print("   (Como aún no tenemos NLP, la búsqueda será literal)")

    while True:
        term = input("\n>> Escribe qué buscar (o 'salir'): ").strip()
        if term.lower() in ["salir", "exit", "quit"]:
            break

        if not term:
            continue

        # Simulamos lo que haría el NLP Pipeline:
        # Creamos una query donde "expandido" es igual a "original" por ahora.
        fake_nlp_query = ExpandedQuery(original_text=term, expanded_terms=[term])

        # Instanciamos el lector y buscamos
        reader = WhooshReader(adapter)
        results = reader.search(fake_nlp_query)

        print(f"📊 Resultados: {len(results)}")

        if not results:
            print(
                "   (Intenta buscar una palabra que sepas que está en los documentos)"
            )

        for i, res in enumerate(results, 1):
            print(f"   {i}. [{res.score:.2f}] {res.title}")
            # Limpiamos saltos de línea del snippet para que se vea bonito
            snippet_clean = res.snippet.replace("\n", " ")
            print(f"      📝 Snippet: ...{snippet_clean}...")
            print(f"      📍 Path: {res.path}")

    print("\n👋 Test finalizado.")


if __name__ == "__main__":
    main()
