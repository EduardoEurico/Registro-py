from datetime import datetime
from app import db

class Heroi(db.Model):
    __tablename__ = 'herois'

    id = db.Column(db.Integer, primary_key=True)
    real_name = db.Column(db.String(100), nullable=False)  # Ajustei para refletir o nome real
    hero_name = db.Column(db.String(100), nullable=False)  # Ajustei para refletir o nome do herói
    gender = db.Column(db.String(10), nullable=True)  # Adicionado para refletir o gênero
    height = db.Column(db.Float, nullable=True)  # Adicionado para refletir altura
    weight = db.Column(db.Float, nullable=True)  # Adicionado para refletir peso
    birth_date = db.Column(db.Date, nullable=True)  # Adicionado para refletir data de nascimento
    birth_place = db.Column(db.String(100), nullable=True)  # Adicionado para refletir o local de nascimento
    powers = db.Column(db.String(255), nullable=False)
    strength_level = db.Column(db.Integer, nullable=False)
    popularity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default="Ativo")
    losses = db.Column(db.Integer, default=0)  # Novo campo para derrotas

    crimes = db.relationship('Crime', back_populates='hero')  # Relacionamento com crimes

    def to_dict(self):
        return {
            "id": self.id,
            "real_name": self.real_name,
            "hero_name": self.hero_name,
            "gender": self.gender,
            "height": self.height,
            "weight": self.weight,
            "birth_date": self.birth_date,
            "birth_place": self.birth_place,
            "powers": self.powers,
            "strength_level": self.strength_level,
            "popularity": self.popularity,
            "status": self.status,
            "losses": self.losses
        }

    def __repr__(self):
        return f"<Heroi {self.hero_name}>"


class Crime(db.Model):
    __tablename__ = 'crimes'

    id = db.Column(db.Integer, primary_key=True)
    crime_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    crime_date = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    res_hero = db.Column(db.String(100), nullable=False)  # Ajustado para refletir o nome do herói
    res_hero_id = db.Column(db.Integer, db.ForeignKey('herois.id'), nullable=False)


    hero  = db.relationship('Heroi', back_populates='crimes')  # Relacionamento

    def to_dict(self):
        return {
            'id': self.id,
            'crime_name': self.crime_name,
            'description': self.description,
            'crime_date': self.crime_date.strftime('%Y-%m-%d'),
            'severity': self.severity,
            'res_hero': self.hero.hero_name  # Aqui pegamos o nome do herói diretamente
        }

    def __repr__(self):
        return f"<Crime {self.crime_name}>"

class Battle(db.Model):
    __tablename__ = 'battles'

    id = db.Column(db.Integer, primary_key=True)
    battle_date = db.Column(db.String(100), nullable=False)
    hero1_id = db.Column(db.Integer, db.ForeignKey('herois.id'), nullable=False)
    hero2_id = db.Column(db.Integer, db.ForeignKey('herois.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('herois.id'), nullable=False)
    hero1_strength = db.Column(db.Integer, nullable=False)
    hero2_strength = db.Column(db.Integer, nullable=False)

    hero1 = db.relationship('Heroi', foreign_keys=[hero1_id])
    hero2 = db.relationship('Heroi', foreign_keys=[hero2_id])
    winner = db.relationship('Heroi', foreign_keys=[winner_id])

    def to_dict(self):
        battle_date_obj = datetime.strptime(self.battle_date, '%Y-%m-%d')
        current_date = datetime.utcnow()

        if battle_date_obj > current_date:
            winner_name = "A decidir"
        else:
            winner_name = self.winner.hero_name

        return {
            'id': self.id,
            'battle_date': self.battle_date,
            'hero1_name': self.hero1.hero_name,
            'hero2_name': self.hero2.hero_name,
            'hero1_strength': self.hero1_strength,
            'hero2_strength': self.hero2_strength,
            'winner_name': winner_name,
        }

    def __repr__(self):
        return f"<Battle {self.hero1.hero_name} vs {self.hero2.hero_name}>"

class Missao(db.Model):
    __tablename__ = 'missoes'

    id = db.Column(db.Integer, primary_key=True)
    mission_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    des_heroes = db.Column(db.String(255), nullable=False)
    resultado = db.Column(db.String(20), nullable=False)
    reward = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "mission_name": self.mission_name,
            "description": self.description,
            "difficulty": self.difficulty,
            "des_heroes": self.des_heroes,
            "resultado": self.resultado,
            "reward": self.reward
        }

    def __repr__(self):
        return f"<Missao {self.mission_name}>"