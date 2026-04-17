# src/agents/visualizer/tools.py

from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Any
import json

class ChartSpec(BaseModel):
    chart_type: Literal["line", "bar", "scatter"] = Field(description="El tipo de gráfico: line, bar, o scatter")
    data: List[Dict[str, Any]] = Field(description="Los datos a graficar como una lista de diccionarios (orientación 'records')")
    title: str = Field(description="Título del gráfico")
    x_axis: str = Field(description="Nombre de la columna para el eje X (ej. 'WEEK')")
    y_axis: List[str] = Field(description="Nombres de las columnas numéricas para el eje Y (ej. ['Wealthy', 'Non Wealthy'])")

def generate_chart_spec(spec: ChartSpec) -> str:
    """
    Genera una especificación para un gráfico de Plotly.
    La salida debe ser un string JSON que describa la configuración del gráfico.
    """
    return json.dumps(spec.model_dump())
