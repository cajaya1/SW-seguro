"""
Machine Learning Model Package
Contains training and data mining scripts
"""

from pathlib import Path

# Model paths
MODEL_DIR = Path(__file__).parent.parent.parent / "data"
MODEL_PATH = MODEL_DIR / "modelo_seguridad_final.pkl"
DATASET_PATH = MODEL_DIR / "dataset_contraste.csv"
