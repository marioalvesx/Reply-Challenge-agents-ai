"""
Transaction Pattern Agent - Análise de Padrões Transacionais
Detecta anomalias em valores, frequências e sequências de transações
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


class TransactionPatternAgent:
    """
    Agente especializado em análise de padrões transacionais
    
    Features analisadas:
    - Valores de transações vs histórico do usuário
    - Frequência de transações em janelas temporais
    - Sequências incomuns de tipos de transação
    - Desvios de saldo
    - Primeiro uso de merchants/categorias
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize transaction pattern agent
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.user_profiles = {}  # Histórico de padrões por usuário
        
    def build_user_profile(self, transactions_df: pd.DataFrame):
        """
        Build user transaction profiles from historical data
        
        Args:
            transactions_df: DataFrame with transaction history
        """
        print("Building user transaction profiles...")
        
        # Convert timestamp to datetime
        df = transactions_df.copy()
        df['datetime'] = pd.to_datetime(df['timestamp'])
        
        # Aggregate statistics by sender
        for sender_id in df['sender_id'].unique():
            user_txs = df[df['sender_id'] == sender_id]
            
            self.user_profiles[sender_id] = {
                'amount_mean': user_txs['amount'].mean(),
                'amount_std': user_txs['amount'].std() or 0,
                'amount_max': user_txs['amount'].max(),
                'amount_min': user_txs['amount'].min(),
                'tx_count': len(user_txs),
                'common_tx_type': user_txs['transaction_type'].mode()[0] if len(user_txs) > 0 else None,
                'common_hour': user_txs['datetime'].dt.hour.mode()[0] if len(user_txs) > 0 else 12,
                'unique_recipients': user_txs['recipient_id'].nunique()
            }
        
        print(f"✓ Built profiles for {len(self.user_profiles)} users")
    
    def predict(self, transaction: Dict[str, Any]) -> float:
        """
        Calculate fraud probability based on transaction patterns
        
        Args:
            transaction: Dictionary with transaction data
            
        Returns:
            float: Fraud probability [0, 1]
        """
        sender_id = transaction.get('sender_id')
        amount = transaction.get('amount', 0)
        tx_type = transaction.get('transaction_type')
        
        if sender_id not in self.user_profiles:
            return 0.5  # Unknown user - neutral
        
        profile = self.user_profiles[sender_id]
        risk_score = 0.0
        
        # Amount deviation
        avg_amount = profile['amount_mean']
        if avg_amount > 0:
            ratio = amount / avg_amount
            if ratio > 3:
                risk_score += 0.3
            elif ratio > 2:
                risk_score += 0.2
            elif ratio > 1.5:
                risk_score += 0.1
        
        # Transaction type change
        if tx_type != profile['common_tx_type']:
            risk_score += 0.05
        
        return min(0.95, risk_score)
    
    def extract_features(self, transaction: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract transaction pattern features
        
        Args:
            transaction: Transaction data
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # TODO: Implementar extração de features
        # - amount_zscore: desvio do valor vs histórico
        # - frequency_1h, frequency_24h, frequency_7d
        # - amount_to_balance_ratio
        # - is_new_merchant
        # - is_new_transaction_type
        # - consecutive_transactions
        
        return features
