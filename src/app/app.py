"""
Simple Flask Application for CI/CD Demo
This app will be analyzed, tested, and deployed automatically
"""

from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# Homepage template
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure DevOps Demo</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #2c3e50; }
        .status { 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px 0;
        }
        .success { background: #d4edda; color: #155724; }
        .info { background: #d1ecf1; color: #0c5460; }
        code {
            background: #f8f9fa;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Secure DevOps CI/CD Pipeline Demo</h1>
        <div class="status success">
            <strong>✅ Application Deployed Successfully!</strong>
        </div>
        <div class="status info">
            <p><strong>Pipeline Status:</strong> All security checks passed</p>
            <p><strong>Environment:</strong> {{ env }}</p>
            <p><strong>Version:</strong> 1.0.0</p>
        </div>
        <h2>About This Project</h2>
        <p>This application demonstrates a complete CI/CD pipeline with AI-powered security scanning:</p>
        <ul>
            <li>🔍 Automatic vulnerability detection using ML model</li>
            <li>🤖 Telegram notifications for all pipeline events</li>
            <li>🚀 Automatic deployment to production</li>
            <li>✅ Comprehensive testing and validation</li>
        </ul>
        
        <h3>API Endpoints:</h3>
        <ul>
            <li><code>GET /</code> - This homepage</li>
            <li><code>GET /health</code> - Health check endpoint</li>
            <li><code>GET /api/status</code> - Application status (JSON)</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    """Homepage"""
    environment = os.getenv('ENVIRONMENT', 'production')
    return render_template_string(HOME_TEMPLATE, env=environment)

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'secure-devops-demo',
        'version': '1.0.0'
    })

@app.route('/api/status')
def status():
    """Application status endpoint"""
    return jsonify({
        'application': 'Secure DevOps Demo',
        'status': 'running',
        'security_check': 'passed',
        'environment': os.getenv('ENVIRONMENT', 'production'),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
