import sys
import os
import shutil
import datetime

# --- CONFIGURACIÓN DE RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importamos tu arquitectura
from src.core.models import Document
from src.infrastructure.search_engine.adapter import WhooshAdapter
from src.infrastructure.search_engine.writer import WhooshWriter

# Ruta del índice
INDEX_DIR = os.path.join(current_dir, 'data', 'index_storage')

def main():
    print("=========================================================")
    print("🌱 GENERADOR DE ÍNDICE MASIVO (SEMANTIC TEST DATASET)")
    print("=========================================================")

    # 1. Limpieza
    if os.path.exists(INDEX_DIR):
        print(f"🧹 Eliminando índice antiguo en: {INDEX_DIR}")
        shutil.rmtree(INDEX_DIR)
    
    # 2. Inicialización
    print("⚙️  Inicializando Motor Whoosh...")
    adapter = WhooshAdapter(INDEX_DIR)
    writer = WhooshWriter(adapter)

    # 3. DATASET ESTRATÉGICO
    # Hemos diseñado estos datos para probar capacidades específicas del NLP
    
    raw_data = [
        # --- CATEGORÍA: TRANSPORTE (Sinónimos: Car, Auto, Vehicle, Machine) ---
        {
            "title": "F1 Racing Championship",
            "content": "The red racing car is extremely fast on the track. Drivers love the speed of this machine.",
            "path": "transport/f1_news.txt",
            "category": "Sports"
        },
        {
            "title": "Urban Mobility Report",
            "content": "The automobile is the primary cause of traffic in big cities. We need more buses.",
            "path": "transport/city_study.pdf",
            "category": "Urban Planning"
        },
        {
            "title": "Vintage Motorcars",
            "content": "Restoring an old motorcar takes time and patience. The engine parts are rare.",
            "path": "transport/hobbies.doc",
            "category": "Hobbies"
        },

        # --- CATEGORÍA: ANIMALES (Sinónimos: Dog, Canine, Pooch, Hound) ---
        {
            "title": "Guide to Puppies",
            "content": "My dog barks loudly when he sees the mailman. It is a loyal companion.",
            "path": "animals/pets.txt",
            "category": "Pets"
        },
        {
            "title": "Veterinary Science Journal",
            "content": "The canine patient exhibited signs of fatigue. The hound needs rest.",
            "path": "animals/vet_record.docx",
            "category": "Science"
        },
        {
            "title": "Stray Animals",
            "content": "We found a poor pooch wandering the streets alone. We took the mutt to the shelter.",
            "path": "animals/shelter.html",
            "category": "Social"
        },
        {
            "title": "The Big Cat",
            "content": "The tiger is the largest feline species in the world. It hunts in the jungle.",
            "path": "animals/wildlife.txt",
            "category": "Nature"
        },

        # --- CATEGORÍA: TECNOLOGÍA (Sinónimos: Computer, Processor, Machine) ---
        {
            "title": "Quantum Leap",
            "content": "The new quantum computer will revolutionize data processing and cryptography.",
            "path": "tech/quantum.pdf",
            "category": "Science"
        },
        {
            "title": "Coding in Python",
            "content": "Python is a great language to control any computing machine or server.",
            "path": "tech/coding.py",
            "category": "Programming"
        },
        {
            "title": "Data Center Specs",
            "content": "This powerful processor handles millions of calculations per second.",
            "path": "tech/hardware.spec",
            "category": "Hardware"
        },

        # --- CATEGORÍA: SENTIMIENTOS (Sinónimos: Happy, Glad, Joy) ---
        {
            "title": "Psychology Today",
            "content": "Feeling happy is essential for mental health. Being glad about small things helps.",
            "path": "health/mind.txt",
            "category": "Health"
        },
        {
            "title": "The Joy of Painting",
            "content": "Painting brings pure joy and bliss to the artist's soul.",
            "path": "arts/bob_ross.txt",
            "category": "Art"
        },

        # --- CATEGORÍA: LEMATIZACIÓN (Plurales vs Singulares) ---
        {
            "title": "Migration Patterns",
            "content": "The geese are flying south for the winter.",
            "path": "nature/birds.txt",
            "category": "Nature"
        },
        {
            "title": "Marathon Results",
            "content": "The athletes were running for 4 hours straight.",
            "path": "sports/marathon.txt",
            "category": "Sports"
        },
        {
            "title": "Kindergarten Class",
            "content": "The children are playing in the sandbox.",
            "path": "education/school.doc",
            "category": "Education"
        },

        # --- CATEGORÍA: AMBIGÜEDAD (Palabras con doble sentido) ---
        {
            "title": "River Geography",
            "content": "We sat by the bank of the river to fish and watch the water flow.",
            "path": "geo/rivers.txt",
            "category": "Geography"
        },
        {
            "title": "Financial Crisis",
            "content": "The bank refused to give a loan due to the economic recession.",
            "path": "finance/money.pdf",
            "category": "Economy"
        }
    ]

    # 4. Procesamiento e Inyección
    print(f"📦 Procesando {len(raw_data)} documentos simulados...")
    
    docs_to_index = []
    for entry in raw_data:
        # Simulamos metadatos ricos
        meta = {
            "type": "hardcoded", 
            "category": entry["category"], 
            "created_at": datetime.datetime.now().isoformat()
        }
        
        doc = Document(
            title=entry["title"],
            content=entry["content"],
            path=entry["path"],
            metadata=meta
        )
        docs_to_index.append(doc)

    # 5. Escritura
    writer.add_documents(docs_to_index)
    writer.commit()

    print("✅ Indexación finalizada.")
    print("=========================================================")
    print("🚀 GUÍA DE PRUEBAS PARA LA WEB (http://localhost:5000)")
    print("=========================================================")
    print("1. Prueba de Sinónimos (Vehículos):")
    print("   -> Busca: 'Vehicle'")
    print("   -> Resultado esperado: 'F1 Racing' (Car), 'Urban Mobility' (Automobile)")
    print("")
    print("2. Prueba de Sinónimos (Perros):")
    print("   -> Busca: 'Hound' (Sabueso) o 'Pooch'")
    print("   -> Resultado esperado: 'Guide to Puppies' (Dog), 'Veterinary Science'")
    print("")
    print("3. Prueba de Lematización (Plurales Irregulares):")
    print("   -> Busca: 'Goose' (Singular)")
    print("   -> Resultado esperado: 'Migration Patterns' (Contiene 'Geese')")
    print("")
    print("   -> Busca: 'Child' (Singular)")
    print("   -> Resultado esperado: 'Kindergarten Class' (Contiene 'Children')")
    print("")
    print("4. Prueba de Lematización (Verbos):")
    print("   -> Busca: 'Run'")
    print("   -> Resultado esperado: 'Marathon Results' (Contiene 'Running')")
    print("")
    print("5. Prueba de Contexto (Tech):")
    print("   -> Busca: 'Machine'")
    print("   -> Resultado esperado: Debería traer tanto coches ('racing car') como computadoras ('computing machine').")

if __name__ == "__main__":
    main()