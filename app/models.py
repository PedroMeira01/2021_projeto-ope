from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

class Usuario(db.Model):
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

    atendimentos = db.relationship('Reserva', backref='barbeiro', lazy='dynamic')

    def __repr__(self):
        return f"<Barbeiro {self.nome}>"

    def criptografar_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha, senha)

class Servico(db.Model):
    id_servico = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    valor = db.Column(db.Float)

    servico_executado = db.relationship('Reserva', backref='servico', lazy='dynamic')

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

    def reservas_por_cliente(self, usuario_id):
        reservas = Reserva.query\
                .join(Usuario, Reserva.usuario_id==Usuario.id)\
                .join(Barbeiro, Reserva.barbeiro_id==Barbeiro.id_barbeiro)\
                .join(Servico, Reserva.servico_id==Servico.id_servico)\
                .add_columns( 
                    Reserva.data,
                    Reserva.horario_inicio.label('hora'),
                    Barbeiro.nome.label('barbeiro'), 
                    Servico.nome.label('servico')
                )\
                .filter(Reserva.usuario_id == usuario_id)\
                .order_by(desc(Reserva.data))\
                .all()

        return reservas

    def reservas_por_barbeiro(self, barbeiro_id):
        reservas = Reserva.query\
            .join(Usuario, Reserva.usuario_id==Usuario.id)\
            .join(Servico, Reserva.servico_id==Servico.id_servico)\
            .add_columns(
                Reserva.id_reserva,
                Reserva.data,
                Usuario.nome.label('cliente'),
                Servico.nome.label('servico')
            )\
            .filter(Reserva.barbeiro_id == barbeiro_id)\
            .order_by(desc(Reserva.data))\
            .all()
        return reservas
