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
        # TODO: Implementar construção de perfis
        # 1. Agrupar por sender_id
        # 2. Calcular estatísticas: média, std, max, min valores
        # 3. Calcular frequência típica
        # 4. Identificar merchants/categorias habituais
        # 5. Salvar perfis em self.user_profiles
        
        print("Building user transaction profiles...")
        
        # Exemplo de agregações
        user_stats = transactions_df.groupby('sender_id').agg({
            'amount': ['mean', 'std', 'max', 'min', 'count'],
            'transaction_type': lambda x: x.mode()[0] if len(x) > 0 else None,
        })
        
        # TODO: Armazenar perfis mais detalhados
        self.user_profiles = user_stats.to_dict('index')
        
        print(f"✓ Built profiles for {len(self.user_profiles)} users")
    
    def predict(self, transaction: Dict[str, Any]) -> float:
        """
        Calculate fraud probability based on transaction patterns
        
        Args:
            transaction: Dictionary with transaction data
            
        Returns:
            float: Fraud probability [0, 1]
        """
        # TODO: Implementar detecção de anomalias
        # 1. Comparar valor com perfil do usuário
        # 2. Verificar frequência recente
        # 3. Detectar sequências suspeitas
        # 4. Verificar saldo vs histórico
        # 5. Retornar score de risco
        
        sender_id = transaction.get('sender_id')
        amount = transaction.get('amount', 0)
        
        # Placeholder: detectar valores muito altos
        if sender_id in self.user_profiles:
            profile = self.user_profiles[sender_id]
            avg_amount = profile.get('amount', {}).get('mean', 0)
            
            if avg_amount > 0 and amount > 3 * avg_amount:
                return 0.8  # High risk
            elif avg_amount > 0 and amount > 2 * avg_amount:
                return 0.6  # Medium risk
        
        return 0.3  # Default low risk
    
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
