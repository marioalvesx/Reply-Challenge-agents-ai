"""
Custom metrics for fraud detection with asymmetric costs
"""

import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix


def calculate_economic_cost(y_true, y_pred, cost_fp=1, cost_fn=5):
    """
    Calculate economic cost considering asymmetric costs
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        cost_fp (float): Cost of false positive (blocking legitimate transaction)
        cost_fn (float): Cost of false negative (allowing fraud)
        
    Returns:
        float: Total economic cost
    """
    cm = confusion_matrix(y_true, y_pred)
    # cm[0,1] = False Positives, cm[1,0] = False Negatives
    fp = cm[0, 1] if cm.shape == (2, 2) else 0
    fn = cm[1, 0] if cm.shape == (2, 2) else 0
    
    total_cost = (fp * cost_fp) + (fn * cost_fn)
    return total_cost


def calculate_metrics(y_true, y_pred, y_proba=None, cost_fp=1, cost_fn=5):
    """
    Calculate comprehensive metrics for fraud detection
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional)
        cost_fp (float): Cost of false positive
        cost_fn (float): Cost of false negative
        
    Returns:
        dict: Dictionary with all metrics
    """
    metrics = {}
    
    # Basic metrics
    metrics['precision'] = precision_score(y_true, y_pred, zero_division=0)
    metrics['recall'] = recall_score(y_true, y_pred, zero_division=0)
    metrics['f1_score'] = f1_score(y_true, y_pred, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        metrics['true_negatives'] = tn
        metrics['false_positives'] = fp
        metrics['false_negatives'] = fn
        metrics['true_positives'] = tp
        
        # Derived metrics
        metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0
        metrics['false_positive_rate'] = fp / (fp + tn) if (fp + tn) > 0 else 0
        metrics['false_negative_rate'] = fn / (fn + tp) if (fn + tp) > 0 else 0
    
    # Economic cost
    metrics['economic_cost'] = calculate_economic_cost(y_true, y_pred, cost_fp, cost_fn)
    
    # ROC-AUC if probabilities provided
    if y_proba is not None:
        from sklearn.metrics import roc_auc_score
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_proba)
        except:
            metrics['roc_auc'] = None
    
    return metrics


def print_metrics(metrics):
    """
    Pretty print metrics
    
    Args:
        metrics (dict): Metrics dictionary
    """
    print(f"\n{'='*60}")
    print(f"FRAUD DETECTION METRICS")
    print(f"{'='*60}")
    
    print(f"\nAccuracy Metrics:")
    print(f"  Precision:       {metrics.get('precision', 0):.4f}")
    print(f"  Recall:          {metrics.get('recall', 0):.4f}")
    print(f"  F1-Score:        {metrics.get('f1_score', 0):.4f}")
    
    if 'roc_auc' in metrics and metrics['roc_auc'] is not None:
        print(f"  ROC-AUC:         {metrics['roc_auc']:.4f}")
    
    print(f"\nConfusion Matrix:")
    if 'true_positives' in metrics:
        print(f"  True Positives:  {metrics['true_positives']}")
        print(f"  True Negatives:  {metrics['true_negatives']}")
        print(f"  False Positives: {metrics['false_positives']}")
        print(f"  False Negatives: {metrics['false_negatives']}")
    
    print(f"\nError Rates:")
    if 'false_positive_rate' in metrics:
        print(f"  FP Rate:         {metrics['false_positive_rate']:.4f}")
        print(f"  FN Rate:         {metrics['false_negative_rate']:.4f}")
    
    print(f"\nEconomic Impact:")
    print(f"  Total Cost:      {metrics.get('economic_cost', 0):.2f}")
    
    print(f"{'='*60}\n")


def find_optimal_threshold(y_true, y_proba, cost_fp=1, cost_fn=5, thresholds=None):
    """
    Find optimal threshold that minimizes economic cost
    
    Args:
        y_true: True labels
        y_proba: Predicted probabilities
        cost_fp (float): Cost of false positive
        cost_fn (float): Cost of false negative
        thresholds: List of thresholds to test (default: 0.1 to 0.9 in steps of 0.05)
        
    Returns:
        tuple: (optimal_threshold, min_cost)
    """
    if thresholds is None:
        thresholds = np.arange(0.1, 0.95, 0.05)
    
    min_cost = float('inf')
    optimal_threshold = 0.5
    
    for threshold in thresholds:
        y_pred = (y_proba >= threshold).astype(int)
        cost = calculate_economic_cost(y_true, y_pred, cost_fp, cost_fn)
        
        if cost < min_cost:
            min_cost = cost
            optimal_threshold = threshold
    
    return optimal_threshold, min_cost
