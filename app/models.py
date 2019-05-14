from app import db


class Kitty(db.Model):
    """Create a data model for the database to be set up for capturing songs"""

    __tablename__ = "kitties"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=False)
    generation = db.Column(db.Integer, unique=False, nullable=False)
    birthday = db.Column(db.DateTime, unique=False, nullable=False)
    color = db.Column(db.String(100), unique=False, nullable=False)
    fancy = db.Column(db.Boolean, unique=False, nullable=False)
    fancy_type = db.Column(db.String(100), unique=False, nullable=True)
    exclusive = db.Column(db.Boolean, unique=False, nullable=False)
    cooldown = db.Column(db.Integer, unique=False, nullable=False)
    purrs = db.Column(db.Integer, unique=False, nullable=False)
    watches = db.Column(db.Integer, unique=False, nullable=False)
    hatched = db.Column(db.Boolean, unique=False, nullable=False)
    prestige = db.Column(db.Boolean, unique=False, nullable=False)
    prestige_type = db.Column(db.String(100), unique=False, nullable=True)
    prestige_ranking = db.Column(db.Integer, unique=False, nullable=True)
    fancy_ranking = db.Column(db.Integer, unique=False, nullable=True)
    body = db.Column(db.String(100), unique=False, nullable=False)
    mouth = db.Column(db.String(100), unique=False, nullable=False)
    eyes = db.Column(db.String(100), unique=False, nullable=False)
    pattern = db.Column(db.String(100), unique=False, nullable=False)
    colorprimary = db.Column(db.String(100), unique=False, nullable=False)
    colorsecondary = db.Column(db.String(100), unique=False, nullable=False)
    colortertiary = db.Column(db.String(100), unique=False, nullable=False)
    coloreyes = db.Column(db.String(100), unique=False, nullable=False)
    mother_id = db.Column(db.Integer, unique=False, nullable=True)
    mother_fancy = db.Column(db.Boolean, unique=False, nullable=True)
    mother_exclusive = db.Column(db.Boolean, unique=False, nullable=True)
    father_id = db.Column(db.Integer, unique=False, nullable=True)
    father_fancy = db.Column(db.Boolean, unique=False, nullable=True)
    father_exclusive = db.Column(db.Boolean, unique=False, nullable=True)
    start_price = db.Column(db.Float, unique=False, nullable=True)
    end_price = db.Column(db.Float, unique=False, nullable=True)
    current_price = db.Column(db.Float, unique=False, nullable=True)
    auction_type = db.Column(db.String(100), unique=False, nullable=True)
    auction_start = db.Column(db.DateTime, unique=False, nullable=True)
    auction_end = db.Column(db.DateTime, unique=False, nullable=True)
    auction_duration = db.Column(db.Float, unique=False, nullable=True)    

    def __repr__(self):
        return '<Kitty(id: %s, name: %s)>' % (self.id, self.name)
