from . import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price_per_day = db.Column(db.Float, nullable=False)
    availability_status = db.Column(db.String(20), default='available', nullable=False)  # Nuevo atributo

    def to_dict(self):
        """Convierte el objeto Vehicle en un diccionario para respuestas JSON."""
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'price_per_day': self.price_per_day,
            'availability_status': self.availability_status  # Incluido en la salida
        }
