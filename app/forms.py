from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Usuario, Barbeiro
from flask import session

# Para os formulários do site, usamos a extensão FlaskWTF
# que é uma parte do pacote WTForms. Os formulários do site
# serão representados por classes que herdarão a classe FlaskForm
# do pacote FlaskWTF

class LoginForm(FlaskForm):
    # Os atributos da classe serão os campos do formulário e eles
    # recebem instância de classes do "WTForms" de acordo com o tipo
    # de dado que irá receber, tem também como parâmetro o tipo de
    # validação que irá protegê-lo, como por exemplo a "DataRequired"
    # que obriga o usuário a preencher o campo. O tipo de validação
    # vem do módulo "validators" do pacote WTForms.

    # O primeiro parametro das instâncias abaixo corresponde a label do formulário
    email = StringField('E-mail', validators=[DataRequired(message="O e-mail é obrigatório.")])
    senha = PasswordField('Senha', validators=[DataRequired(message="A senha é obrigatória")])
    lembrar_me = BooleanField('Lembrar Me')
    entrar = SubmitField('Entrar')

class CadastrarUsuario(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message="O nome é obrigatório.")])
    email = StringField('E-mail', validators=[
        DataRequired(message="O e-mail é obrigatório."), 
        Email(message="Digite um e-mail válido.")
    ])
    senha = PasswordField('Senha', validators=[DataRequired(message="A senha é obrigatória.")])
    confirmar_senha = PasswordField('Confirmação de senha', 
        validators=[
            DataRequired(message="A confirmação de senha é obrigatória."),
            EqualTo('senha', message="As senhas não coincidem.")
        ]
    )
    cadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is not None:
            raise ValidationError('O e-mail inserido já está sendo usado por outro usuário!')

class EditarPerfilUsuario(FlaskForm):
<<<<<<< HEAD
    nome = StringField('Nome de usuário', validators=[DataRequired(message="O nome é obrigatório.")])
    email = StringField('E-mail', validators=[DataRequired(), Email(message="O e-mail é obrigatório.")])
    senha_atual = PasswordField('Senha atual', validators=[DataRequired(message="A senha atual é obrigatória.")])
    nova_senha = PasswordField('Nova senha', validators=[DataRequired(message="Escolha uma nova senha.")])
    confirmar_senha = PasswordField('Confirmar nova senha', 
        validators=[
            DataRequired(message="Confirme a nova senha."),
            EqualTo('nova_senha')
        ]
    )
=======
    nome = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])

>>>>>>> 3bdffbb8a8eda1121bb44794b64d8e3dc3cb1bd4
    editar = SubmitField('Editar')

    def __init__(self, email_original, *args, **kwargs):
        super(EditarPerfilUsuario, self).__init__(*args, **kwargs)
        self.email_original = email_original

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            if usuario.id != session['id_usuario']:
                raise ValidationError('O e-mail inserido já está sendo usado por outro usuário!')


class CadastrarBarbeiro(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(message="O nome é obrigatório.")])
    email = StringField('E-mail', validators=[DataRequired(message="O e-mail é obrigatório."), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(message="A senha é obrigatória.")])

    cadastrar = SubmitField('Cadastrar')

    def validate_email(self, email):
        barbeiro = Barbeiro.query.filter_by(email=email.data).first()
        if barbeiro is not None:
            raise ValidationError('O e-mail inserido já está sendo usado!')

class EditarPerfilBarbeiro(FlaskForm):
<<<<<<< HEAD
    nome = StringField('Nome de usuário', validators=[DataRequired(message="O nome é obrigatório.")])
    email = StringField('E-mail', validators=[DataRequired(message="O e-mail é obrigatório."), Email()])
    senha_atual = PasswordField('Senha atual', validators=[DataRequired(message="Preencha a senha atual.")])
    nova_senha = PasswordField('Nova senha', validators=[DataRequired(message="Escolha uma nova senha.")])
=======
    nome = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])

    editar = SubmitField('Editar')

    def __init__(self, email_original, *args, **kwargs):
        super(EditarPerfilBarbeiro, self).__init__(*args, **kwargs)
        self.email_original = email_original

    def validate_email(self, email):
        barbeiro = Barbeiro.query.filter_by(email=email.data).first()
        if barbeiro:
            if barbeiro.id_barbeiro != session['id_barbeiro']:
                raise ValidationError('O e-mail inserido já está sendo usado!')

class AlterarSenhaBarbeiro(FlaskForm):
    senha_atual = PasswordField('Senha atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova senha', validators=[DataRequired()])
>>>>>>> 3bdffbb8a8eda1121bb44794b64d8e3dc3cb1bd4
    confirmar_senha = PasswordField('Confirmar nova senha', 
        validators=[
            DataRequired(message="É necessário confirmar a senha."),
            EqualTo('nova_senha')
        ]
    )

    redefinir = SubmitField('Redefinir senha')

    def __init__(self, id_barbeiro, *args, **kwargs):
        super(AlterarSenhaBarbeiro, self).__init__(*args, **kwargs)
        self.id_barbeiro = id_barbeiro

    def validate_senha_atual(self, senha_atual):
        barbeiro = Barbeiro.query.filter_by(id_barbeiro=self.id_barbeiro).first()
        if not barbeiro.checar_senha(senha_atual.data):
            raise ValidationError('A senha atual está incorreta.')

class AlterarSenhaUsuario(FlaskForm):
    senha_atual = PasswordField('Senha atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova senha', validators=[DataRequired()])
    confirmar_senha = PasswordField('Confirmar nova senha', 
        validators=[
            DataRequired(),
            EqualTo('nova_senha')
        ]
    )

    redefinir = SubmitField('Redefinir senha')

    def __init__(self, id, *args, **kwargs):
        super(AlterarSenhaUsuario, self).__init__(*args, **kwargs)
        self.id = id

    def validate_senha_atual(self, senha_atual):
        usuario = Usuario.query.filter_by(id=self.id).first()
        if not usuario.checar_senha(senha_atual.data):
            raise ValidationError('A senha atual está incorreta.')