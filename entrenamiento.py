import pandas as pd
import numpy as np
import lizard
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import time

from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# --- CONFIGURACIÓN ---
INPUT_FILE = "dataset_contraste.csv"
MODEL_FILE = "modelo_seguridad_final.pkl"
SAMPLE_SIZE = 30000   
MAX_CODE_LEN = 30000 

# --- FUNCIONES ---
RISK_PATTERNS = {
    'py': [r'eval\(', r'exec\(', r'subprocess\.', r'os\.system', r'cursor\.execute'],
    'js': [r'eval\(', r'innerHTML', r'document\.write', r'dangerouslySetInnerHTML'],
    'java': [r'Statement\s+', r'\+\s*request\.getParameter', r'Runtime\.exec']
}

def extract_features_safe(code, filename):
    features = {}
    code_str = str(code)
    
    if len(code_str) > MAX_CODE_LEN:
        return {'nloc': 0, 'avg_complexity': 0, 'max_complexity': 0, 'risk_keywords': 0}

    try:
        analysis = lizard.analyze_file.analyze_source_code(filename, code_str)
        features['nloc'] = analysis.nloc
        features['avg_complexity'] = analysis.average_cyclomatic_complexity
        features['max_complexity'] = max([f.cyclomatic_complexity for f in analysis.function_list]) if analysis.function_list else 0
    except:
        features['nloc'] = len(code_str.split('\n'))
        features['avg_complexity'] = 0
        features['max_complexity'] = 0

    try:
        ext = str(filename).split('.')[-1]
        lang = 'py' if ext == 'py' else ('js' if ext in ['js', 'ts'] else ('java' if ext == 'java' else None))
        score = 0
        if lang and lang in RISK_PATTERNS:
            for p in RISK_PATTERNS[lang]:
                if re.search(p, code_str): score += 1
        features['risk_keywords'] = score
    except:
        features['risk_keywords'] = 0
        
    return features

# --- PROCESO PRINCIPAL ---
if __name__ == "__main__":
    start_total = time.time()
    print(f"Starting model training process (corrected version)")
    
    print("\n[1/4] Loading dataset and balancing classes...")
    try:
        # 1. Load dataset (full or large sample)
        df = pd.read_csv(INPUT_FILE, nrows=SAMPLE_SIZE * 3) 
        
        # 2. Basic data cleaning
        df = df.dropna(subset=['code', 'label'])
        df = df.drop_duplicates(subset=['code'])
        
        # 3. Separate classes for analysis
        df_vuln = df[df['label'] == 1]
        df_safe = df[df['label'] == 0]
        
        print(f"   Class distribution: {len(df_vuln)} Vulnerable vs {len(df_safe)} Secure")
        
        # 4. Class balancing using undersampling
        # Use minimum class size to achieve 50/50 balance
        min_len = min(len(df_vuln), len(df_safe))
        
        # Sample equal amounts from each class
        df_vuln_bal = df_vuln.sample(n=min_len, random_state=42)
        df_safe_bal = df_safe.sample(n=min_len, random_state=42)
        
        # Recombine balanced datasets
        df = pd.concat([df_vuln_bal, df_safe_bal])
        
        # Shuffle and reset index (critical for proper alignment)
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
            
        print(f"   Balanced dataset ready: {len(df)} records (50% Vulnerable / 50% Secure).")

    except FileNotFoundError:
        print("Error: Dataset file not found")
        exit()

    print(f"\n[2/4] Extracting features...")
    tqdm.pandas()
    
    # Reset index generates sequential indices 0, 1, 2...
    df_features = df.progress_apply(lambda row: extract_features_safe(row['code'], row['filename']), axis=1, result_type='expand')
    
    # Perfect row-by-row alignment
    df_final = pd.concat([df, df_features], axis=1)

    print("\n[3/4] Training the model...")
    
    X = df_final
    y = df_final['label']
    
    # Security verification before training
    if y.isnull().any():
        print("WARNING: NaN values detected in target variable. Removing corrupted rows...")
        mask = ~y.isnull()
        X = X[mask]
        y = y[mask]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    pipeline = Pipeline([
        ('preprocessor', ColumnTransformer(transformers=[
            ('text', TfidfVectorizer(max_features=1000, stop_words='english'), 'code'),
            ('num', StandardScaler(), ['nloc', 'avg_complexity', 'max_complexity', 'risk_keywords'])
        ])),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    
    pipeline.fit(X_train, y_train)
    
    print("\n[4/4] Finalizing...")
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("-" * 40)
    print(f"FINAL RESULT (Accuracy): {acc:.2%}")
    print("-" * 40)
    print(classification_report(y_test, y_pred, target_names=['Secure', 'Vulnerable']))
    
    joblib.dump(pipeline, MODEL_FILE)
    print(f"\nModel saved: {MODEL_FILE}")
    
    plt.figure(figsize=(8,6))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Greens')
    plt.title(f'Confusion Matrix (Acc: {acc:.2%})')
    plt.savefig('resultado_final_matriz.png')
    
    print(f"\nTotal training time: {(time.time() - start_total) / 60:.1f} minutes.")