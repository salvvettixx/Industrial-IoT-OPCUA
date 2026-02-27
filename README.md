# AI Insight - Sistema RAG de Última Generación 🚀

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Pro-00ADFF?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-yellow?style=for-the-badge)

**AI Insight** es una solución de Generación Aumentada por Recuperación (RAG) diseñada con una arquitectura modular de grado producción. Implementa técnicas avanzadas de IA para garantizar respuestas precisas, contextualizadas y libres de alucinaciones basadas en tus propios documentos.

## 🌟 Características Principales

- **Arquitectura Modular LCEL:** Orquestación flexible utilizando LangChain Expression Language.
- **Búsqueda Híbrida (Hybrid Search):** Combina recuperación semántica (Dense) con recuperación léxica (Sparse/BM25).
- **Multi-Query Expansion:** Genera variaciones de la consulta original para asegurar la captura de información relevante.
- **Re-ranking Avanzado (Cross-Encoder):** Implementa un modelo de re-clasificación BERT (FlashRank) para maximizar la relevancia de los documentos finales.
- **Interfaz Web Premium:** Dashboard interactivo desarrollado con Flask y estética de vanguardia.

## 🏗️ Arquitectura del Sistema

El flujo de información sigue este pipeline de ingeniería:
1. **Ingesta:** Carga y fragmentación recursiva de PDFs, DOCX y TXT.
2. **Retrieval:** Búsqueda combinada en base de datos vectorial y léxica.
3. **Optimización:** Re-ordenamiento de documentos mediante re-ranker local.
4. **Generación:** Contextualización mediante GPT-4o-mini con reglas estrictas de citación.

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.9 o superior.
- Clave de API de OpenAI.

### Configuración
1. Clona el repositorio:
   ```bash
   git clone https://github.com/salvvettixx/SistemaRAG.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tu archivo `.env`:
   ```env
   OPENAI_API_KEY=tu_clave_aqui
   ```

### Ejecución
- **Fase de Ingesta:** Coloca tus archivos en `/data` y ejecuta `python -m src.ingesta`.
- **Lanzar Web App:** Ejecuta `python app.py` y abre `http://localhost:5000`.

## 📁 Estructura del Proyecto

```
SistemaRAG/
├── src/
│   ├── motor_rag.py   # Lógica central del sistema
│   ├── ingesta.py     # Procesamiento de documentos
│   ├── config.py      # Gestor de configuración
│   └── prompts.py     # Plantillas de IA
├── data/              # Carpeta para documentos base
├── templates/         # Interfaz web
├── app.py             # Servidor Flask
└── requirements.txt   # Dependencias
```

---
Desarrollado con ❤️ para desafíos técnicos de IA Senior.
