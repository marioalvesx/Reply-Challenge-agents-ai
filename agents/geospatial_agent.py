"""
Geospatial Agent - Análise Geoespacial
Detecta impossibilidades físicas e desvios de localização
"""

from typing import Dict, Any
import pandas as pd
import numpy as np


class GeospatialAgent:
    """
    Agente especializado em análise geoespacial
    
    Features analisadas:
    - Impossibilidades físicas (transação muito distante de GPS recente)
    - Desvios de áreas habituais do usuário
    - Velocidade de deslocamento implausível
    - Densidade de transações por região
    - Padrões de mobilidade
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize geospatial agent
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.user_location_profiles = {}
        self.distance_threshold_km = config.get('features', {}).get('distance_threshold_km', 50)
        
    def build_location_profiles(self, locations_df: pd.DataFrame):
        """
        Build location profiles from GPS data
        
        Args:
            locations_df: DataFrame with GPS tracking data (BioTag, Datetime, Lat, Lng)
        """
        # TODO: Implementar construção de perfis de localização
        # 1. Identificar áreas habituais por usuário
        # 2. Calcular centro geográfico de atividade
        # 3. Identificar raio típico de movimento
        # 4. Detectar padrões de mobilidade
        
        print("Building location profiles...")
        
        if not locations_df.empty and 'BioTag' in locations_df.columns:
            # Calcular centroide de localização por usuário
            user_locations = locations_df.groupby('BioTag').agg({
                'Lat': ['mean', 'std'],
                'Lng': ['mean', 'std']
            })
            
            self.user_location_profiles = user_locations.to_dict('index')
            
        print(f"✓ Built location profiles for {len(self.user_location_profiles)} users")
    
    def calculate_distance_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        # Haversine formula
        R = 6371  # Earth radius in km
        
        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)
        
        a = np.sin(delta_lat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        
        distance = R * c
        return distance
    
    def predict(self, transaction: Dict[str, Any], recent_gps: Dict[str, Any] = None) -> float:
        """
        Calculate fraud probability based on geospatial analysis
        
        Args:
            transaction: Transaction data (must include location for in-person payments)
            recent_gps: Most recent GPS location for user
            
        Returns:
            float: Fraud probability [0, 1]
        """
        # TODO: Implementar detecção de anomalias geoespaciais
        # 1. Comparar localização de transação com GPS recente
        # 2. Calcular distância vs perfil do usuário
        # 3. Detectar impossibilidades físicas (ex: transação em Paris e GPS em São Paulo)
        # 4. Verificar velocidade de deslocamento
        
        # Apenas para transações presenciais
        if transaction.get('transaction_type') != 'in-person payment':
            return 0.3  # Not applicable
        
        # Placeholder: detectar se há dados de localização
        if 'location' not in transaction or not recent_gps:
            return 0.4  # No data to verify
        
        return 0.3  # Default
    
    def extract_features(self, transaction: Dict[str, Any], gps_history: pd.DataFrame = None) -> Dict[str, float]:
        """
        Extract geospatial features
        
        Args:
            transaction: Transaction data
            gps_history: GPS history for the user
            
        Returns:
            Dictionary of features
        """
        features = {}
        
        # TODO: Implementar extração de features geoespaciais
        # - distance_from_home
        # - distance_from_last_gps
        # - is_usual_area
        # - travel_speed_km_h (implausível se muito alta)
        # - region_fraud_density
        # - is_impossible_location (muito longe de GPS recente)
        
        return features
