#!/usr/bin/env python3
"""
Reply Mirror - AI Agent Challenge 2026
Main entry point for training and prediction
"""

import argparse
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_config():
    """Load configuration from config.yaml"""
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config


def train_mode(level, input_file, config):
    """
    Training mode - train models on training dataset
    
    Args:
        level (int): Challenge level (1-5)
        input_file (str): Path to training CSV file
        config (dict): Configuration dictionary
    """
    print(f"\n{'='*60}")
    print(f"TRAINING MODE - Level {level}")
    print(f"{'='*60}")
    print(f"Input file: {input_file}\n")
    
    import pandas as pd
    import json
    from pathlib import Path
    from features.engineering import FeatureEngineer
    from models.ensemble import FraudDetectionEnsemble
    from utils.metrics import find_optimal_threshold
    
    # Load data
    print("Loading data...")
    transactions = pd.read_csv(input_file)
    print(f"  OK Transactions: {len(transactions)} rows")
    
    # Load auxiliary data
    data_dir = Path(input_file).parent
    locations = None
    users = None
    
    if (data_dir / 'locations.json').exists():
        with open(data_dir / 'locations.json') as f:
            locations = pd.DataFrame(json.load(f))
        print(f"  OK Locations: {len(locations)} rows")
    
    if (data_dir / 'users.json').exists():
        with open(data_dir / 'users.json') as f:
            users = pd.DataFrame(json.load(f))
        print(f"  OK Users: {len(users)} rows")
    
    print()
    
    # Feature engineering
    engineer = FeatureEngineer(config)
    features_df = engineer.create_all_features(
        transactions,
        locations_df=locations,
        users_df=users
    )
    
    # Check if labels exist
    if 'is_fraud' in features_df.columns:
        # Supervised learning
        print("Training supervised model (labels found)...\n")
        
        # Prepare features and labels
        exclude_cols = [
            'transaction_id', 'is_fraud', 'timestamp', 'datetime', 'sender_id', 'recipient_id',
            'transaction_type', 'location', 'payment_method', 'sender_iban', 'recipient_iban',
            'balance_after', 'description', 'sender_country', 'recipient_country'
        ]
        feature_cols = [c for c in features_df.columns if c not in exclude_cols]
        
        X = features_df[feature_cols].fillna(0)
        y = features_df['is_fraud']
        
        print(f"Training with {len(feature_cols)} features on {len(X)} samples")
        print(f"Fraud rate: {y.mean():.2%}\n")
        
        # Train ensemble
        ensemble = FraudDetectionEnsemble(config)
        metrics = ensemble.train(X, y)
        
        # Find optimal threshold
        y_pred_proba = ensemble.predict_proba(X)
        optimal_threshold = find_optimal_threshold(y, y_pred_proba, cost_fp=1, cost_fn=5)
        print(f"\nOptimal threshold: {optimal_threshold:.3f}")
        
        # Save models
        models_dir = Path('models/trained')
        models_dir.mkdir(parents=True, exist_ok=True)
        ensemble.save(models_dir / f'level{level}_ensemble.pkl')
        print(f"\nModels saved to {models_dir}/level{level}_ensemble.pkl")
    else:
        # Unsupervised learning
        print("WARNING: No labels found - using unsupervised anomaly detection")
        print("   Feature engineering complete. Use predict mode to detect fraud.\n")
    
    return True


def predict_mode(level, input_file, output_file, config):
    """
    Prediction mode - generate predictions on evaluation dataset
    
    Args:
        level (int): Challenge level (1-5)
        input_file (str): Path to evaluation CSV file
        output_file (str): Path to output file
        config (dict): Configuration dictionary
    """
    print(f"\n{'='*60}")
    print(f"PREDICTION MODE - Level {level}")
    print(f"{'='*60}")
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}\n")
    
    import pandas as pd
    import json
    from pathlib import Path
    from features.engineering import FeatureEngineer
    from models.unsupervised_detector import UnsupervisedFraudDetector
    
    # Check if trained model exists (supervised)
    models_path = Path(f'models/trained/level{level}_ensemble.pkl')
    use_supervised = models_path.exists()
    
    if use_supervised:
        from models.ensemble import FraudDetectionEnsemble
        ensemble = FraudDetectionEnsemble(config)
        ensemble.load(models_path)
        print(f"Loaded supervised model from {models_path}\n")
    else:
        print("WARNING: No trained model found - using unsupervised detection\n")
    
    # Load data
    print("\nLoading data...")
    transactions = pd.read_csv(input_file)
    print(f"  OK Transactions: {len(transactions)} rows")
    
    # Load auxiliary data
    data_dir = Path(input_file).parent
    locations = None
    users = None
    
    if (data_dir / 'locations.json').exists():
        with open(data_dir / 'locations.json') as f:
            locations = pd.DataFrame(json.load(f))
        print(f"  OK Locations: {len(locations)} rows")
    
    if (data_dir / 'users.json').exists():
        with open(data_dir / 'users.json') as f:
            users = pd.DataFrame(json.load(f))
        print(f"  OK Users: {len(users)} rows")
    
    print()
    
    # Feature engineering (same as training)
    engineer = FeatureEngineer(config)
    features_df = engineer.create_all_features(
        transactions,
        locations_df=locations,
        users_df=users
    )
    
    # Prepare features (same columns as training)
    exclude_cols = [
        'transaction_id', 'is_fraud', 'timestamp', 'datetime', 'sender_id', 'recipient_id',
        'transaction_type', 'location', 'payment_method', 'sender_iban', 'recipient_iban',
        'balance_after', 'description', 'sender_country', 'recipient_country'
    ]
    feature_cols = [c for c in features_df.columns if c not in exclude_cols]
    X = features_df[feature_cols].fillna(0)
    
    # Generate predictions
    
    if use_supervised:
        # Supervised prediction
        y_pred_proba = ensemble.predict_proba(X)
        threshold = config.get('detection', {}).get('default_threshold', 0.5)
        y_pred = (y_pred_proba >= threshold).astype(int)
        fraud_ids = features_df[y_pred == 1]['transaction_id'].tolist()
    else:
        # Unsupervised detection
        detector = UnsupervisedFraudDetector(config)
        results = detector.detect_fraud(features_df)
        fraud_ids = results[results['is_fraud'] == 1]['transaction_id'].tolist()
    
    print(f"\nDetected {len(fraud_ids)} potential frauds ({len(fraud_ids)/len(features_df):.1%})")
    
    # Save output in required format (one ID per line, ASCII)
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='ascii') as f:
        for txn_id in fraud_ids:
            f.write(f"{txn_id}\n")
    
    print(f"Output saved to {output_path}")
    
    return True


def validate_mode(input_file, total_transactions=None):
    """
    Validation mode - validate output file format
    
    Args:
        input_file (str): Path to output file to validate
        total_transactions (int): Total number of transactions (optional)
    """
    print(f"\n{'='*60}")
    print(f"VALIDATION MODE")
    print(f"{'='*60}")
    print(f"Validating: {input_file}")
    
    from utils.validation import validate_output_format, validate_percentage_range
    
    # Validate format
    is_valid, error = validate_output_format(input_file)
    
    if not is_valid:
        print(f"\nERROR: VALIDATION FAILED: {error}")
        return False
    
    # Validate percentage if total provided
    if total_transactions:
        is_valid, percentage, error = validate_percentage_range(input_file, total_transactions)
        
        if not is_valid:
            print(f"\nERROR: VALIDATION FAILED: {error}")
            return False
    
    print(f"\nVALIDATION PASSED")
    print(f"\nOutput file is ready for submission!")
    print(f"\nWARNING: REMEMBER: Only 1 submission per level - first submission is FINAL!")
    
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Reply Mirror Fraud Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Train on level 1
  python main.py --level 1 --mode train --input data/raw/level1_train.csv
  
  # Generate predictions for level 1
  python main.py --level 1 --mode predict --input data/raw/level1_eval.csv --output data/outputs/level1_output.txt
  
  # Validate output
  python main.py --mode validate --input data/outputs/level1_output.txt --total 10000
        """
    )
    
    parser.add_argument(
        "--level",
        type=int,
        help="Challenge level (1-5)"
    )
    parser.add_argument(
        "--mode",
        choices=["train", "predict", "validate"],
        required=True,
        help="Operation mode"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Input file path"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (required for predict mode)"
    )
    parser.add_argument(
        "--total",
        type=int,
        help="Total number of transactions (for validation mode)"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.mode in ["train", "predict"] and not args.level:
        print("ERROR: --level required for train and predict modes")
        sys.exit(1)
    
    if args.mode == "predict" and not args.output:
        print("ERROR: --output required for predict mode")
        sys.exit(1)
    
    # Check input file exists
    if not Path(args.input).exists():
        print(f"ERROR: Input file not found: {args.input}")
        sys.exit(1)
    
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"ERROR: Error loading config.yaml: {e}")
        sys.exit(1)
    
    # Execute mode
    try:
        if args.mode == "train":
            success = train_mode(args.level, args.input, config)
            
        elif args.mode == "predict":
            success = predict_mode(args.level, args.input, args.output, config)
            
        elif args.mode == "validate":
            success = validate_mode(args.input, args.total)
        
        if success:
            print(f"\n{args.mode.upper()} completed successfully!")
            sys.exit(0)
        else:
            print(f"\n{args.mode.upper()} failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nERROR: Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
