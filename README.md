# Celene-Search-2.0
# 🔍 Motor de Búsqueda Semántica con Expansión de Consultas

> ⚠️ **Estado del Proyecto:** **Completado / En Stand-by**
>
> Este proyecto ha alcanzado satisfactoriamente los objetivos establecidos para su propósito académico. Actualmente, el desarrollo activo se encuentra pausado para dar prioridad a otros proyectos. Sin embargo, la arquitectura está diseñada para ser escalable y podríamos retomar futuras implementaciones.

> Un sistema de Recuperación de Información (IR) inteligente que utiliza **WordNet** para entender lo que buscas, no solo lo que escribes.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![NLP](https://img.shields.io/badge/NLP-NLTK-yellow)
![Search](https://img.shields.io/badge/Engine-Whoosh-orange)
![License](https://img.shields.io/badge/License-MIT-grey)

## 📖 Descripción

Este proyecto es una implementación de un **Motor de Búsqueda Semántico** diseñado bajo una arquitectura modular y escalable. 

A diferencia de los buscadores tradicionales que buscan coincidencias exactas de texto, este sistema implementa un **Pipeline de NLP** que analiza gramaticalmente la consulta del usuario, filtra palabras irrelevantes y expande los términos de búsqueda utilizando sinónimos de la base de datos léxica **WordNet**.

**Ejemplo:**
Si buscas: *"Coche veloz"*
El sistema busca internamente: *"Coche OR Auto OR Automóvil OR Carro AND Veloz OR Rápido OR Ligero..."*

## ✨ Características Principales

*   **Arquitectura SOLID:** Diseño desacoplado en capas (Presentación, Servicios, Dominio NLP, Infraestructura).
*   **Expansión de Consultas (Query Expansion):** Uso de `nltk.corpus.wordnet` para encontrar sinónimos contextuadas.
*   **Procesamiento Inteligente:**
    *   **POS Tagging:** Distingue si una palabra es sustantivo, verbo o adjetivo para buscar el sinónimo correcto.
    *   **Stop-word Removal:** Ignora palabras vacías ("el", "la", "de") para optimizar la expansión.
*   **Motor de Indexación:** Basado en **Whoosh**, con soporte para ranking BM25F.
*   **Interfaz Web:** Aplicación ligera en ???? para realizar búsquedas y ver resultados resaltados.

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura de capas estricta:

1.  **Capa de Presentación:** Interfaz Web (Flask).
2.  **Capa de Aplicación:** Servicios de Búsqueda e Indexación.
3.  **Capa de Dominio (NLP):** Lógica de expansión semántica.
4.  **Capa de Infraestructura:** Adaptadores para Whoosh y Sistema de Archivos.

## 📂 Estructura del Proyecto

```semantic_search_engine/
│
├── data/                       # 🗄️ CAPA DE DATOS (Ignorada por Git excepto .keep)
│   ├── documents/              # Aquí pones tus archivos (.txt, .pdf, .docx, .html)
│   │   ├── articulo_ia.pdf
│   │   ├── notas_clase.docx
│   │   └── prueba.txt
│   │
│   └── index_storage/          # Aquí Whoosh guardará sus archivos binarios (generado auto)
│
├── src/                        # 🧠 CÓDIGO FUENTE PRINCIPAL
│   ├── __init__.py
│   │
│   ├── core/                   # 1. CAPA DE MODELOS Y CONTRATOS (Interfaces)
│   │   ├── __init__.py
│   │   ├── models.py           # DTOs: Document, SearchResult, ExpandedQuery
│   │   └── interfaces.py       # Clases Abstractas: IIndexReader, IIndexWriter, INLPComponent
│   │
│   ├── domain_nlp/             # 2. CAPA DE DOMINIO (Lógica Lingüística)
│   │   ├── __init__.py
│   │   ├── pipeline.py         # Clase NLPPipeline (Orquestador)
│   │   └── components.py       # Tokenizer, StopwordFilter, POSTagger, WordNetExpander
│   │
│   ├── infrastructure/         # 3. CAPA DE INFRAESTRUCTURA (Implementación Técnica)
│   │   ├── __init__.py
│   │   │
│   │   ├── fs/                 # File System (Lectura de archivos)
│   │   │   ├── __init__.py
│   │   │   ├── loader.py       # FileDocumentLoader (Usa los extractores)
│   │   │   └── extractors.py   # PDFExtractor, DocxExtractor, HTMLExtractor (Strategy)
│   │   │
│   │   └── search_engine/      # Motor de Búsqueda (Whoosh)
│   │       ├── __init__.py
│   │       ├── adapter.py      # WhooshAdapter (Config y Schema)
│   │       ├── writer.py       # WhooshWriter
│   │       └── reader.py       # WhooshReader
│   │
│   ├── services/               # 4. CAPA DE APLICACIÓN (Orquestadores)
│   │   ├── __init__.py
│   │   ├── search_service.py   # Coordina: Query -> NLP -> Reader -> Result
│   │   └── index_service.py    # Coordina: Docs -> Loader -> Writer
│   │
│   └── web/                    # 5. CAPA DE PRESENTACIÓN (Flask)
│       ├── __init__.py         # Crea la 'app' de Flask
│       ├── routes.py           # Endpoints: /, /search
│       |
│       │  
│       └── templates/          # HTML (Jinja2)
│           ├── base.html
│           ├── index.html
│           └── results.html
│
├── tests/                      # 🧪 PRUEBAS UNITARIAS
│   ├── __init__.py
│   ├── test_nlp.py
│   └── test_extractors.py
│
├── .gitignore                  # Archivos a ignorar (venv, pycache, index_storage)
├── config.py                   # Variables globales (Rutas, Idioma, etc.)
├── requirements.txt            # Dependencias (Flask, Whoosh, NLTK, pypdf...)
├── README.md                   # Documentación del proyecto
├── manage_index.py             # Script CLI para ejecutar la indexación
└── run_server.py               # Script CLI para iniciar el servidor Web

```

## ⚙️ Configuración del Entorno

Sigue estos pasos para reproducir el entorno de desarrollo y ejecutar el proyecto localmente.

### 1. Requisitos Previos
*   **Python 3.10** o superior (Necesario para el sistema de tipado moderno).
*   **pip** (Gestor de paquetes).

### 2. Creación del Entorno Virtual
Es recomendable crear un entorno aislado para evitar conflictos.

*   **Linux / Mac:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   **Windows:**
    ```powershell
    python -m venv venv
    venv\Scripts\activate
    ```

### 3. Instalación de Librerías
Instala directamente las dependencias necesarias para el servidor web, el motor de búsqueda, NLP y el procesamiento de archivos:

```bash
pip install Flask Whoosh nltk pypdf python-docx beautifulsoup4
python -m nltk.downloader punkt punkt_tab stopwords averaged_perceptron_tagger averaged_perceptron_tagger_eng wordnet omw-1.4
