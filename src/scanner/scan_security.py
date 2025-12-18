"""
Security Scanner Script for CI/CD Pipeline
Analyzes code changes and classifies them as SECURE or VULNERABLE
using trained ML model, with detailed vulnerability detection.
"""

import sys
import os
import joblib
import pandas as pd
import lizard
import re
import json
from pathlib import Path
from .vulnerability_detector import detect_vulnerabilities, get_vulnerability_summary, format_vulnerability_report
from pathlib import Path

# Model and configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "data" / "modelo_seguridad_final.pkl"
THRESHOLD = 0.40  # Probability threshold for VULNERABLE classification

# Risk patterns (same as training)
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
    'py': [r'escape\(', r'quote\(', r'sanitize', r'validate', r'strip\(', r'clean'],
    'js': [r'escape', r'sanitize', r'DOMPurify', r'textContent', r'innerText'],
    'java': [r'PreparedStatement', r'escape', r'sanitize', r'validate']
}

def extract_features(code, filename):
    """Extract features from code for ML model prediction"""
    features = {}
    code_str = str(code)
    
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
        
        # Count risk patterns
        risk_score = 0
        if lang and lang in RISK_PATTERNS:
            for p in RISK_PATTERNS[lang]:
                if re.search(p, code_str, re.IGNORECASE): 
                    risk_score += 1
        features['risk_keywords'] = risk_score
        
        # Count sanitization patterns
        sanitization_score = 0
        if lang and lang in SANITIZATION_PATTERNS:
            for p in SANITIZATION_PATTERNS[lang]:
                if re.search(p, code_str, re.IGNORECASE):
                    sanitization_score += 1
        features['sanitization_count'] = sanitization_score
        
        # Risk density
        total_lines = len(code_str.split('\n'))
        features['risk_density'] = (risk_score / max(total_lines, 1)) * 100
        
        # Comment ratio
        comment_lines = len(re.findall(r'^\s*[#//]', code_str, re.MULTILINE))
        features['comment_ratio'] = comment_lines / max(total_lines, 1)
        
    except:
        features['risk_keywords'] = 0
        features['sanitization_count'] = 0
        features['risk_density'] = 0
        features['comment_ratio'] = 0
        
    return features

def scan_file(filepath):
    """Scan a single file and return vulnerability assessment with detailed detection"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        # Load model
        if not os.path.exists(MODEL_PATH):
            return {
                'status': 'ERROR',
                'message': f'Model file not found: {MODEL_PATH}',
                'file': filepath
            }
        
        model = joblib.load(MODEL_PATH)
        
        # Extract features
        features = extract_features(code, filepath)
        df_input = pd.DataFrame([features])
        df_input['code'] = code
        df_input['filename'] = filepath
        
        # Predict
        probability = model.predict_proba(df_input)[0][1]  # Probability of VULNERABLE
        prediction = "VULNERABLE" if probability > THRESHOLD else "SECURE"
        
        # Detailed vulnerability detection
        vulnerabilities = []
        vulnerability_summary = {}
        if prediction == "VULNERABLE":
            vulnerabilities = detect_vulnerabilities(code, filepath)
            vulnerability_summary = get_vulnerability_summary(vulnerabilities)
        
        result = {
            'status': prediction,
            'probability': float(probability),
            'threshold': THRESHOLD,
            'file': filepath,
            'metrics': features,
            'vulnerabilities': vulnerabilities,
            'vulnerability_summary': vulnerability_summary
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'message': str(e),
            'file': filepath
        }

def scan_directory(directory, extensions=None):
    """Scan all files in directory with given extensions"""
    if extensions is None:
        extensions = ['.py', '.js', '.java', '.ts', '.jsx', '.tsx']
    
    results = []
    for root, dirs, files in os.walk(directory):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                result = scan_file(filepath)
                results.append(result)
    
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_security.py <file_or_directory>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    print(f"Security Scanner - Analyzing: {target}")
    print("=" * 60)
    
    if os.path.isfile(target):
        results = [scan_file(target)]
    elif os.path.isdir(target):
        results = scan_directory(target)
    else:
        print(f"ERROR: Path not found: {target}")
        sys.exit(1)
    
    # Analyze results
    vulnerable_files = [r for r in results if r.get('status') == 'VULNERABLE']
    secure_files = [r for r in results if r.get('status') == 'SECURE']
    error_files = [r for r in results if r.get('status') == 'ERROR']
    
    # Print summary
    print(f"\nScan Results:")
    print(f"  Total files scanned: {len(results)}")
    print(f"  SECURE: {len(secure_files)}")
    print(f"  VULNERABLE: {len(vulnerable_files)}")
    print(f"  ERRORS: {len(error_files)}")
    print("=" * 60)
    
    # Print vulnerable files details
    if vulnerable_files:
        print("\nVULNERABLE FILES DETECTED:")
        for r in vulnerable_files:
            print(f"\n  File: {r['file']}")
            print(f"  Risk Probability: {r['probability']:.2%}")
            print(f"  Risk Keywords: {r['metrics'].get('risk_keywords', 0)}")
            print(f"  Sanitization: {r['metrics'].get('sanitization_count', 0)}")
            
            # Print detailed vulnerability report
            if r.get('vulnerabilities'):
                print(format_vulnerability_report(r['vulnerabilities'], r['file']))
    
    # Output JSON for CI/CD
    output = {
        'total': len(results),
        'secure': len(secure_files),
        'vulnerable': len(vulnerable_files),
        'errors': len(error_files),
        'vulnerable_files': vulnerable_files,
        'passed': len(vulnerable_files) == 0
    }
    
    with open('security_scan_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: security_scan_results.json")
    
    # Exit with appropriate code
    if vulnerable_files:
        print("\n❌ SECURITY CHECK FAILED: Vulnerable code detected")
        sys.exit(1)
    elif error_files:
        print("\n⚠️  SECURITY CHECK WARNING: Some files had errors")
        sys.exit(2)
    else:
        print("\n✅ SECURITY CHECK PASSED: All code is secure")
        sys.exit(0)

if __name__ == "__main__":
    main()
