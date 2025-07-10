from . import db
from datetime import datetime

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pets = db.relationship('Pet', backref='dono', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(10))
    raca = db.Column(db.String(50))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servicos = db.relationship('Servico', backref='pet_obj', lazy=True)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cargo = db.Column(db.String(30))
    servicos = db.relationship('Servico', backref='funcionario_obj', lazy=True)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    data_agendada = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='agendado')

    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
