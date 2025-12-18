#!/usr/bin/env python3
"""
Quick Start Script
Sets up the project and runs a quick security scan demo
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    print("=" * 80)
    print("🔒 SW SEGURO - Security Vulnerability Detection System")
    print("=" * 80)
    print("\nProject Structure:")
    print("  ├── src/          - Source code")
    print("  ├── tests/        - Test suite")
    print("  ├── demos/        - Demo scripts")
    print("  ├── examples/     - Example files")
    print("  ├── data/         - Datasets and models")
    print("  └── docs/         - Documentation")
    
    print("\n" + "=" * 80)
    print("Quick Start Options:")
    print("=" * 80)
    print("\n1. Run Interactive Scanner:")
    print("   python demos/demo_scanner.py")
    
    print("\n2. Run Comprehensive Demo:")
    print("   python demos/demo_comprehensive_scan.py")
    
    print("\n3. Scan a Directory:")
    print("   python src/scanner/scan_security.py <directory>")
    
    print("\n4. Train Model:")
    print("   python src/model/entrenamiento.py")
    
    print("\n5. Run Tests:")
    print("   pytest tests/")
    
    print("\n" + "=" * 80)
    print("Documentation: docs/")
    print("=" * 80)
    
    # Check if model exists
    model_path = PROJECT_ROOT / "data" / "modelo_seguridad_final.pkl"
    if model_path.exists():
        print("\n✅ Model found: data/modelo_seguridad_final.pkl")
    else:
        print("\n⚠️  Model not found. Train it with: python src/model/entrenamiento.py")
    
    # Check if datasets exist
    dataset_path = PROJECT_ROOT / "data" / "dataset_contraste.csv"
    if dataset_path.exists():
        print("✅ Dataset found: data/dataset_contraste.csv")
    else:
        print("⚠️  Dataset not found. Check data/ directory")
    
    print("\n" + "=" * 80)
    print("Ready to scan! 🚀")
    print("=" * 80)

if __name__ == "__main__":
    main()
