"""
Unsupervised Fraud Detection
Rule-based + statistical anomaly detection for unlabeled data
"""

import numpy as np
import pandas as pd
from typing import Dict, Any


class UnsupervisedFraudDetector:
    """
    Detect fraud without labeled training data using:
    - Statistical outliers (Z-scores, IQR)
    - Rule-based heuristics
    - Behavioral deviations
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize detector
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.detection_config = config.get('detection', {})
        self.min_fraud_rate = self.detection_config.get('min_fraud_detection_rate', 0.15)
        self.max_fraud_rate = self.detection_config.get('max_fraud_detection_rate', 0.40)
    
    def calculate_anomaly_scores(self, features_df: pd.DataFrame) -> np.ndarray:
        """
        Calculate composite anomaly score for each transaction
        
        Args:
            features_df: DataFrame with engineered features
            
        Returns:
            Array of anomaly scores (0-1, higher = more suspicious)
        """
        scores = np.zeros(len(features_df))
        weights = []
        
        # 1. Amount anomalies (Z-score based)
        if 'amount_zscore' in features_df.columns:
            amount_anomaly = np.abs(features_df['amount_zscore'].fillna(0))
            amount_anomaly = np.clip(amount_anomaly / 3, 0, 1)  # Normalize to 0-1
            scores += amount_anomaly * 0.25
            weights.append(0.25)
        
        # 2. Unusual timing
        timing_score = np.zeros(len(features_df))
        if 'is_night' in features_df.columns:
            timing_score += features_df['is_night'] * 0.5
        if 'is_weekend' in features_df.columns:
            timing_score += features_df['is_weekend'] * 0.3
        if 'is_unusual_hour' in features_df.columns:
            timing_score += features_df['is_unusual_hour'] * 0.7
        scores += timing_score * 0.15
        weights.append(0.15)
        
        # 3. Velocity anomalies (rapid transactions)
        velocity_score = np.zeros(len(features_df))
        for window in [1, 24]:
            col = f'tx_count_{window}h'
            if col in features_df.columns:
                velocity = features_df[col].fillna(0)
                # Flag if > 3 transactions in 1h or > 10 in 24h
                threshold = 3 if window == 1 else 10
                velocity_score += (velocity > threshold).astype(float) * (0.8 if window == 1 else 0.5)
        scores += np.clip(velocity_score, 0, 1) * 0.20
        weights.append(0.20)
        
        # 4. New recipient risk
        if 'is_new_recipient' in features_df.columns:
            new_recipient_score = features_df['is_new_recipient'] * 0.6
            scores += new_recipient_score * 0.10
            weights.append(0.10)
        
        # 5. Unusual amount for user
        if 'is_unusual_amount' in features_df.columns:
            scores += features_df['is_unusual_amount'] * 0.15
            weights.append(0.15)
        
        # 6. International transaction risk
        if 'is_international' in features_df.columns:
            scores += features_df['is_international'] * 0.10
            weights.append(0.10)
        
        # 7. GPS anomalies
        if 'no_recent_gps' in features_df.columns:
            scores += features_df['no_recent_gps'] * 0.05
            weights.append(0.05)
        
        # Normalize by total weights used
        total_weight = sum(weights) if weights else 1.0
        scores = scores / total_weight
        
        return np.clip(scores, 0, 1)
    
    def detect_fraud(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect fraudulent transactions
        
        Args:
            features_df: DataFrame with engineered features
            
        Returns:
            DataFrame with transaction_id and is_fraud columns
        """
        print("Running unsupervised fraud detection...")
        
        # Calculate anomaly scores
        scores = self.calculate_anomaly_scores(features_df)
        features_df['anomaly_score'] = scores
        
        # Determine threshold to achieve target fraud rate
        # Use percentile to hit between min and max fraud rate
        target_percentile = 100 - (self.min_fraud_rate * 100)
        threshold = np.percentile(scores, target_percentile)
        
        # Adjust if needed
        pred_fraud_rate = (scores >= threshold).mean()
        print(f"  Initial threshold: {threshold:.3f} → fraud rate: {pred_fraud_rate:.1%}")
        
        if pred_fraud_rate < self.min_fraud_rate:
            # Lower threshold
            target_percentile = 100 - (self.min_fraud_rate * 100)
            threshold = np.percentile(scores, target_percentile)
        elif pred_fraud_rate > self.max_fraud_rate:
            # Raise threshold
            target_percentile = 100 - (self.max_fraud_rate * 100)
            threshold = np.percentile(scores, target_percentile)
        
        # Apply threshold
        is_fraud = (scores >= threshold).astype(int)
        fraud_rate = is_fraud.mean()
        
        print(f"  Final threshold: {threshold:.3f}")
        print(f"  Detected frauds: {is_fraud.sum()} ({fraud_rate:.1%})")
        
        # Return results
        results = pd.DataFrame({
            'transaction_id': features_df['transaction_id'],
            'is_fraud': is_fraud,
            'anomaly_score': scores
        })
        
        return results
