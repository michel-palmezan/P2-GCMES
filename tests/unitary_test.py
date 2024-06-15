import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, handle_candidatura_insertion, delete_from_db
import unittest
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_default_page(client):
    response = client.get('/teste')
    assert response.status_code == 404

def test_handle_candidatura_insertion():
    with patch('app.get_db_connection') as mock_get_db_connection:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        form_data = {
            'cod_candidatura': '1',
            'cod_individuo': '12345678901',
            'cod_cargo': '2',
            'cod_Partido': '3',
            'ano': '2024',
            'pleito': '4',
            'cod_candidatura_vice': '5',
            'eleito': 'SIM',
            'total_doacoes': '1000'
        }

        handle_candidatura_insertion(mock_cursor, form_data)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

def test_delete_from_db():
    with patch('app.get_db_connection') as mock_get_db_connection:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        table = 'Candidatura'
        id_column = 'Cod_Candidatura'
        entity_id = '1'
        entity = 'candidatura'

        message = delete_from_db(table, id_column, entity_id, entity)

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        assert message == 'Candidatura com ID 1 removido com sucesso.'