from flask import Blueprint, render_template, request, jsonify
from app.models.modelos import db, Heroi, Battle  # Certifique-se de importar os modelos Heroi e Battle
from datetime import datetime
from app.services.Factory.Battle import create_battle, calculate_battle  # Importe as funções do novo arquivo battle.py
import logging

battles_bp = Blueprint('battles', __name__, url_prefix='/battles')

@battles_bp.route('/criar', methods=['POST'])
def create_battle_route():
    data = request.json  # Recebe os dados do cliente
    hero1_id = data.get('hero1_id')
    hero2_id = data.get('hero2_id')
    battle_date = data.get('battle_date', datetime.utcnow().strftime('%Y-%m-%d'))

    try:
        battle = create_battle(hero1_id, hero2_id, battle_date)
        return jsonify({"message": "Batalha criada com sucesso!", "battle": battle}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Erro ao criar batalha: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Erro ao criar batalha."}), 500

@battles_bp.route('/listar', methods=['GET'])
def list_battles():
    battles = Battle.query.all()
    battles_json = [battle.to_dict() for battle in battles]
    return jsonify(battles_json), 200

@battles_bp.route('/<int:id>', methods=['GET'])
def get_battle(id):
    battle = Battle.query.get(id)
    if battle:
        return jsonify(battle.to_dict()), 200
    return jsonify({"error": "Batalha não encontrada."}), 404

@battles_bp.route('/', methods=['GET'])
def index():
    battles = Battle.query.all()
    battles_json = [battle.to_dict() for battle in battles]
    return render_template('batalhas.html', battles=battles_json)
