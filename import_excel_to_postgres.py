#desenvolvido por Tiago Linhares

import os
import pandas as pd
from dotenv import load_dotenv, set_key
from sqlalchemy import create_engine


# Função para mapear tipos de dados do pandas para tipos em sql
# Modifique a função map_data_types para retornar sempre "TEXT"
def map_data_types(pd_type):
    return "TEXT"


def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print("O arquivo não foi encontrado. Por favor, verifique o caminho e tente novamente.")
        return False
    return True


# Função para carregar conexões salvas
def load_saved_connections():
    saved_connections = {}
    for key, value in os.environ.items():
        if key.endswith("_URL"):
            db_name = key[:-4].lower()
            saved_connections[db_name] = value
    return saved_connections


# Função para excluir uma conexão salva
def delete_saved_connection(saved_connections, alias):
    del_key = f"{alias.upper()}_URL"
    if del_key in os.environ:
        os.environ.pop(del_key)
        with open('.env', 'r') as f:
            lines = f.readlines()
        with open('.env', 'w') as f:
            for line in lines:
                if not line.startswith(del_key):
                    f.write(line)
        print(f"A conexão '{alias}' foi excluída.")
    else:
        print(f"Não foi possível encontrar a conexão '{alias}' para excluir.")

def choose_saved_connection(saved_connections):
    if not saved_connections:
        print("Nenhuma conexão salva encontrada.")
        return None

    print("Conexões salvas:")
    for alias, url in saved_connections.items():
        print(f"{alias}: {url}")

    chosen_alias = input("Digite o apelido da conexão que deseja usar ou 'n' para criar uma nova conexão: ").lower()
    if chosen_alias == 'n':
        return None
    elif chosen_alias in saved_connections:
        return saved_connections[chosen_alias]
    else:
        print("Apelido de conexão inválido.")
        return choose_saved_connection(saved_connections)


# Carregar as variaveis de ambiente do arquivo .Env
load_dotenv()

saved_connections = load_saved_connections()
db_url = choose_saved_connection(saved_connections)

if db_url is None:
    delete_choice = input("Deseja excluir uma conexão salva? (s/n): ").lower()
    if delete_choice == 's':
        alias_to_delete = input("Digite o apelido da conexão que deseja excluir: ")
        delete_saved_connection(saved_connections, alias_to_delete)
        saved_connections = load_saved_connections()
        db_url = choose_saved_connection(saved_connections)

if db_url is None:
    db_choice = input("Escolha o banco de dados (postgres, mysql, sqlserver, bigquery): ").lower()

    if db_choice not in ["postgres", "mysql", "sqlserver", "bigquery"]:
        print("Opção inválida. Escolha entre 'postgres', 'mysql', 'sqlserver' e 'bigquery'.")
        exit(1)



# Ler dados do arquivo excel usando a biblioteca pandas
while True:
    excel_file = input("Informe o caminho do arquivo excel a ser importado: ")
    if check_file_exists(excel_file):
        break
    else:
        print("O caminho do arquivo fornecido não é válido. Tente novamente.")

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


table_action = input("Escolha a ação para a tabela(estará entre parenteses): criar tabela do zero(nova) ou adicionar dados em uma existente(adicionar): ")


if table_action not in ["nova", "truncar", "adicionar"]:
    print("Opção inválida. Escolha nova, truncar ou adicionar")
    exit(1)


with engine.connect() as connection:
    if table_action == "nova":
        if_exists = 'replace'
    elif table_action == "truncar":
        connection.execute(f"TRUNCATE TABLE {schema}.{table_name}")
        if_exists = 'append'
    else: # table_action == "adicionar"
        if_exists = 'append'



# Inserir os dados na tabela do banco de dados
excel_data.to_sql(table_name, engine, schema=schema, if_exists=if_exists, index=False)
