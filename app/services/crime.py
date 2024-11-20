from flask import jsonify, request
from datetime import datetime
from app import db
from app.models.modelos import db, Crime, Heroi
import logging


def add_crime(request):
    data = request.json  # Recebe os dados do cliente
    try:
        hero_name = data.get('res_hero')
        hero = Heroi.query.filter_by(hero_name=hero_name).first()

        if not hero:
            return jsonify({"error": "Herói não encontrado"}), 404

        # Garantir que a severidade seja um número inteiro
        severity = int(data.get('severity'))  # Convertendo para inteiro

        # Criar uma nova instância de Crime associada ao herói encontrado
        new_crime = Crime(
            crime_name=data.get('crime_name'),
            description=data.get('description'),
            crime_date=datetime.strptime(data.get('crime_date'), "%Y-%m-%d"),
            res_hero_id=hero.id,  # Associando ao ID do herói
            res_hero=hero.hero_name,  # Atribuindo o nome correto do herói
            severity=severity  # A severidade agora é um número inteiro
        )

        # Atualizar a popularidade do herói
        hero.popularity -= severity * 10  # Subtrai 10 pontos por cada ponto de severidade

        db.session.add(new_crime)
        db.session.commit()

        # Salvar alterações na popularidade do herói
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
        logging.debug(f"Dados recebidos: {data}")  # Log dos dados recebidos
        return jsonify({"error": f"Erro ao adicionar crime: {str(e)}"}), 500

    


def listar_crimes():
    crimes = Crime.query.all()
    crimes_json = [crime.to_dict() for crime in crimes]
    return jsonify(crimes_json), 200


def obter_crime(id):
    crime = Crime.query.get(id)
    if crime:
        return jsonify({
            'id': crime.id,
            'crime_name': crime.crime_name,
            'description': crime.description,
            'crime_date': crime.crime_date,
            'res_hero': crime.res_hero,
            'severity': crime.severity
        })
    return jsonify({'error': 'Crime not found'}), 404


def atualizar_crime(id):
    """
    Rota para atualizar os dados de um crime pelo ID.
    Recebe os dados em formato de JSON e atualiza no banco de dados.
    """
    crime = Crime.query.get(id)

    if not crime:
        return jsonify({"error": "Crime não encontrado."}), 404

    try:
        # Atualiza os campos com os valores enviados via JSON
        dados = request.get_json()

        crime.crime_name = dados.get('crime_name', crime.crime_name)
        crime.description = dados.get('description', crime.description)
        crime.crime_date = dados.get('crime_date', crime.crime_date)
        crime.res_hero = dados.get('res_hero', crime.res_hero)
        crime.severity = dados.get('severity', crime.severity)

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
        print(f"Erro ao deletar crime: {str(e)}")  
        return jsonify({"error": f"Erro ao deletar crime: {str(e)}"}), 500
