import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask
from app.main import create_app
from app.database import db as db_module

# Monkeypatch for in-memory database during tests
@pytest.fixture(autouse=True)
def override_db(monkeypatch):
    def get_test_connection():
        conn = db_module.sqlite3.connect(":memory:")
        conn.row_factory = db_module.sqlite3.Row
        conn.execute('''
            CREATE TABLE urls (
                short_code TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                click_count INTEGER DEFAULT 0
            );
        ''')
        conn.commit()
        return conn
    monkeypatch.setattr(db_module, "get_db_connection", get_test_connection)

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# -------------------------------
# Test Cases
# -------------------------------

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_invalid_url(client):
    response = client.post('/api/shorten', json={'url': 'invalid-url'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_shorten_valid_url(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_code' in data

def test_redirect_and_stats(client):
    # Shorten a valid URL
    post = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = post.get_json()['short_code']

    # Redirect
    redirect = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect.status_code == 302
    assert redirect.headers['Location'] == 'https://example.com'

    # Stats
    stats = client.get(f'/api/stats/{short_code}')
    assert stats.status_code == 200
    data = stats.get_json()
    assert data['click_count'] == 1
    assert data['original_url'] == 'https://example.com'

def test_redirect_invalid_code(client):
    response = client.get('/invalid123')
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_stats_invalid_code(client):
    response = client.get('/api/stats/notfound')
    assert response.status_code == 404
    assert 'error' in response.get_json()
