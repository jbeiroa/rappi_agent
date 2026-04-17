# Especificaciones Técnicas: Agente de Operaciones Inteligentes Rappi

## 1. Descripción del Proyecto
Este proyecto tiene como objetivo construir un sistema de IA multi-agente de alto rendimiento para democratizar el acceso a los datos de los equipos de Strategy, Planning & Analytics (SP&A) de Rappi. El sistema permitirá a los usuarios realizar consultas sobre métricas operacionales en lenguaje natural y recibir tanto insights textuales como visualizaciones interactivas.

## 2. Arquitectura del Sistema (Sistema Multi-Agente)
Utilizando el **Google Agent Development Kit (ADK)**, el sistema está estructurado jerárquicamente:

### 2.1 Agente Root (La Interfaz)
- **Rol:** Punto de entrada para todas las interacciones del usuario.
- **Funciones Clave:**
    - Guardrails de entrada (asegurando que las consultas estén relacionadas con el negocio).
    - Gestión de sesiones y memoria.
    - Detección de intención (Consulta General vs. Análisis Detallado vs. Generación de Reportes).
- **Herramientas:** Almacén de memoria, Enrutador.

### 2.2 Agente Orquestador (El Planificador)
- **Rol:** Razonamiento de alto nivel y delegación de tareas.
- **Funciones Clave:**
    - Descomponer consultas complejas (ej., "Compara X e Y" -> 1. Obtener X, 2. Obtener Y, 3. Comparar).
    - Gestionar el flujo de información entre sub-agentes especializados.
- **Herramientas:** Planificador, Registro de sub-agentes.

### 2.3 Sub-Agentes Especializados
1.  **Agente Analista de Datos:**
    - **Capacidad:** Experto en Python/Pandas.
    - **Tarea:** Escribir y ejecutar código para filtrar, agregar y analizar el archivo `dummy_data.xlsx`.
    - **Contexto:** Conocimiento del Diccionario de Datos (Lead Penetration, Gross Profit UE, etc.).
2.  **Agente Visualizador de Datos:**
    - **Capacidad:** Especialista en Plotly.
    - **Tarea:** Transformar los resultados de JSON/DataFrame en gráficos interactivos (Líneas, Barras, Dispersión).
3.  **Agente de Sugerencias:**
    - **Capacidad:** Generador Proactivo de Insights.
    - **Tarea:** Realizar comprobaciones en segundo plano para detectar anomalías o correlaciones interesantes relacionadas con la consulta del usuario.

## 3. Diccionario de Datos y Fuentes
- **Archivo Fuente:** `data/dummy_data.xlsx`
- **Datasets:**
    - **Metrics Input:** Métricas operacionales (Lead Penetration, Perfect Order, etc.) por País/Ciudad/Zona/Tipo/Prioridad para las semanas L8W a L0W.
    - **Orders:** Volumen transaccional por zona para las semanas L8W a L0W.
- **Definiciones de Métricas:** (Según el documento de consigna, ej., *Perfect Order* = Pedidos sin cancelaciones, defectos o retrasos / Pedidos Totales).

## 4. Stack Tecnológico y Estándares de Ingeniería
- **Entorno:** Python 3.12+ gestionado por `uv`.
- **Capa de LLM:** `LiteLLM` para una implementación agnóstica del modelo (Predeterminado: `gemini-3-flash-preview`).
- **Interfaz de Usuario:** `Plotly Dash` para una interfaz de tablero profesional centrada en los datos.
- **Pruebas:** `pytest` para una cobertura completa de unidades e integración.
- **Documentación:** Docstrings estilo Google y registros de proyecto en formato Markdown.

## 5. Hoja de Ruta de Implementación
### Fase 1: Base y Datos
- Configuración del entorno con `uv`.
- Módulo de carga y limpieza de datos.
- Validación de cálculos de métricas.

### Fase 2: Chatbot Principal (Multi-Agente)
- Implementación de los agentes Root y Orquestador.
- Definición de herramientas para el Analista de Datos (sandbox de Pandas).
- Integración de LiteLLM.

### Fase 3: Visualización e Interfaz de Usuario
- Implementación del agente Visualizador de Datos.
- Desarrollo de la interfaz Dash (Ventana de chat + Panel lateral para gráficos).

### Fase 4: Insights Automáticos
- Lógica para detección de anomalías y análisis de tendencias.
- Módulo de generación de reportes ejecutivos (Markdown).

### Fase 5: Refinamiento y Demo
- Optimización del rendimiento.
- Preparación de los 5 casos de demo.
