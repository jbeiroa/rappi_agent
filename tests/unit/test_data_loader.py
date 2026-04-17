import pytest
from src.data_loader import DataLoader
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd

def test_data_loader_file_not_found():
    """Verify FileNotFoundError is raised if file doesn't exist."""
    loader = DataLoader("non_existent_file.xlsx")
    with pytest.raises(FileNotFoundError):
        loader.load_raw_data()

def test_data_loader_processing(mock_excel_file):
    """Verify transformation from wide to long format."""
    with patch('pathlib.Path.exists', return_value=True):
        loader = DataLoader("mock.xlsx")
        df = loader.process_data()
        
        assert not df.empty
        # Check for expected columns
        assert 'WEEK' in df.columns
        assert 'VALUE' in df.columns
        assert 'WEEK_NUM' in df.columns
        
        # Verify WEEK_NUM mapping (e.g., L8W -> 8)
        assert df[df['WEEK'] == 'L8W']['WEEK_NUM'].iloc[0] == 8
        assert df[df['WEEK'] == 'L0W']['WEEK_NUM'].iloc[0] == 0

        # Verify combined metrics and orders
        metrics = df['METRIC'].unique()
        assert 'Gross Profit UE' in metrics
        assert 'Orders' in metrics

def test_geo_attributes_broadcast(mock_excel_file):
    """Verify geo attributes (ZONE_TYPE) are correctly broadcasted to Orders."""
    with patch('pathlib.Path.exists', return_value=True):
        loader = DataLoader("mock.xlsx")
        df = loader.process_data()
        
        # 'Orders' rows should have 'Wealthy' from 'Polanco' mapping
        orders_df = df[df['METRIC'] == 'Orders']
        assert all(orders_df['ZONE_TYPE'] == 'Wealthy')
        assert all(orders_df['CITY'] == 'CDMX')
