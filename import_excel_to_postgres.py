#desenvolvido por Tiago Linhares

import os
import pandas as pd
from dotenv import load_dotenv, set_key
from sqlalchemy import create_engine


# Função para mapear tipos de dados do pandas para tipos em sql
# Modifique a função map_data_types para retornar sempre "TEXT"
def map_data_types(pd_type):
    return "TEXT"


# Carregar as variaveis de ambiente do arquivo .Env
load_dotenv()


# Solicitar os argumentos interativamente
db_choice = input("Escolha o banco de dados (postgres, mysql, sqlserver, bigquery): ").lower()

if db_choice not in ["postgres", "mysql", "sqlserver", "bigquery"]:
    print("Opção inválida. Escolha entre 'postgres', 'mysql', 'sqlserver' e 'bigquery'.")
    exit(1)

db_url = os.getenv(f'{db_choice.upper()}_URL')

if not db_url:
    print(f"As informações de conexão para {db_choice} não foram encontradas. Por favor, insira os detalhes de conexão:")

    host = input("Informe o host do banco de dados: ")
    port = input("Informe a porta do banco de dados: ")
    db_name = input("Informe o nome do banco de dados: ")
    user = input("Informe o nome de usuário do banco de dados: ")
    password = input("Informe a senha do usuário do banco de dados: ")

    if db_choice == "postgres":
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    elif db_choice == "mysql":
        db_url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"
    elif db_choice == "sqlserver":
        db_url = f"mssql+pyodbc://{user}:{password}@{host}:{port}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
    else:  # db_choice == "bigquery":
        db_url = f"bigquery://{db_name}"

    save_credentials = input("Deseja salvar essas informações de conexão? (s/n): ").lower()
    if save_credentials == "s":
        set_key(".env", f"{db_choice.upper()}_URL", db_url)
        print("As informações de conexão foram salvas.")



# Ler dados do arquivo excel usando a biblioteca pandas
excel_file = input("Informe o caminho do arquivo excel a ser importado: ")
file_type = input("Informe o tipo de arquivo excel (xls ou xlsx): ")



if file_type == 'xls':
    excel_data = pd.read_excel(excel_file, engine='xlrd')
else:
    excel_data = pd.read_excel(excel_file)


schema = input("Informe o schema onde a tabela será criada: ")


table_name = input("Informe o nome da tabela a ser criada ou usada no banco de dados: ")


# Altere a criação da tabela de acordo com os tipos de dados do pandas
column_defs = [f"{col} {map_data_types(excel_data[col].dtype)}" for col in excel_data.columns]
create_table_query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({', '.join(column_defs)})"


# Conectar ao banco de dados usando SQLAlchemy
engine = create_engine(db_url)


table_action = input("Escolha a ação para a tabela(estará entre parenteses): criar tabela do zero(nova), apagar dados da existente e substituir(truncar) ou adicionar dados em uma existente(adicionar)")


if table_action not in ["nova", "truncar", "adicionar"]:
    print("Opção inválida. Escolha nova, truncar ou adicionar")
    exit(1)


with engine.connect() as connection:
    if table_action == "nova":
        if_exists = 'replace'
    elif table_action == "truncar":
        connection.execute(f"TRUNCATE TABLE {table_name}")
        if_exists = 'append'
    else: # table_action == "adicionar"
        if_exists = 'append'


# Inserir os dados na tabela do banco de dados
excel_data.to_sql(table_name, engine, schema=schema, if_exists=if_exists, index=False)