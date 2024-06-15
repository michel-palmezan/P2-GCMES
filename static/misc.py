
from app import get_db_connection

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

def delete_from_db(table, id_column, id, entity):
    query = f"DELETE FROM {table} WHERE {id_column} = %s"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        
        if cursor.rowcount == 0:
            message = f"Nenhum registro encontrado para {entity} com ID {id}."
        else:
            conn.commit()
            message = f"{entity.capitalize()} com ID {id} removido com sucesso."
    except Exception as e:
        conn.rollback()
        message = f"Erro ao remover {entity}: {e}"
    finally:
        cursor.close()
        conn.close()
    return message