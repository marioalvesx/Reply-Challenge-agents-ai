"""
Validation utilities for Reply Mirror Challenge
"""

import pandas as pd
from pathlib import Path


def validate_output_format(output_file):
    """
    Validate that output file meets challenge requirements
    
    Requirements:
    - ASCII text file
    - One Transaction ID per line
    - Not empty (> 0% reported)
    - Not all transactions (< 100% reported)
    - At least 15% of frauds correctly identified (requires ground truth)
    
    Args:
        output_file (str): Path to output file
        
    Returns:
        tuple: (is_valid, error_message)
    """
    file_path = Path(output_file)
    
    # Check file exists
    if not file_path.exists():
        return False, f"Output file not found: {output_file}"
    
    # Read file
    try:
        with open(file_path, 'r', encoding='ascii') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        return False, "File is not ASCII encoded"
    except Exception as e:
        return False, f"Error reading file: {e}"
    
    # Remove empty lines
    transaction_ids = [line.strip() for line in lines if line.strip()]
    
    # Check not empty
    if len(transaction_ids) == 0:
        return False, "Output is empty (0% transactions reported) - INVALID"
    
    # Check format (should be UUIDs)
    for i, tid in enumerate(transaction_ids):
        if not tid:
            return False, f"Line {i+1}: Empty transaction ID"
        # Basic validation - should be UUID format
        if len(tid) < 10:
            return False, f"Line {i+1}: Invalid transaction ID format: {tid}"
    
    print(f"✓ Output format valid")
    print(f"  - {len(transaction_ids)} transactions flagged as fraudulent")
    print(f"  - All Transaction IDs are properly formatted")
    
    return True, None


def validate_detection_rate(output_file, ground_truth_file, min_rate=0.15):
    """
    Validate that at least min_rate of frauds are detected
    
    Args:
        output_file (str): Path to output file with predicted frauds
        ground_truth_file (str): Path to ground truth file
        min_rate (float): Minimum detection rate (default 0.15 = 15%)
        
    Returns:
        tuple: (is_valid, detection_rate, error_message)
    """
    # Read predictions
    with open(output_file, 'r') as f:
        predictions = set(line.strip() for line in f if line.strip())
    
    # Read ground truth
    try:
        gt_df = pd.read_csv(ground_truth_file)
        if 'is_fraud' not in gt_df.columns or 'transaction_id' not in gt_df.columns:
            return False, 0.0, "Ground truth file must have 'transaction_id' and 'is_fraud' columns"
        
        true_frauds = set(gt_df[gt_df['is_fraud'] == 1]['transaction_id'].astype(str))
    except Exception as e:
        return False, 0.0, f"Error reading ground truth: {e}"
    
    # Calculate detection rate
    detected_frauds = predictions.intersection(true_frauds)
    detection_rate = len(detected_frauds) / len(true_frauds) if len(true_frauds) > 0 else 0.0
    
    # Validate
    if detection_rate < min_rate:
        return False, detection_rate, f"Detection rate {detection_rate:.2%} < {min_rate:.2%} minimum - INVALID"
    
    print(f"✓ Detection rate: {detection_rate:.2%} (minimum: {min_rate:.2%})")
    print(f"  - Detected {len(detected_frauds)} out of {len(true_frauds)} frauds")
    
    return True, detection_rate, None


def validate_percentage_range(output_file, total_transactions):
    """
    Validate that output is not 0% or 100% of transactions
    
    Args:
        output_file (str): Path to output file
        total_transactions (int): Total number of transactions in dataset
        
    Returns:
        tuple: (is_valid, percentage, error_message)
    """
    with open(output_file, 'r') as f:
        flagged_count = sum(1 for line in f if line.strip())
    
    percentage = flagged_count / total_transactions if total_transactions > 0 else 0.0
    
    # Check boundaries
    if flagged_count == 0:
        return False, 0.0, "Output reports 0% of transactions - INVALID"
    
    if flagged_count == total_transactions:
        return False, 1.0, "Output reports 100% of transactions - INVALID"
    
    print(f"✓ Percentage check: {percentage:.2%} of transactions flagged")
    print(f"  - {flagged_count} out of {total_transactions} total transactions")
    
    return True, percentage, None
