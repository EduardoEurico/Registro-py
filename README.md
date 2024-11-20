# Registro-py
$env:FLASK_APP="app.py" 
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass 
.\venv\Scripts\Activate.ps1

pip install flask-migrate

flask db init
flask db migrate -m "Criando a tabela herois"
flask db upgrade




# Banco de dados
CREATE TABLE herois (
    id SERIAL PRIMARY KEY,
    real_name VARCHAR(100) NOT NULL,
    hero_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    height FLOAT,
    weight FLOAT,
    birth_date DATE,
    birth_place VARCHAR(100),
    powers VARCHAR(255) NOT NULL,
    strength_level INTEGER NOT NULL,
    popularity INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Ativo'
);
CREATE TABLE crimes (
    id SERIAL PRIMARY KEY,
    crime_name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    crime_date VARCHAR(100) NOT NULL,
    severity INTEGER NOT NULL,
    res_hero VARCHAR(100) NOT NULL,
    res_hero_id INTEGER NOT NULL,
    FOREIGN KEY (res_hero_id) REFERENCES herois(id) ON DELETE CASCADE
);