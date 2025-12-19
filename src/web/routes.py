import os
from flask import Blueprint, render_template, request

from src.infrastructure.fs.loader import FileDocumentLoader
from src.infrastructure.search_engine.adapter import WhooshAdapter
from src.infrastructure.search_engine.reader import WhooshReader
from src.domain_nlp.pipeline import NLPPipeline
from src.services.search_service import SearchService

# Definimos el Blueprint (agrupación de rutas)
main_bp = Blueprint('main', __name__)

# --- CONFIGURACIÓN E INYECCIÓN DE DEPENDENCIAS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_DIR = os.path.join(BASE_DIR, 'data', 'index_storage')

# Instanciamos las dependencias
adapter = WhooshAdapter(INDEX_DIR)
reader = WhooshReader(adapter)
nlp = NLPPipeline()

# Inyectamos todo en el servicio
search_service = SearchService(reader, nlp)


@main_bp.route('/')
def home():
    """Renderiza la portada del buscador."""
    return render_template('index.html')

@main_bp.route('/search')
def search():
    """Procesa la búsqueda y muestra resultados."""
    query = request.args.get('q', '')
    
    if not query:
        return render_template('index.html')
        
    # Llamamos a tu lógica de negocio
    results = search_service.execute_search(query)
    
    # Enviamos los datos a la vista
    return render_template('results.html', query=query, results=results)