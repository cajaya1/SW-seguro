"""
Unit Tests for Flask Application
These tests will run in the CI/CD pipeline
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.app.app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test homepage loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Secure DevOps' in response.data

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_status_endpoint(client):
    """Test status API endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'running'
    assert data['security_check'] == 'passed'

def test_404_error(client):
    """Test 404 for non-existent routes"""
    response = client.get('/non-existent-page')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
