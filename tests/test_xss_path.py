"""
Example file with XSS and Path Traversal vulnerabilities
"""

from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/search')
def search_vulnerable():
    """Vulnerable to XSS - directly rendering user input"""
    query = request.args.get('q', '')
    
    # VULNERABLE: User input rendered without escaping
    html = f"<h1>Search results for: {query}</h1>"
    return render_template_string(html)

@app.route('/profile')
def profile_xss():
    """Vulnerable to XSS - innerHTML equivalent"""
    username = request.args.get('name', 'Guest')
    
    # VULNERABLE: String concatenation with user input
    response = "<div>Welcome " + username + "</div>"
    return response

@app.route('/download')
def download_file_vulnerable():
    """Vulnerable to Path Traversal"""
    filename = request.args.get('file', '')
    
    # VULNERABLE: User controls file path
    filepath = os.path.join('/uploads/', filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    return content

@app.route('/delete')
def delete_file_unsafe():
    """Vulnerable to Path Traversal and unsafe file operations"""
    filename = request.args.get('file', '')
    
    # VULNERABLE: User can delete any file
    os.remove(filename)
    
    return "File deleted"

if __name__ == '__main__':
    app.run(debug=True)
