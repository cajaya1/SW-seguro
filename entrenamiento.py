import pandas as pd
import numpy as np
import lizard
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import time

from tqdm import tqdm
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score,
    roc_curve, auc, precision_recall_curve
)

# --- CONFIGURACIÓN ---
INPUT_FILE = "dataset_contraste.csv"
MODEL_FILE = "modelo_seguridad_final.pkl"
SAMPLE_SIZE = 30000   
MAX_CODE_LEN = 30000
USE_GRID_SEARCH = False  # Set to True for hyperparameter optimization (slower but better) 

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
    
    # Improved pipeline with optimized parameters
    pipeline = Pipeline([
        ('preprocessor', ColumnTransformer(transformers=[
            ('text', TfidfVectorizer(max_features=2000, stop_words='english', ngram_range=(1, 2)), 'code'),
            ('num', StandardScaler(), ['nloc', 'avg_complexity', 'max_complexity', 'risk_keywords'])
        ])),
        ('classifier', RandomForestClassifier(
            n_estimators=200,           # Increased from 100
            max_depth=30,                # Prevent overfitting
            min_samples_split=5,         # Better generalization
            min_samples_leaf=2,          # Reduce noise sensitivity
            max_features='sqrt',         # Feature randomness
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'      # Handle any residual imbalance
        ))
    ])
    
    # Optional: Grid Search for hyperparameter optimization
    if USE_GRID_SEARCH:
        print("   Performing Grid Search for hyperparameter optimization...")
        param_grid = {
            'classifier__n_estimators': [150, 200, 250],
            'classifier__max_depth': [20, 30, 40],
            'classifier__min_samples_split': [3, 5, 7],
            'preprocessor__text__max_features': [1500, 2000, 2500]
        }
        grid_search = GridSearchCV(pipeline, param_grid, cv=3, scoring='f1', n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        pipeline = grid_search.best_estimator_
        print(f"   Best parameters: {grid_search.best_params_}")
        print(f"   Best cross-validation F1-score: {grid_search.best_score_:.4f}")
    else:
        pipeline.fit(X_train, y_train)
    
    print("\n[4/4] Evaluating model performance...")
    
    # Predictions
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Calculate comprehensive metrics
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    # Display results
    print("\n" + "=" * 60)
    print("                    MODEL PERFORMANCE METRICS")
    print("=" * 60)
    print(f"  Accuracy:          {acc:.4f} ({acc*100:.2f}%)")
    print(f"  Precision:         {precision:.4f} ({precision*100:.2f}%)")
    print(f"  Recall:            {recall:.4f} ({recall*100:.2f}%)")
    print(f"  F1-Score:          {f1:.4f} ({f1*100:.2f}%)")
    print(f"  ROC-AUC Score:     {roc_auc:.4f} ({roc_auc*100:.2f}%)")
    print("=" * 60)
    
    # Cross-validation scores
    print("\nPerforming 5-fold cross-validation...")
    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='f1', n_jobs=-1)
    print(f"  Cross-validation F1 scores: {cv_scores}")
    print(f"  Mean CV F1-Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    print("\n" + "-" * 60)
    print("DETAILED CLASSIFICATION REPORT")
    print("-" * 60)
    print(classification_report(y_test, y_pred, target_names=['Secure', 'Vulnerable'], digits=4))
    
    # Save model
    joblib.dump(pipeline, MODEL_FILE)
    print(f"\nModel saved: {MODEL_FILE}")
    
    # --- VISUALIZATION ---
    print("\nGenerating performance visualizations...")
    
    # 1. Confusion Matrix
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 2, 1)
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title(f'Confusion Matrix\n(Accuracy: {acc:.2%})')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # 2. ROC Curve
    plt.subplot(2, 2, 2)
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    roc_auc_val = auc(fpr, tpr)
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc_val:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    
    # 3. Precision-Recall Curve
    plt.subplot(2, 2, 3)
    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_pred_proba)
    plt.plot(recall_vals, precision_vals, color='green', lw=2, label=f'PR curve (F1 = {f1:.4f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.grid(alpha=0.3)
    
    # 4. Metrics Comparison Bar Chart
    plt.subplot(2, 2, 4)
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    metrics_values = [acc, precision, recall, f1, roc_auc]
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    bars = plt.bar(metrics_names, metrics_values, color=colors, alpha=0.7)
    plt.ylim([0, 1])
    plt.ylabel('Score')
    plt.title('Performance Metrics Summary')
    plt.xticks(rotation=45, ha='right')
    for bar, value in zip(bars, metrics_values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{value:.3f}', ha='center', va='bottom', fontsize=9)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("   Visualization saved: model_performance_analysis.png")
    
    print(f"\nTotal training time: {(time.time() - start_total) / 60:.1f} minutes.")
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)