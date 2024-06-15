from unittest.mock import MagicMock
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

def is_valid_entity(entity):
    valid_entities = [
        'pleito', 'candidatura', 'cargo', 'individuo',
        'equipeapoio', 'doadoresf', 'doadoresj',
        'processojudicial', 'empresa'
    ]
    return entity in valid_entities

def is_valid_id(entity, id):
    if entity == 'individuo' and len(id) != 14:
        return False
    if entity == 'empresa' and len(id) != 18:
        return False
    return True

def get_invalid_message(entity):
    if entity == 'individuo':
        return "CPF inválido ou não encontrado!"
    if entity == 'empresa':
        return "CNPJ inválido ou não encontrado!"
    return "Entidade ou coluna de ID inválida."

def get_table_and_column(entity):
    table_mapping = {
        'pleito': 'Pleito',
        'candidatura': 'Candidatura',
        'cargo': 'Cargo',
        'individuo': 'Individuo',
        'equipeapoio': 'EquipeApoio',
        'doadoresf': 'DoacaoPF',
        'doadoresj': 'DoadorPJ',
        'processojudicial': 'ProcessoJudicial',
        'empresa': 'empresa'
    }
    id_column_mapping = {
        'pleito': 'Cod_Pleito',
        'candidatura': 'Cod_Candidatura',
        'individuo': 'CPF',
        'cargo': 'Cod_Cargo',
        'equipeapoio': 'Cod_Equipe',
        'doadoresf': 'Cod_Nota',
        'doadoresj': 'Cod_Candidatura',
        'processojudicial': 'Cod_Processo',
        'empresa': 'cnpj'
    }
    return table_mapping.get(entity), id_column_mapping.get(entity)

## INSERÇÕES

def handle_pleito_insertion(cursor, form):
    cod_pleito = form['Cod_Pleito']
    qtd_votos = form['qtdVotos']
    query = "INSERT INTO Pleito (Cod_Pleito, Qtd_Votos) VALUES (%s, %s)"
    cursor.execute(query, (cod_pleito, qtd_votos))

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
