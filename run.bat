@echo off

REM Verificar se Python está instalado
where python >nul 2>nul
if ERRORLEVEL 1 (
    echo Python não está instalado. Por favor, instale o Python e tente novamente.
    echo Visite https://www.python.org/downloads/ para obter instruções de instalação.
    exit /b 1
)

REM Verificar se pip está instalado
where pip >nul 2>nul
if ERRORLEVEL 1 (
    echo pip não está instalado. Por favor, instale o pip e tente novamente.
    echo Visite https://pip.pypa.io/en/stable/installation/ para obter instruções de instalação.
    exit /b 1
)

REM Instalar dependências
pip install pandas psycopg2-binary python-dotenv

REM Executar o programa
python import_excel_to_postgres.py
