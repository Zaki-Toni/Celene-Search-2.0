from src.core.models import ExpandedQuery
from src.domain_nlp.components import (
    TokenizerComponent, 
    StopwordFilter, 
    POSTagger, 
    WordNetExpander
)

class NLPPipeline:
    """
    Orquesta el flujo de procesamiento de lenguaje natural.
    Convierte un string crudo en una ExpandedQuery.
    """
    
    def __init__(self):
        # Inicializamos los pasos del pipeline en orden estricto
        self.tokenizer = TokenizerComponent()
        self.sw_filter = StopwordFilter(language='spanish')
        self.tagger = POSTagger()
        self.expander = WordNetExpander()

    def process(self, raw_query: str) -> ExpandedQuery:
        """
        Ejecuta el pipeline paso a paso.
        """
        # 1. Tokenizar: "El coche veloz" -> ["el", "coche", "veloz"]
        tokens = self.tokenizer.process(raw_query)
        
        # 2. Filtrar: ["el", "coche", "veloz"] -> ["coche", "veloz"]
        clean_tokens = self.sw_filter.process(tokens)
        
        # 3. Etiquetar: ["coche", "veloz"] -> [("coche", "NN"), ("veloz", "ADJ")]
        tagged_tokens = self.tagger.process(clean_tokens)
        
        # 4. Expandir: -> ["coche", "auto", "carro", "veloz", "rápido"...]
        expanded_terms = self.expander.process(tagged_tokens)
        
        # 5. Empaquetar en el DTO
        return ExpandedQuery(
            original_text=raw_query,
            expanded_terms=expanded_terms
        )