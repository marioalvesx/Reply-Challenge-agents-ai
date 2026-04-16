"""
Ensemble Model for Fraud Detection
Combina múltiplos modelos para robustez e adaptabilidade
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


class FraudEnsemble:
    """
    Ensemble de modelos para detecção de fraudes
    
    Modelos incluídos:
    - XGBoost (gradient boosting)
    - LightGBM (gradient boosting otimizado)
    - CatBoost (categóricas nativas)
    - Random Forest (robustez)
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ensemble
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.models = {}
        self.model_weights = {}
        self.threshold = config.get('detection', {}).get('default_threshold', 0.5)
        self.feature_names = []
        
    def _initialize_models(self):
        """Initialize all models in the ensemble"""
        ensemble_config = self.config.get('training', {}).get('ensemble', {})
        
        if not ensemble_config.get('enabled', True):
            print("⚠️  Ensemble disabled in config")
            return
        
        for model_config in ensemble_config.get('models', []):
            if not model_config.get('enabled', True):
                continue
                
            model_name = model_config['name']
            weight = model_config.get('weight', 1.0)
            
            try:
                if model_name == 'xgboost':
                    import xgboost as xgb
                    self.models['xgboost'] = xgb.XGBClassifier(
                        n_estimators=100,
                        max_depth=6,
                        learning_rate=0.1,
                        random_state=42,
                        eval_metric='logloss'
                    )
                    self.model_weights['xgboost'] = weight
                    
                elif model_name == 'lightgbm':
                    import lightgbm as lgb
                    self.models['lightgbm'] = lgb.LGBMClassifier(
                        n_estimators=100,
                        max_depth=6,
                        learning_rate=0.1,
                        random_state=42
                    )
                    self.model_weights['lightgbm'] = weight
                    
                elif model_name == 'catboost':
                    from catboost import CatBoostClassifier
                    self.models['catboost'] = CatBoostClassifier(
                        iterations=100,
                        depth=6,
                        learning_rate=0.1,
                        random_state=42,
                        verbose=False
                    )
                    self.model_weights['catboost'] = weight
                    
                elif model_name == 'random_forest':
                    from sklearn.ensemble import RandomForestClassifier
                    self.models['random_forest'] = RandomForestClassifier(
                        n_estimators=100,
                        max_depth=10,
                        random_state=42,
                        n_jobs=-1
                    )
                    self.model_weights['random_forest'] = weight
                    
            except ImportError:
                print(f"⚠️  Could not import {model_name}, skipping...")
        
        # Normalize weights
        total_weight = sum(self.model_weights.values())
        if total_weight > 0:
            self.model_weights = {k: v/total_weight for k, v in self.model_weights.items()}
        
        print(f"✓ Initialized {len(self.models)} models")
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, Any]:
        """
        Train all models in ensemble
        
        Args:
            X: Feature matrix
            y: Target labels (0 = legitimate, 1 = fraud)
            
        Returns:
            Dictionary with training metrics
        """
        print("\nTraining ensemble models...")
        
        self.feature_names = X.columns.tolist()
        self._initialize_models()
        
        # Handle class imbalance
        imbalance_config = self.config.get('training', {})
        if imbalance_config.get('handle_imbalance', True):
            # TODO: Implementar SMOTE ou class_weight
            pass
        
        # Train each model
        metrics = {}
        for model_name, model in self.models.items():
            print(f"  Training {model_name}...")
            
            try:
                model.fit(X, y)
                
                # Calculate training metrics
                y_pred = model.predict(X)
                y_proba = model.predict_proba(X)[:, 1]
                
                from sklearn.metrics import accuracy_score, precision_score, recall_score
                metrics[model_name] = {
                    'accuracy': accuracy_score(y, y_pred),
                    'precision': precision_score(y, y_pred, zero_division=0),
                    'recall': recall_score(y, y_pred, zero_division=0)
                }
                
                print(f"    ✓ {model_name}: Accuracy={metrics[model_name]['accuracy']:.3f}")
                
            except Exception as e:
                print(f"    ✗ {model_name} failed: {e}")
        
        return metrics
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict fraud probabilities using weighted ensemble
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of fraud probabilities
        """
        if not self.models:
            raise ValueError("Models not trained. Call train() first.")
        
        # Collect predictions from each model
        predictions = []
        weights = []
        
        for model_name, model in self.models.items():
            try:
                proba = model.predict_proba(X)[:, 1]
                predictions.append(proba)
                weights.append(self.model_weights.get(model_name, 1.0))
            except Exception as e:
                print(f"Warning: {model_name} prediction failed: {e}")
        
        if not predictions:
            raise ValueError("No models could make predictions")
        
        # Weighted average
        predictions = np.array(predictions)
        weights = np.array(weights)
        weights = weights / weights.sum()  # Normalize
        
        ensemble_proba = np.average(predictions, axis=0, weights=weights)
        
        return ensemble_proba
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict fraud labels using optimized threshold
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of predictions (0 or 1)
        """
        proba = self.predict_proba(X)
        return (proba >= self.threshold).astype(int)
    
    def optimize_threshold(self, X: pd.DataFrame, y: pd.Series,
                          cost_fp: float = 1, cost_fn: float = 5) -> Tuple[float, float]:
        """
        Optimize decision threshold based on economic cost
        
        Args:
            X: Feature matrix
            y: True labels
            cost_fp: Cost of false positive
            cost_fn: Cost of false negative
            
        Returns:
            Tuple of (optimal_threshold, min_cost)
        """
        from utils.metrics import find_optimal_threshold
        
        y_proba = self.predict_proba(X)
        optimal_threshold, min_cost = find_optimal_threshold(
            y, y_proba, cost_fp, cost_fn
        )
        
        self.threshold = optimal_threshold
        
        print(f"✓ Optimized threshold: {optimal_threshold:.3f} (cost: {min_cost:.2f})")
        
        return optimal_threshold, min_cost
    
    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance from models
        
        Args:
            top_n: Number of top features to return
            
        Returns:
            DataFrame with feature importances
        """
        # TODO: Implementar agregação de feature importance
        # de múltiplos modelos
        pass
