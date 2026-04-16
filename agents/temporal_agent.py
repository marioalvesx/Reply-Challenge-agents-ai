"""
Temporal Behavior Agent - Análise de Comportamento Temporal
Detecta anomalias em padrões temporais e sazonalidade
"""

from typing import Dict, Any
import pandas as pd
from datetime import datetime, timedelta


class TemporalBehaviorAgent:
    """
    Agente especializado em análise temporal
    
    Features analisadas:
    - Horários atípicos para o usuário
    - Mudanças súbitas de padrão (dia → noite)
    - Atividade em dias incomuns (feriados, fins de semana)
    - Velocidade de transações (múltiplas em curto período)
    - Sazonalidade e tendências
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize temporal behavior agent
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.user_temporal_profiles = {}
        
    def build_temporal_profiles(self, transactions_df: pd.DataFrame):
        """
        Build temporal behavior profiles for users
        
        Args:
            transactions_df: DataFrame with transaction history
        """
        print("Building temporal behavior profiles...")
        
        # Convert timestamp to datetime
        df = transactions_df.copy()
        df['datetime'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        
        # Build profiles by user
        for sender_id in df['sender_id'].unique():
            user_txs = df[df['sender_id'] == sender_id]
            hours = user_txs['hour'].tolist()
            
            self.user_temporal_profiles[sender_id] = {
                'common_hours': list(set(hours)),
                'weekday_pref': user_txs[user_txs['day_of_week'] < 5].shape[0] > user_txs[user_txs['day_of_week'] >= 5].shape[0],
                'is_night_user': sum(1 for h in hours if 22 <= h or h < 6) > len(hours) * 0.3
            }
        
        print(f"✓ Built temporal profiles for {len(self.user_temporal_profiles)} users")
    
    def predict(self, transaction: Dict[str, Any]) -> float:
        """
        Calculate fraud probability based on temporal behavior
        
        Args:
            transaction: Dictionary with transaction data
            
        Returns:
            float: Fraud probability [0, 1]
        """
        sender_id = transaction.get('sender_id')
        timestamp = transaction.get('timestamp')
        
        if not timestamp:
            return 0.5
        
        try:
            dt = pd.to_datetime(timestamp)
            hour = dt.hour
            
            # Base risk from hour
            risk = 0.1
            if 0 <= hour < 6:
                risk += 0.3
            elif 22 <= hour < 24:
                risk += 0.2
            
            # Check user profile
            if sender_id in self.user_temporal_profiles:
                profile = self.user_temporal_profiles[sender_id]
                if hour not in profile['common_hours']:
                    risk += 0.15
                if not profile['is_night_user'] and (22 <= hour or hour < 6):
                    risk += 0.1
            
            return min(0.95, risk)
        except:
            return 0.5
    
    def extract_features(self, transaction: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract temporal features
        
        Args:
            transaction: Transaction data
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # TODO: Implementar extração de features temporais
        # - hour_of_day
        # - day_of_week
        # - is_weekend
        # - is_night (00:00-06:00)
        # - time_since_last_transaction
        # - transactions_last_1h
        # - transactions_last_24h
        # - is_unusual_hour_for_user
        
        return features
