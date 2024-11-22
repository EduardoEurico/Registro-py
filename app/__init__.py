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

    from app.routes.index_route import index_bp
    from app.routes.heroi_routes import heroes_bp  # Importação tardia para evitar a dependência circular
    from app.routes.crime_routes import crimes_bp  # Rotas para crimes
    from app.routes.battle_routes import battles_bp  # Importa as rotas de batalhas
    from app.routes.missao_routes import missoes_bp #Importa as rotas das missões

    app.register_blueprint(index_bp)
    app.register_blueprint(heroes_bp)  # Registra o Blueprint com as rotas
    app.register_blueprint(crimes_bp)  # Registra o Blueprint com as rotas
    app.register_blueprint(battles_bp)  # Registra o Blueprint das batalhas
    app.register_blueprint(missoes_bp) #Registra o Blueprint das missões

    return app
