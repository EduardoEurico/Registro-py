from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.modelos import Crime, Heroi
from app.services.crime import add_crime, listar_crimes, obter_crime, atualizar_crime, deletar_crime, formatar_data

# Criando o Blueprint para crimes
crimes_bp = Blueprint('crimes', __name__)

@crimes_bp.route('/crimes/cadastrar', methods=['POST'])
def add_crime_route():
    return add_crime(request)

@crimes_bp.route('/crimes', methods=['GET'])
def listar_crimes():
    return listar_crimes()

@crimes_bp.route('/crimes/<int:id>', methods=['GET'])
def obter_crimes(id):
   return obter_crime(id)


@crimes_bp.route('/crimes/<int:id>', methods=['PUT'])
def atualizar_crimes(id):
    return atualizar_crime(id)


@crimes_bp.route('/crimes/<int:id>', methods=['DELETE'])
def deletar_crime_route(id):
    return deletar_crime(id)

@crimes_bp.route('/crimes/pagina', methods=['GET'])
def exibir_crimes():
    crimes = Crime.query.all()
    herois = Heroi.query.all()  # Pegue a lista de heróis
    

    return render_template('crime.html', crimes=crimes, herois=herois)


@crimes_bp.route('/crimes/editar/<int:id>', methods=['GET'])
def editar_crime(id):
    crime = Crime.query.get(id)
    herois = Heroi.query.all()  # Carrega todos os heróis
    if crime:
        return render_template('crime.html', crime=crime, herois=herois)
    else:
        return jsonify({"error": "Crime não encontrado!"}), 404

