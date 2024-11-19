from flask import Blueprint, render_template, request, jsonify
from app.models.modelos import db, Heroi  # Corrigido
from datetime import datetime
from app.services.heroi import add_hero # Importe a função add_hero do novo arquivo heroi.py

heroes_bp = Blueprint('heroes', __name__, url_prefix='/heroes')

@heroes_bp.route('/cadastrar', methods=['POST'])
def add_hero_route():
    return add_hero(request)  # Chama a função do arquivo heroi.py

@heroes_bp.route('/herois', methods=['GET'])
def get_heroes():
    heroes = Heroi.query.all()
    return render_template('herois.html', heroes=heroes)

@heroes_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@heroes_bp.route('/heroes', methods=['GET'])
def get_heroes_crime():
    heroes = Heroi.query.all()
    return jsonify([hero.to_dict() for hero in heroes])