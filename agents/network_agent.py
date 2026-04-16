"""
Network Analysis Agent - Análise de Rede e Grafos
Detecta padrões suspeitos em relacionamentos entre usuários
"""

from typing import Dict, Any, Set
import pandas as pd
import networkx as nx


class NetworkAnalysisAgent:
    """
    Agente especializado em análise de rede
    
    Features analisadas:
    - Centralidade no grafo de transações
    - Comunidades suspeitas (clusters densamente conectados)
    - Ciclos de transações (A→B→C→A)
    - Novos relacionamentos vs estabelecidos
    - Padrões de lavagem de dinheiro (múltiplos hops)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize network analysis agent
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.transaction_graph = nx.DiGraph()
        self.user_centrality = {}
        self.communities = []
        
    def build_transaction_graph(self, transactions_df: pd.DataFrame):
        """
        Build directed graph from transaction history
        
        Args:
            transactions_df: DataFrame with transactions (sender_id, recipient_id, amount)
        """
        print("Building transaction network graph...")
        
        # Criar grafo direcionado de transações
        for _, row in transactions_df.iterrows():
            sender = row.get('sender_id')
            recipient = row.get('recipient_id')
            amount = row.get('amount', 0)
            
            if pd.notna(sender) and pd.notna(recipient):
                # Adicionar aresta (ou incrementar peso se já existe)
                if self.transaction_graph.has_edge(sender, recipient):
                    self.transaction_graph[sender][recipient]['weight'] += amount
                    self.transaction_graph[sender][recipient]['count'] += 1
                else:
                    self.transaction_graph.add_edge(sender, recipient, weight=amount, count=1)
        
        # Calcular métricas de centralidade
        if len(self.transaction_graph.nodes()) > 0:
            try:
                self.user_centrality['degree'] = nx.degree_centrality(self.transaction_graph)
                self.user_centrality['betweenness'] = nx.betweenness_centrality(self.transaction_graph)
                # PageRank pode identificar nós importantes
                self.user_centrality['pagerank'] = nx.pagerank(self.transaction_graph)
            except:
                print("Warning: Could not calculate all centrality metrics")
        
        print(f"✓ Built graph with {self.transaction_graph.number_of_nodes()} nodes and {self.transaction_graph.number_of_edges()} edges")
    
    def detect_cycles(self, max_length: int = 5) -> list:
        """
        Detect cycles in transaction graph (potential money laundering)
        
        Args:
            max_length: Maximum cycle length to search
            
        Returns:
            List of cycles found
        """
        # TODO: Implementar detecção de ciclos
        # Ciclos podem indicar lavagem de dinheiro: A→B→C→A
        cycles = []
        
        try:
            # NetworkX tem funções para detectar ciclos
            simple_cycles = list(nx.simple_cycles(self.transaction_graph))
            cycles = [c for c in simple_cycles if len(c) <= max_length]
        except:
            pass
        
        return cycles
    
    def predict(self, transaction: Dict[str, Any]) -> float:
        """
        Calculate fraud probability based on network analysis
        
        Args:
            transaction: Transaction data
            
        Returns:
            float: Fraud probability [0, 1]
        """
        # TODO: Implementar detecção de anomalias de rede
        # 1. Verificar se é novo relacionamento
        # 2. Calcular centralidade dos envolvidos
        # 3. Detectar se faz parte de ciclo suspeito
        # 4. Verificar padrões de comunidade
        
        sender = transaction.get('sender_id')
        recipient = transaction.get('recipient_id')
        
        risk_score = 0.3  # Default
        
        # Verificar se é novo relacionamento
        if sender and recipient:
            if not self.transaction_graph.has_edge(sender, recipient):
                risk_score += 0.2  # Novo relacionamento aumenta risco
            
            # Verificar centralidade (nós muito centrais podem ser suspeitos)
            if sender in self.user_centrality.get('degree', {}):
                degree = self.user_centrality['degree'][sender]
                if degree > 0.1:  # Muito conectado
                    risk_score += 0.1
        
        return min(risk_score, 1.0)
    
    def extract_features(self, transaction: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract network features
        
        Args:
            transaction: Transaction data
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # TODO: Implementar extração de features de rede
        # - sender_degree_centrality
        # - sender_betweenness_centrality
        # - sender_pagerank
        # - recipient_degree_centrality
        # - is_new_relationship
        # - is_part_of_cycle
        # - community_id
        # - edge_weight (total transacionado anteriormente)
        # - edge_count (número de transações anteriores)
        
        return features
