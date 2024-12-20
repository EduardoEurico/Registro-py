from app.models.modelos import db, Heroi, Battle  # Certifique-se de importar o modelo Heroi e Battle
from app.services.heroi import atualizar_status_heroi
from datetime import datetime
import logging
from flask import jsonify, request

def calculate_battle(hero1_id, hero2_id):
    hero1 = Heroi.query.get(hero1_id)
    hero2 = Heroi.query.get(hero2_id)

    if not hero1 or not hero2:
        raise ValueError("Herói(s) não encontrado(s)")

    strength_diff = abs(hero1.popularity - hero2.popularity) // 2

    hero1_strength = hero1.strength_level + (strength_diff if hero1.popularity > hero2.popularity else 0)
    hero2_strength = hero2.strength_level + (strength_diff if hero2.popularity > hero1.popularity else 0)

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

def create_battle(hero1_id, hero2_id, battle_date):
    battle_result = calculate_battle(hero1_id, hero2_id)

    new_battle = Battle(
        battle_date=battle_date,
        hero1_id=hero1_id,
        hero2_id=hero2_id,
        winner_id=battle_result['winner'].id,
        hero1_strength=battle_result['hero1_strength'],
        hero2_strength=battle_result['hero2_strength']
    )

    db.session.add(new_battle)
    db.session.commit()

    return new_battle.to_dict()