import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_metrics_df():
    data = {
        'COUNTRY': ['Mexico', 'Mexico'],
        'CITY': ['CDMX', 'CDMX'],
        'ZONE': ['Polanco', 'Polanco'],
        'ZONE_TYPE': ['Wealthy', 'Wealthy'],
        'ZONE_PRIORITIZATION': [1, 1],
        'METRIC': ['Gross Profit UE', 'Perfect Orders']
    }
    # Add all weeks L8W_ROLL to L0W_ROLL
    for i in range(9):
        data[f'L{i}W_ROLL'] = [2.5 + 0.1*i, 88.0 + i]
    return pd.DataFrame(data)

@pytest.fixture
def mock_orders_df():
    data = {
        'COUNTRY': ['Mexico'],
        'CITY': ['CDMX'],
        'ZONE': ['Polanco']
    }
    # Add all weeks L8W to L0W
    for i in range(9):
        data[f'L{i}W'] = [100 + 10*i]
    return pd.DataFrame(data)

@pytest.fixture
def mock_excel_file(mock_metrics_df, mock_orders_df):
    """Mocks pd.ExcelFile and its sheet reading."""
    with patch('pandas.ExcelFile') as mock_xl:
        mock_instance = mock_xl.return_value
        mock_instance.sheet_names = ['RAW_INPUT_METRICS', 'RAW_ORDERS']
        
        # Define side_effect for read_excel to return different DFs based on sheet name
        def side_effect(xl_file, sheet_name=None, **kwargs):
            if sheet_name == 'RAW_INPUT_METRICS':
                return mock_metrics_df
            if sheet_name == 'RAW_ORDERS':
                return mock_orders_df
            return None
            
        with patch('pandas.read_excel', side_effect=side_effect) as mock_read:
            yield mock_read
