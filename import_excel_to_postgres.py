import os
import pandas as pd
import psycopg2
from psycopg2.extensions import AsIs
from dotenv import load_dotenv

# Função para mapear tipos de dados do pandas para tipos de dados do PostgreSQL
def map_data_types(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"
    else:
        return "TEXT"

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Solicitar os argumentos interativamente
excel_file = input('Digite o caminho do arquivo Excel a ser importado: ')
db_host = input('Digite o host do banco de dados PostgreSQL (padrão: ' + os.getenv('DB_HOST') + '): ') or os.getenv('DB_HOST')
db_name = input('Digite o nome do banco de dados PostgreSQL (padrão: ' + os.getenv('DB_NAME') + '): ') or os.getenv('DB_NAME')
db_user = input('Digite o nome do usuário do banco de dados PostgreSQL (padrão: ' + os.getenv('DB_USER') + '): ') or os.getenv('DB_USER')
db_password = input('Digite a senha do usuário do banco de dados PostgreSQL (padrão: ' + os.getenv('DB_PASSWORD') + '): ') or os.getenv('DB_PASSWORD')
table_name = input('Digite o nome da tabela a ser criada no banco de dados: ')
file_type = input('Digite o tipo de arquivo Excel (xls ou xlsx, padrão: xlsx): ') or 'xlsx'

create_table = input('Deseja criar uma nova tabela no banco de dados, se não existir? (s/n): ').lower() == 's'
truncate_table = input('Deseja truncar a tabela antes de inserir os novos dados? (s/n): ').lower() == 's'
append = input('Deseja adicionar dados à tabela existente? (s/n): ').lower() == 's'

# Ler os dados do arquivo Excel usando a biblioteca pandas
if file_type == 'xls':
    excel_data = pd.read_excel(excel_file, engine='xlrd')
else:
    excel_data = pd.read_excel(excel_file)

# Conectar ao banco de dados PostgreSQL
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

c = conn.cursor()

if create_table:
    # Identificar os nomes das colunas e os tipos de dados
    column_names = excel_data.columns
    column_types = [map_data_types(dtype) for dtype in excel_data.dtypes]

    # Criar a tabela no banco de dados (caso ela ainda não exista)
    columns_str = ', '.join([f'{column_name} {column_type}' for column_name, column_type in zip(column_names, column_types)])
    create_table_query = f'''CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});'''
    c.execute(create_table_query)

if truncate_table:
    # Truncar a tabela antes de inserir os novos dados
    c.execute(f'''TRUNCATE TABLE {table_name};''')

# Inserir os dados na tabela do banco de dados
column_names_str = ', '.join(column_names)
placeholders = ', '.join(['%s' for _ in column_names])

for row in excel_data.itertuples(index=False):
    c.execute(f'''INSERT INTO {table_name} ({column_names_str})
                VALUES ({placeholders})''', row)

# Salvar as mudanças no banco de dados e fechar a conexão
conn.commit()
conn.close()
