from app.models.modelos import db, Heroi, Missao
import logging
from flask import request, jsonify

def add_mission():
    data = request.json  # Recebe os dados do cliente
    logging.debug(f"Dados recebidos: {data}")

    try:
        # Verifica se todos os campos necessários foram fornecidos
        required_fields = ['mission_name', 'description', 'difficulty', 'des_heroes', 'resultado']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            logging.error(f"Campos obrigatórios ausentes: {missing_fields}")
            return jsonify({"error": f"Campos obrigatórios ausentes: {missing_fields}"}), 400

        # Verifica se o resultado é válido (deve ser "Sucesso" ou "Fracasso")
        if data['resultado'] not in ['Sucesso', 'Fracasso']:
            logging.error(f"Resultado inválido: {data['resultado']}")
            return jsonify({"error": "O resultado deve ser 'Sucesso' ou 'Fracasso'."}), 400

        # Log dos dados recebidos
        for key, value in data.items():
            logging.debug(f"{key}: {value}")

        # Tenta converter a lista de heróis designados
        herois_ids = data.get('des_heroes')
        if isinstance(herois_ids, str):
            herois_ids = [int(h_id.strip()) for h_id in herois_ids.split(",")]

        # Verifica se todos os heróis existem
        herois = Heroi.query.filter(Heroi.id.in_(herois_ids)).all()
        if len(herois) != len(herois_ids):
            logging.error("Alguns heróis designados não foram encontrados no banco de dados.")
            return jsonify({"error": "Alguns heróis designados não foram encontrados."}), 400

        difficulty = int(data['difficulty'])

        # Valida compatibilidade entre dificuldade e força dos heróis
        incompatibles = [
            heroi.hero_name for heroi in herois if abs(heroi.strength_level - difficulty) > 2
        ]
        if incompatibles:
            logging.error(f"Heróis incompatíveis: {incompatibles}")
            return jsonify({
                "error": f"Os seguintes heróis não podem ser designados devido à incompatibilidade de força: {', '.join(incompatibles)}"
            }), 400

        # Cria a nova missão
        new_mission = Missao(
            mission_name=data.get('mission_name'),
            description=data.get('description'),
            difficulty=difficulty,
            des_heroes=",".join(map(str, herois_ids)),
            resultado=data.get('resultado'),
            reward=data.get('reward', 'Nenhuma')
        )

        # Adiciona a missão ao banco de dados
        db.session.add(new_mission)

        # Distribui impacto nos atributos dos heróis com base na dificuldade
        for heroi in herois:
            if difficulty > heroi.strength_level:
                heroi.popularity -= 1
                heroi.strength_level = max(1, heroi.strength_level - 1)
                logging.debug(f"Herói {heroi.hero_name} perdeu popularidade e força devido à missão difícil.")
            else:
                heroi.popularity += 2
                heroi.strength_level += 1
                logging.debug(f"Herói {heroi.hero_name} ganhou popularidade e força com a missão.")

        db.session.commit()
        logging.debug("Commit realizado com sucesso!")
        logging.debug("Missão cadastrada com sucesso!")

        return jsonify({"message": "Missão cadastrada e atribuída com sucesso!"}), 201

    except Exception as e:
        logging.error(f"Erro ao cadastrar missão: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

def get_missions_by_difficulty_and_hero(difficulty=None, hero_id=None):
    try:
        query = Missao.query
        if difficulty:
            query = query.filter_by(difficulty=int(difficulty))
        if hero_id:
            query = query.filter(Missao.des_heroes.contains(str(hero_id)))

        missions = query.all()
        missions_data = [mission.to_dict() for mission in missions]

        return jsonify({"missions": missions_data}), 200

    except Exception as e:
        logging.error(f"Erro ao consultar missões: {str(e)}")
        return jsonify({"error": str(e)}), 400

def listar_missoes():
    try:
        missao = Missao.query.all()
        missao_data = [m.to_dict() for m in missao]
        return jsonify(missao_data), 200
    except Exception as e:
        logging.error(f"Erro ao listar missões: {str(e)}")
        return jsonify({"error": str(e)}), 500

def deletar_missao(id):
    missao = Missao.query.get(id)
    if not missao:
        return jsonify({"error": "Missão não encontrada."}), 404

    try:
        db.session.delete(missao)
        db.session.commit()
        return jsonify({"message": "Missão deletada com sucesso!"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar missão: {str(e)}")
        return jsonify({"error": f"Erro ao deletar missão: {str(e)}"}), 500
