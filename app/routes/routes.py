from flask import Blueprint, request, jsonify
from models import db, Hero
from datetime import datetime

heroes_bp = Blueprint('heroes', __name__, url_prefix='/heroes')

@heroes_bp.route('/add', methods=['POST'])
def add_hero():
    data = request.json  # Recebe os dados do cliente
    try:
        new_hero = Hero(
            real_name=data.get('real_name'),
            hero_name=data.get('hero_name'),
            gender=data.get('gender'),
            height=float(data.get('height', 0)),
            weight=float(data.get('weight', 0)),
            birth_date=datetime.strptime(data.get('birth_date'), '%Y-%m-%d'),
            birth_place=data.get('birth_place'),
            powers=data.get('powers'),  # String separada por vírgulas
            strength_level=int(data.get('strength_level', 0)),
            popularity=int(data.get('popularity', 0)),
            status=data.get('status', 'Ativo')
        )
        db.session.add(new_hero)
        db.session.commit()
        return jsonify({"message": "Herói cadastrado com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
