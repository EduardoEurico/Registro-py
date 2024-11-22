from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.modelos import Missao, Heroi
from app.services.missao import add_mission, listar_missoes, get_missions_by_difficulty_and_hero, deletar_missao

# Criando o Blueprint para missões
missoes_bp = Blueprint('missoes', __name__)


@missoes_bp.route('/missoes/cadastrar', methods=['POST'])
def add_mission_route():
    data = request.json
    return add_mission()


@missoes_bp.route('/missoes', methods=['GET'])
def list_missoes():
    return listar_missoes()


@missoes_bp.route('/missoes/<int:id>', methods=['GET'])
def obter_missoes():
    difficulty = request.args.get('difficulty')
    hero_id = request.args.get('hero_id')
    return get_missions_by_difficulty_and_hero(difficulty=difficulty, hero_id=hero_id)


@missoes_bp.route('/missoes/deletar/<int:id>', methods=['DELETE'])
def deletar_missoes_route(id):
    return deletar_missao(id)


@missoes_bp.route('/missoes/pagina', methods=['GET'])
def exibir_missoes():
    missoes = Missao.query.all()
    herois = Heroi.query.all()  # Pegue a lista de heróis

    return render_template('missoes.html', missao=missoes, herois=herois)

