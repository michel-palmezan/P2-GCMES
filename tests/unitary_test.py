from unittest.mock import MagicMock
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from misc import *

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

def test_is_valid_entity_invalid_length():
    assert is_valid_entity('empresa', '123') == False
    assert is_valid_entity('empresa', '123456789012345678') == False

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

def test_handle_cargo_insertion():
    cursor_mock = MagicMock()
    form_mock = {
    'cod_Cargo': '123',
    'descricao': 'Cargo Test',
    'localidade': 'Local Test',
    'qtd_Eleitos': '2',
    'pais': 'Brasil',
    'estado': 'SP',
    'cidade': 'São Paulo'
}
    handle_cargo_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once()

def test_handle_equipeapoio_insertion():
    cursor_mock = MagicMock()
    form_mock = {
    'cod_equipe': '101',
    'nomeEquipe': 'Equipe Z'
}
    handle_equipeapoio_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once()  

def test_handle_empresa_insertion():
    cursor_mock = MagicMock()
    form_mock = {'cnpj': '12345678901234', 'nomeEmpresa': 'Empresa A'}
    handle_empresa_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once()  

def test_handle_processojudicial_insertion():
    cursor_mock = MagicMock()
    form_mock = {
    'codigo_processo': '456',
    'codigo_individuo': '789',
    'data_Inicio': '2024-06-20',
    'julgado': 'TRUE',
    'data_termino': '2024-12-31',
    'procedente': 'TRUE'
}
    handle_processojudicial_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once()  

def test_handle_cargo_insertion_execute_called():
    cursor_mock = MagicMock()
    form_mock = {
        'cod_Cargo': '123',
        'descricao': 'Cargo Test',
        'localidade': 'Local Test',
        'qtd_Eleitos': '2',
        'pais': 'Brasil',
        'estado': 'SP',
        'cidade': 'São Paulo'
    }
    handle_cargo_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once()

def test_handle_processojudicial_insertion_execute_called():
    cursor_mock = MagicMock()
    form_mock = {
        'codigo_processo': '456',
        'codigo_individuo': '789',
        'data_Inicio': '2024-06-20',
        'julgado': 'TRUE',
        'data_termino': '2024-12-31',
        'procedente': 'TRUE'
    }
    handle_processojudicial_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once()
