# Quick Start Guide

## Prerequisites

Make sure you have Python 3.7+ installed and the following packages:

```bash
pip install pandas numpy scikit-learn joblib matplotlib seaborn tqdm lizard pydriller flask
```

## Step-by-Step Usage

### 1. First Time Setup

If you don't have a trained model yet, you'll need to either:

**Option A: Train from scratch (requires dataset)**
```bash
python entrenamiento.py
```

**Option B: Mine data first, then train**
```bash
python mineria.py        # This will take time - mines from GitHub repos
python entrenamiento.py  # Train model with collected data
```

### 2. Analyze Files

Once you have a model (`modelo_seguridad_final.pkl`), run:

```bash
python demo_scanner.py
```

Then enter file paths when prompted. Examples:
- `vulnerable.py`
- `seguro.py`
- `C:\path\to\your\file.py`

### 3. Understanding Results

The scanner will output:
- **Status**: `SECURE` or `HIGH RISK`
- **Risk probability**: Percentage (>40% = HIGH RISK)
- **Details**: Code metrics used for analysis

### 4. Example Commands

```bash
# Train a model
python entrenamiento.py

# Scan a file interactively  
python demo_scanner.py

# Mine new training data
python mineria.py
```

## File Descriptions

- `demo_scanner.py` - Interactive file analyzer
- `entrenamiento.py` - Model training script
- `mineria.py` - Data collection from repositories
- `seguro.py` - Example of secure code
- `vulnerable.py` - Example of vulnerable code

## Troubleshooting

**"Model file not found"**
- Run `python entrenamiento.py` first to create the model

**"dataset_local.csv not found"**  
- Run `python mineria.py` first to collect training data

**Memory issues**
- Reduce `SAMPLE_SIZE` in `entrenamiento.py`
- Close other applications

**Slow training**
- Use smaller dataset
- Ensure you have adequate RAM and CPU cores