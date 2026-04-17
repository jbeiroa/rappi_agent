import pytest
from src.agents.suggestion.tools import get_available_metrics
from unittest.mock import patch

def test_get_available_metrics(mock_excel_file):
    """Verify that get_available_metrics returns the expected metrics from shared state."""
    with patch('pathlib.Path.exists', return_value=True):
        metrics = get_available_metrics()
        # From mock data in conftest.py: 'Gross Profit UE', 'Perfect Orders', 'Orders'
        assert 'Gross Profit UE' in metrics
        assert 'Orders' in metrics
        assert len(metrics) == 3
