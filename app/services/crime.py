from flask import jsonify, request
from datetime import datetime
from app import db
from app.models.modelos import db,Crime
import logging


def add_crime(request):
    
    data = request.json  # Recebe os dados do cliente
    logging.debug(f"Dados recebidos: {data}")  # Log dos dados recebidos
    try:
        # Validar e converter a data do crime
        data['crime_date'] = datetime.strptime(data['crime_date'], "%Y-%m-%d")
        
        # Criar uma nova instância de Crime
        new_crime = Crime(
            crime_name=data.get('crime_name'),
            description=data.get('description'),
            crime_date=data.get('crime_date'),
            res_hero=data.get('res_hero'),
            severity=data.get('severity')
        )
        
        # Adicionar ao banco de dados
        db.session.add(new_crime)
        db.session.commit()
        
        return jsonify({
            "message": "Crime adicionado com sucesso!",
            "crime": new_crime.to_dict()
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Formato de data inválido. Use 'YYYY-MM-DD'."}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao adicionar crime: {str(e)}"}), 500

def listar_crimes():
    """
    Rota para listar todos os crimes.
    Retorna uma lista de crimes no formato JSON.
    """
    crimes = Crime.query.all()
    crimes_json = [crime.to_dict() for crime in crimes]
    return jsonify(crimes_json), 200

def obter_crime(id):
    """
    Rota para obter um crime específico pelo ID.
    """
    crime = Crime.query.get(id)
    if crime:
        return jsonify(crime.to_dict()), 200
    return jsonify({"error": "Crime não encontrado."}), 404

def atualizar_crime(id):
    """
    Rota para atualizar os dados de um crime pelo ID.
    Recebe os dados em JSON e atualiza no banco de dados.
    """
    data = request.get_json()
    crime = Crime.query.get(id)

    if not crime:
        return jsonify({"error": "Crime não encontrado."}), 404

    try:
        crime.crime_name = data.get('crime_name', crime.crime_name)
        crime.description = data.get('description', crime.description)
        crime.crime_date = data.get('crime_date', crime.crime_date)
        crime.res_hero = data.get('res_hero', crime.res_hero)
        crime.severity = data.get('severity', crime.severity)

        db.session.commit()
        return jsonify({"message": "Crime atualizado com sucesso!", "crime": crime.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar crime: {str(e)}"}), 500

def deletar_crime(id):
    """
    Rota para deletar um crime pelo ID.
    """
    crime = Crime.query.get(id)

    if not crime:
        return jsonify({"error": "Crime não encontrado."}), 404

    try:
        db.session.delete(crime)
        db.session.commit()
        return jsonify({"message": "Crime deletado com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar crime: {str(e)}"}), 500