import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    def __init__(self, file_path: str = "data/dummy_data.xlsx"):
        self.file_path = Path(file_path)
        self._metrics_df = None
        self._orders_df = None
        self._combined_df = None

    def load_raw_data(self):
        """Loads raw data from Excel sheets."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Data file not found at {self.file_path}")
        
        xl = pd.ExcelFile(self.file_path)
        self._metrics_df = pd.read_excel(xl, 'RAW_INPUT_METRICS')
        self._orders_df = pd.read_excel(xl, 'RAW_ORDERS')
        return self._metrics_df, self._orders_df

    def process_data(self):
        """Transforms wide-format metrics and orders into a long-format combined dataframe."""
        if self._metrics_df is None or self._orders_df is None:
            self.load_raw_data()

        # 1. Process Metrics
        # Identify week columns (L8W to L0W)
        # Note: In the excel they are named L8W_ROLL, L7W_ROLL...
        metric_cols = [c for c in self._metrics_df.columns if '_ROLL' in c]
        id_cols_metrics = [c for c in self._metrics_df.columns if '_ROLL' not in c]
        
        metrics_long = self._metrics_df.melt(
            id_vars=id_cols_metrics,
            value_vars=metric_cols,
            var_name='WEEK',
            value_name='VALUE'
        )
        metrics_long['WEEK'] = metrics_long['WEEK'].str.replace('_ROLL', '')

        # 2. Process Orders
        order_cols = [f'L{i}W' for i in range(9)]
        id_cols_orders = [c for c in self._orders_df.columns if c not in order_cols and c != 'METRIC']
        
        orders_long = self._orders_df.melt(
            id_vars=id_cols_orders,
            value_vars=order_cols,
            var_name='WEEK',
            value_name='VALUE'
        )
        orders_long['METRIC'] = 'Orders'

        # 3. Combine
        # Ensure column names match for concatenation
        # Metrics has: COUNTRY, CITY, ZONE, ZONE_TYPE, ZONE_PRIORITIZATION, METRIC, WEEK, VALUE
        # Orders has: COUNTRY, CITY, ZONE, WEEK, VALUE, METRIC
        # We need to broadcast ZONE_TYPE and ZONE_PRIORITIZATION to orders if possible, 
        # but the assignment says they are separate. Let's merge instead of concat to keep geo attributes.
        
        geo_attributes = self._metrics_df[['COUNTRY', 'CITY', 'ZONE', 'ZONE_TYPE', 'ZONE_PRIORITIZATION']].drop_duplicates()
        
        # Add geo attributes to orders_long
        orders_long = pd.merge(orders_long, geo_attributes, on=['COUNTRY', 'CITY', 'ZONE'], how='left')
        
        # Combine metrics and orders
        self._combined_df = pd.concat([metrics_long, orders_long], ignore_index=True)
        
        # Clean WEEK to be numeric for easier sorting/filtering (0 is current, 8 is oldest)
        self._combined_df['WEEK_NUM'] = self._combined_df['WEEK'].str.extract(r'(\d+)').astype(int)
        
        return self._combined_df

    def get_data(self):
        if self._combined_df is None:
            self.process_data()
        return self._combined_df

if __name__ == "__main__":
    loader = DataLoader()
    df = loader.process_data()
    print("Combined Data Sample:")
    print(df.head())
    print("\nUnique Metrics Found:")
    print(df['METRIC'].unique())
    print("\nData Shape:", df.shape)
