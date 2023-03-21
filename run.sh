#!/bin/bash

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não está instalado. Por favor, instale o Python3 e tente novamente."
    echo "Visite https://www.python.org/downloads/ para obter instruções de instalação."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip não está instalado. Por favor, instale o pip e tente novamente."
    echo "Visite https://pip.pypa.io/en/stable/installation/ para obter instruções de instalação."
    exit 1
fi

# Instalar dependências
pip install --user pandas psycopg2-binary python-dotenv

# Executar o programa
python3 import_excel_to_postgres.py
