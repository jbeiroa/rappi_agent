# Rappi Intelligent Operations Agent 🚀

Este proyecto es un sistema multi-agente de inteligencia artificial diseñado para democratizar el acceso a datos operacionales en Rappi. Permite que equipos de Estrategia, Planeación y Analytics (SP&A) obtengan insights profundos, visualizaciones interactivas y reportes estratégicos utilizando lenguaje natural.

## 📋 Descripción del Proyecto
El sistema procesa métricas operacionales complejas distribuidas en 9 países y cientos de zonas. Utiliza una arquitectura jerárquica de agentes y un pipeline de Machine Learning para detectar anomalías, tendencias de deterioro y generar reportes ejecutivos automatizados.

## 🏗️ Arquitectura del Sistema (Multi-Agent System)
Desarrollado con el **Google Agent Development Kit (ADK)**, el sistema se divide en:

1.  **Root Agent (Gateway)**: Maneja la interacción inicial, memoria conversacional y reglas de seguridad.
2.  **Orchestrator Agent**: El cerebro del sistema. Descompone consultas complejas y delega tareas.
3.  **Data Analyst Agent**: Especialista en Pandas que ejecuta consultas enriquecidas con flags de anomalías y cambios WoW.
4.  **Data Visualizer Agent**: Experto en Plotly que genera especificaciones de gráficos interactivos.
5.  **Report Agent**: Consultor estratégico que genera narrativas de negocio para el reporte ejecutivo.

## 🧠 Inteligencia de Datos y ML
El sistema incluye un pipeline avanzado de procesamiento:
- **Detección de Anomalías**: Utiliza `IsolationForest` (Scikit-Learn) para detectar comportamientos inusuales en las métricas.
- **Seguimiento con MLflow**: Todos los modelos y métricas se registran localmente en una base de datos SQLite (`mlflow.db`).
- **Análisis de Tendencias**: Identifica automáticamente deterioros constantes (3+ semanas) y cambios WoW significativos (>10%).

## 🛠️ Stack Tecnológico
- **Lenguaje**: Python 3.12+
- **Gestión de Dependencias**: `uv`
- **Framework de Agentes**: Google ADK (`google-adk`)
- **Modelos**: Gemini 3 Flash via Google ADK.
- **ML & Data**: `Pandas`, `Scikit-Learn`, `MLflow`.
- **UI/UX**: `Plotly Dash` con Rappi Branding y componentes interactivos.

## 🚀 Cómo Ejecutar el Proyecto

### 1. Configuración del Entorno
Asegúrate de tener `uv` instalado. Luego, clona el repositorio:

```bash
# Instalar dependencias
uv sync

# Configurar claves de API
cp .env.example .env
# Edita el archivo .env con tu GEMINI_API_KEY
```

### 2. Ejecutar la Interfaz (Dashboard)
Para iniciar el chatbot interactivo y el panel de visualización:

```bash
uv run python main.py
```
Luego abre tu navegador en `http://127.0.0.1:8050`.

### 3. Revisar el Tracking de MLflow
Para visualizar los experimentos de detección de anomalías:

```bash
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## 📊 Capacidades Destacadas
- **Reporte Ejecutivo**: Generación proactiva de un reporte estratégico en HTML con los 5 insights más críticos y recomendaciones.
- **Exportación de Datos**: Cada gráfico permite visualizar su tabla de origen y descargar los datos en CSV o JSON.
- **Centro de Ayuda**: Guía integrada con ejemplos reales de preguntas operacionales.
- **Branding Rappi**: Interfaz optimizada con la identidad visual y colores de la marca.

---
*Este proyecto es parte de un proceso técnico para Rappi.*
