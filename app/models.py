from . import db
from datetime import datetime

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    pet = db.Column(db.String(50))
    profissional = db.Column(db.String(50))
    data_agendada = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='agendado')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    genero = db.Column(db.String(10))
    raca = db.Column(db.String(50))

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    cargo = db.Column(db.String(30))
