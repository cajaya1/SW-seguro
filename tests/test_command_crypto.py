"""
Example file with Command Injection and weak crypto
"""

import os
import subprocess
import hashlib
import random

def ping_server_vulnerable(ip_address):
    """Vulnerable to Command Injection"""
    # VULNERABLE: User input in system command
    command = f"ping -c 4 {ip_address}"
    os.system(command)

def execute_command_unsafe(user_cmd):
    """Vulnerable to Command Injection"""
    # VULNERABLE: shell=True with user input
    subprocess.call(user_cmd, shell=True)

def backup_files_vulnerable(directory):
    """Vulnerable to Command Injection"""
    # VULNERABLE: Using os.popen with user input
    os.popen(f"tar -czf backup.tar.gz {directory}")

def hash_password_weak(password):
    """Vulnerable - Weak cryptography (MD5)"""
    # VULNERABLE: Using MD5 for password hashing
    return hashlib.md5(password.encode()).hexdigest()

def generate_token_insecure():
    """Vulnerable - Weak random number generation"""
    # VULNERABLE: Using random.random() for security tokens
    return str(random.random())

# Hardcoded credentials
API_KEY = "sk-1234567890abcdef"  # VULNERABLE: Hardcoded secret
PASSWORD = "admin123"  # VULNERABLE: Hardcoded password
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"  # VULNERABLE

def connect_database():
    """Vulnerable - Hardcoded credentials"""
    db_password = "MySecurePassword123!"  # VULNERABLE
    connection_string = f"postgresql://user:{db_password}@localhost/db"
    return connection_string
