#!/usr/bin/env python3
"""
Test script to validate environment setup
Run this to ensure everything is properly configured before starting
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv


def test_python_version():
    """Verify Python 3.13"""
    print("\n1. Testing Python Version...")
    print("-" * 60)
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 13:
        print("✅ Python 3.13 - OK")
        return True
    elif version.major == 3 and version.minor == 14:
        print("⚠️  Python 3.14 detected - may cause issues with Langfuse")
        print("   Recommendation: Use Python 3.13")
        return False
    else:
        print(f"❌ Python {version.major}.{version.minor} - Expected 3.13")
        return False


def test_imports():
    """Test critical imports"""
    print("\n2. Testing Package Imports...")
    print("-" * 60)
    
    packages = [
        ("langchain", "LangChain", True),
        ("langfuse", "Langfuse", True),
        ("pandas", "Pandas", True),
        ("numpy", "NumPy", True),
        ("sklearn", "Scikit-learn", True),
        ("xgboost", "XGBoost", True),
        ("lightgbm", "LightGBM", True),
        ("catboost", "CatBoost", True),
        ("ulid", "ULID", True),
        ("networkx", "NetworkX", True),
        ("yaml", "PyYAML", True),
        ("dotenv", "Python-dotenv", True),
        ("geopandas", "GeoPandas", False),  # Optional
        ("spacy", "spaCy", False),  # Optional
        ("torch", "PyTorch", False),  # Optional
    ]
    
    all_ok = True
    for module, name, required in packages:
        try:
            __import__(module)
            print(f"✅ {name:20s} - OK")
        except ImportError:
            if required:
                print(f"❌ {name:20s} - NOT FOUND (REQUIRED)")
                all_ok = False
            else:
                print(f"⚠️  {name:20s} - NOT FOUND (optional)")
    
    return all_ok


def test_langfuse_version():
    """Test Langfuse version"""
    print("\n3. Testing Langfuse Version...")
    print("-" * 60)
    
    try:
        import langfuse
        version = langfuse.__version__
        print(f"Langfuse version: {version}")
        
        major = int(version.split('.')[0])
        if major == 3:
            print("✅ Langfuse v3 - OK")
            return True
        elif major == 4:
            print("❌ Langfuse v4 detected - NOT SUPPORTED")
            print("   Run: pip uninstall langfuse && pip install 'langfuse>=3.0.0,<4.0.0'")
            return False
        else:
            print(f"⚠️  Langfuse v{major} - Unexpected version")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Langfuse version: {e}")
        return False


def test_env_variables():
    """Test .env configuration"""
    print("\n4. Testing Environment Variables...")
    print("-" * 60)
    
    load_dotenv()
    
    required = [
        "OPENROUTER_API_KEY",
        "LANGFUSE_PUBLIC_KEY",
        "LANGFUSE_SECRET_KEY",
        "LANGFUSE_HOST",
        "TEAM_NAME"
    ]
    
    all_ok = True
    for var in required:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var or "SECRET" in var:
                masked = value[:15] + "..." if len(value) > 15 else value
            else:
                masked = value
            print(f"✅ {var:25s} : {masked}")
        else:
            print(f"❌ {var:25s} : NOT SET")
            all_ok = False
    
    # Validate session ID format
    if os.getenv("TEAM_NAME"):
        team = os.getenv("TEAM_NAME").replace(" ", "-")
        print(f"\n   Session ID format: {team}-ULID")
        if " " in os.getenv("TEAM_NAME"):
            print(f"   ⚠️  Note: Spaces in TEAM_NAME will be replaced with '-' in session IDs")
    
    return all_ok


def test_langfuse_connection():
    """Test Langfuse connection"""
    print("\n5. Testing Langfuse Connection...")
    print("-" * 60)
    
    try:
        from langfuse import Langfuse
        load_dotenv()
        
        client = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )
        
        # Try to flush (sends any pending traces)
        client.flush()
        print("✅ Langfuse connection - OK")
        print(f"   Host: {os.getenv('LANGFUSE_HOST')}")
        return True
        
    except Exception as e:
        print(f"❌ Langfuse connection - FAILED")
        print(f"   Error: {e}")
        return False


def test_project_structure():
    """Test project structure"""
    print("\n6. Testing Project Structure...")
    print("-" * 60)
    
    required_files = [
        "requirements.txt",
        "config.yaml",
        "README.md",
        ".env",
        "main.py"
    ]
    
    required_dirs = [
        "agents",
        "features",
        "models",
        "utils",
        "data/raw",
        "data/processed",
        "data/outputs",
        "tests"
    ]
    
    all_ok = True
    
    # Check files
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file:25s} - exists")
        else:
            print(f"❌ {file:25s} - NOT FOUND")
            all_ok = False
    
    # Check directories
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"✅ {dir:25s} - exists")
        else:
            print(f"❌ {dir:25s} - NOT FOUND")
            all_ok = False
    
    return all_ok


def main():
    """Run all tests"""
    print("=" * 60)
    print("Reply Mirror Challenge - Setup Validation")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("Package Imports", test_imports()))
    results.append(("Langfuse Version", test_langfuse_version()))
    results.append(("Environment Variables", test_env_variables()))
    results.append(("Langfuse Connection", test_langfuse_connection()))
    results.append(("Project Structure", test_project_structure()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:25s} : {status}")
    
    print("=" * 60)
    
    if all(passed for _, passed in results):
        print("✅ ALL TESTS PASSED - Setup is complete!")
        print("\nNext steps:")
        print("  1. Run: python test_langfuse.py (to test tracking)")
        print("  2. Download Level 1 datasets from Reply platform")
        print("  3. Start implementing the fraud detection system")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME TESTS FAILED - Review errors above")
        print("\nPlease fix the issues before proceeding.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
