import pytest
from src.agents import shared_state
from unittest.mock import patch, MagicMock

def test_singleton_behavior(mock_excel_file):
    """Verify get_combined_data returns data and reuses loader."""
    with patch('pathlib.Path.exists', return_value=True):
        # First call triggers load/process
        df1 = shared_state.get_combined_data()
        assert not df1.empty
        
        # Second call should return the same object from the singleton loader
        df2 = shared_state.get_combined_data()
        assert df1 is df2

def test_get_metrics_list(mock_excel_file):
    """Verify get_metrics_list returns correct unique values."""
    with patch('pathlib.Path.exists', return_value=True):
        metrics = shared_state.get_metrics_list()
        assert 'Gross Profit UE' in metrics
        assert 'Perfect Orders' in metrics
        assert 'Orders' in metrics
        assert len(metrics) == 3
