from app import db
from datetime import datetime

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    senha = db.Column(db.String(128))

    reservas = db.relationship('Reserva', backref='autor', lazy='dynamic')

    def __repr__(self):
        return f"<Usuario {self.nome}>"

class Barbeiro(db.Model):
    id_barbeiro = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    senha = db.Column(db.String(128))

    reservas = db.relationship('Reserva', backref='responsavel', lazy='dynamic')

    def __repr__(self):
        return f"<Barbeiro {self.nome}>"

class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    valor = db.Column(db.Float)

    reservas = db.relationship('Reserva', backref='associado', lazy='dynamic')

    def __repr__(self):
        return f"<Servico {self.nome}>"

class Reserva(db.Model):
    id_reserva = db.Column(db.Integer, primary_key=True)
    horario_inicio = db.Column(db.Time)
    horario_fim = db.Column(db.Time)
    data = db.Column(db.Date)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    barbeiro_id = db.Column(db.Integer, db.ForeignKey('barbeiro.id_barbeiro'))
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id_servico'))
    
    def __repr__(self):
        return f"<Servico código da reserva: {self.id_reserva}>"