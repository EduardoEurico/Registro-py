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
            
        }

    def __repr__(self):
        return f"<Heroi {self.hero_name}>"
