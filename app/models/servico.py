from .. import db
from datetime import datetime

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    data_agendada = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='agendado')

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)

    pet = db.relationship('Pet', backref='servicos')
    funcionario = db.relationship('Funcionario', backref='servicos')
