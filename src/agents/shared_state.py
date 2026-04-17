from src.data_loader import DataLoader
import os

# Global loader instance
_loader = DataLoader()

def get_combined_data():
    """Returns the processed combined dataframe."""
    return _loader.get_data()

def get_metrics_list():
    """Returns list of unique metrics."""
    df = get_combined_data()
    return df['METRIC'].unique().tolist()
