# Registro-py
$env:FLASK_APP="app.py" 
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass 
.\venv\Scripts\Activate.ps1


flask db init
flask db migrate -m "Criando a tabela herois"
flask db upgrade
