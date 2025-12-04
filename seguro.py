import subprocess
import sqlite3
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# SECURE: Secret key is read from environment variables (not hardcoded)
SECRET_KEY = os.getenv("APP_SECRET_KEY")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # SECURE: Use of parameterized queries (?)
    # Database treats inputs as data only, never as SQL code
    query = "SELECT * FROM users WHERE user = ? AND pass = ?"
    cursor.execute(query, (username, password))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return "Welcome"
    return "Invalid credentials"

@app.route('/ping', methods=['GET'])
def ping_service():
    address = request.args.get('address')
    
    # SECURE: Input validation (only allow safe characters)
    if not all(c.isalnum() or c in ".-" for c in address):
        return "Invalid IP address", 400

    try:
        # SECURE: Use of subprocess.run with argument list
        # Prevents system from interpreting additional commands (; rm -rf /)
        subprocess.run(["ping", "-c", "1", address], check=True, timeout=5)
        return "Ping successful"
    except subprocess.CalledProcessError:
        return "Host not responding"

@app.route('/calc', methods=['POST'])
def calculadora():
    expression = request.form.get('expr')
    
    # SECURE: Replacement of eval() with safe logic or mathematical libraries
    # Only integer addition allowed as a simple example
    try:
        a, b = map(int, expression.split('+'))
        return str(a + b)
    except ValueError:
        return "Operation not supported"

if __name__ == '__main__':
    # SECURE: Debug disabled for production
    app.run(debug=False)