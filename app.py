from psycopg2 import Error, connect
from flask import Flask, request, jsonify, render_template
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from os import getenv
from misc import handle_candidatura_insertion, handle_cargo_insertion, handle_empresa_insertion
from misc import handle_equipeapoio_insertion, handle_individuo_insertion, handle_partido_insertion
from misc import handle_pleito_insertion, handle_processojudicial_insertion, handle_programa_partido_insertion
from misc import is_valid_entity, is_valid_id, get_invalid_message, get_table_and_column

app = Flask(__name__, template_folder='./docs')
app.config['WTF_CSRF_ENABLED'] = getenv("WTF_CSRF_ENABLED")
csrf = CSRFProtect(app)
load_dotenv()

# Definindo constantes
DELETE_TEMPLATE = 'delete.html'
METHODS = ['GET', 'POST']

def get_db_connection():
    try:
        conn = connect(
            dbname=getenv("DB_NAME"),
            user=getenv("USER"),
            password=getenv("PSSWD"),
            host=getenv("HOST"),
            port=getenv("PORT")
        )
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def delete_from_db(table, id_column, entity_id, entity):
    query = f"DELETE FROM {table} WHERE {id_column} = %s"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (entity_id,))
        
        if cursor.rowcount == 0:
            message = f"Nenhum registro encontrado para {entity} com ID {entity_id}."
        else:
            conn.commit()
            message = f"{entity.capitalize()} com ID {entity_id} removido com sucesso."
    except:
        conn.rollback()
        message = f"Erro ao remover {entity}"
    finally:
        cursor.close()
        conn.close()
    return message

message = "Dados inseridos com sucesso!"

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/candidaturas/eleitos', methods=['GET'])
def get_eleitos():
    query = """
    SELECT Candidatura.*, Individuo.Nome AS Nome, Partido.Nome AS Partido, Cargo.Localidade, Vice.Cod_Candidato AS Vice_Candidato
    FROM Candidatura
        JOIN Individuo ON Candidatura.Cod_Candidato = Individuo.CPF
        JOIN Partido ON Candidatura.Cod_Partido = Partido.Cod_Partido
        JOIN Cargo ON Candidatura.Cod_Cargo = Cargo.Cod_Cargo
        LEFT JOIN Candidatura AS Vice ON Candidatura.Cod_Candidatura_Vice = Vice.Cod_Candidatura
    WHERE Candidatura.Eleito = TRUE
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    candidaturas = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for candidatura in candidaturas:
        result.append({
            'Cod_Candidatura': candidatura[0],
            'Cod_Candidato': candidatura[1],
            'Cod_Cargo': candidatura[2],
            'Ano': candidatura[3],
            'Cod_Pleito': candidatura[4],
            'Cod_Candidatura_Vice': candidatura[5],
            'Eleito': candidatura[6],
            'Partido': candidatura[7],
            'Localidade': candidatura[8],
            'Vice_Candidato': candidatura[9]
        })
    return render_template('eleitos.html', candidaturas=result)

@app.route('/candidaturas', methods=['GET'])
def list_candidaturas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        ano = request.args.get('ano')
        nome_candidato = request.args.get('nome_candidato')
        cargo = request.args.get('cargo')
        order_by = request.args.get('order_by', 'Ano')
        order_dir = request.args.get('order_dir', 'ASC')

        # Whitelist for order_by and order_dir values
        valid_order_by_columns = ['Ano', 'Nome_Candidato', 'Partido', 'Localidade', 'Total_doacoes']
        valid_order_dir = ['ASC', 'DESC']

        if order_by not in valid_order_by_columns:
            order_by = 'Ano'
        if order_dir not in valid_order_dir:
            order_dir = 'ASC'

        query = """
        SELECT Candidatura.*, Individuo.Nome AS Nome_Candidato, Partido.Nome AS Partido, Cargo.Localidade, Total_doacoes AS totDoacoes
        FROM Candidatura 
        JOIN Individuo ON Candidatura.Cod_Candidato = Individuo.CPF 
        JOIN Partido ON Candidatura.Cod_Partido = Partido.Cod_Partido 
        JOIN Cargo ON Candidatura.Cod_Cargo = Cargo.Cod_Cargo
        """
        filters = []
        params = []

        if ano:
            filters.append("Candidatura.Ano = %s")
            params.append(ano)
        elif nome_candidato:
            filters.append("Individuo.Nome LIKE %s")
            params.append(f"%{nome_candidato}%")
        elif cargo:
            filters.append("Cargo.cod_cargo = %s")
            params.append(cargo)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Add the ORDER BY clause with sanitized values
        query += f" ORDER BY {order_by} {order_dir}"

        cursor.execute(query, tuple(params))
        candidaturas = cursor.fetchall()

        cursor.close()
        conn.close()

        result = []
        for candidatura in candidaturas:
            result.append({
                'Cod_Candidatura': candidatura[0],
                'Cod_Candidato': candidatura[1],
                'Cod_Cargo': candidatura[2],
                'Ano': candidatura[4],
                'Cod_Pleito': candidatura[5],
                'Cod_Candidatura_Vice': candidatura[6],
                'Eleito': candidatura[7],
                'Nome_Candidato': candidatura[9],
                'Partido': candidatura[3],
                'Localidade': candidatura[9],
                'total_doacoes': candidatura[8]
            })

        return render_template('candidaturas.html', candidaturas=result)

    except Error as e:
        return jsonify({'error': str(e)}), 500

# Rota para obter candidatos com ficha limpa
@app.route('/candidatos/ficha-limpa', methods=['GET'])
def get_ficha_limpa():
    query = "SELECT * FROM Individuo WHERE Ficha_Limpa = TRUE"
    
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        candidatos = cursor.fetchall()
        cursor.close()
        conn.close()
    except Error as e:
        if conn:
            conn.close()
        return jsonify({'error': str(e)}), 500

    result = []
    for candidato in candidatos:
        result.append({
            'CPF': candidato[0],
            'Nome': candidato[1],
            'Ficha_Limpa': candidato[2]
        })
    return render_template('ficha_limpa.html', candidatos=result)

@app.route('/delete',methods=METHODS)
def delete_entity():
    if request.method == 'POST':
        entity = request.form['entity'].lower()
        user_id = request.form['id']
        
        if not is_valid_entity(entity) or not is_valid_id(entity, user_id):
            message = get_invalid_message(entity)
            return render_template(DELETE_TEMPLATE, message=message)
        
        table, id_column = get_table_and_column(entity)
        if not table or not id_column:
            message = "Entidade ou coluna de ID inválida."
            return render_template(DELETE_TEMPLATE, message=message)
        
        message = delete_from_db(table, id_column, user_id, entity)
        return render_template(DELETE_TEMPLATE, message=message)
    
    return render_template(DELETE_TEMPLATE)

@app.route('/inserir', methods=METHODS)
def inserir():
    if request.method == 'POST':
        entity = request.form['entity']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if entity == 'pleito':
                handle_pleito_insertion(cursor, request.form)
            elif entity == 'partido':
                handle_partido_insertion(cursor, request.form)
            elif entity == 'programaPartido':
                handle_programa_partido_insertion(cursor, request.form)
            elif entity == 'candidatura':
                handle_candidatura_insertion(cursor, request.form)
            elif entity == 'individuo':
                handle_individuo_insertion(cursor, request.form)
            elif entity == 'cargo':
                handle_cargo_insertion(cursor, request.form)
            elif entity == 'equipeapoio':
                handle_equipeapoio_insertion(cursor, request.form)
            elif entity == 'empresa':
                handle_empresa_insertion(cursor, request.form)
            elif entity == 'processojudicial':
                handle_processojudicial_insertion(cursor, request.form)
            conn.commit()
        except Exception as error:
            conn.rollback()
            message = f"Erro ao inserir dados: {error}"
        finally:
            cursor.close()
            conn.close()
        
        return render_template('inserir.html', message=message)

    return render_template('inserir.html')

@app.route('/doacoes', methods=METHODS)
def doacoes():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        doador_tipo = request.form['doador_tipo']
        
        try:
            if doador_tipo == "Físico":
                nf_doacao = request.form['nota_doacao']
                cod_doador = request.form['cod_doador_pf']
                valor = request.form['valor_pf']
                data_doacao = request.form['data_doacao_pf']
                query_check = "SELECT 1 FROM DoacaoPF WHERE Cod_Nota = %s"
                cursor.execute(query_check, (nf_doacao,))
                exists = cursor.fetchone()
                
                if exists:
                    query_update_candidatura = """
                        UPDATE Candidatura
                        SET Total_Doacoes = Total_Doacoes + %s
                        WHERE Cod_Candidatura = (
                            SELECT Cod_Candidatura FROM Candidatura WHERE Cod_Candidato = %s
                        )
                    """
                    cursor.execute(query_update_candidatura, (valor, cod_doador))
                else:
                    query_update_candidatura = """
                        UPDATE Candidatura
                        SET Total_Doacoes = Total_Doacoes + %s
                        WHERE Cod_Candidatura = (
                            SELECT Cod_Candidatura FROM Candidatura WHERE Cod_Candidato = %s
                        )
                    """
                    cursor.execute(query_update_candidatura, (valor, cod_doador))

                    query_insert_doacaopf = """
                        INSERT INTO DoacaoPF (Cod_Nota, Cod_Individuo, Valor, data_doacao)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(query_insert_doacaopf, (nf_doacao, cod_doador, valor, data_doacao))
                
                conn.commit()
            elif doador_tipo == "Jurídico":
                cod_doador = request.form['cod_doador_pj']
                cod_candidatura = request.form['cod_candidatura_pj']
                valor = request.form['valor_pj']
                data_doacao = request.form['data_doacao_pj']
                query = "INSERT INTO DoadorPJ (Cod_Empresa, Cod_Candidatura, Valor, data_doacao) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (cod_doador, cod_candidatura, valor, data_doacao))
                conn.commit()
            else:
                raise ValueError("Tipo de doador inválido.")
        
        except Exception as e:
            conn.rollback()
            message = "Erro ao registrar doação"
            print(e)
        
        finally:
            cursor.close()
            conn.close()
    
        return render_template('doacoes.html', message=message)

    return render_template('doacoes.html')

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=getenv("DEBUG"))
