# src/agents/suggestion/tools.py

from src.agents.shared_state import get_metrics_list
from typing import List

def get_available_metrics() -> List[str]:
    """
    Retorna la lista de todas las métricas disponibles en el dataset.
    Útil para sugerir otras variables que el usuario podría analizar.
    """
    return get_metrics_list()
