import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback
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

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Inteligencia Operacional Rappi", className="text-center my-4"), width=12)
    ]),
    dbc.Row([
        # Left Column: Chat
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Chatbot de Operaciones"),
                dbc.CardBody([
                    html.Div(id="chat-history", style={
                        "height": "600px", 
                        "overflowY": "auto", 
                        "display": "flex", 
                        "flexDirection": "column",
                        "gap": "10px",
                        "padding": "10px"
                    }),
                ]),
                dbc.CardFooter(
                    dbc.InputGroup([
                        dbc.Input(id="user-input", placeholder="Pregunta sobre métricas de Rappi...", type="text"),
                        dbc.Button("Enviar", id="send-btn", color="primary", n_clicks=0),
                    ])
                )
            ])
        ], width=5),

        # Right Column: Visualizations
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Insights y Visualizaciones"),
                dbc.CardBody([
                    html.Div(id="viz-container", children=[
                        html.P("Los gráficos aparecerán aquí cuando los solicites.", className="text-muted text-center")
                    ])
                ])
            ])
        ], width=7)
    ])
], fluid=True)

def parse_chart_spec_from_text(text):
    """Fallback: extraction of JSON chart spec from agent markdown text or raw text."""
    try:
        # Try finding markdown-wrapped json first
        if "```json" in text:
            json_str = text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        
        # Try finding a raw JSON-like block { ... }
        match = re.search(r'\{[^{}]*"type"[^{}]*\}', text)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
            
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
            
            x_vals = [v.strip() for v in x_str.split(',')]
            y_vals = [float(v.strip()) for v in y_str.split(',')]
            
            if len(x_vals) == len(y_vals):
                return pd.DataFrame({"Semana": x_vals, "Valor": y_vals})
        return None
    except:
        return None

def create_plotly_figure(spec):
    """Transforms a JSON spec into a Plotly figure."""
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
            return None

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
            return None

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

        if chart_type == "line":
            fig = px.line(df, x=x_col, y=y_cols, title=title, markers=True)
        elif chart_type == "bar":
            fig = px.bar(df, x=x_col, y=y_cols, title=title)
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_col, y=y_cols, title=title)
        else:
            logger.warning(f"Unsupported chart type: {chart_type}")
            return None
        
        fig.update_layout(template="plotly_white")
        return fig
    except Exception as e:
        logger.error(f"Failed to create figure: {e}", exc_info=True)
        return None

@app.callback(
    [Output("chat-history", "children"),
     Output("viz-container", "children"),
     Output("user-input", "value")],
    [Input("send-btn", "n_clicks"),
     Input("user-input", "n_submit")],
    [State("user-input", "value"),
     State("chat-history", "children"),
     State("viz-container", "children")],
    prevent_initial_call=True
)
def update_chat(n_clicks, n_submit, user_query, current_history, current_viz):
    if not user_query:
        return current_history, current_viz, ""

    # 1. Add User Message to History
    user_msg = html.Div(user_query, style={
        "alignSelf": "flex-end",
        "backgroundColor": "#e9ecef",
        "padding": "10px",
        "borderRadius": "10px",
        "maxWidth": "80%"
    })
    
    if current_history is None:
        current_history = []
    
    new_history = current_history + [user_msg]
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
                    # Robust argument capture: convert object to dict if necessary
                    args = tool_call.args
                    if not isinstance(args, dict):
                        # Attempt to extract all attributes as a dict
                        try:
                            args = {k: getattr(args, k) for k in dir(args) if not k.startswith('_')}
                        except:
                            pass
                    
                    logger.info(f"AGENT TOOL CALL: {tool_name}")
                    if tool_name != "transfer_to_agent":
                        logger.debug(f"TOOL ARGS: {args}")
                    
                    if tool_name == "generate_chart_spec":
                        logger.info("Captured chart specification from tool call.")
                        # Save the whole args object for flexible mapping in create_plotly_figure
                        captured_chart_spec = args
                    elif tool_name == "run_pandas_query":
                        query_code = args.get("python_code") if isinstance(args, dict) else ""
                        if query_code:
                            logger.info(f"PANDAS QUERY: {query_code}")

                # Accumulate Text
                if hasattr(event, 'content') and event.content:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            full_text += part.text

        except Exception as e:
            logger.error(f"Exception in agent response loop: {e}", exc_info=True)
            full_text = f"Ocurrió un error al procesar tu solicitud: {str(e)}"
            
        return full_text, captured_chart_spec

    agent_response_text, chart_spec = asyncio.run(get_agent_response())

    # 3. Handle Chart Spec
    # Prioritize captured spec from tool call, fallback to manual parsing
    if not chart_spec:
        chart_spec = parse_chart_spec_from_text(agent_response_text)
    
    if chart_spec:
        logger.info(f"Rendering chart...")
        fig = create_plotly_figure(chart_spec)
        if fig:
            current_viz = dcc.Graph(figure=fig)
            # Remove raw JSON block from UI for cleaner experience
            # We match the specific JSON block to avoid stripping text that just looks like JSON
            try:
                match = re.search(r'\{[^{}]*"type"[^{}]*\}', agent_response_text)
                if match:
                    agent_response_text = agent_response_text.replace(match.group(0), "").strip()
            except:
                pass
    
    # 4. Add Agent Message to History
    agent_msg = html.Div(dcc.Markdown(agent_response_text), style={
        "alignSelf": "flex-start",
        "backgroundColor": "#007bff",
        "color": "white",
        "padding": "10px",
        "borderRadius": "10px",
        "maxWidth": "80%"
    })
    
    new_history = new_history + [agent_msg]

    return new_history, current_viz, ""

if __name__ == "__main__":
    logger.info("🚀 Starting Rappi Operations Dashboard...")
    logger.info("👉 Access URL: http://127.0.0.1:8050")
    app.run(debug=False, port=8050)
