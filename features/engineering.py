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
        # TODO: Implementar agregações por usuário
        # Por cada janela temporal (1h, 24h, 7d, 30d):
        # - count_transactions
        # - sum_amount
        # - mean_amount
        # - std_amount
        # - max_amount
        # - unique_recipients
        # - unique_merchants
        
        pass
    
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
        # TODO: Implementar features de desvio
        # - amount_zscore: (amount - user_mean) / user_std
        # - amount_ratio_to_avg: amount / user_avg_amount
        # - is_unusual_hour
        # - is_unusual_merchant
        # - is_unusual_amount
        
        pass
    
    def create_network_features(self, transactions_df: pd.DataFrame, 
                                graph_metrics: Dict[str, Any]) -> pd.DataFrame:
        """
        Create network/graph features
        
        Args:
            transactions_df: DataFrame with transactions
            graph_metrics: Network metrics from NetworkAnalysisAgent
            
        Returns:
            DataFrame with network features
        """
        # TODO: Implementar features de rede
        # - sender_degree_centrality
        # - sender_pagerank
        # - recipient_degree_centrality
        # - is_new_relationship
        # - previous_transaction_count
        # - previous_transaction_sum
        
        pass
    
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
        # TODO: Implementar features geoespaciais
        # - distance_from_last_gps_km
        # - is_impossible_location (> 50km de GPS recente)
        # - travel_speed_km_h
        # - is_usual_area
        
        pass
    
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
        
        # TODO: Adicionar todas as outras features
        # - Aggregation features
        # - User deviation features
        # - Network features
        # - Geospatial features
        # - NLP features (if communication data available)
        
        print(f"✓ Created {len(df.columns)} features")
        
        return df
