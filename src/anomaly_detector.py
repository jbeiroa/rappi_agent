import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import mlflow
import mlflow.sklearn
from src.data_loader import DataLoader
import os
import logging

logger = logging.getLogger(__name__)

def get_enriched_data():
    """
    Enriches the operational data with:
    - WoW Change percentages.
    - Anomaly detection using IsolationForest.
    - Deterioration streaks (3+ weeks).
    - Benchmarking against zone type averages.
    - MLflow logging of metrics and models.
    """
    loader = DataLoader()
    df = loader.get_data()
    
    # 1. Sort and Calculate WoW Changes
    df = df.sort_values(['COUNTRY', 'CITY', 'ZONE', 'METRIC', 'WEEK_NUM'], ascending=True)
    df['PREV_VALUE'] = df.groupby(['COUNTRY', 'CITY', 'ZONE', 'METRIC'])['VALUE'].shift(1)
    # Avoid division by zero
    df['WOW_CHANGE'] = np.where(df['PREV_VALUE'] != 0, 
                                (df['VALUE'] - df['PREV_VALUE']) / df['PREV_VALUE'], 
                                0)
    
    # 2. Identify Worrying Metrics (3+ weeks deterioration)
    # All metrics (Lead Penetration, Perfect Order, Gross Profit UE, Orders) are "higher is better"
    df['IS_DETERIORATING'] = df['WOW_CHANGE'] < 0
    df['DETERIORATION_STREAK'] = df.groupby(['COUNTRY', 'CITY', 'ZONE', 'METRIC'])['IS_DETERIORATING'].transform(
        lambda x: x.rolling(window=3).sum()
    )
    df['WORRYING_METRIC'] = df['DETERIORATION_STREAK'] >= 3
    
    # 3. Isolation Forest Anomaly Detection
    features = ['VALUE', 'WOW_CHANGE']
    # Drop rows with NaNs in features for training (first week of every group has NaN WoW Change)
    train_df = df.dropna(subset=features).copy()
    
    # MLflow configuration
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("rappi_ops_anomaly_detection")
    
    try:
        with mlflow.start_run():
            contamination = 0.05
            model = IsolationForest(contamination=contamination, random_state=42)
            model.fit(train_df[features])
            
            # Log params, metrics and model
            mlflow.log_param("contamination", contamination)
            mlflow.log_param("features", features)
            
            # Predict
            train_df['IF_SCORE'] = model.decision_function(train_df[features])
            train_df['IS_ANOMALY'] = model.predict(train_df[features])
            # -1 is anomaly, 1 is normal
            train_df['IS_ANOMALY'] = train_df['IS_ANOMALY'] == -1
            
            mlflow.log_metric("num_anomalies", train_df['IS_ANOMALY'].sum())
            mlflow.log_metric("avg_wow_change", train_df['WOW_CHANGE'].mean())
            
            mlflow.sklearn.log_model(model, "isolation_forest_model")
            logger.info("MLflow run completed and model logged.")
    except Exception as e:
        logger.error(f"Failed to log to MLflow: {e}")
        # If MLflow fails, still run the model locally
        model = IsolationForest(contamination=0.05, random_state=42)
        model.fit(train_df[features])
        train_df['IS_ANOMALY'] = model.predict(train_df[features]) == -1

    # Merge anomaly info back to the main dataframe
    df = pd.merge(df, train_df[['COUNTRY', 'CITY', 'ZONE', 'METRIC', 'WEEK', 'IS_ANOMALY']], 
                  on=['COUNTRY', 'CITY', 'ZONE', 'METRIC', 'WEEK'], how='left')
    df['IS_ANOMALY'] = df['IS_ANOMALY'].fillna(False)
    
    # 4. Benchmarking (Zone Type Averages)
    avg_by_type = df.groupby(['ZONE_TYPE', 'METRIC', 'WEEK'])['VALUE'].mean().reset_index()
    avg_by_type.columns = ['ZONE_TYPE', 'METRIC', 'WEEK', 'TYPE_AVG_VALUE']
    df = pd.merge(df, avg_by_type, on=['ZONE_TYPE', 'METRIC', 'WEEK'], how='left')
    df['DIFF_FROM_TYPE_AVG'] = df['VALUE'] - df['TYPE_AVG_VALUE']
    df['PCT_DIFF_FROM_TYPE_AVG'] = np.where(df['TYPE_AVG_VALUE'] != 0,
                                           (df['VALUE'] - df['TYPE_AVG_VALUE']) / df['TYPE_AVG_VALUE'],
                                           0)
    
    return df

def get_correlations(df):
    """Computes a correlation matrix between operational metrics."""
    # Pivot to wide format: index by geographic keys and time, columns by metrics
    wide_df = df.pivot_table(index=['COUNTRY', 'CITY', 'ZONE', 'WEEK'], 
                             columns='METRIC', 
                             values='VALUE').reset_index()
    # Select only numeric columns for correlation
    metrics_cols = df['METRIC'].unique().tolist()
    available_metrics = [c for c in metrics_cols if c in wide_df.columns]
    corr_matrix = wide_df[available_metrics].corr()
    return corr_matrix

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    enriched_df = get_enriched_data()
    print("Enriched Data Sample (Anomalies & Worrying):")
    print(enriched_df[enriched_df['IS_ANOMALY'] | enriched_df['WORRYING_METRIC']].head())
    
    print("\nCorrelations:")
    print(get_correlations(enriched_df))
