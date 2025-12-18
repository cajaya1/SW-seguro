"""
Example file with SQL Injection vulnerabilities
"""

import sqlite3

def buscar_usuario_inseguro(nombre):
    """Vulnerable function - SQL Injection"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: String concatenation in SQL query
    query = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"
    cursor.execute(query)
    
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def actualizar_datos_inseguro(user_id, email):
    """Vulnerable function - SQL Injection with format"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Using % formatting in SQL
    query = "UPDATE usuarios SET email = '%s' WHERE id = %s" % (email, user_id)
    cursor.execute(query)
    
    conn.commit()
    conn.close()

def login_vulnerable(username, password):
    """Vulnerable function - SQL Injection with f-string"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Using f-string in SQL
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    return cursor.fetchone() is not None
