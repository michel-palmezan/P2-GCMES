duplicate_error = 'Candidato já se candidatou para o mesmo cargo no mesmo ano.'

## REMOÇÕES

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

def handle_partido_insertion(cursor, form):
    cod_partido = form['cod_partido']
    nome = form['nome']
    cod_programa = form['cod_programa']
    query = "INSERT INTO Partido (Cod_Partido, Nome, Cod_Programa) VALUES (%s, %s, %s)"
    cursor.execute(query, (cod_partido, nome, cod_programa))

def handle_programa_partido_insertion(cursor, form):
    cod_programa = form['cod_programaPartido']
    descricao = form['programa']
    query = "INSERT INTO ProgramaPartido (Cod_Programa, Descricao) VALUES (%s, %s)"
    cursor.execute(query, (cod_programa, descricao))

def handle_candidatura_insertion(cursor, form):
    codigo_candidatura = form['cod_candidatura']
    codigo_candidato = form['cod_individuo']
    codigo_cargo = form['cod_cargo']
    cod_partido = form['cod_Partido']
    ano = form['ano']
    cod_pleito = form['pleito']
    cod_candidatura_vice = form['cod_candidatura_vice'] or None
    eleito = form['eleito'] == 'SIM'
    total_doacoes = form['total_doacoes'] or 0

    if candidatura_exists(cursor, codigo_candidato, ano, codigo_cargo):
        raise Exception(duplicate_error)
    
    if other_candidatura_exists(cursor, codigo_candidato, ano, codigo_cargo):
        raise Exception(duplicate_error)

    query = """
        INSERT INTO Candidatura 
        (Cod_Candidatura, Cod_Candidato, Cod_Cargo, Cod_Partido, Ano, Cod_Pleito, Cod_Candidatura_Vice, Eleito, Total_Doacoes) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (codigo_candidatura, codigo_candidato, codigo_cargo, cod_partido, ano, cod_pleito, cod_candidatura_vice, eleito, total_doacoes))

def candidatura_exists(cursor, codigo_candidato, ano, codigo_cargo):
    query_check_same_cargo = """
        SELECT 1 FROM Candidatura 
        WHERE Cod_Candidato = %s 
        AND Ano = %s 
        AND Cod_Cargo = %s
    """
    cursor.execute(query_check_same_cargo, (codigo_candidato, ano, codigo_cargo))
    return cursor.fetchone() is not None

def other_candidatura_exists(cursor, codigo_candidato, ano, codigo_cargo):
    query_check_other_cargo = """
        SELECT 1 FROM Candidatura 
        WHERE Cod_Candidato = %s 
        AND Ano = %s 
        AND Cod_Cargo <> %s
    """
    cursor.execute(query_check_other_cargo, (codigo_candidato, ano, codigo_cargo))
    return cursor.fetchone() is not None

def handle_individuo_insertion(cursor, form):
    cpf = form['cpf']
    nome = form['nome_ind']
    ficha_limpa = form.get('ficha_limpa', 'FALSE')
    cod_equipe = form['partido'] or None
    query = "INSERT INTO Individuo (CPF, Nome, Ficha_Limpa, Cod_Equipe) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (cpf, nome, ficha_limpa, cod_equipe))

def handle_cargo_insertion(cursor, form):
    codigo_cargo = form['cod_Cargo']
    descricao = form['descricao']
    localidade = form['localidade']
    qtd_eleitos = form['qtd_Eleitos']
    pais = form['pais']
    estado = form.get('estado', None)
    cidade = form.get('cidade', None)
    query = """
        INSERT INTO Cargo (Cod_Cargo, Descricao, Localidade, Qtd_Eleitos, Pais, Estado, Cidade) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (codigo_cargo, descricao, localidade, qtd_eleitos, pais, estado, cidade))

def handle_equipeapoio_insertion(cursor, form):
    cod_equipe = form['cod_equipe']
    nome_equipe = form['nomeEquipe']
    query = "INSERT INTO EquipeApoio (Cod_Equipe, Nome) VALUES (%s, %s)"
    cursor.execute(query, (cod_equipe, nome_equipe))

def handle_empresa_insertion(cursor, form):
    cnpj = form['cnpj']
    nome = form['nomeEmpresa']
    query = "INSERT INTO Empresa (CNPJ, Nome) VALUES (%s, %s)"
    cursor.execute(query, (cnpj, nome))

def handle_processojudicial_insertion(cursor, form):
    codigo_processo = form['codigo_processo']
    codigo_individuo = form['codigo_individuo']
    data_inicio = form['data_Inicio']
    julgado = form.get('julgado', 'FALSE')
    data_termino = form.get('data_termino', None)
    procedente = form.get('procedente', 'FALSE')
    query = """
        INSERT INTO ProcessoJudicial 
        (Cod_Processo, Cod_Individuo, Data_Inicio, Julgado, Data_Termino, Procedente) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (codigo_processo, codigo_individuo, data_inicio, julgado, data_termino, procedente))