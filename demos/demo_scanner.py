import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import pandas as pd
import lizard
import re
from src.scanner.vulnerability_detector import detect_vulnerabilities, format_vulnerability_report, get_vulnerability_summary

# Cargar el modelo entrenado
MODEL_PATH = PROJECT_ROOT / "data" / "modelo_seguridad_final.pkl"

print("Loading AI model...")
try:
    model = joblib.load(MODELO_PATH)
except:
    print("Error: Model file not found. Please ensure the .pkl file exists.")
    exit()

# Replicamos la función de extracción (necesaria para procesar nuevos inputs)
RISK_PATTERNS = {
    'py': [r'eval\(', r'exec\(', r'subprocess\.', r'os\.system', r'cursor\.execute'],
    'js': [r'eval\(', r'innerHTML', r'document\.write', r'dangerouslySetInnerHTML'],
    'java': [r'Statement\s+', r'\+\s*request\.getParameter', r'Runtime\.exec']
}

def extract_features_demo(code, filename):
    features = {}
    try:
        analysis = lizard.analyze_file.analyze_source_code(filename, code)
        features['nloc'] = analysis.nloc
        features['avg_complexity'] = analysis.average_cyclomatic_complexity
        features['max_complexity'] = max([f.cyclomatic_complexity for f in analysis.function_list]) if analysis.function_list else 0
    except:
        features['nloc'] = len(code.split('\n')); features['avg_complexity'] = 0; features['max_complexity'] = 0
    
    ext = filename.split('.')[-1]
    lang = 'py' if ext == 'py' else ('js' if ext in ['js', 'ts'] else ('java' if ext == 'java' else None))
    score = 0
    if lang and lang in RISK_PATTERNS:
        for p in RISK_PATTERNS[lang]:
            if re.search(p, code): score += 1
    features['risk_keywords'] = score
    return features

def analizar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
        
        # Preparar datos
        feats = extract_features_demo(contenido, ruta_archivo)
        df_input = pd.DataFrame([feats])
        df_input['code'] = contenido
        
        # Predecir
        prob = model.predict_proba(df_input)[0][1] # Probabilidad de Vulnerable (1)
        pred = model.predict(df_input)[0]
        
        # Security threshold logic
        # Files with probability greater than 40% are marked as high risk
        status = "HIGH RISK" if prob > 0.40 else "SECURE"
        print(f"\nAnalysis results for: {ruta_archivo}")
        print("=" * 80)
        print(f"Status: {status}")
        print(f"Risk probability: {prob:.1%}")
        print(f"Complexity metrics: NLOC={feats['nloc']}, Avg Complexity={feats['avg_complexity']:.2f}")
        print(f"Risk indicators: {feats['risk_keywords']} patterns detected")
        
        # Detailed vulnerability detection if high risk
        if status == "HIGH RISK":
            vulnerabilities = detect_vulnerabilities(contenido, ruta_archivo)
            if vulnerabilities:
                summary = get_vulnerability_summary(vulnerabilities)
                print(f"\n🔍 DETAILED VULNERABILITY ANALYSIS:")
                print(f"   Total vulnerabilities found: {summary['total']}")
                print(f"   By severity: {summary['by_severity']}")
                print(f"   By type: {summary['by_type']}")
                print(format_vulnerability_report(vulnerabilities, ruta_archivo))
            else:
                print("\n⚠️  File flagged as HIGH RISK but no specific vulnerabilities identified.")
                print("   Manual review recommended.")
        
    except Exception as e:
        print(f"Error reading file: {e}")

# --- USER INTERFACE ---
print("\n--- VULNERABILITY SCANNER (LOCAL) ---")
while True:
    path = input("\nEnter file path to analyze (or 'exit' to quit): ")
    if path.lower() == 'exit': break
    analizar_archivo(path.strip('"')) # Strip quotes when dragging files