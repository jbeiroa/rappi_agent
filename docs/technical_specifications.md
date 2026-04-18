# Especificaciones Técnicas: Agente de Operaciones Inteligentes Rappi

## 1. Descripción del Proyecto
Este sistema es una solución de IA multi-agente diseñada para potenciar la toma de decisiones estratégica en Rappi. Combina el procesamiento de lenguaje natural (NLP) con modelos de Machine Learning para analizar métricas operacionales, detectar anomalías y generar reportes ejecutivos automatizados.

## 2. Arquitectura del Sistema
El sistema utiliza una estructura jerárquica basada en el **Google Agent Development Kit (ADK)** y una capa de persistencia para el tracking de modelos.

### 2.1 Jerarquía de Agentes
1.  **Root Agent (Gateway)**: Punto de entrada único. Gestiona guardrails, memoria de sesión y delega al Orquestador.
2.  **Orchestrator Agent**: Descompone consultas complejas en planes de acción y coordina la ejecución entre analistas y visualizadores.
3.  **Data Analyst Agent**: Traduce lenguaje natural a consultas de Pandas. Utiliza un entorno de ejecución seguro para procesar el dataframe enriquecido.
4.  **Data Visualizer Agent**: Genera especificaciones de Plotly para renderizar gráficos interactivos en el frontend.
5.  **Report Agent**: Especializado en análisis estratégico; procesa hallazgos técnicos (ML/Stats) para redactar el reporte ejecutivo.

### 2.2 Pipeline de Machine Learning e Inteligencia
- **Motor de Anomalías**: Implementación de `IsolationForest` para detección de outliers multivariables.
- **Tracking (MLflow)**: Registro local de experimentos, hiperparámetros y modelos utilizando un backend SQLite (`mlflow.db`).
- **Lógica de Deterioro**: Algoritmos de ventana deslizante para detectar caídas consecutivas de rendimiento.

## 3. Flujo de Datos
- **Fuente**: `data/dummy_data.xlsx`.
- **Carga y Enriquecimiento**: Los datos se cargan en memoria y se enriquecen con cálculos de cambio porcentual WoW, flags de anomalías y promedios por tipo de zona para benchmarking.
- **Estado Compartido**: Uso de un singleton en `shared_state.py` para asegurar que todos los agentes trabajen sobre la misma versión de los datos enriquecidos.

## 4. Tecnologías Core
- **Framework de Agentes**: Google ADK.
- **Modelos de Lenguaje**: Gemini 3 Flash.
- **Visualización**: Plotly Dash & Plotly.py.
- **Backend de ML**: Scikit-Learn & MLflow.
- **Gestión de Paquetes**: `uv`.

## 5. Capacidades Operacionales
- **Consultas Ad-hoc**: Preguntas sobre cualquier métrica o zona geográfica.
- **Análisis de Tendencias**: Detección visual y textual de evolución temporal.
- **Reportes Bajo Demanda**: Generación de reportes ejecutivos en HTML con recomendaciones estratégicas.
- **Exportación**: Descarga directa de datos filtrados en formatos CSV y JSON.

---
*Documentación técnica finalizada para el proceso de selección de Rappi.*
