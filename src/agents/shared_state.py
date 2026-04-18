from src.anomaly_detector import get_enriched_data
import os

# Cache for enriched data
_enriched_df = None

def get_combined_data():
    """Returns the enriched combined dataframe with anomalies and metrics."""
    global _enriched_df
    if _enriched_df is None:
        _enriched_df = get_enriched_data()
    return _enriched_df

def get_metrics_list():
    """Returns list of unique metrics."""
    df = get_combined_data()
    return df['METRIC'].unique().tolist()
