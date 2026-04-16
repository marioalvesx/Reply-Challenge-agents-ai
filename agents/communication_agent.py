"""
Communication Agent - Análise de Comunicações (NLP)
Detecta coordenação suspeita em SMS e e-mails
"""

from typing import Dict, Any
import pandas as pd


class CommunicationAgent:
    """
    Agente especializado em análise de comunicações
    
    Features analisadas:
    - Palavras-chave suspeitas em SMS/emails
    - Coordenação temporal entre mensagens e transações
    - Sentimento de urgência
    - Padrões de linguagem associados a fraude
    - Densidade de comunicação vs transações
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize communication agent
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.nlp_enabled = config.get('features', {}).get('nlp_enabled', True)
        self.suspicious_keywords = self._load_suspicious_keywords()
        
    def _load_suspicious_keywords(self) -> set:
        """
        Load list of suspicious keywords
        
        Returns:
            Set of suspicious keywords
        """
        # TODO: Expandir lista baseado em análise de dados
        keywords = {
            # Urgência
            'urgent', 'immediately', 'now', 'quick', 'hurry', 'asap',
            # Fraude comum
            'transfer', 'verify', 'account', 'password', 'pin', 'code',
            'winner', 'prize', 'lottery', 'refund', 'tax',
            # Coordenação
            'do it', 'send to', 'split', 'share', 'divide',
            # Português
            'urgente', 'agora', 'imediato', 'senha', 'código', 'transferir'
        }
        return keywords
    
    def analyze_messages(self, user_id: str, messages_df: pd.DataFrame, 
                        conversations_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze SMS and email communications for a user
        
        Args:
            user_id: User identifier
            messages_df: DataFrame with email threads
            conversations_df: DataFrame with SMS threads
            
        Returns:
            Dictionary with communication analysis
        """
        analysis = {
            'has_suspicious_keywords': False,
            'urgency_score': 0.0,
            'communication_frequency': 0,
            'suspicious_patterns': []
        }
        
        # TODO: Implementar análise de NLP
        # 1. Filtrar mensagens do usuário
        # 2. Detectar palavras-chave suspeitas
        # 3. Análise de sentimento (urgência, medo)
        # 4. Correlação temporal com transações
        
        if not self.nlp_enabled:
            return analysis
        
        # Placeholder: detectar keywords simples
        user_messages = []
        
        if messages_df is not None and 'user_id' in messages_df.columns:
            user_emails = messages_df[messages_df['user_id'] == user_id]
            user_messages.extend(user_emails['mail'].tolist() if 'mail' in user_emails else [])
        
        if conversations_df is not None and 'user_id' in conversations_df.columns:
            user_sms = conversations_df[conversations_df['user_id'] == user_id]
            user_messages.extend(user_sms['SMS'].tolist() if 'SMS' in user_sms else [])
        
        # Análise básica de keywords
        for message in user_messages:
            if isinstance(message, str):
                message_lower = message.lower()
                for keyword in self.suspicious_keywords:
                    if keyword in message_lower:
                        analysis['has_suspicious_keywords'] = True
                        analysis['suspicious_patterns'].append(keyword)
                        analysis['urgency_score'] += 0.1
        
        analysis['communication_frequency'] = len(user_messages)
        analysis['urgency_score'] = min(analysis['urgency_score'], 1.0)
        
        return analysis
    
    def predict(self, transaction: Dict[str, Any], communication_analysis: Dict[str, Any] = None) -> float:
        """
        Calculate fraud probability based on communication analysis
        
        Args:
            transaction: Transaction data
            communication_analysis: Pre-computed communication analysis
            
        Returns:
            float: Fraud probability [0, 1]
        """
        if not communication_analysis:
            return 0.3  # No data
        
        risk_score = 0.3
        
        # Aumentar risco se há keywords suspeitas
        if communication_analysis.get('has_suspicious_keywords'):
            risk_score += 0.3
        
        # Aumentar risco baseado em urgência
        urgency = communication_analysis.get('urgency_score', 0)
        risk_score += urgency * 0.2
        
        return min(risk_score, 1.0)
    
    def extract_features(self, user_id: str, messages_df: pd.DataFrame = None,
                        conversations_df: pd.DataFrame = None) -> Dict[str, float]:
        """
        Extract NLP features from communications
        
        Args:
            user_id: User identifier
            messages_df: Email data
            conversations_df: SMS data
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # TODO: Implementar extração de features NLP
        # - has_urgent_keywords
        # - sentiment_score
        # - message_frequency_24h
        # - avg_message_length
        # - has_coordination_language
        # - time_correlation_with_transactions
        
        return features
