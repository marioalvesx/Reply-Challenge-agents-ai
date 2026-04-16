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
        # TODO: Implementar construção de perfis temporais
        # 1. Extrair hora, dia da semana, mês
        # 2. Identificar padrões típicos por usuário
        # 3. Calcular distribuições horárias
        # 4. Identificar janelas de atividade normal
        
        print("Building temporal behavior profiles...")
        
        # Converter timestamp para datetime se necessário
        if 'timestamp' in transactions_df.columns:
            transactions_df['hour'] = pd.to_datetime(transactions_df['timestamp']).dt.hour
            transactions_df['day_of_week'] = pd.to_datetime(transactions_df['timestamp']).dt.dayofweek
            
            # Agrupar por usuário e calcular padrões
            user_temporal = transactions_df.groupby('sender_id').agg({
                'hour': lambda x: list(x),
                'day_of_week': lambda x: list(x)
            })
            
            self.user_temporal_profiles = user_temporal.to_dict('index')
            
        print(f"✓ Built temporal profiles for {len(self.user_temporal_profiles)} users")
    
    def predict(self, transaction: Dict[str, Any]) -> float:
        """
        Calculate fraud probability based on temporal behavior
        
        Args:
            transaction: Dictionary with transaction data
            
        Returns:
            float: Fraud probability [0, 1]
        """
        # TODO: Implementar detecção de anomalias temporais
        # 1. Verificar se horário é atípico para usuário
        # 2. Detectar múltiplas transações em curto período
        # 3. Verificar dia da semana vs padrão
        # 4. Calcular score de risco temporal
        
        sender_id = transaction.get('sender_id')
        timestamp = transaction.get('timestamp')
        
        if not timestamp:
            return 0.5
        
        # Placeholder: detectar transações noturnas (00:00 - 05:00)
        try:
            dt = pd.to_datetime(timestamp)
            hour = dt.hour
            
            if hour >= 0 and hour < 5:
                return 0.7  # Higher risk for late night transactions
            elif hour >= 22 or hour < 7:
                return 0.5  # Medium risk
        except:
            pass
        
        return 0.3  # Default
    
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
