from app.services.heroi import atualizar_status_heroi
from app.models.modelos import db, Heroi, Battle
from datetime import datetime
from flask import jsonify
import random


def validate_battle(hero1_id, hero2_id):
    """
    Valida se a batalha pode ocorrer entre os heróis especificados.
    :param hero1_id: ID do primeiro herói (desafiante)
    :param hero2_id: ID do segundo herói (adversário)
    :return: True se a batalha for válida, senão uma mensagem de erro.
    """
    # Garantir que os IDs sejam diferentes
    if hero1_id == hero2_id:
        return False, "Um herói não pode lutar contra ele mesmo."

    # Verificar se os heróis existem no banco de dados
    hero1 = Heroi.query.get(hero1_id)
    hero2 = Heroi.query.get(hero2_id)

    if not hero1 or not hero2:
        return False, "Um ou ambos os heróis não foram encontrados no banco de dados."

    # Adicionar outras validações se necessário (e.g., status do herói)
    return True, "Batalha válida"


def calculate_battle(hero1_id, hero2_id):
    """
    Calcula a batalha entre dois heróis, levando em consideração força, popularidade e fatores aleatórios.
    :param hero1_id: ID do primeiro herói (desafiante)
    :param hero2_id: ID do segundo herói (adversário)
    :return: Resultado da batalha incluindo o vencedor e a força final dos heróis.
    """
    hero1 = Heroi.query.get(hero1_id)
    hero2 = Heroi.query.get(hero2_id)

    # Cálculo base da força de cada herói
    hero1_strength = hero1.strength_level
    hero2_strength = hero2.strength_level

    # Fator aleatório: um valor de -10% a +10% da força do herói
    hero1_bonus = random.uniform(-0.1, 0.1) * hero1_strength
    hero2_bonus = random.uniform(-0.1, 0.1) * hero2_strength

    # Atualiza a força final com o fator aleatório
    hero1_strength += hero1_bonus
    hero2_strength += hero2_bonus

    # Verificar qual herói tem maior popularidade e aplicar bônus adicional
    if hero1.popularity > hero2.popularity:
        # Herói 1 recebe uma chance de ganhar um bônus adicional
        if random.random() < 0.2:  # 20% de chance de bônus
            hero1_buff_level = random.choice([5, 10, 15])  # Escolhe entre três níveis de buff de força
            hero1_strength += hero1_buff_level
    elif hero2.popularity > hero1.popularity:
        # Herói 2 recebe uma chance de ganhar um bônus adicional
        if random.random() < 0.2:  # 20% de chance de bônus
            hero2_buff_level = random.choice([5, 10, 15])  # Escolhe entre três níveis de buff de força
            hero2_strength += hero2_buff_level

    # Determina o vencedor com base na força final
    if hero1_strength > hero2_strength:
        winner = hero1
        loser = hero2
    else:
        winner = hero2
        loser = hero1

    # Atualizar popularidade
    winner.popularity += 10
    loser.popularity -= 10

    # Atualizar status dos heróis com base na popularidade
    atualizar_status_heroi(winner)
    atualizar_status_heroi(loser)

    db.session.commit()  # Salva as alterações no banco de dados

    return {
        'winner': winner,
        'loser': loser,
        'hero1_strength': hero1_strength,
        'hero2_strength': hero2_strength
    }