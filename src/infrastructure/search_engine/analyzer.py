import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from whoosh.analysis import Filter, RegexTokenizer, LowercaseFilter, StopFilter, Token
from typing import Iterator, Any, cast # <--- Añadimos Any y cast

class NLTKLemmatizerFilter(Filter):
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, tokens: Iterator[Token]) -> Iterator[Token]:
        for token in tokens:
            # --- SOLUCIÓN ERROR PYLANCE ---
            # Casteamos el token a 'Any' para que Pylance nos deje 
            # acceder a .text sin quejarse.
            t = cast(Any, token)
            
            # Ahora accedemos a t.text sin problemas
            lemma = self.lemmatizer.lemmatize(t.text, pos=wordnet.NOUN)
            
            if lemma != t.text:
                t.text = lemma
            
            yield t

def NLTKAnalyzer(stopwords_lang: str = 'english'):
    """
    Analizador personalizado que incluye lematización.
    """
    return (RegexTokenizer() | LowercaseFilter() | StopFilter(lang=stopwords_lang) | NLTKLemmatizerFilter())