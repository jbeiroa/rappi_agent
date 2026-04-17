# Rappi Intelligent Operations Agent 🚀

Este proyecto es un sistema multi-agente de inteligencia artificial diseñado para democratizar el acceso a datos operacionales en Rappi. Permite que equipos de Estrategia, Planeación y Analytics (SP&A) obtengan insights profundos y visualizaciones interactivas utilizando lenguaje natural.

## 📋 Descripción del Proyecto
El sistema procesa métricas operacionales complejas (como Lead Penetration, Perfect Orders y Gross Profit UE) distribuidas en 9 países y cientos de zonas. Utiliza una arquitectura jerárquica de agentes para descomponer preguntas de negocio, ejecutar consultas de datos en tiempo real y generar reportes visuales.

## 🏗️ Arquitectura del Sistema (Multi-Agent System)
Desarrollado con el **Google Agent Development Kit (ADK)**, el sistema se divide en:

1.  **Root Agent (Gateway)**: Punto de entrada que maneja la interacción con el usuario, memoria conversacional y reglas de seguridad (guardrails).
2.  **Orchestrator Agent**: El cerebro del sistema. Descompone consultas complejas y delega tareas a agentes especializados.
3.  **Data Analyst Agent**: Especialista en Pandas que traduce preguntas de negocio a consultas técnicas sobre los datasets.
4.  **Data Visualizer Agent**: Experto en Plotly que genera especificaciones de gráficos (Line, Bar, Scatter) basadas en los resultados del analista.

## 🛠️ Stack Tecnológico
- **Lenguaje**: Python 3.12+
- **Gestión de Dependencias**: `uv`
- **Framework de Agentes**: Google ADK (`google-adk`)
- **Orquestación de LLM**: `LiteLLM` (soporte para Gemini 2.0/3.0 y OpenAI)
- **Interfaz de Usuario**: `Plotly Dash` con componentes Bootstrap.
- **Análisis de Datos**: `Pandas`, `NumPy`.

## 🚀 Cómo Ejecutar el Proyecto

### 1. Configuración del Entorno
Asegúrate de tener `uv` instalado. Luego, clona el repositorio y configura las variables de entorno:

```bash
# Instalar dependencias
uv sync

# Configurar claves de API
cp .env.example .env
# Edita el archivo .env con tu GEMINI_API_KEY u OPENAI_API_KEY
```

### 2. Ejecutar la Interfaz (Dashboard)
Para iniciar el chatbot interactivo y el panel de visualización:

```bash
PYTHONPATH=. uv run python main.py
```
Luego abre tu navegador en `http://127.0.0.1:8050`.

### 3. Exploración de Datos (Notebooks)
Para revisar el análisis exploratorio inicial (EDA) y las respuestas a los escenarios del caso técnico:

```bash
uv run jupyter notebook notebooks/exploratory_data_analysis.ipynb
```

## 📊 Capacidades del Bot
- **Consultas Temporales**: "Muestra la evolución del Gross Profit UE en Chapinero las últimas 8 semanas".
- **Comparaciones Geográficas**: "Compara el Perfect Order entre zonas Wealthy y Non Wealthy en México".
- **Análisis Multivariable**: "¿Qué zonas tienen alto Lead Penetration pero bajo Perfect Order?".
- **Inferencia de Crecimiento**: "Identifica las zonas que más crecen en órdenes y explica por qué".

---
*Este proyecto es parte de un proceso técnico para Rappi.*
