# src/agents/visualizer/tools.py

from typing import Annotated
import json

def generate_chart_spec(chart_type: Annotated[str, "El tipo de gráfico: line, bar, o scatter"], 
                        data_summary: Annotated[str, "Un string tipo JSON de los datos a graficar"],
                        title: Annotated[str, "Título del gráfico"]) -> str:
    """
    Genera una especificación para un gráfico de Plotly.
    La salida debe ser un string JSON que describa la configuración del gráfico.
    """
    spec = {
        "type": chart_type,
        "data": data_summary,
        "title": title
    }
    return json.dumps(spec)
