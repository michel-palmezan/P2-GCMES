from unittest.mock import MagicMock
import pytest
import os
import sys

from static.misc import is_valid_entity, is_valid_id, get_table_and_column, handle_pleito_insertion
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_default_page(client):
    response = client.get('/teste')
    assert response.status_code == 404

def test_is_valid_entity():
    assert is_valid_entity('pleito') == True
    assert is_valid_entity('invalid_entity') == False

def test_is_valid_id():
    assert is_valid_id('individuo', '12345678901234') == True
    assert is_valid_id('individuo', '12345') == False

def test_get_table_and_column():
    assert get_table_and_column('candidatura') == ('Candidatura', 'Cod_Candidatura')
    assert get_table_and_column('invalid_entity') == (None, None)

def test_handle_pleito_insertion():
    mock_cursor = MagicMock()
    form_data = {'Cod_Pleito': '123', 'qtdVotos': '100'}
    handle_pleito_insertion(mock_cursor, form_data)
    mock_cursor.execute.assert_called_once()
