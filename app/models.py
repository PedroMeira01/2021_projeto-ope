from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_usuario(id):
    return Usuario.query.get(int(id))

class Usuario(UserMixin, db.Model):
    # Para que o FlaskLogin funcione, a PK do usuário deve ter o nome "id" apenas.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    senha = db.Column(db.String(128))

    reservas = db.relationship('Reserva', backref='cliente', lazy='dynamic')

    def __repr__(self):
        return f"<Usuario {self.nome}>"

    def criptografar_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha, senha)


class Barbeiro(db.Model):
    id_barbeiro = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), index=True, unique=True)
    senha = db.Column(db.String(128))

    reservas = db.relationship('Reserva', backref='barbeiro', lazy='dynamic')

    def __repr__(self):
        return f"<Barbeiro {self.nome}>"

class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    valor = db.Column(db.Float)

    reservas = db.relationship('Reserva', backref='servico', lazy='dynamic')

    def __repr__(self):
        return f"<Servico {self.nome}>"

class Reserva(db.Model):
    id_reserva = db.Column(db.Integer, primary_key=True)
    horario_inicio = db.Column(db.Time)
    horario_fim = db.Column(db.Time)
    data = db.Column(db.Date)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    barbeiro_id = db.Column(db.Integer, db.ForeignKey('barbeiro.id_barbeiro'))
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id_servico'))
    
    def __repr__(self):
        return f"<Servico código da reserva: {self.id_reserva}>"