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
    print(f"Input file: {input_file}")
    
    # TODO: Implementar training pipeline
    # 1. Carregar dados (Transactions + auxiliares)
    # 2. Feature engineering
    # 3. Treinar modelos
    # 4. Salvar modelos para usar em predict
    
    print("\n⚠️  Training pipeline not yet implemented")
    print("Next steps:")
    print("  1. Load Transactions.csv + auxiliary datasets")
    print("  2. Feature engineering (temporal, network, geo, etc.)")
    print("  3. Train ensemble of models (XGBoost, LightGBM, CatBoost)")
    print("  4. Cross-validation with temporal splits")
    print("  5. Optimize threshold based on asymmetric costs")
    print("  6. Save trained models to models/trained/")
    
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
    print(f"Output file: {output_file}")
    
    # TODO: Implementar prediction pipeline
    # 1. Carregar modelos treinados
    # 2. Carregar dados de avaliação
    # 3. Feature engineering (mesmas features do treino)
    # 4. Gerar predições
    # 5. Aplicar threshold otimizado
    # 6. Salvar Transaction IDs suspeitos no formato correto
    
    print("\n⚠️  Prediction pipeline not yet implemented")
    print("Next steps:")
    print("  1. Load trained models from models/trained/")
    print("  2. Load evaluation Transactions.csv + auxiliary datasets")
    print("  3. Apply same feature engineering as training")
    print("  4. Generate predictions with ensemble")
    print("  5. Apply optimized threshold")
    print("  6. Write Transaction IDs to output file (ASCII, one per line)")
    
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
        print(f"\n❌ VALIDATION FAILED: {error}")
        return False
    
    # Validate percentage if total provided
    if total_transactions:
        is_valid, percentage, error = validate_percentage_range(input_file, total_transactions)
        
        if not is_valid:
            print(f"\n❌ VALIDATION FAILED: {error}")
            return False
    
    print(f"\n✅ VALIDATION PASSED")
    print(f"\nOutput file is ready for submission!")
    print(f"\n⚠️  REMEMBER: Only 1 submission per level - first submission is FINAL!")
    
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
        print("❌ Error: --level required for train and predict modes")
        sys.exit(1)
    
    if args.mode == "predict" and not args.output:
        print("❌ Error: --output required for predict mode")
        sys.exit(1)
    
    # Check input file exists
    if not Path(args.input).exists():
        print(f"❌ Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"❌ Error loading config.yaml: {e}")
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
            print(f"\n✅ {args.mode.upper()} completed successfully!")
            sys.exit(0)
        else:
            print(f"\n❌ {args.mode.upper()} failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
