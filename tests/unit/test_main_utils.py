import pytest
import pandas as pd
from main import (
    try_parse_natural_language_data, 
    parse_chart_spec_from_text, 
    create_plotly_figure
)
import plotly.graph_objs as go

def test_try_parse_natural_language_data():
    """Verify parsing of 'Semanas: ... Valores: ...' format."""
    text = "Semanas: L1W, L2W, Valores: 10, 20.5"
    df = try_parse_natural_language_data(text)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.iloc[0]['Semana'] == 'L1W'
    assert df.iloc[0]['Valor'] == 10
    assert df.iloc[1]['Valor'] == 20.5

def test_parse_chart_spec_from_text():
    """Verify extraction of JSON block from markdown text."""
    text = "Here's the data:\n```json\n{\"type\": \"line\", \"data\": [], \"title\": \"Trend\"}\n```\nInsight..."
    spec = parse_chart_spec_from_text(text)
    
    assert spec is not None
    assert spec["type"] == "line"
    assert spec["title"] == "Trend"

def test_create_plotly_figure_unwrap():
    """Verify that create_plotly_figure unwraps nested 'spec' and handles fallbacks."""
    # Simulation of nested spec
    nested_spec = {
        "spec": {
            "chart_type": "line",
            "data": [{"x": 1, "y": 10}, {"x": 2, "y": 20}],
            "title": "Nested Plot",
            "x_axis": "x",
            "y_axis": ["y"]
        }
    }
    fig = create_plotly_figure(nested_spec)
    
    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == "Nested Plot"

def test_create_plotly_figure_fallback_y():
    """Verify it filters numeric columns if y_axis is missing/invalid."""
    data = [
        {"DATE": "2024-01-01", "CITY": "CDMX", "Value1": 10, "Value2": 20},
        {"DATE": "2024-01-02", "CITY": "CDMX", "Value1": 12, "Value2": 22}
    ]
    spec = {
        "chart_type": "bar",
        "data": data,
        "title": "Safe Bar",
        "x_axis": "DATE"
        # y_axis is missing, should pick Value1 and Value2, ignore CITY
    }
    fig = create_plotly_figure(spec)
    assert isinstance(fig, go.Figure)
    # Trace count should be 2 (Value1 and Value2)
    assert len(fig.data) == 2
    assert fig.data[0].name == "Value1"
    assert fig.data[1].name == "Value2"
