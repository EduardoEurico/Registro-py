from app.models.modelos import db, Heroi  # Certifique-se de importar o modelo Heroi
from datetime import datetime
import logging

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
