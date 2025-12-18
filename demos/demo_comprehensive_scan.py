"""
Comprehensive vulnerability detection demo
"""

import sys
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.scanner.vulnerability_detector import detect_vulnerabilities, format_vulnerability_report, get_vulnerability_summary

test_files = [
    (PROJECT_ROOT / 'examples' / 'vulnerable.py', 'Original vulnerable file'),
    (PROJECT_ROOT / 'examples' / 'secure.py', 'Secure code example'),
    (PROJECT_ROOT / 'tests' / 'test_sql_injection.py', 'SQL Injection examples'),
    (PROJECT_ROOT / 'tests' / 'test_xss_path.py', 'XSS and Path Traversal examples'),
    (PROJECT_ROOT / 'tests' / 'test_command_crypto.py', 'Command Injection and weak crypto examples')
]

print("=" * 80)
print("COMPREHENSIVE VULNERABILITY DETECTION DEMO")
print("=" * 80)

total_files = 0
total_vulnerabilities = 0
results_summary = []

for filepath, description in test_files:
    filename = str(filepath.name)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        vulnerabilities = detect_vulnerabilities(code, filename)
        summary = get_vulnerability_summary(vulnerabilities)
        
        total_files += 1
        total_vulnerabilities += summary['total']
        
        results_summary.append({
            'file': filename,
            'description': description,
            'count': summary['total'],
            'summary': summary
        })
        
        print(f"\n{'='*80}")
        print(f"FILE: {filename}")
        print(f"Description: {description}")
        print('='*80)
        
        if summary['total'] > 0:
            print(f"\n[!] Found {summary['total']} vulnerabilities")
            print(f"   By severity: {summary['by_severity']}")
            print(f"   By type: {summary['by_type']}")
            print(format_vulnerability_report(vulnerabilities, filename))
        else:
            print("\n[+] No vulnerabilities detected - Code appears secure!")
            
    except FileNotFoundError:
        print(f"\n[!] File not found: {filename}")
    except Exception as e:
        print(f"\n[ERROR] Error processing {filename}: {e}")

# Final summary
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
print(f"\nTotal files analyzed: {total_files}")
print(f"Total vulnerabilities found: {total_vulnerabilities}")
print("\nDetailed breakdown:")
for result in results_summary:
    status = "[+] SECURE" if result['count'] == 0 else f"[!] {result['count']} issues"
    print(f"  {result['file']}: {status}")
    if result['count'] > 0:
        print(f"    Severity: {result['summary']['by_severity']}")

print("\n" + "="*80)
