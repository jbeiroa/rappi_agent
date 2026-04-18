import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table, ctx, Patch
from dash_chat import ChatComponent
import asyncio
import os
import json
import logging
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.agents.root.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import sys
import ast
import re

# --- Configure Logging ---
load_dotenv()
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("rappi_ops_dashboard")

# Suppress noisy logs from third-party libraries
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("dash").setLevel(logging.WARNING)

# --- Initialize Agent Runner ---
session_service = InMemorySessionService()
app_name = "rappi_ops_agent"

# Pre-create a default session
async def init_session():
    try:
        await session_service.create_session(
            user_id="default_user",
            session_id="chat_session",
            app_name=app_name
        )
        logger.info("Conversational session initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize session: {e}")

asyncio.run(init_session())

runner = Runner(
    agent=root_agent,
    app_name=app_name,
    session_service=session_service
)

# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Rappi Intelligent Operations"

# Inject global CSS to handle full-height and non-scrollable behavior
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --rappi-red: #f6553f;
                --rappi-red-dark: #c81c20;
                --rappi-white: #ffffff;
                --rappi-light: #f8f9fa;
            }
            body, html {
                height: 100vh;
                margin: 0;
                overflow: hidden;
                background-color: var(--rappi-light);
                font-family: 'Inter', sans-serif;
            }
            .main-container {
                height: 100vh;
                display: flex;
                flex-direction: column;
                padding: 15px 20px 20px 20px;
            }
            .header-row {
                background-color: var(--rappi-red);
                color: white;
                margin: -15px -20px 15px -20px;
                padding: 10px 30px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-shrink: 0;
            }
            .header-title {
                margin: 0;
                font-weight: 700;
                font-size: 1.5rem;
            }
            .content-row {
                flex-grow: 1;
                overflow: hidden;
                display: flex;
            }
            .full-height-card {
                height: 100%;
                display: flex;
                flex-direction: column;
                border: none;
                border-radius: 12px;
            }
            .card-header {
                background-color: white !important;
                border-bottom: 1px solid #eee !important;
                font-weight: 600;
                color: var(--rappi-dark);
                padding: 15px 20px;
            }
            .card-body-scroll {
                flex-grow: 1;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                padding: 0;
            }
            /* Override ChatComponent to take full space */
            .dash-chat-container {
                flex-grow: 1;
                height: 100% !important;
            }
            .btn-rappi {
                background-color: var(--rappi-red);
                border-color: var(--rappi-red);
                color: white;
                font-weight: 600;
                border-radius: 8px;
            }
            .btn-rappi:hover {
                background-color: var(--rappi-red-dark);
                border-color: var(--rappi-red-dark);
                color: white;
            }
            .btn-outline-rappi {
                color: var(--rappi-red);
                border-color: var(--rappi-red);
                font-weight: 600;
                border-radius: 8px;
            }
            .btn-outline-rappi:hover {
                background-color: var(--rappi-red);
                color: white;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

from src.report_generator import generate_executive_report_html

app.layout = html.Div([
    dbc.Container([
        # Header Row
        html.Div([
            html.H1("Inteligencia Operacional Rappi", className="header-title"),
            html.Div([
                dbc.Button("Reporte Ejecutivo", id="btn-executive-report", className="btn-rappi me-2", size="sm"),
                dbc.Button("Ayuda", id="open-help", className="btn-rappi", size="sm")
            ], className="d-flex align-items-center")
        ], className="header-row"),
        
        # Help Offcanvas
        dbc.Offcanvas(
            html.Div([
                html.H4("¿Cómo usar esta aplicación?", className="mb-3"),
                html.P([
                    "Este asistente te permite consultar datos operativos de Rappi usando lenguaje natural. ",
                    "Puedes pedir análisis de tendencias, comparaciones entre verticales o métricas específicas."
                ]),
                html.H5("Consejos:", className="mt-4"),
                html.Ul([
                    html.Li("Sé específico con los periodos de tiempo (ej. 'últimas 8 semanas')."),
                    html.Li("Menciona si prefieres un tipo de gráfico (líneas, barras, dispersión)."),
                    html.Li("Puedes descargar los datos de cualquier gráfico generado usando los botones debajo del mismo.")
                ]),
                html.H5("Ejemplos:", className="mt-4"),
                html.Em("'¿Cómo evolucionó el GMV semana a semana?'"),
                html.Br(),
                html.Em("'Métricas de eficiencia de la última semana por país'")
            ]),
            id="help-offcanvas",
            title="Centro de Ayuda",
            is_open=False,
            placement="end",
        ),
        
        dbc.Row([
            # Left Column: Chat
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Chatbot de Operaciones"),
                    dbc.CardBody([
                        ChatComponent(
                            id="chat-component",
                            messages=[],
                            fill_height=True
                        )
                    ], className="card-body-scroll")
                ], className="full-height-card shadow-sm")
            ], width=7, style={"height": "100%"}),

            # Right Column: Visualizations
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Insights y Visualizaciones"),
                    dbc.CardBody([
                        html.Div(id="viz-container", children=[
                            html.P("Los gráficos aparecerán aquí cuando los solicites.", className="text-muted text-center", style={"marginTop": "50%"})
                        ], style={"height": "100%", "overflowY": "auto", "padding": "20px"})
                    ], className="card-body-scroll")
                ], className="full-height-card shadow-sm")
            ], width=5, style={"height": "100%"})
        ], className="content-row", style={"flex-grow": 1})
    ], fluid=True, className="main-container"),
    dcc.Download(id="download-data"),
    dcc.Download(id="download-report"),
    dbc.Spinner(html.Div(id="report-spinner-output"), fullscreen_style={"visibility": "visible", "filter": "blur(2px)"}, fullscreen=True)
], style={"height": "100vh"})

# --- Helper Callbacks ---
@app.callback(
    Output("download-report", "data"),
    Input("btn-executive-report", "n_clicks"),
    prevent_initial_call=True
)
def download_executive_report(n):
    if not n:
        return dash.no_update
    
    # Generate the report (running the async function in a sync wrapper)
    report_html = asyncio.run(generate_executive_report_html())
    
    return dcc.send_string(report_html, filename="Reporte_Ejecutivo_Rappi.html")

@app.callback(
    Output("help-offcanvas", "is_open"),
    Input("open-help", "n_clicks"),
    [State("help-offcanvas", "is_open")],
)
def toggle_help(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output({"type": "collapse", "index": dash.dependencies.MATCH}, "is_open"),
    Input({"type": "collapse-button", "index": dash.dependencies.MATCH}, "n_clicks"),
    State({"type": "collapse", "index": dash.dependencies.MATCH}, "is_open"),
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("download-data", "data"),
    [Input({"type": "btn-csv", "index": dash.dependencies.ALL}, "n_clicks"),
     Input({"type": "btn-json", "index": dash.dependencies.ALL}, "n_clicks")],
    [State({"type": "chart-data", "index": dash.dependencies.ALL}, "data")],
    prevent_initial_call=True
)
def download_chart_data(csv_clicks, json_clicks, all_data):
    if not any(csv_clicks + json_clicks):
        return dash.no_update
    
    # Identify which button was clicked
    triggered_id = ctx.triggered_id
    if not triggered_id:
        return dash.no_update
    
    # triggered_id is a dict like {'index': 123, 'type': 'btn-csv'}
    btn_index = triggered_id['index']
    btn_type = triggered_id['type']
    
    # Find the data corresponding to this index
    # Note: State ALL returns a list. We need to find the one matching the triggered index.
    # Since we use Store with the same index, we can usectx.inputs_list or just find it.
    
    # Using ctx.inputs_list is more direct but let's be robust
    data_to_download = None
    # inputs_list is only for Inputs. We need States.
    # We can use the triggered index to find it in the States list if we know the order, 
    # but ALL might not guarantee order matching triggered_id's index perfectly if elements were removed/added.
    # Actually, ALL returns values in order of the components in the layout.
    
    # A better way: Use ctx.states to find the value for that specific index
    for state_id_str, value in ctx.states.items():
        if f'"index":{btn_index}' in state_id_str and "chart-data" in state_id_str:
            data_to_download = value
            break
            
    if not data_to_download:
        return dash.no_update
        
    df = pd.DataFrame(data_to_download)
    
    if "btn-csv" in btn_type:
        return dcc.send_data_frame(df.to_csv, f"rappi_data_{btn_index}.csv", index=False)
    else:
        return dcc.send_data_frame(df.to_json, f"rappi_data_{btn_index}.json", orient="records")

def parse_chart_spec_from_text(text):
    """Fallback: extraction of JSON chart spec from agent markdown text or raw text."""
    try:
        # Try finding markdown-wrapped json first
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        
        # Try finding a raw JSON-like block { ... "chart_type": ... }
        # More flexible regex to find a block containing chart_type or type
        match = re.search(r'\{[^{}]*"(chart_type|type)"[^{}]*\}', text, re.DOTALL)
        if match:
            # Attempt to find the full balanced object if nested
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except:
                # If balanced search failed, try to just find the biggest { } block
                start = text.find('{')
                end = text.rfind('}')
                if start != -1 and end != -1:
                    return json.loads(text[start:end+1])
            
        return None
    except:
        return None

def try_parse_natural_language_data(data_str):
    """Attempts to parse strings like 'Semanas: L1, L2, Valores: 10, 20' into a DataFrame-ready format."""
    try:
        # Example format: "Semanas: L8W, L7W, Valores: 2.9, 3.0"
        parts = re.split(r'Valores:', data_str, flags=re.IGNORECASE)
        if len(parts) == 2:
            x_str = parts[0].replace('Semanas:', '').strip()
            y_str = parts[1].strip()
            
            x_vals = [v.strip() for v in x_str.split(',') if v.strip()]
            y_vals = [float(v.strip()) for v in y_str.split(',') if v.strip()]
            
            if len(x_vals) == len(y_vals) and len(x_vals) > 0:
                return pd.DataFrame({"Semana": x_vals, "Valor": y_vals})
        return None
    except:
        return None

def create_plotly_figure(spec):
    """Transforms a JSON spec into a Plotly figure and returns (fig, df)."""
    try:
        # Unwrap nested spec if present (sometimes happens with Pydantic tool arguments)
        if isinstance(spec, dict) and "spec" in spec and len(spec) == 1:
            spec = spec["spec"]

        # Be flexible with key names
        chart_type = spec.get("chart_type") or spec.get("type")
        data_raw = spec.get("data") or spec.get("data_summary")
        title = spec.get("title", "Gráfico de Insight")
        x_col = spec.get("x_axis")
        y_cols = spec.get("y_axis")

        if not chart_type:
            logger.warning(f"No chart type found in spec: {spec}")
            return None, None

        # Data handling
        df = None
        if isinstance(data_raw, str):
            # 1. Try ast.literal_eval for python-style strings
            try:
                data_obj = ast.literal_eval(data_raw)
                if isinstance(data_obj, (list, dict)):
                    df = pd.DataFrame(data_obj)
            except:
                # 2. Try standard json.loads
                try:
                    data_obj = json.loads(data_raw)
                    df = pd.DataFrame(data_obj)
                except:
                    # 3. Fallback to natural language parsing
                    df = try_parse_natural_language_data(data_raw)
        elif isinstance(data_raw, (list, dict)):
            df = pd.DataFrame(data_raw)

        if df is None or df.empty:
            logger.error(f"Failed to parse data for chart: {data_raw}")
            return None, None

        # Clean up column names for better display
        rename_mapping = {
            "WEEK": "Semana",
            "VALUE": "Valor",
            "METRIC": "Métrica",
            "COUNTRY": "País",
            "CITY": "Ciudad",
            "ZONE": "Zona",
            "ZONE_TYPE": "Tipo de Zona",
            "ZONE_PRIORITIZATION": "Prioridad de Zona",
            "WEEK_NUM": "Nro. de Semana"
        }
        df = df.rename(columns=rename_mapping)

        # Update x_col and y_cols to match the new Spanish column names
        if x_col in rename_mapping:
            x_col = rename_mapping[x_col]
        
        if y_cols:
            y_cols = [rename_mapping.get(c, c) for c in y_cols]

        # Determine default X and Y if not provided or to ensure numeric consistency
        if not x_col or x_col not in df.columns:
            x_col = df.columns[0]
        
        # Filter for numeric columns for Y if not explicitly provided or to be safe
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if not y_cols:
            y_cols = [c for c in numeric_cols if c != x_col]
            if not y_cols: # fallback to everything but x
                y_cols = [c for c in df.columns if c != x_col]
        else:
            # Ensure provided y_cols exist in df
            y_cols = [c for c in y_cols if c in df.columns]

        # Standardize legend labels
        labels = {
            "variable": "Métrica / Categoría",
            "value": "Valor"
        }

        if chart_type == "line":
            fig = px.line(df, x=x_col, y=y_cols, title=title, markers=True, labels=labels)
        elif chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_cols, title=title, labels=labels)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_cols, title=title, labels=labels)
        else:
            logger.warning(f"Unsupported chart type: {chart_type}")
            return None, None
        
        fig.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=40, t=60, b=40),
            font=dict(family="Inter, sans-serif"),
            legend_title_text="Categoría"
        )
        return fig, df
    except Exception as e:
        logger.error(f"Failed to create figure: {e}", exc_info=True)
        return None, None

import time

@app.callback(
    [Output("chat-component", "messages"),
     Output("viz-container", "children")],
    Input("chat-component", "new_message"),
    [State("chat-component", "messages"),
     State("viz-container", "children")],
)
def update_chat(new_message, current_messages, current_viz_list):
    # Initialization logic: if no messages and no new_message, provide greeting
    if not current_messages and not new_message:
        return [
            {
                "role": "assistant", 
                "content": """¡Hola! Soy tu asistente de Inteligencia Operacional de Rappi. Puedo ayudarte a analizar métricas de negocio, visualizar tendencias y responder preguntas sobre la operación.

**Ejemplos de lo que puedes preguntarme:**
* **Filtrado:** *'¿Cuáles son las 5 zonas con mayor % Lead Penetration esta semana?'*
* **Comparaciones:** *'Compara el Perfect Order entre zonas Wealthy y Non Wealthy en México'*
* **Tendencias:** *'Muestra la evolución de Gross Profit UE en Chapinero últimas 8 semanas'*
* **Agregaciones:** *'¿Cuál es el promedio de Lead Penetration por país?'*
* **Multivariable:** *'¿Qué zonas tienen alto Lead Penetration pero bajo Perfect Order?'*
* **Inferencia:** *'¿Cuáles son las zonas que más crecen en órdenes en las últimas 5 semanas y qué podría explicar el crecimiento?'*"""
            }
        ], current_viz_list

    if not new_message:
        return dash.no_update, dash.no_update

    user_query = new_message.get("content")
    if not user_query:
        return current_messages, current_viz_list

    # 1. Add User Message to History
    new_history = current_messages + [new_message]
    logger.info(f"USER QUERY: {user_query}")

    # 2. Call Agent (Async run)
    async def get_agent_response():
        message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_query)]
        )
        full_text = ""
        captured_chart_spec = None
        
        try:
            async for event in runner.run_async(
                user_id="default_user",
                session_id="chat_session",
                new_message=message
            ):
                # Check for Tool Calls
                tool_call = getattr(event, 'tool_call', None)
                if not tool_call and hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            tool_call = part.function_call
                            break
                
                if tool_call:
                    tool_name = tool_call.name
                    args = tool_call.args
                    if not isinstance(args, dict):
                        try:
                            if hasattr(args, 'model_dump'):
                                args = args.model_dump()
                            else:
                                args = {k: getattr(args, k) for k in dir(args) if not k.startswith('_')}
                        except:
                            pass
                    
                    logger.info(f"AGENT TOOL CALL: {tool_name}")
                    
                    if tool_name == "generate_chart_spec":
                        logger.info("Captured chart specification from tool call.")
                        captured_chart_spec = args
                    elif tool_name == "run_pandas_query":
                        query_code = args.get("python_code") if isinstance(args, dict) else ""
                        if query_code:
                            logger.info(f"PANDAS QUERY: {query_code}")

                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            if full_text and not full_text.endswith(('\n', ' ')):
                                full_text += "\n\n"
                            full_text += part.text

        except Exception as e:
            logger.error(f"Exception in agent response loop: {e}", exc_info=True)
            full_text = f"Ocurrió un error al procesar tu solicitud: {str(e)}"
            
        return full_text, captured_chart_spec

    agent_response_text, chart_spec = asyncio.run(get_agent_response())

    # 3. Handle Chart Spec
    # Initialize viz list if empty or contains only the placeholder
    if not isinstance(current_viz_list, list) or (len(current_viz_list) == 1 and hasattr(current_viz_list[0], 'className') and 'text-muted' in current_viz_list[0].className):
        current_viz_list = []

    if not chart_spec:
        chart_spec = parse_chart_spec_from_text(agent_response_text)
    
    if chart_spec:
        logger.info(f"Creating chart for side panel...")
        fig, df = create_plotly_figure(chart_spec)
        if fig is not None:
            chart_id = int(time.time() * 1000)
            # Create a new card for the plot with data table and download buttons
            new_plot_card = dbc.Card([
                dbc.CardBody([
                    dcc.Graph(figure=fig, config={'displayModeBar': False}),
                    html.Hr(),
                    html.Div([
                        dbc.Button(
                            "Ver Tabla de Datos",
                            id={"type": "collapse-button", "index": chart_id},
                            className="btn-outline-rappi",
                            size="sm",
                        ),
                    ], className="d-grid gap-2"),
                    dbc.Collapse(
                        dbc.Card([
                            dbc.CardBody([
                                dash_table.DataTable(
                                    data=df.to_dict('records'),
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    page_size=5,
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'textAlign': 'left', 'fontFamily': 'Inter, sans-serif', 'fontSize': '12px'},
                                    style_header={'fontWeight': 'bold', 'backgroundColor': '#f8f9fa'}
                                ),
                                html.Div([
                                    dbc.Button("CSV", id={"type": "btn-csv", "index": chart_id}, className="btn-rappi mt-2 me-2", size="sm"),
                                    dbc.Button("JSON", id={"type": "btn-json", "index": chart_id}, className="btn-rappi mt-2", size="sm"),
                                ], className="d-flex justify-content-end")
                            ])
                        ], className="mt-2 border-0 bg-light"),
                        id={"type": "collapse", "index": chart_id},
                        is_open=False,
                    ),
                    dcc.Store(id={"type": "chart-data", "index": chart_id}, data=df.to_dict('records'))
                ])
            ], className="mb-3 shadow-sm")
            # Prepend the new plot
            current_viz_list = [new_plot_card] + current_viz_list

    # 4. Final UI Cleanup
    try:
        json_match = re.search(r'\{[^{}]*"(chart_type|type)"[^{}]*\}', agent_response_text, re.DOTALL)
        if json_match:
            agent_response_text = agent_response_text.replace(json_match.group(0), "").strip()
        
        if "```json" in agent_response_text:
            block_match = re.search(r'```json.*?```', agent_response_text, re.DOTALL)
            if block_match:
                agent_response_text = agent_response_text.replace(block_match.group(0), "").strip()
        
        tag_match = re.search(r'RECOMENDACIÓN_VISUALIZACIÓN:\s*\b(line|bar|scatter)\b', agent_response_text, re.IGNORECASE)
        if tag_match:
            agent_response_text = agent_response_text.replace(tag_match.group(0), "").strip()
        
        agent_response_text = re.sub(r'\n{3,}', '\n\n', agent_response_text).strip()
    except Exception as e:
        logger.warning(f"Failed to clean agent response text: {e}")

    # 5. Add Agent Text Message to History
    if agent_response_text:
        new_history.append({"role": "assistant", "content": agent_response_text})
    elif not chart_spec:
        new_history.append({"role": "assistant", "content": "He procesado tu consulta pero no he generado una respuesta textual clara."})

    return new_history, current_viz_list

if __name__ == "__main__":
    logger.info("🚀 Starting Rappi Operations Dashboard...")
    logger.info("👉 Access URL: http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
