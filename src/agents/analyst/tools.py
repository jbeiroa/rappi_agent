# src/agents/analyst/tools.py

from src.agents.shared_state import get_combined_data
from typing import Annotated
import pandas as pd

def run_pandas_query(python_code: Annotated[str, "Código Python válido para filtrar o agregar la variable 'df'. Debe retornar un string o un dict."]) -> str:
    """
    Ejecuta una consulta pandas sobre el dataset operacional (df).
    Ejemplo: df[df['METRIC'] == 'Orders'].groupby('CITY')['VALUE'].sum().to_dict()
    """
    df = get_combined_data()
    try:
        # Usamos un entorno restringido para seguridad
        local_vars = {'df': df, 'pd': pd}
        result = eval(python_code, {"__builtins__": {}}, local_vars)
        return str(result)
    except Exception as e:
        return f"Error ejecutando la consulta: {str(e)}"
