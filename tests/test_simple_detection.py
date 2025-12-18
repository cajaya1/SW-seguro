"""
Simple test to demonstrate vulnerability detection without ML model
"""

from vulnerability_detector import detect_vulnerabilities, format_vulnerability_report, get_vulnerability_summary

# Test with vulnerable.py
print("=" * 80)
print("TESTING VULNERABLE FILE: vulnerable.py")
print("=" * 80)

with open('vulnerable.py', 'r', encoding='utf-8') as f:
    code_vulnerable = f.read()

vulnerabilities = detect_vulnerabilities(code_vulnerable, 'vulnerable.py')
summary = get_vulnerability_summary(vulnerabilities)

print(f"\nVulnerabilities found: {summary['total']}")
print(f"By severity: {summary['by_severity']}")
print(f"By type: {summary['by_type']}")
print(format_vulnerability_report(vulnerabilities, 'vulnerable.py'))

# Test with secure.py
print("\n" + "=" * 80)
print("TESTING SECURE FILE: secure.py")
print("=" * 80)

with open('secure.py', 'r', encoding='utf-8') as f:
    code_secure = f.read()

vulnerabilities_secure = detect_vulnerabilities(code_secure, 'secure.py')
summary_secure = get_vulnerability_summary(vulnerabilities_secure)

print(f"\nVulnerabilities found: {summary_secure['total']}")
print(format_vulnerability_report(vulnerabilities_secure, 'secure.py'))

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"vulnerable.py: {summary['total']} vulnerabilities detected")
print(f"secure.py: {summary_secure['total']} vulnerabilities detected")
