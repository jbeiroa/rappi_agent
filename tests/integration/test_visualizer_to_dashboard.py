import pytest
from src.agents.visualizer.tools import generate_chart_spec, ChartSpec
from main import create_plotly_figure
import plotly.graph_objs as go
import json

def test_pipeline_visualizer_to_dashboard():
    """Verify end-to-end spec generation to Plotly rendering."""
    # 1. Agent generates a spec via the tool
    data = [
        {"WEEK": "L2W", "Sales": 100, "GP": 5},
        {"WEEK": "L1W", "Sales": 110, "GP": 6}
    ]
    spec_obj = ChartSpec(
        chart_type="line",
        data=data,
        title="Performance Trend",
        x_axis="WEEK",
        y_axis=["Sales", "GP"]
    )
    spec_json = generate_chart_spec(spec_obj)
    
    # 2. Main dashboard receives and parses the JSON
    parsed_spec = json.loads(spec_json)
    
    # 3. Main dashboard creates the figure
    fig = create_plotly_figure(parsed_spec)
    
    # 4. Assertions
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2  # One for Sales, one for GP
    assert fig.layout.title.text == "Performance Trend"
    assert fig.data[0].name == "Sales"
    assert fig.data[1].name == "GP"
    
    # Verify the X data matches
    assert list(fig.data[0].x) == ["L2W", "L1W"]
