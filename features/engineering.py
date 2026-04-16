"""
Feature Engineering Pipeline
Extrai e processa features de múltiplas fontes de dados
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta


class FeatureEngineer:
    """
    Pipeline centralizado de feature engineering
    
    Combina features de:
    - Transações (valores, tipos, frequências)
    - Temporal (horários, sazonalidade)
    - Geoespacial (distâncias, mobilidade)
    - Rede (grafos, relacionamentos)
    - Comunicações (NLP, sentimento)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize feature engineer
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.temporal_windows = config.get('features', {}).get('temporal_windows', [1, 24, 168, 720])
        
    def create_temporal_features(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create temporal features
        
        Args:
            transactions_df: DataFrame with transactions
            
        Returns:
            DataFrame with temporal features
        """
        df = transactions_df.copy()
        
        # Converter timestamp para datetime
        df['datetime'] = pd.to_datetime(df['timestamp'])
        
        # Extrair componentes temporais
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['day_of_month'] = df['datetime'].dt.day
        df['month'] = df['datetime'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_night'] = df['hour'].between(0, 5).astype(int)
        df['is_business_hours'] = df['hour'].between(9, 17).astype(int)
        
        # TODO: Adicionar mais features temporais
        # - time_since_last_transaction (por usuário)
        # - transactions_last_1h, 24h, 7d
        # - velocity features
        
        return df
    
    def create_aggregation_features(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Create aggregation features by user
        
        Args:
            transactions_df: DataFrame with transactions
            
        Returns:
            DataFrame with aggregation features
        """
        df = transactions_df.copy()
        
        # User-level lifetime aggregations
        user_agg = df.groupby('sender_id').agg({
            'amount': ['count', 'sum', 'mean', 'std', 'min', 'max'],
            'recipient_id': 'nunique',
            'transaction_type': lambda x: x.mode()[0] if len(x) > 0 else None
        }).reset_index()
        user_agg.columns = ['sender_id', 'user_tx_count', 'user_amount_sum', 'user_amount_mean', 
                            'user_amount_std', 'user_amount_min', 'user_amount_max', 
                            'user_unique_recipients', 'user_common_tx_type']
        df = df.merge(user_agg, on='sender_id', how='left')
        
        # Simple rolling windows by sender
        df = df.sort_values(['sender_id', 'datetime'])
        
        for window_hours in self.temporal_windows:
            # Count transactions in last N hours for each sender
            df[f'tx_count_{window_hours}h'] = 0
            df[f'amount_sum_{window_hours}h'] = 0.0
            
            for sender in df['sender_id'].unique():
                mask = df['sender_id'] == sender
                sender_df = df[mask].copy()
                
                for idx in sender_df.index:
                    current_time = df.loc[idx, 'datetime']
                    window_start = current_time - pd.Timedelta(hours=window_hours)
                    
                    # Count previous transactions in window
                    prev_mask = (sender_df['datetime'] >= window_start) & (sender_df['datetime'] < current_time)
                    df.loc[idx, f'tx_count_{window_hours}h'] = prev_mask.sum()
                    df.loc[idx, f'amount_sum_{window_hours}h'] = sender_df.loc[prev_mask, 'amount'].sum()
        
        return df
    
    def create_user_deviation_features(self, transactions_df: pd.DataFrame, 
                                       user_profiles: Dict[str, Any]) -> pd.DataFrame:
        """
        Create features based on deviation from user's normal behavior
        
        Args:
            transactions_df: DataFrame with transactions
            user_profiles: Dictionary with user profiles
            
        Returns:
            DataFrame with deviation features
        """
        df = transactions_df.copy()
        
        # Amount deviation from user mean
        df['amount_zscore'] = (df['amount'] - df['user_amount_mean']) / (df['user_amount_std'] + 1e-6)
        df['amount_ratio_to_avg'] = df['amount'] / (df['user_amount_mean'] + 1e-6)
        df['is_unusual_amount'] = (np.abs(df['amount_zscore']) > 2).astype(int)
        
        # User common hour detection
        user_hour_mode = df.groupby('sender_id')['hour'].transform(lambda x: x.mode()[0] if len(x) > 0 else 12)
        df['hour_deviation'] = np.abs(df['hour'] - user_hour_mode)
        df['is_unusual_hour'] = (df['hour_deviation'] > 6).astype(int)
        
        # Recipient frequency
        df['is_new_recipient'] = df.groupby(['sender_id', 'recipient_id']).cumcount()
        df['is_new_recipient'] = (df['is_new_recipient'] == 0).astype(int)
        
        return df
    
    def create_network_features(self, transactions_df: pd.DataFrame, 
                                graph_metrics: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Create network/graph features
        
        Args:
            transactions_df: DataFrame with transactions
            graph_metrics: Network metrics from NetworkAnalysisAgent
            
        Returns:
            DataFrame with network features
        """
        df = transactions_df.copy()
        
        # Relationship history
        df['sender_tx_to_recipient'] = df.groupby(['sender_id', 'recipient_id']).cumcount()
        df['is_new_relationship'] = (df['sender_tx_to_recipient'] == 0).astype(int)
        
        # Recipient frequency by sender
        df['recipient_frequency'] = df.groupby('recipient_id')['sender_id'].transform('count')
        df['sender_unique_recipients_ever'] = df.groupby('sender_id')['recipient_id'].transform('nunique')
        
        # Network degree approximation
        df['sender_degree'] = df.groupby('sender_id')['recipient_id'].transform('nunique')
        df['recipient_degree'] = df.groupby('recipient_id')['sender_id'].transform('nunique')
        
        return df
    
    def create_geospatial_features(self, transactions_df: pd.DataFrame,
                                   locations_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Create geospatial features
        
        Args:
            transactions_df: DataFrame with transactions
            locations_df: DataFrame with GPS data
            
        Returns:
            DataFrame with geospatial features
        """
        df = transactions_df.copy()
        
        # Default values if no location data
        df['no_recent_gps'] = 0
        df['gps_gap_hours'] = 0
        
        if locations_df is not None and len(locations_df) > 0:
            try:
                # Parse biotag from locations
                locations_df['datetime'] = pd.to_datetime(locations_df['timestamp'])
                
                # For each transaction, find if there's recent GPS data
                for idx in df.index:
                    sender = df.loc[idx, 'sender_id']
                    tx_time = df.loc[idx, 'datetime']
                    
                    # Get sender's GPS points
                    user_locs = locations_df[locations_df['biotag'] == sender]
                    if len(user_locs) == 0:
                        df.loc[idx, 'no_recent_gps'] = 1
                        df.loc[idx, 'gps_gap_hours'] = 999
                        continue
                    
                    # Find most recent GPS before transaction
                    prior_locs = user_locs[user_locs['datetime'] <= tx_time]
                    if len(prior_locs) == 0:
                        df.loc[idx, 'no_recent_gps'] = 1
                        df.loc[idx, 'gps_gap_hours'] = 999
                    else:
                        nearest = prior_locs.sort_values('datetime').iloc[-1]
                        hours_diff = (tx_time - nearest['datetime']).total_seconds() / 3600
                        df.loc[idx, 'gps_gap_hours'] = hours_diff
                        df.loc[idx, 'no_recent_gps'] = int(hours_diff > 24)
            except Exception as e:
                print(f"  Warning: GPS feature extraction failed: {e}")
        
        return df
    
    def create_all_features(self, transactions_df: pd.DataFrame,
                           locations_df: pd.DataFrame = None,
                           users_df: pd.DataFrame = None,
                           messages_df: pd.DataFrame = None,
                           conversations_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Create all features from all data sources
        
        Args:
            transactions_df: Main transactions data
            locations_df: GPS locations
            users_df: User demographics
            messages_df: Email data
            conversations_df: SMS data
            
        Returns:
            DataFrame with all engineered features
        """
        print("Creating features...")
        
        # Start with temporal features
        df = self.create_temporal_features(transactions_df)
        print(f"  OK Temporal features: {len(df.columns)} columns")
        
        # Aggregation features
        df = self.create_aggregation_features(df)
        print(f"  OK Aggregation features: {len(df.columns)} columns")
        
        # User deviation features
        df = self.create_user_deviation_features(df, users_df)
        print(f"  OK User deviation features: {len(df.columns)} columns")
        
        # Network features
        df = self.create_network_features(df)
        print(f"  OK Network features: {len(df.columns)} columns")
        
        # Geospatial features
        if locations_df is not None:
            df = self.create_geospatial_features(df, locations_df)
            print(f"  OK Geospatial features: {len(df.columns)} columns")
        
        print(f"Total features: {len(df.columns)}\n")
        
        return df
