from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializa os objetos do banco de dados e migração
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Carrega as configurações do Config

    # Inicializa o banco de dados e o Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Importa e registra as rotas dentro da função
    from app.routes.heroi_routes import heroes_bp  # Importação tardia para evitar a dependência circular
    from app.routes.crime_routes import crimes_bp  # Rotas para crimes

    app.register_blueprint(heroes_bp)  # Registra o Blueprint com as rotas
    app.register_blueprint(crimes_bp)  # Registra o Blueprint com as rotas

    return app
