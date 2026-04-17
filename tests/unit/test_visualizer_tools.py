import pytest
from src.agents.visualizer.tools import generate_chart_spec, ChartSpec
from pydantic import ValidationError
import json

def test_chart_spec_validation_success():
    """Verify ChartSpec validation works for valid inputs."""
    spec = ChartSpec(
        chart_type="line",
        data=[{"WEEK": "L1W", "Value": 10}],
        title="Test",
        x_axis="WEEK",
        y_axis=["Value"]
    )
    assert spec.chart_type == "line"
    assert spec.title == "Test"

def test_chart_spec_validation_invalid_type():
    """Verify it fails on invalid chart type."""
    with pytest.raises(ValidationError):
        ChartSpec(
            chart_type="pie",  # only line, bar, scatter allowed
            data=[],
            title="Title",
            x_axis="x",
            y_axis=["y"]
        )

def test_generate_chart_spec_output():
    """Verify generate_chart_spec returns correct JSON."""
    spec = ChartSpec(
        chart_type="bar",
        data=[{"ZONE": "Polanco", "Value": 5}],
        title="Insight",
        x_axis="ZONE",
        y_axis=["Value"]
    )
    output_json = generate_chart_spec(spec)
    output = json.loads(output_json)
    
    assert output["chart_type"] == "bar"
    assert output["x_axis"] == "ZONE"
    assert output["y_axis"] == ["Value"]
    assert isinstance(output["data"], list)
