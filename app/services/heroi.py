from app.models.modelos import db, Heroi  # Certifique-se de importar o modelo Heroi
from datetime import datetime
import logging
from flask import jsonify, request


def add_hero(request):
    data = request.json  # Recebe os dados do cliente
    logging.debug(f"Dados recebidos: {data}")  # Log dos dados recebidos

    try:
        # Verifique se a data de nascimento foi recebida
        if not data.get('data_nascimento'):
            logging.error("Data de nascimento não foi fornecida.")
            return {"error": "Data de nascimento não foi fornecida. {data}" }, 400
        
        
        # Log de todos os dados recebidos
        for key, value in data.items():
            logging.debug(f"{key}: {value}")

        # Tenta converter a data de nascimento
        data['data_nascimento'] = datetime.strptime(data['data_nascimento'], "%Y-%m-%d")
        
        new_hero = Heroi(
            real_name=data.get('nome_real'),
            hero_name=data.get('nome_heroi'),
            powers=data.get('poderes'),
            strength_level=int(data.get('nivel_forca', 0)),
            popularity=int(data.get('popularidade', 0)),
            birth_date=data.get('data_nascimento'),
            birth_place=data.get('local_nascimento'),
            gender=data.get('genero'),  # Novo campo para gênero
            height=float(data.get('altura', 0)),  # Novo campo para altura
            weight=float(data.get('peso', 0)),  # Novo campo para peso
            status=data.get('status', 'Ativo')
        )



        # Adiciona o novo herói ao banco de dados
        db.session.add(new_hero)
        db.session.commit()
        logging.debug("Herói cadastrado com sucesso!")
        
        return {"message": "Herói cadastrado com sucesso!"}, 201

    except Exception as e:
        logging.error(f"Erro ao cadastrar herói: {str(e)}")  # Log do erro
        db.session.rollback()
        return {"error": str(e)}, 400
def listar_herois():
    heroi = Heroi.query.all()
    heroi_json = [heroi.to_dict() for heroi in heroi]
    return jsonify(heroi_json), 200


def obter_herois(id):
    """
    Rota para obter um heroi específico pelo ID.
    """
    heroi = Heroi.query.get(id)
    if heroi:
        return jsonify(heroi.to_dict()), 200
    return jsonify({"error": "heroi não encontrado."}), 404

def atualizar_heroi(id):
    """
    Rota para atualizar os dados de um heroi pelo ID.
    Recebe os dados em JSON e atualiza no banco de dados.
    """
    data = request.get_json()
    heroi = Heroi.query.get(id)

    if not heroi:
        return jsonify({"error": "Heroi não encontrado."}), 404

    try:
        heroi.real_name = data.get('real_name', heroi.real_name)
        heroi.hero_name = data.get('hero_name', heroi.hero_name)
        heroi.powers = data.get('powers', heroi.powers)
        heroi.strength_level = data.get('strength_level', heroi.strength_level)
        heroi.popularity = data.get('popularity', heroi.popularity)
        heroi.birth_date = data.get('birth_date', heroi.birth_date)
        heroi.birth_place = data.get('birth_place', heroi.birth)
        heroi.gender = data.get('gender', heroi.gender)
        heroi.height = data.get('height', heroi.height)
        heroi.weight = data.get('weight', heroi.weight)                       
        heroi.status = data.get('status', heroi.status)

        


        db.session.commit()
        return jsonify({"message": "Lista de Herois atualizada com sucesso!", "heroi": heroi.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar crime: {str(e)}"}), 500
    
def atualizar_status_heroi(heroi):
    """
    Função para atualizar o status do herói com base na popularidade e derrotas.
    """
    # Se a popularidade for menor que 20, o status é Inativo
    if heroi.popularity < 20:
        heroi.status = "Inativo"
    
    # Se a popularidade for menor ou igual a 0, o status é Banido
    if heroi.popularity <= 0:
        heroi.status = "Banido"

    # Considerando derrotas (adicione lógica de derrotas aqui se necessário)
    # Por exemplo, se derrotas forem mais de 5, o status pode ser alterado para "Inativo"
    if heroi.losses > 5:  # Suponha que 'losses' seja o número de derrotas
        heroi.status = "Inativo"

    db.session.commit()  # Salva as alterações no banco de dados