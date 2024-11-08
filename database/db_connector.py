import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'sis3')
    )

def pega_dados_refacao(db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor(dictionary=True)  # dictionary=True para acessar colunas por nome
        query = """
            SELECT * FROM `DadosApiReprocesso`
            WHERE status = 'solicitado' AND quantidade IS NOT NULL AND quantidade > 0
            ORDER BY `DadosApiReprocesso`.`id` DESC
        """
        cursor.execute(query)
        
        # Guardar os resultados na lista
        lista = []
        for row in cursor.fetchall():
            # Concatenando os valores para ter o mesmo formato que no C#
            lista.append(
                f"{row['idpedido']}|{row['tipo']}|{row['id']}|{row['quantidade']}"
            )

    except mysql.connector.Error as err:
        print(f"Erro ao acessar o banco de dados: {err}")
        lista = []  # Retorna uma lista vazia em caso de erro

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return lista

def pega_pedido_por_id(id, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor(dictionary=True)  # Para acessar colunas por nome
        query = f"""
            SELECT * FROM `DadosApi`
            WHERE id = '{id}' AND status != 'Pdfs não localizados'
        """
        cursor.execute(query)
        
        # Guardar os resultados na lista
        lista = []
        for row in cursor.fetchall():
            lista.append(
                f"{row['nomedialetica']}|{row['codproduto']}|{row['tipodeproduto']}|{row['numpedido']}|{row['numitem']}|"
                f"{row['isbn']}|{row['titulodolivro']}|{row['subtitulo']}|{row['editoraSelo']}|{row['tiragem']}|"
                f"{row['papelcapa']}|{row['gramaturacapa']}|{row['corescapa']}|{row['formatoabertocapa']}|{row['formatodalombada']}|"
                f"{row['medidadaorelha']}|{row['acabamentocapa']}|{row['papelmiolo']}|{row['gramaturamiolo']}|{row['coresmiolo']}|"
                f"{row['formatomiolo']}|{row['paginasmiolototal']}|{row['paginasmiolopb']}|{row['paginasmiolocor']}|"
                f"{row['acabamentolivro']}|{row['embalagemdolivro']}|{row['precounitdolivro']}|{row['tiragemmarcador']}|"
                f"{row['datapedido']}|{row['data']}|{row['status']}|{row['id']}|{row['marketplace']}"
            )

    except mysql.connector.Error as err:
        print(f"Erro ao acessar o banco de dados: {err}")
        lista = []  # Retorna uma lista vazia em caso de erro

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    return lista

def atualiza_status_refacao(id, db_config):
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()
        query = f"""
            UPDATE DadosApiReprocesso
            SET status = 'Pedido enviado para impressao'
            WHERE id = '{id}'
        """
        cursor.execute(query)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao atualizar o status da refação: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
