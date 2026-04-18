# src/report_generator.py

import pandas as pd
import numpy as np
from src.anomaly_detector import get_enriched_data, get_correlations
from src.agents.report.agent import report_agent
from google.genai import types
from jinja2 import Template
import markdown
import logging
import time

logger = logging.getLogger(__name__)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio

# Setup a local runner for the report agent
report_session_service = InMemorySessionService()
report_runner = Runner(
    agent=report_agent,
    app_name="rappi_report_generator",
    session_service=report_session_service
)

async def generate_executive_report_html():
    """
    Orchestrates the data enrichment, ML analysis, and LLM-based report generation.
    Returns a string containing the full HTML report.
    """
    logger.info("Starting executive report generation...")
    
    # ... (rest of data prep)
    df = get_enriched_data()
    corrs = get_correlations(df)
    
    # ... (summaries)
    recent_anomalies = df[df['IS_ANOMALY'] | (df['WOW_CHANGE'].abs() > 0.15)].tail(15)
    anomalies_list = recent_anomalies[['COUNTRY', 'CITY', 'ZONE', 'METRIC', 'WEEK', 'VALUE', 'WOW_CHANGE']].to_dict('records')
    
    worrying_metrics = df[df['WORRYING_METRIC']].tail(15)
    worrying_list = worrying_metrics[['COUNTRY', 'CITY', 'ZONE', 'METRIC', 'WEEK', 'VALUE', 'DETERIORATION_STREAK']].to_dict('records')
    
    divergent_zones = df.sort_values('PCT_DIFF_FROM_TYPE_AVG', ascending=False).head(10)
    benchmarks_list = divergent_zones[['ZONE', 'METRIC', 'VALUE', 'TYPE_AVG_VALUE', 'PCT_DIFF_FROM_TYPE_AVG']].to_dict('records')
    
    corr_summary = corrs.unstack().sort_values(ascending=False)
    top_corrs = corr_summary[corr_summary < 0.99].head(10).to_dict()
    
    # 3. Construct Prompt Context
    context = f"""
DATOS PARA EL ANÁLISIS ESTRATÉGICO:

1. ANOMALÍAS RECIENTES (Detección ML & WoW >15%):
{anomalies_list}

2. MÉTRICAS CON DETERIORO CONSTANTE (3+ Semanas en caída):
{worrying_list}

3. BENCHMARKING (Zonas con mayor desviación vs su tipo de zona):
{benchmarks_list}

4. CORRELACIONES ENTRE MÉTRICAS:
{top_corrs}
"""

    # 4. Invoke LLM Agent via Runner
    logger.info("Invoking report agent via runner...")
    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=context)]
    )
    
    report_text = ""
    try:
        # Create a unique session ID for this report run
        unique_session_id = f"report_{int(time.time())}"
        
        # Ensure session exists in the service
        await report_session_service.create_session(
            user_id="system", 
            session_id=unique_session_id, 
            app_name="rappi_report_generator"
        )

        logger.info(f"Invoking report agent via runner with session {unique_session_id}...")
        async for event in report_runner.run_async(
            user_id="system",
            session_id=unique_session_id,
            new_message=message
        ):
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        report_text += part.text
    except Exception as e:
        logger.error(f"Error during report agent invocation: {e}", exc_info=True)
        report_text = "# Error en la generación del reporte\nNo se pudo obtener el análisis del agente."

    # 5. Render HTML
    logger.info("Rendering final HTML report...")
    report_html_body = markdown.markdown(report_text, extensions=['tables', 'fenced_code'])
    
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte Ejecutivo Rappi</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body { 
                font-family: 'Inter', sans-serif; 
                line-height: 1.6; 
                color: #2d3436; 
                max-width: 1000px; 
                margin: 0 auto; 
                padding: 40px 20px; 
                background-color: #f1f2f6; 
            }
            .container {
                background-color: #ffffff; 
                padding: 50px; 
                border-radius: 16px; 
                box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            }
            .header { 
                background-color: #f6553f; 
                color: white; 
                padding: 40px; 
                border-radius: 16px; 
                margin-bottom: 40px; 
                text-align: center;
                box-shadow: 0 4px 12px rgba(246, 85, 63, 0.3);
            }
            .header h1 { margin: 0; font-size: 2.5em; font-weight: 700; }
            .header p { margin: 10px 0 0 0; opacity: 0.9; font-size: 1.2em; }
            
            h1, h2, h3 { color: #f6553f; margin-top: 1.5em; }
            h2 { border-bottom: 2px solid #f6553f; padding-bottom: 8px; font-size: 1.8em; }
            
            table { width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.9em; }
            th, td { padding: 15px; border-bottom: 1px solid #dfe6e9; text-align: left; }
            th { background-color: #f8f9fa; font-weight: 700; color: #636e72; text-transform: uppercase; letter-spacing: 0.05em; }
            tr:hover { background-color: #fbfbfb; }
            
            .footer { 
                text-align: center; 
                margin-top: 50px; 
                font-size: 0.85em; 
                color: #b2bec3; 
                border-top: 1px solid #dfe6e9;
                padding-top: 20px;
            }
            .badge {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                background-color: #ffeaa7;
                color: #d63031;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Reporte Estratégico de Operaciones</h1>
            <p>Inteligencia Operacional Rappi | Insights Enriquecidos</p>
        </div>
        <div class="container">
            {{ report_content }}
        </div>
        <div class="footer">
            Este reporte fue generado automáticamente por el Agente Rappi utilizando IsolationForest y Modelos de Lenguaje de Última Generación.
            <br>&copy; 2024 Rappi Strategy & Planning
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    final_html = template.render(report_content=report_html_body)
    
    logger.info("Executive report HTML generated successfully.")
    return final_html
