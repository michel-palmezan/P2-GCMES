from unittest.mock import MagicMock, patch
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from misc_test import *

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

def test_get_invalid_message():
    assert get_invalid_message('individuo') == "CPF inválido ou não encontrado!"
    assert get_invalid_message('empresa') == "CNPJ inválido ou não encontrado!"
    assert get_invalid_message('invalid_entity') == "Entidade ou coluna de ID inválida."

def test_handle_partido_insertion():
    mock_cursor = MagicMock()
    form_data = {'cod_partido': '123', 'nome': 'Partido X', 'cod_programa': '456'}
    handle_partido_insertion(mock_cursor, form_data)
    mock_cursor.execute.assert_called_once()

def test_handle_programa_partido_insertion():
    mock_cursor = MagicMock()
    form_data = {'cod_programaPartido': '789', 'programa': 'Programa Y'}
    handle_programa_partido_insertion(mock_cursor, form_data)
    mock_cursor.execute.assert_called_once()

def test_handle_equipeapoio_insertion():
    mock_cursor = MagicMock()
    form_data = {'cod_equipe': '101', 'nomeEquipe': 'Equipe Z'}
    handle_equipeapoio_insertion(mock_cursor, form_data)
    mock_cursor.execute.assert_called_once()

def test_handle_empresa_insertion():
    mock_cursor = MagicMock()
    form_data = {'cnpj': '12345678901234', 'nomeEmpresa': 'Empresa A'}
    handle_empresa_insertion(mock_cursor, form_data)
    mock_cursor.execute.assert_called_once()

