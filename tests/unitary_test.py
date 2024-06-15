from unittest.mock import MagicMock, patch
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, delete_from_db
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
    assert is_valid_entity('empresa') == True
    assert is_valid_id('empresa', '123456789012345678987897988') == False

def test_is_valid_id():
    assert is_valid_id('individuo', '12345678901234') == True
    assert is_valid_id('individuo', '12345') == False

def test_get_table_and_column():
    assert get_table_and_column('candidatura') == ('Candidatura', 'Cod_Candidatura')
    assert get_table_and_column('invalid_entity') == (None, None)

def test_handle_pleito_insertion():
    mock_cursor = MagicMock()
    form_data = {'Cod_Pleito': '49301656876', 'qtdVotos': '100'}
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
    'cod_Cargo': '49301656876',
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
        'cod_Cargo': '49301656876',
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

def test_handle_partido_insertion_execute_called():
        cursor_mock = MagicMock()
        form_mock = {
            'cod_partido': '49301656876',
            'nome': 'Partido X',
            'cod_programa': '456'
        }
        handle_partido_insertion(cursor_mock, form_mock)
        cursor_mock.execute.assert_called_once()

def test_candidatura_exists_execute_called():
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (1,)
    result = candidatura_exists(cursor_mock, '49301656876', '2024', '202')
    assert result is True

def test_other_candidatura_exists_execute_called():
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (1,)
    result = other_candidatura_exists(cursor_mock, '101', '2024', '303')
    assert result is True

def test_handle_individuo_insertion_execute_called():
    cursor_mock = MagicMock()
    form_mock = {
        'cpf': '12345678900',
        'nome_ind': 'João da Silva',
        'ficha_limpa': 'TRUE',
        'partido': '101'
    }
    handle_individuo_insertion(cursor_mock, form_mock)
    cursor_mock.execute.assert_called_once_with(
        "INSERT INTO Individuo (CPF, Nome, Ficha_Limpa, Cod_Equipe) VALUES (%s, %s, %s, %s)",
        ('12345678900', 'João da Silva', 'TRUE', '101')
    )

def test_delete_from_db():
    conn_mock = MagicMock()
    cursor_mock = MagicMock()
    conn_mock.cursor.return_value = cursor_mock

    cursor_mock.rowcount = 1

    with patch('app.get_db_connection', return_value=conn_mock):
        table = 'usuarios'
        id_column = 'id'
        entity_id = '49301656876'
        entity = 'usuário'
        
        result = delete_from_db(table, id_column, entity_id, entity)

        cursor_mock.execute.assert_called_once_with("DELETE FROM usuarios WHERE id = %s", ('49301656876',))

        assert result == "Usuário com ID 123 removido com sucesso."

def test_delete_from_db_no_record_found():
    conn_mock = MagicMock()
    cursor_mock = MagicMock()
    conn_mock.cursor.return_value = cursor_mock

    cursor_mock.rowcount = 0

    with patch('app.get_db_connection', return_value=conn_mock):
        table = 'usuarios'
        id_column = 'id'
        entity_id = '49301656876'
        entity = 'individuo'

        result = delete_from_db(table, id_column, entity_id, entity)

        cursor_mock.execute.assert_called_once_with("DELETE FROM usuarios WHERE id = %s", ('49301656876',))

        assert result == "Nenhum registro encontrado para usuário com ID 123."

def test_handle_candidatura_insertion():
    cursor_mock = MagicMock()

    form_mock = {
        'cod_candidatura': '49301656876',
        'cod_individuo': '25477345732',
        'cod_cargo': '789',
        'cod_Partido': '101',
        'ano': '2024',
        'pleito': '303',
        'cod_candidatura_vice': '404',
        'eleito': 'SIM',
        'total_doacoes': '100000'
    }
    candidatura_exists_mock = MagicMock(return_value=False)
    other_candidatura_exists_mock = MagicMock(return_value=False)

    with patch('app.candidatura_exists', candidatura_exists_mock), \
         patch('app.other_candidatura_exists', other_candidatura_exists_mock):
        
        handle_candidatura_insertion(cursor_mock, form_mock)
        cursor_mock.execute.assert_called_once()

        candidatura_exists_mock.assert_called_once_with(cursor_mock, '456', '2024', '789')
        other_candidatura_exists_mock.assert_called_once_with(cursor_mock, '456', '2024', '789')