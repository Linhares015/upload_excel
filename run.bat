@echo off

echo.
echo -----------------------------------------
echo UPLOAD EXCEL TO POSTGRES - by Tiago Linhares
echo -----------------------------------------
echo.

call vm_py/Scripts/activate.bat

python import_excel_to_postgres.py

pause