from database import db
# Como Route tiene una relación con City, necesitamos importarlo.
from .city import City

class Route(db.Model):
    __tablename__ = 'route' # Nombre de la tabla explícito

    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer, nullable=False)
    
    origin_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    origin = db.relationship('City', foreign_keys=[origin_id], backref='routes_from')
    destination = db.relationship('City', foreign_keys=[destination_id], backref='routes_to')

    def __repr__(self):
        return f'<Route from {self.origin.name} to {self.destination.name}>'