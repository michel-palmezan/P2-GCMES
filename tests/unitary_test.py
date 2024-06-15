import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_default_page(client):
    response = client.get('/teste')
    assert response.status_code == 404

def test_index():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_get_eleitos():
    with app.test_client() as client:
        response = client.get('/candidaturas/eleitos')
        assert response.status_code == 200

def test_list_candidaturas():
    with app.test_client() as client:
        response = client.get('/candidaturas')
        assert response.status_code == 200

def test_get_ficha_limpa():
    with app.test_client() as client:
        response = client.get('/candidatos/ficha-limpa')
        assert response.status_code == 200

def test_delete_entity():
    with app.test_client() as client:
        response = client.get('/delete')
        assert response.status_code == 200

def test_inserir():
    with app.test_client() as client:
        response = client.get('/inserir')
        assert response.status_code == 200

def test_doacoes():
    with app.test_client() as client:
        response = client.get('/doacoes')
        assert response.status_code == 200