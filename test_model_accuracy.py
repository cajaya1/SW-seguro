"""
Test the actual accuracy of the existing model
"""
import joblib
import pandas as pd
import numpy as np
import lizard
import re
from tqdm import tqdm
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from pathlib import Path

# Import feature extraction patterns
RISK_PATTERNS = {
    'py': [
        r'eval\(', r'exec\(', r'subprocess\.', r'os\.system', r'cursor\.execute',
        r'pickle\.loads', r'yaml\.load', r'shell=True', r'input\(', r'__import__',
        r'compile\(', r'open\(.*["\']w', r'rmtree', r'unlink'
    ],
    'js': [
        r'eval\(', r'innerHTML', r'document\.write', r'dangerouslySetInnerHTML',
        r'setTimeout.*\(', r'setInterval.*\(', r'Function\(', r'\.href\s*=',
        r'document\.cookie', r'localStorage', r'sessionStorage'
    ],
    'java': [
        r'Statement\s+', r'\+\s*request\.getParameter', r'Runtime\.exec',
        r'ProcessBuilder', r'ScriptEngine', r'\.createQuery\(',
        r'Reflection', r'Class\.forName'
    ]
}

SANITIZATION_PATTERNS = {
    'py': [r'escape\(', r'quote\(', r'PreparedStatement', r'parameterized', r'validate'],
    'js': [r'sanitize', r'DOMPurify', r'escape', r'textContent', r'innerText'],
    'java': [r'PreparedStatement', r'setString\(', r'validate', r'escape']
}

MAX_CODE_LEN = 30000

def extract_features_safe(code, filename):
    features = {}
    code_str = str(code)
    
    if len(code_str) > MAX_CODE_LEN:
        return {
            'nloc': 0, 'avg_complexity': 0, 'max_complexity': 0, 
            'risk_keywords': 0, 'sanitization_count': 0, 
            'risk_density': 0, 'comment_ratio': 0
        }

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
        
        risk_score = 0
        if lang and lang in RISK_PATTERNS:
            for p in RISK_PATTERNS[lang]:
                if re.search(p, code_str, re.IGNORECASE): 
                    risk_score += 1
        features['risk_keywords'] = risk_score
        
        sanitization_score = 0
        if lang and lang in SANITIZATION_PATTERNS:
            for p in SANITIZATION_PATTERNS[lang]:
                if re.search(p, code_str, re.IGNORECASE):
                    sanitization_score += 1
        features['sanitization_count'] = sanitization_score
        
        total_lines = len(code_str.split('\n'))
        features['risk_density'] = (risk_score / max(total_lines, 1)) * 100
        
        comment_lines = len(re.findall(r'^\s*[#//]', code_str, re.MULTILINE))
        features['comment_ratio'] = comment_lines / max(total_lines, 1)
        
    except:
        features['risk_keywords'] = 0
        features['sanitization_count'] = 0
        features['risk_density'] = 0
        features['comment_ratio'] = 0
        
    return features

def test_model_accuracy():
    print("Loading model and dataset...")
    
    # Load model
    model_path = Path('data/modelo_seguridad_final.pkl')
    model = joblib.load(model_path)
    print(f"✅ Model loaded: {type(model)}")
    
    # Load dataset
    df = pd.read_csv('data/dataset_contraste.csv')
    print(f"✅ Dataset loaded: {len(df)} samples")
    print(f"   Columns: {list(df.columns)}")
    
    # Check class distribution
    if 'label' in df.columns:
        print(f"\n📊 Class distribution:")
        print(df['label'].value_counts())
    
    # Prepare data
    if 'code' not in df.columns or 'label' not in df.columns:
        print("\n❌ Missing 'code' or 'label' columns")
        return
    
    # Extract features
    print("\n⚙️  Extracting features (this may take a moment)...")
    tqdm.pandas()
    df_features = df.progress_apply(lambda row: extract_features_safe(row['code'], row['filename']), axis=1, result_type='expand')
    df_final = pd.concat([df, df_features], axis=1)
    
    X = df_final
    y = df_final['label']
    
    # Make predictions
    print("\n🔮 Making predictions...")
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    
    print("\n" + "="*60)
    print("MODEL ACCURACY TEST RESULTS")
    print("="*60)
    print(f"\n✅ Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    if accuracy >= 0.82:
        print(f"   ✅ PASSED: Model meets 82% accuracy requirement!")
    else:
        print(f"   ⚠️  WARNING: Model accuracy ({accuracy*100:.2f}%) is below 82% threshold")
        print(f"   Need to improve by: {(0.82 - accuracy)*100:.2f}%")
    
    # Detailed classification report
    print("\n📊 Classification Report:")
    print(classification_report(y, y_pred))
    
    # Confusion matrix
    print("\n🔢 Confusion Matrix:")
    cm = confusion_matrix(y, y_pred)
    print(cm)
    
    print("\n" + "="*60)
    
    return accuracy

if __name__ == "__main__":
    try:
        accuracy = test_model_accuracy()
    except Exception as e:
        print(f"\n❌ Error testing model: {e}")
        import traceback
        traceback.print_exc()
