from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.modelos import Crime
from app.services.crime import add_crime, listar_crimes, obter_crime, atualizar_crime, deletar_crime

# Criando o Blueprint para crimes
crimes_bp = Blueprint('crimes', __name__)

@crimes_bp.route('/crimes/cadastrar', methods=['POST'])
def add_crime_route():
    return add_crime(request)

@crimes_bp.route('/crimes', methods=['GET'])
def listar_crimes():
    return listar_crimes()

@crimes_bp.route('/crimes/<int:id>', methods=['GET'])
def obter_crime(id):
   return obter_crime(id)


@crimes_bp.route('/crimes/<int:id>', methods=['PUT'])
def atualizar_crime(id):
    return atualizar_crime(id)


@crimes_bp.route('/crimes/<int:id>', methods=['DELETE'])
def deletar_crime_route(id):
    return deletar_crime(id)

@crimes_bp.route('/crimes/pagina', methods=['GET'])
def exibir_crimes():
    crimes = Crime.query.all()
    return render_template('crime.html', crimes=crimes)