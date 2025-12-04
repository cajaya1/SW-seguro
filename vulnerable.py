import os
import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key (security risk)
SECRET_KEY = "12345"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: Classic SQL injection (string concatenation)
    # Attacker can bypass authentication using: admin' --
    query = "SELECT * FROM users WHERE user = '" + username + "' AND pass = '" + password + "'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    if user:
        return "Welcome"
    return "Error"

@app.route('/ping', methods=['GET'])
def ping_service():
    address = request.args.get('address')
    
    # VULNERABILITY: OS Command injection 
    # Attacker can execute malicious commands: 8.8.8.8; rm -rf /
    os.system("ping -c 1 " + address)
    
    return "Ping executed"

@app.route('/calc', methods=['POST'])
def calculadora():
    expression = request.form.get('expr')
    
    # VULNERABILITY: Use of eval() (Remote code execution)
    # User can send malicious Python code through this input
    resultado = eval(expression)
    
    return str(resultado)

if __name__ == '__main__':
    # VULNERABILITY: Debug=True in production exposes error traces
    app.run(debug=True)