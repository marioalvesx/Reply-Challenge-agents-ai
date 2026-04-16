"""
Orchestrator Agent - Coordenador do Sistema Multi-Agente
Gerencia o fluxo entre agentes especializados e agrega decisões
"""

from typing import Dict, List, Any
import numpy as np


class OrchestratorAgent:
    """
    Agente coordenador que gerencia os agentes especializados
    
    Responsabilidades:
    - Distribuir dados para agentes especializados
    - Agregar scores de risco de múltiplos agentes
    - Manter memória de padrões históricos
    - Calibrar pesos dos agentes baseado em performance
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize orchestrator
        
        Args:
            config: Configuration dictionary from config.yaml
        """
        self.config = config
        self.agent_weights = self._initialize_weights()
        self.agents = {}
        
    def _initialize_weights(self) -> Dict[str, float]:
        """
        Initialize agent weights from configuration
        
        Returns:
            Dictionary of agent names to weights
        """
        weights = {}
        agent_config = self.config.get('agents', {})
        
        for agent_name, agent_conf in agent_config.items():
            if agent_name != 'orchestrator' and agent_conf.get('enabled', False):
                weights[agent_name] = agent_conf.get('weight', 1.0)
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v/total_weight for k, v in weights.items()}
        
        return weights
    
    def register_agent(self, name: str, agent: Any):
        """
        Register a specialized agent
        
        Args:
            name: Agent name
            agent: Agent instance
        """
        self.agents[name] = agent
        print(f"✓ Registered agent: {name} (weight: {self.agent_weights.get(name, 0):.2f})")
    
    def predict(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fraud prediction by aggregating agent scores
        
        Args:
            transaction_data: Dictionary with transaction information
            
        Returns:
            Dictionary with prediction results
        """
        # TODO: Implement agent coordination
        # 1. Distribute data to all registered agents
        # 2. Collect risk scores from each agent
        # 3. Aggregate scores using weighted voting
        # 4. Apply threshold to make final decision
        
        agent_scores = {}
        
        # Collect scores from each agent
        for agent_name, agent in self.agents.items():
            if agent_name in self.agent_weights:
                try:
                    score = agent.predict(transaction_data)
                    agent_scores[agent_name] = score
                except Exception as e:
                    print(f"Warning: Agent {agent_name} failed: {e}")
                    agent_scores[agent_name] = 0.5  # neutral score
        
        # Weighted aggregation
        if agent_scores:
            final_score = sum(
                score * self.agent_weights.get(name, 0)
                for name, score in agent_scores.items()
            )
        else:
            final_score = 0.5
        
        return {
            'fraud_probability': final_score,
            'agent_scores': agent_scores,
            'is_fraud': final_score > 0.5  # TODO: Use optimized threshold
        }
    
    def update_weights(self, performance_metrics: Dict[str, float]):
        """
        Update agent weights based on performance
        
        Args:
            performance_metrics: Dictionary of agent names to performance scores
        """
        # TODO: Implement adaptive weight adjustment
        # Could use metrics like precision, recall, or economic cost per agent
        pass
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get information about registered agents
        
        Returns:
            Dictionary with agent information
        """
        return {
            'registered_agents': list(self.agents.keys()),
            'weights': self.agent_weights,
            'total_agents': len(self.agents)
        }
